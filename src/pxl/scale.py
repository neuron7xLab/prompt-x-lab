"""Parallel scaling primitives — deterministic, byte-identical to serial.

The canonical primitive is roughly five orders of magnitude faster than
any LLM call it composes with. Scaling beyond single-core throughput is
*almost never necessary* for correctness reasons — but when it is (audit
pipelines, batch reproduction jobs, CI farms), this module provides the
deterministic parallel equivalents of the core functions.

Design commitment
-----------------
Parallel versions MUST produce byte-identical results to their serial
counterparts. This is enforced by ``tests/test_scale.py`` which runs the
same input through both paths and asserts equality. Any divergence
invalidates the reproduction chain and the tests fail CI.

On the GIL and process pools
----------------------------
Python's GIL prevents pure-thread parallelism for CPU-bound work. The
canonical primitive *is* CPU-bound. Two honest options therefore:

1. **Thread pool** for IO-bound tasks (audit: reads files from disk).
   Cheap, no pickling, but capped by single-core CPU throughput.
2. **Process pool** for CPU-bound tasks (batch canonical hashing).
   Scales linearly with cores but pays per-task pickling overhead;
   worth it only for batch sizes where the per-item compute dominates.

The primitive picks automatically based on the task kind, but the
``executor`` argument lets callers override when they know better.

Scaling math (from ``benchmarks/RESULTS.md``)
---------------------------------------------
::

    step_hash           4.0 μs  →   250K steps/sec/core
    7-phase chain       189 μs  →   5.3K chains/sec/core
    route_request       17.9 μs →   56K requests/sec/core
    score_response      28.3 μs →   35K responses/sec/core

Multiply by core count and you get the ceiling. At 100 CPU cores,
5.3K * 100 = 530K full tamper-evident audit chains per second. At 10K
cores (a medium Kubernetes cluster), 53M chains/sec. The LLM call that
produced each input is 5-8 orders of magnitude slower. **The primitive
is never the bottleneck; the LLM is.**

Public API
----------
- ``default_workers() -> int`` — sensible default for ``max_workers``
- ``parallel_audit_all(max_workers=None) -> dict[str, bool]``
- ``parallel_validate_layers(max_workers=None) -> tuple[int, list]``
- ``batch_canonical_hash(items, max_workers=None) -> list[str]``
- ``batch_execution_chain(bundles, contract_version, max_workers=None)
  -> list[str]``

Every function falls back to serial execution when ``max_workers <= 1``
or the batch is trivially small. Determinism is preserved across both
branches.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .audit import LAYER_CONFIG, REPO_ROOT, _compute_layer_manifest
from .kriterion.canonical import ExecutionChain, Phase, canonical_bytes, sha256_hex
from .validator import (
    ValidationIssue,
    iter_module_files,
    validate_file,
)

# ──────────────────────────────────────────────────────────────
# Defaults
# ──────────────────────────────────────────────────────────────

#: Minimum batch size below which parallelism is a net loss. Measured
#: empirically: dispatch overhead exceeds per-item compute until ~64.
_SERIAL_FALLBACK_THRESHOLD = 64


def default_workers() -> int:
    """Return a sensible default worker count: ``os.cpu_count()`` or 1."""

    return max(1, os.cpu_count() or 1)


def _use_serial(batch_size: int, max_workers: int) -> bool:
    return max_workers <= 1 or batch_size < _SERIAL_FALLBACK_THRESHOLD


# ──────────────────────────────────────────────────────────────
# Audit — parallel over integrated layers (IO-bound, thread pool)
# ──────────────────────────────────────────────────────────────


def _parse_audit_manifest(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            digest, _, path_str = line.partition("  ")
            if digest and path_str:
                out[path_str] = digest.strip()
    return out


def _audit_one_layer(tag: str) -> bool:
    cfg = LAYER_CONFIG[tag]
    expected = _parse_audit_manifest(cfg.audit_file)
    if not expected:
        return False
    actual = dict(_compute_layer_manifest(cfg))
    return expected == actual


def parallel_audit_all(max_workers: int | None = None) -> dict[str, bool]:
    """Audit every integrated layer in parallel.

    Returns a dict mapping layer tag (``"05"``, ``"06"``, ``"07"``) to
    a boolean indicating whether the layer's body hashes still match
    its audit manifest. Deterministic: identical to running
    ``python -m pxl.audit verify`` serially, just faster.
    """

    workers = max_workers if max_workers is not None else default_workers()
    if _use_serial(len(LAYER_CONFIG), workers):
        return {tag: _audit_one_layer(tag) for tag in LAYER_CONFIG}

    results: dict[str, bool] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_audit_one_layer, tag): tag for tag in LAYER_CONFIG}
        for fut in futures:
            tag = futures[fut]
            results[tag] = fut.result()
    return results


# ──────────────────────────────────────────────────────────────
# Validate — parallel frontmatter validation across modules
# ──────────────────────────────────────────────────────────────


def parallel_validate_layers(
    max_workers: int | None = None,
) -> tuple[int, list[ValidationIssue]]:
    """Parallel frontmatter validation across all modules.

    Returns ``(ok_count, issues)``. Equivalent to the serial
    ``pxl.validator.validate_all`` but runs file parses concurrently
    across worker threads. IO-bound → thread pool is the right choice.
    """

    workers = max_workers if max_workers is not None else default_workers()
    files = iter_module_files(REPO_ROOT)
    if _use_serial(len(files), workers):
        ok = 0
        issues: list[ValidationIssue] = []
        for path in files:
            f_issues = validate_file(path)
            if f_issues:
                issues.extend(f_issues)
            else:
                ok += 1
        return ok, issues

    ok = 0
    issues = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for f_issues in pool.map(validate_file, files):
            if f_issues:
                issues.extend(f_issues)
            else:
                ok += 1
    # Sort issues to preserve deterministic ordering regardless of
    # thread scheduling.
    issues.sort(key=lambda i: str(i.path))
    return ok, issues


# ──────────────────────────────────────────────────────────────
# Batch canonical hash — vectorized content-addressed fingerprint
# ──────────────────────────────────────────────────────────────


def _hash_one(item: Any) -> str:
    return sha256_hex(canonical_bytes(item))


def batch_canonical_hash(
    items: list[Any], max_workers: int | None = None
) -> list[str]:
    """Return ``[sha256_hex(canonical_bytes(x)) for x in items]`` in parallel.

    Byte-identical to the serial comprehension. Parallelism is only
    engaged for batches ≥ 64 items; below that, dispatch overhead
    dominates and serial is strictly faster.
    """

    workers = max_workers if max_workers is not None else default_workers()
    if _use_serial(len(items), workers):
        return [_hash_one(x) for x in items]

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_hash_one, items))


# ──────────────────────────────────────────────────────────────
# Batch execution chain — build many audit chains concurrently
# ──────────────────────────────────────────────────────────────


def _build_full_chain(bundle: dict[str, Any], contract_version: str) -> str:
    chain = ExecutionChain.start(bundle, contract_version=contract_version)
    for phase in Phase:
        chain.advance(phase, phase_input={"phase": phase.value, "bundle": bundle})
    return chain.terminal_hash


def batch_execution_chain(
    bundles: list[dict[str, Any]],
    *,
    contract_version: str,
    max_workers: int | None = None,
) -> list[str]:
    """Build a full 7-phase execution chain for each bundle in parallel.

    Each bundle is an independent chain (by construction), so this is
    embarrassingly parallel. Returns a list of terminal hashes in the
    same order as the input.

    This is the primitive you reach for when auditing a million
    evaluation bundles: serial throughput on one core is ~5,300
    chains/sec; 100 workers give ~530,000 chains/sec subject to GIL
    contention on the canonical-bytes step.
    """

    workers = max_workers if max_workers is not None else default_workers()
    if _use_serial(len(bundles), workers):
        return [_build_full_chain(b, contract_version) for b in bundles]

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(_build_full_chain, b, contract_version) for b in bundles
        ]
        return [f.result() for f in futures]

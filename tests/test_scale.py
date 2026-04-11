"""Scale primitives — parallel must equal serial, byte-for-byte.

Determinism is the whole point of the canonical primitive. If the
parallel version produces a different result from the serial version,
the reproduction chain collapses. These tests guard the invariant.
"""

from __future__ import annotations

import hashlib
import json

from pxl.kriterion.canonical import (
    ExecutionChain,
    Phase,
    canonical_bytes,
    sha256_hex,
)
from pxl.scale import (
    _use_serial,
    batch_canonical_hash,
    batch_execution_chain,
    default_workers,
    parallel_audit_all,
    parallel_validate_layers,
)
from pxl.validator import validate_all

# ──────────────────────────────────────────────────────────────
# Defaults + fallbacks
# ──────────────────────────────────────────────────────────────


def test_default_workers_is_at_least_one() -> None:
    assert default_workers() >= 1


def test_use_serial_forces_serial_below_threshold() -> None:
    assert _use_serial(batch_size=10, max_workers=8) is True
    assert _use_serial(batch_size=100, max_workers=8) is False
    assert _use_serial(batch_size=10, max_workers=1) is True  # single worker = serial


# ──────────────────────────────────────────────────────────────
# Audit parity
# ──────────────────────────────────────────────────────────────


def test_parallel_audit_matches_all_integrated_layers() -> None:
    results = parallel_audit_all()
    assert set(results) == {"05", "06", "07"}
    # Every integrated layer must currently pass
    assert all(results.values()), results


def test_parallel_audit_is_deterministic_across_runs() -> None:
    a = parallel_audit_all(max_workers=2)
    b = parallel_audit_all(max_workers=4)
    assert a == b


# ──────────────────────────────────────────────────────────────
# Validator parity
# ──────────────────────────────────────────────────────────────


def test_parallel_validator_matches_serial() -> None:
    serial_ok, serial_issues = validate_all()
    parallel_ok, parallel_issues = parallel_validate_layers()
    assert serial_ok == parallel_ok
    # Same issues, ordering may differ — compare as sets
    serial_keys = {(str(i.path), i.message) for i in serial_issues}
    parallel_keys = {(str(i.path), i.message) for i in parallel_issues}
    assert serial_keys == parallel_keys


def test_parallel_validator_count_matches_expected() -> None:
    ok, issues = parallel_validate_layers(max_workers=4)
    assert ok >= 91  # 8 layers, 91+ module files
    assert issues == []


# ──────────────────────────────────────────────────────────────
# Batch canonical hash parity
# ──────────────────────────────────────────────────────────────


def test_batch_canonical_hash_equals_serial_for_small_batch() -> None:
    items = [{"k": i, "v": f"item-{i}"} for i in range(10)]
    serial = [sha256_hex(canonical_bytes(x)) for x in items]
    parallel = batch_canonical_hash(items)
    assert parallel == serial


def test_batch_canonical_hash_equals_serial_for_large_batch() -> None:
    items = [{"k": i, "nested": [i, i * 2, i * 3]} for i in range(500)]
    serial = [sha256_hex(canonical_bytes(x)) for x in items]
    parallel = batch_canonical_hash(items, max_workers=4)
    assert parallel == serial


def test_batch_canonical_hash_preserves_order() -> None:
    items = [{"id": i} for i in range(100)]
    result = batch_canonical_hash(items)
    # Each hash must match the hash of its input at the same index
    for i, digest in enumerate(result):
        expected = hashlib.sha256(
            json.dumps({"id": i}, separators=(",", ":"), sort_keys=True).encode("utf-8")
        ).hexdigest()
        assert digest == expected


# ──────────────────────────────────────────────────────────────
# Batch execution chain parity
# ──────────────────────────────────────────────────────────────


def _build_serial_chain(bundle: dict[str, object], contract_version: str) -> str:
    chain = ExecutionChain.start(bundle, contract_version=contract_version)
    for phase in Phase:
        chain.advance(phase, phase_input={"phase": phase.value, "bundle": bundle})
    return chain.terminal_hash


def test_batch_execution_chain_matches_serial_small() -> None:
    bundles = [{"artifacts": [{"id": f"a{i}"}]} for i in range(5)]
    serial = [_build_serial_chain(b, "1.0.0") for b in bundles]
    parallel = batch_execution_chain(bundles, contract_version="1.0.0")
    assert parallel == serial


def test_batch_execution_chain_matches_serial_large() -> None:
    bundles = [
        {"artifacts": [{"id": f"a{i}", "body": "x" * (i % 16)}]}
        for i in range(200)
    ]
    serial = [_build_serial_chain(b, "1.0.0") for b in bundles]
    parallel = batch_execution_chain(
        bundles, contract_version="1.0.0", max_workers=4
    )
    assert parallel == serial


def test_batch_execution_chain_every_hash_differs_for_distinct_bundles() -> None:
    """Distinct bundles must produce distinct terminal hashes."""

    bundles = [{"id": i} for i in range(100)]
    hashes = batch_execution_chain(bundles, contract_version="1.0.0")
    assert len(set(hashes)) == 100


def test_batch_execution_chain_empty_input_returns_empty() -> None:
    assert batch_execution_chain([], contract_version="1.0.0") == []

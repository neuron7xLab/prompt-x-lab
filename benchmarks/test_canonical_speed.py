"""Canonical primitive benchmarks — measured ops/sec and per-op latency."""

from __future__ import annotations

import pytest

from pxl.kriterion.canonical import (
    ExecutionChain,
    Phase,
    build_genesis_hash,
    build_step_hash,
    canonical_bytes,
    sha256_hex,
)

# Representative payloads — the shape an evaluation artifact actually has.
_SMALL = {"id": "a1", "value": 42}
_MEDIUM = {
    "artifact_id": "ART.A1",
    "artifact_type": "RUNBOOK",
    "title": "Ops runbook",
    "provenance": {
        "origin_actor": "demo-author",
        "origin_system": "demo-repository",
        "acquisition_method": "DIRECT_EXPORT",
        "source_class": "PRIMARY",
    },
    "reviewer": {
        "reviewer_id": "reviewer-001",
        "reviewer_independence": True,
        "review_status": "INDEPENDENTLY_REVIEWED",
    },
    "fingerprint": "a" * 64,
    "references": ["ref-1", "ref-2", "ref-3"],
    "evidence_class": "PRIMARY",
    "domain_mapping": ["ops", "security"],
    "payload": {"sections": [{"heading": "Phase 1", "body": "do the thing"}]},
}
_LARGE = {
    "bundle_id": "case-001",
    "artifacts": [_MEDIUM] * 10,
    "metadata": {"expected_mode": "deep_analysis", "expected_ship": True},
}


@pytest.mark.benchmark(group="canonical_bytes")
def test_bench_canonical_bytes_small(benchmark: pytest.FixtureRequest) -> None:
    result = benchmark(canonical_bytes, _SMALL)
    assert isinstance(result, bytes)


@pytest.mark.benchmark(group="canonical_bytes")
def test_bench_canonical_bytes_medium(benchmark: pytest.FixtureRequest) -> None:
    result = benchmark(canonical_bytes, _MEDIUM)
    assert isinstance(result, bytes)


@pytest.mark.benchmark(group="canonical_bytes")
def test_bench_canonical_bytes_large(benchmark: pytest.FixtureRequest) -> None:
    result = benchmark(canonical_bytes, _LARGE)
    assert isinstance(result, bytes)


@pytest.mark.benchmark(group="sha256")
def test_bench_sha256_hex_64b(benchmark: pytest.FixtureRequest) -> None:
    data = b"x" * 64
    result = benchmark(sha256_hex, data)
    assert len(result) == 64


@pytest.mark.benchmark(group="sha256")
def test_bench_sha256_hex_1kb(benchmark: pytest.FixtureRequest) -> None:
    data = b"x" * 1024
    result = benchmark(sha256_hex, data)
    assert len(result) == 64


@pytest.mark.benchmark(group="chain")
def test_bench_build_genesis_hash(benchmark: pytest.FixtureRequest) -> None:
    bundle_hash, genesis = benchmark(build_genesis_hash, _LARGE)
    assert len(bundle_hash) == 64
    assert len(genesis) == 64


@pytest.mark.benchmark(group="chain")
def test_bench_build_step_hash(benchmark: pytest.FixtureRequest) -> None:
    digest = sha256_hex(canonical_bytes(_MEDIUM))
    step = benchmark(
        build_step_hash,
        phase_id=Phase.ARTIFACT_VALIDATION.value,
        phase_input_digest=digest,
        previous_step_hash="0" * 64,
        contract_version="1.0.0",
    )
    assert len(step) == 64


@pytest.mark.benchmark(group="chain")
def test_bench_execution_chain_seven_phases(benchmark: pytest.FixtureRequest) -> None:
    """Full seven-phase chain build — the end-to-end production path."""

    def build_full_chain() -> str:
        chain = ExecutionChain.start(_LARGE, contract_version="1.0.0")
        for phase in Phase:
            chain.advance(phase, phase_input={"state": phase.value, "data": _MEDIUM})
        return chain.terminal_hash

    terminal = benchmark(build_full_chain)
    assert len(terminal) == 64

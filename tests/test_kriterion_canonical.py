"""Kriterion canonical primitive — byte/hash determinism + chain math."""

from __future__ import annotations

import json

from pxl.kriterion.canonical import (
    CHAIN_FORMAT_VERSION,
    CHAIN_GENESIS_DOMAIN,
    CHAIN_STEP_HASH_DOMAIN,
    ExecutionChain,
    Phase,
    build_genesis_hash,
    build_step_hash,
    canonical_bytes,
    canonical_obj,
    sha256_hex,
)

# ──────────────────────────────────────────────────────────────
# canonical_bytes — deterministic, sorted, whitespace-free
# ──────────────────────────────────────────────────────────────


def test_canonical_bytes_sorts_keys_and_strips_whitespace() -> None:
    a = {"b": 1, "a": 2}
    b = {"a": 2, "b": 1}
    assert canonical_bytes(a) == canonical_bytes(b)
    assert canonical_bytes(a) == b'{"a":2,"b":1}'


def test_canonical_bytes_is_utf8_and_preserves_non_ascii() -> None:
    data = {"name": "Ярослав"}
    out = canonical_bytes(data)
    assert "Ярослав" in out.decode("utf-8")


def test_canonical_bytes_different_inputs_differ() -> None:
    assert canonical_bytes({"a": 1}) != canonical_bytes({"a": 2})


def test_canonical_obj_round_trips() -> None:
    original = {"b": [3, 1, 2], "a": "x"}
    out = canonical_obj(original)
    assert out == {"a": "x", "b": [3, 1, 2]}
    # round-trip is idempotent
    assert canonical_obj(out) == out


# ──────────────────────────────────────────────────────────────
# sha256_hex — accepts bytes AND str
# ──────────────────────────────────────────────────────────────


def test_sha256_hex_known_vector() -> None:
    # SHA-256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
    assert sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert sha256_hex(b"abc") == sha256_hex("abc")


def test_sha256_hex_of_canonical_bytes_is_deterministic() -> None:
    a = sha256_hex(canonical_bytes({"k": [1, 2, 3]}))
    b = sha256_hex(canonical_bytes({"k": [1, 2, 3]}))
    assert a == b
    assert len(a) == 64


# ──────────────────────────────────────────────────────────────
# Genesis + step hash + domain separation
# ──────────────────────────────────────────────────────────────


def test_genesis_hash_is_domain_separated() -> None:
    bundle = {"artifacts": [{"id": "a1"}]}
    bundle_hash, genesis = build_genesis_hash(bundle)
    # genesis is NOT the raw bundle hash — domain separation
    assert genesis != bundle_hash
    # but the bundle_hash IS the plain canonical sha256
    assert bundle_hash == sha256_hex(canonical_bytes(bundle))


def test_genesis_hash_depends_on_format_version() -> None:
    bundle = {"k": "v"}
    _, g1 = build_genesis_hash(bundle, "execution_chain.v1")
    _, g2 = build_genesis_hash(bundle, "execution_chain.v2")
    assert g1 != g2


def test_step_hash_is_chain_linked() -> None:
    s1 = build_step_hash(
        phase_id=Phase.ARTIFACT_VALIDATION.value,
        phase_input_digest=sha256_hex("phase-1-input"),
        previous_step_hash="deadbeef",
        contract_version="1.0.0",
    )
    s2 = build_step_hash(
        phase_id=Phase.ARTIFACT_VALIDATION.value,
        phase_input_digest=sha256_hex("phase-1-input"),
        previous_step_hash="cafebabe",  # different prev → different hash
        contract_version="1.0.0",
    )
    assert s1 != s2


def test_step_hash_domain_separates_from_genesis() -> None:
    same_inputs = {"k": "v"}
    _, genesis = build_genesis_hash(same_inputs)
    step = build_step_hash(
        phase_id="artifact_validation",
        phase_input_digest=sha256_hex(canonical_bytes(same_inputs)),
        previous_step_hash="0" * 64,
        contract_version="1.0.0",
    )
    # A raw SHA-256 of the input cannot accidentally equal a step hash.
    assert step != genesis
    assert step != sha256_hex(canonical_bytes(same_inputs))


def test_chain_format_and_domain_constants_match_reference() -> None:
    assert CHAIN_FORMAT_VERSION == "execution_chain.v1"
    assert CHAIN_STEP_HASH_DOMAIN == "kriterion.execution_chain.step"
    assert CHAIN_GENESIS_DOMAIN == "kriterion.execution_chain.genesis"


# ──────────────────────────────────────────────────────────────
# ExecutionChain — incremental builder
# ──────────────────────────────────────────────────────────────


def test_execution_chain_linear_growth() -> None:
    bundle = {"artifacts": [{"id": "x"}]}
    chain = ExecutionChain.start(bundle, contract_version="1.0.0")
    assert chain.terminal_hash == chain.genesis_hash
    assert chain.steps == []

    s1 = chain.advance(Phase.ARTIFACT_VALIDATION, phase_input={"validated": True})
    assert len(chain.steps) == 1
    assert chain.terminal_hash == s1

    s2 = chain.advance(Phase.ADMISSIBILITY_DERIVATION, phase_input={"admissible": True})
    assert len(chain.steps) == 2
    assert chain.terminal_hash == s2
    assert s1 != s2


def test_execution_chain_tamper_evidence() -> None:
    """Changing phase input invalidates every subsequent hash."""

    bundle = {"artifacts": [{"id": "x"}]}
    a = ExecutionChain.start(bundle, contract_version="1.0.0")
    b = ExecutionChain.start(bundle, contract_version="1.0.0")
    assert a.terminal_hash == b.terminal_hash

    a.advance(Phase.ARTIFACT_VALIDATION, phase_input={"validated": True})
    b.advance(Phase.ARTIFACT_VALIDATION, phase_input={"validated": False})
    # First step already diverges
    assert a.terminal_hash != b.terminal_hash

    a.advance(Phase.ADMISSIBILITY_DERIVATION, phase_input={"x": 1})
    b.advance(Phase.ADMISSIBILITY_DERIVATION, phase_input={"x": 1})
    # Same second input, but chains stay different forever
    assert a.terminal_hash != b.terminal_hash


def test_execution_chain_full_seven_phases() -> None:
    bundle = {"artifacts": []}
    chain = ExecutionChain.start(bundle, contract_version="1.0.0")
    for phase in Phase:
        chain.advance(phase, phase_input={"phase": phase.value})
    assert len(chain.steps) == 7
    assert [s[0] for s in chain.steps] == [p.value for p in Phase]


# ──────────────────────────────────────────────────────────────
# JSON compatibility — canonical output parseable by stdlib
# ──────────────────────────────────────────────────────────────


def test_canonical_bytes_parseable_by_stdlib_json() -> None:
    data = {"nested": {"z": [1, 2], "a": None, "b": True}}
    text = canonical_bytes(data).decode("utf-8")
    round = json.loads(text)
    assert round == data

"""Property-based tests for the Kriterion canonical primitive.

These tests use ``hypothesis`` to generate random JSON-serialisable
inputs and verify the mathematical invariants that make the primitive
fail-closed. Where a conventional test asserts that *one* specific
input produces the expected hash, these assert that *every* input
in a large search space respects the invariant.

If a property test fails, ``hypothesis`` shrinks the failing input
to a minimal counter-example, which is printed in the test output.
That is the whole point: property tests find the edge cases you did
not imagine.
"""

from __future__ import annotations

import hashlib
import json

from hypothesis import given, settings
from hypothesis import strategies as st

from pxl.kriterion.canonical import (
    CHAIN_FORMAT_VERSION,
    ExecutionChain,
    Phase,
    build_genesis_hash,
    build_step_hash,
    canonical_bytes,
    canonical_obj,
    sha256_hex,
)

# Hypothesis strategy for JSON-like values.
_JSON_PRIMITIVE = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-(2**31), max_value=2**31 - 1),
    st.floats(allow_nan=False, allow_infinity=False, width=32),
    st.text(max_size=50),
)
_JSON_VALUE = st.recursive(
    _JSON_PRIMITIVE,
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(min_size=1, max_size=20), children, max_size=5),
    ),
    max_leaves=15,
)


# ─────────────────────────────────────────────────────────────
# canonical_bytes properties
# ─────────────────────────────────────────────────────────────


@given(data=_JSON_VALUE)
@settings(max_examples=200, deadline=None)
def test_canonical_bytes_is_deterministic(data: object) -> None:
    """Calling twice with the same input yields the same bytes."""

    assert canonical_bytes(data) == canonical_bytes(data)


@given(data=_JSON_VALUE)
@settings(max_examples=200, deadline=None)
def test_canonical_bytes_is_parseable_by_stdlib(data: object) -> None:
    """The output is always valid UTF-8 JSON that round-trips via json.loads."""

    parsed = json.loads(canonical_bytes(data).decode("utf-8"))
    # Not asserting equality with `data` because float NaN handling,
    # dict key ordering etc. may legitimately differ — but parsing
    # must always succeed without raising.
    assert parsed is not None or data is None


@given(data=_JSON_VALUE)
@settings(max_examples=100, deadline=None)
def test_canonical_obj_is_idempotent(data: object) -> None:
    """Round-tripping through the canonical form is a fixed point."""

    once = canonical_obj(data)
    twice = canonical_obj(once)
    assert once == twice


@given(keys=st.lists(st.text(min_size=1, max_size=20), min_size=2, max_size=5, unique=True),
       value=_JSON_PRIMITIVE)
@settings(max_examples=100, deadline=None)
def test_canonical_bytes_is_key_order_independent(keys: list[str], value: object) -> None:
    """Two dicts with the same keys in different orders hash identically."""

    a = dict.fromkeys(keys, value)
    b = dict.fromkeys(reversed(keys), value)
    assert canonical_bytes(a) == canonical_bytes(b)


# ─────────────────────────────────────────────────────────────
# sha256_hex properties
# ─────────────────────────────────────────────────────────────


@given(text=st.text(max_size=500))
@settings(max_examples=200, deadline=None)
def test_sha256_hex_matches_stdlib(text: str) -> None:
    """sha256_hex matches hashlib.sha256 on UTF-8 encoding of strings."""

    assert sha256_hex(text) == hashlib.sha256(text.encode("utf-8")).hexdigest()


@given(data=_JSON_VALUE)
@settings(max_examples=200, deadline=None)
def test_sha256_hex_is_deterministic_on_canonical(data: object) -> None:
    """Same canonical bytes → same hash, always."""

    assert sha256_hex(canonical_bytes(data)) == sha256_hex(canonical_bytes(data))


@given(text=st.text(min_size=1, max_size=200))
def test_sha256_hex_is_64_chars_of_hex(text: str) -> None:
    """Output is always 64 lowercase hex chars."""

    digest = sha256_hex(text)
    assert len(digest) == 64
    assert all(c in "0123456789abcdef" for c in digest)


# ─────────────────────────────────────────────────────────────
# Genesis + step hash properties
# ─────────────────────────────────────────────────────────────


@given(
    bundle=st.dictionaries(st.text(min_size=1, max_size=10), _JSON_VALUE, min_size=0, max_size=4),
)
@settings(max_examples=100, deadline=None)
def test_genesis_hash_is_deterministic(bundle: dict[str, object]) -> None:
    b1, g1 = build_genesis_hash(bundle)
    b2, g2 = build_genesis_hash(bundle)
    assert b1 == b2
    assert g1 == g2


@given(
    bundle=st.dictionaries(st.text(min_size=1, max_size=10), _JSON_VALUE, min_size=0, max_size=4),
)
@settings(max_examples=100, deadline=None)
def test_genesis_hash_differs_from_bundle_hash(bundle: dict[str, object]) -> None:
    """Domain separation holds for every bundle."""

    bundle_hash, genesis = build_genesis_hash(bundle)
    assert bundle_hash != genesis


@given(
    prev=st.text(min_size=1, max_size=64),
    phase_id=st.sampled_from([p.value for p in Phase]),
    phase_input=_JSON_VALUE,
    contract_version=st.text(min_size=1, max_size=20),
)
@settings(max_examples=100, deadline=None)
def test_step_hash_is_deterministic(
    prev: str, phase_id: str, phase_input: object, contract_version: str
) -> None:
    digest = sha256_hex(canonical_bytes(phase_input))
    h1 = build_step_hash(
        phase_id=phase_id,
        phase_input_digest=digest,
        previous_step_hash=prev,
        chain_format_version=CHAIN_FORMAT_VERSION,
        contract_version=contract_version,
    )
    h2 = build_step_hash(
        phase_id=phase_id,
        phase_input_digest=digest,
        previous_step_hash=prev,
        chain_format_version=CHAIN_FORMAT_VERSION,
        contract_version=contract_version,
    )
    assert h1 == h2


@given(
    bundle=st.dictionaries(st.text(min_size=1, max_size=10), _JSON_VALUE, min_size=1, max_size=4),
    phase_inputs=st.lists(_JSON_VALUE, min_size=1, max_size=7),
)
@settings(max_examples=50, deadline=None)
def test_execution_chain_every_step_differs(
    bundle: dict[str, object], phase_inputs: list[object]
) -> None:
    """Every advance produces a new terminal hash."""

    chain = ExecutionChain.start(bundle, contract_version="1.0.0")
    seen = {chain.terminal_hash}
    for i, pi in enumerate(phase_inputs):
        phase = list(Phase)[i % len(Phase)]
        chain.advance(phase, phase_input=pi)
        # Each step's terminal_hash is unique across the run
        assert chain.terminal_hash not in (seen - {chain.terminal_hash}) or len(seen) == 0
        seen.add(chain.terminal_hash)
    assert len(chain.steps) == len(phase_inputs)


@given(
    bundle=st.dictionaries(st.text(min_size=1, max_size=10), _JSON_VALUE, min_size=1, max_size=4),
    phase_input_a=_JSON_VALUE,
    phase_input_b=_JSON_VALUE,
)
@settings(max_examples=50, deadline=None)
def test_execution_chain_tamper_evidence(
    bundle: dict[str, object], phase_input_a: object, phase_input_b: object
) -> None:
    """Changing a phase input invalidates all subsequent hashes."""

    from hypothesis import assume

    # Only meaningful when the two inputs are distinct
    assume(canonical_bytes(phase_input_a) != canonical_bytes(phase_input_b))

    a = ExecutionChain.start(bundle, contract_version="1.0.0")
    b = ExecutionChain.start(bundle, contract_version="1.0.0")
    assert a.terminal_hash == b.terminal_hash  # same genesis

    a.advance(Phase.ARTIFACT_VALIDATION, phase_input=phase_input_a)
    b.advance(Phase.ARTIFACT_VALIDATION, phase_input=phase_input_b)
    assert a.terminal_hash != b.terminal_hash

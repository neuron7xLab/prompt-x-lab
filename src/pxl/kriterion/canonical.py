"""Canonical JSON serialisation + execution-state chain primitives.

These functions are the *entire mathematical core* of Kriterion's fail-
closed guarantee: every phase of an evaluation hashes its canonical
input and links to the previous phase's hash, producing a chain where
any tampering invalidates every subsequent step.

The functions are pure, deterministic, and dependency-free (stdlib
only). They are re-usable for any reproducible audit pipeline — not
just Kriterion. If you want your own evaluation framework to be fail-
closed, this is the 50-line kernel you need.

Byte-for-byte compatibility with the original Kriterion tooling is
enforced by ``tests/test_kriterion_canonical.py`` — the same inputs
produce the same hashes as the reference implementation.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

CHAIN_FORMAT_VERSION = "execution_chain.v1"
CHAIN_STEP_HASH_DOMAIN = "kriterion.execution_chain.step"
CHAIN_GENESIS_DOMAIN = "kriterion.execution_chain.genesis"


class Phase(StrEnum):
    """The seven canonical evaluation phases, in strict execution order."""

    ARTIFACT_VALIDATION = "artifact_validation"
    ADMISSIBILITY_DERIVATION = "admissibility_derivation"
    TASK_SCORING = "task_scoring"
    DOMAIN_SCORING = "domain_scoring"
    GATE_EVALUATION = "gate_evaluation"
    CLASSIFICATION = "classification"
    FINALIZATION = "finalization"


def canonical_bytes(data: Any) -> bytes:
    """Return deterministic UTF-8 bytes for ``data``.

    The canonical form sorts keys, forbids whitespace between tokens,
    preserves non-ASCII characters, and is byte-for-byte stable across
    interpreters. Two structurally-equal inputs always produce the same
    bytes; two structurally-different inputs always produce different
    bytes. This is the foundation of every downstream hash.
    """

    return json.dumps(
        data, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_obj(data: Any) -> Any:
    """Round-trip ``data`` through its canonical form.

    Useful when downstream code consumes the canonical view of a nested
    object (e.g., verification that two inputs are canonically equal
    without comparing bytes).
    """

    return json.loads(canonical_bytes(data).decode("utf-8"))


def sha256_hex(data: bytes | str) -> str:
    """Return the hex SHA-256 of ``data`` (encoding str as UTF-8)."""

    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def build_genesis_hash(bundle: dict[str, Any], chain_format_version: str = CHAIN_FORMAT_VERSION) -> tuple[str, str]:
    """Return ``(bundle_hash, genesis_hash)`` for a reference bundle.

    The genesis hash domain-separates the bundle from other hashes in
    the chain. Do not conflate ``bundle_hash`` with ``genesis_hash``:
    the former is the direct fingerprint of the input; the latter is
    the anchor of the execution chain and depends on the format
    version.
    """

    bundle_hash = sha256_hex(canonical_bytes(canonical_obj(bundle)))
    genesis_payload = {
        "domain": CHAIN_GENESIS_DOMAIN,
        "bundle_hash": bundle_hash,
        "chain_format_version": chain_format_version,
    }
    return bundle_hash, sha256_hex(canonical_bytes(genesis_payload))


def build_step_hash(
    *,
    phase_id: str,
    phase_input_digest: str,
    previous_step_hash: str,
    chain_format_version: str = CHAIN_FORMAT_VERSION,
    contract_version: str,
) -> str:
    """Return the next step hash in an execution chain.

    Every phase produces a step hash that is a function of:
    1. The chain format version (prevents cross-version replay).
    2. The phase ID (domain separation between phases).
    3. The digest of the phase's input.
    4. The previous step hash (linear chain guarantee).
    5. The contract version of the phase implementation.

    The hash is computed over a JSON-canonicalised payload wrapped in a
    domain-separating envelope so that a raw SHA-256 of the input can
    never be confused with a valid step hash.
    """

    step_input = {
        "chain_format_version": chain_format_version,
        "phase_id": phase_id,
        "phase_input_digest": phase_input_digest,
        "previous_step_hash": previous_step_hash,
        "contract_version": contract_version,
    }
    payload = {"domain": CHAIN_STEP_HASH_DOMAIN, "step_hash_input": step_input}
    return sha256_hex(canonical_bytes(payload))


@dataclass(slots=True)
class ExecutionChain:
    """Incremental builder for a Kriterion execution-state chain.

    Usage::

        chain = ExecutionChain.start(bundle, contract_version="1.0.0")
        chain.advance(Phase.ARTIFACT_VALIDATION, phase_input={"...": "..."})
        chain.advance(Phase.ADMISSIBILITY_DERIVATION, phase_input={"...": "..."})
        # ... through all seven phases ...
        terminal = chain.terminal_hash

    Each ``advance`` call appends a ``(phase_id, step_hash)`` tuple to
    ``steps`` and updates ``terminal_hash``. The chain is linear and
    tamper-evident: changing any phase's input invalidates every
    subsequent hash.
    """

    contract_version: str
    bundle_hash: str
    genesis_hash: str
    chain_format_version: str = CHAIN_FORMAT_VERSION
    steps: list[tuple[str, str]] = field(default_factory=list)

    @property
    def terminal_hash(self) -> str:
        """The last step hash, or the genesis hash if no steps yet."""

        return self.steps[-1][1] if self.steps else self.genesis_hash

    @classmethod
    def start(cls, bundle: dict[str, Any], *, contract_version: str) -> ExecutionChain:
        bundle_hash, genesis_hash = build_genesis_hash(bundle)
        return cls(
            contract_version=contract_version,
            bundle_hash=bundle_hash,
            genesis_hash=genesis_hash,
        )

    def advance(self, phase: Phase | str, *, phase_input: Any) -> str:
        """Extend the chain with one phase. Returns the new step hash."""

        phase_id = phase.value if isinstance(phase, Phase) else phase
        phase_input_digest = sha256_hex(canonical_bytes(phase_input))
        step_hash = build_step_hash(
            phase_id=phase_id,
            phase_input_digest=phase_input_digest,
            previous_step_hash=self.terminal_hash,
            chain_format_version=self.chain_format_version,
            contract_version=self.contract_version,
        )
        self.steps.append((phase_id, step_hash))
        return step_hash

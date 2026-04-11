"""Kriterion — Fail-Closed Security Capability Evaluation primitives.

Layer 07 integrates the essential kernel of the Kriterion framework into
prompt-x-lab: canonical JSON hashing, execution-state chain construction,
nine canonical evaluation schemas, and the six security-role protocols.

Kriterion's insight is simple and powerful: if every evaluation phase
hashes its input deterministically and links to the previous phase, the
whole pipeline becomes a cryptographic chain. Tampering with any phase
invalidates every subsequent hash. Fail-closed by construction.

This package exposes that insight as a small, reusable public API —
usable from any reproducible audit pipeline, not just Kriterion's own.

Public API
----------
- ``canonical_bytes(data) -> bytes`` — deterministic UTF-8 JSON bytes
- ``canonical_obj(data) -> Any``     — the round-tripped canonical form
- ``sha256_hex(data) -> str``        — content-addressed fingerprint
- ``build_genesis_hash(bundle, format_version) -> (bundle_hash, genesis)``
- ``build_step_hash(*, phase_id, phase_input_digest, previous_step_hash,
  chain_format_version, contract_version) -> str``
- ``ExecutionChain`` — dataclass builder for incremental chain steps
- ``Phase`` — the seven canonical phase identifiers
- ``load_schema(name) -> dict`` / ``validate_against(name, instance)``
- ``load_protocol(name) -> str`` / ``list_protocols() -> list[str]``
- ``reproduce_benchmark() -> BenchmarkReport`` — full benchmark replay
"""

from __future__ import annotations

from .canonical import (
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
from .protocols import list_protocols, load_protocol
from .schemas import list_schemas, load_schema, validate_against

__all__ = [
    "CHAIN_FORMAT_VERSION",
    "CHAIN_GENESIS_DOMAIN",
    "CHAIN_STEP_HASH_DOMAIN",
    "ExecutionChain",
    "Phase",
    "build_genesis_hash",
    "build_step_hash",
    "canonical_bytes",
    "canonical_obj",
    "list_protocols",
    "list_schemas",
    "load_protocol",
    "load_schema",
    "sha256_hex",
    "validate_against",
]

KRITERION_VERSION = "2026.4.5"

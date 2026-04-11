# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a vulnerability

If you discover a security-relevant issue in prompt-x-lab — particularly in the
`src/pxl/` Python code, the canonical-hashing primitive, the execution-chain
builder, the LLM-as-judge harness, or any of the bundled schemas — please
**do not open a public issue**. Instead:

1. Email **neuron7x@proton.me** with the subject line `[security] prompt-x-lab: <short-description>`.
2. Describe the issue, the affected module (path and version), the minimum
   reproduction, and the impact.
3. If the issue concerns a **cryptographic invariant** (canonical
   serialisation determinism, SHA-256 hashing, HMAC signing, execution
   chain linkage), please also include a proposed counter-example that
   demonstrates the invariant breaking.

You will receive an acknowledgement within 72 hours and a preliminary
assessment within one week. If the report is confirmed, we will:

- Fix the issue privately in a non-public branch.
- Coordinate a disclosure date.
- Credit you in the CHANGELOG under the affected version.

## In-scope vulnerabilities

- Any reproducible break of the canonical-hashing determinism contract
  (two structurally-equal inputs producing different `canonical_bytes`).
- Any reproducible break of the execution-state chain tamper-evidence
  property (changing phase input producing the same terminal hash).
- Any deserialisation vulnerability in the eval harness or the Kriterion
  schema validator.
- Any prompt-injection pathway that allows an adversary to bypass a
  fail-closed refusal in a shipped module.
- Supply-chain compromise of a bundled asset (a mismatch between the
  content hash in `05_orchestration/AUDIT.sha256`, `06_eca_engine/AUDIT.sha256`,
  or `07_kriterion/AUDIT.sha256` and the actual file bodies).

## Out of scope

- LLM hallucinations that do not bypass a module's declared refusal
  path. Those are quality issues, not security issues; file a normal
  issue.
- Rate-limit bypass or other attacks on upstream vendor APIs. Report
  those directly to the vendor.
- Issues in the content-only upstream bundles (Advanced Orchestration v1
  proprietary, Kriterion AGCL-1.0 proprietary) themselves. Those are
  integrated verbatim; reach out to the original upstream author.

## Cryptographic contract we defend

The `src/pxl/kriterion/canonical.py` module implements the mathematical
core of a fail-closed audit pipeline. The contract is:

1. **Determinism.** `canonical_bytes(a) == canonical_bytes(b)` iff `a`
   and `b` are structurally equal JSON values.
2. **Domain separation.** `build_genesis_hash(bundle)` and
   `build_step_hash(...)` return values from disjoint hash-input spaces.
   No raw SHA-256 of a user-controlled payload can collide with a valid
   step or genesis hash.
3. **Chain tamper-evidence.** Given an `ExecutionChain`, changing any
   phase input invalidates every subsequent `step_hash` and therefore
   the `terminal_hash`. This is enforced by `test_kriterion_canonical.py`
   and `test_property_canonical.py` as CI gates.

Any reproducible break of (1), (2), or (3) is a P0 security issue.

## Signed releases

Starting with v0.6.0, tagged releases are published via GitHub Actions
from the `main` branch only, built with `hatch`, and the wheel + sdist
are attached to the release page with SHA-256 checksums. Verify any
release artifact by comparing its hash against the one recorded on the
GitHub Release page before installing.

## Dependency policy

prompt-x-lab pins **minimum** versions, not exact versions. Transitive
dependencies are not locked. If you need a reproducible build for
audited deployment, use `pip install prompt-x-lab==0.6.0 --constraint
your-constraints.txt` with a constraints file generated from a locked
environment on your side.

---

*Thank you for helping keep the project honest.*

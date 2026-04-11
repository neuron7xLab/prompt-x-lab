# 07 — Kriterion

> **Kriterion v2026.4.5** — Fail-Closed Security Capability Evaluation Framework. Integrated as a minimalist kernel: **6 security-role protocols · 9 canonical schemas · typed Python primitive for canonical hashing + execution-state chains · 10-case benchmark reproduction**. No business copy, no HTML dashboard, no CI plumbing — just the mathematical core and the reusable content.

---

## The idea in one sentence

If every evaluation phase hashes its canonical input and links to the previous phase, the whole pipeline becomes a cryptographic chain where tampering with any phase invalidates every subsequent hash. Fail-closed by construction.

---

## What's in this layer

| Subfolder | Count | Contents |
|---|---|---|
| [`protocols/`](protocols/) | **6** | Six security-role protocols — SE-OPS, SSE, ESA, PSE, DSE, GPT-5.4 Audit Hardening |
| [`schemas/`](schemas/) | **9** | CanonicalArtifact, EvaluationResult, TaskScore, DomainScore, GateResult, ArtifactValidationResult, ReferenceInputBundle, OrchestrationHandoff, GovernanceInvariantRegistry |
| [`methodology/`](methodology/) | **3** | Methodology · Threat Model for AI Evaluation · Anti-Fragile Reasoning Framework |
| **Total content** | **18** | files |

Every file carries `source_sha256` in its frontmatter, body-for-byte SHA256 in `07_kriterion/AUDIT.sha256`, and passes `pxl-validate`.

## What's in the Python subsystem (`src/pxl/kriterion/`)

| Module | Responsibility |
|---|---|
| `canonical.py` | The kernel — `canonical_bytes`, `canonical_obj`, `sha256_hex`, `build_genesis_hash`, `build_step_hash`, `ExecutionChain` builder, `Phase` enum. Zero dependencies beyond stdlib. |
| `schemas.py` | Loaders + `jsonschema` validator with `referencing.Registry` (deprecation-free). |
| `protocols.py` | Loaders for the 6 raw protocol text files. |
| `benchmark.py` | 10-case reproduction contract against upstream `dataset_manifest.json`. |
| `cli.py` | `pxl-kriterion { info \| canonical \| validate \| benchmark \| protocol }`. |

And the bundled resources (force-included in the wheel):

```
src/pxl/kriterion/assets/
├── schemas/     9 JSON Schemas
└── protocols/   6 raw protocol text files

src/pxl/kriterion/datasets/
├── synthetic_cases/   10 JSON fixtures
├── dataset_manifest.json       ← the 10 expected hashes
├── adversarial_manifest.json   ← 4 adversarial cases
├── metrics.json                ← published benchmark metrics
├── adjudicated_labels.csv
└── human_ratings.csv
```

## Reproduction contract

`pxl-kriterion benchmark` replays the ten upstream fixtures through `pxl.kriterion.canonical` and compares each computed hash against the `artifact_manifest_hash` field in the bundled `dataset_manifest.json`. All ten must match. If they do not, the canonical primitive has drifted and no downstream chain hash can be trusted.

```
$ pxl-kriterion benchmark | python -c 'import sys, json; d=json.load(sys.stdin); print(d["matched"], "/", d["total"], "ok=", d["ok"])'
10 / 10 ok= True
```

The same contract is enforced by `tests/test_kriterion_benchmark.py` in CI.

## Public API for reproducible audit

The `canonical.py` primitive is the reusable part of this layer — it works for **any** reproducible audit pipeline, not just Kriterion's. If you want fail-closed evaluation, this is the 180-line kernel you need:

```python
from pxl.kriterion import (
    canonical_bytes, sha256_hex,
    build_genesis_hash, build_step_hash,
    ExecutionChain, Phase,
)

# Start a chain from a reference bundle
chain = ExecutionChain.start(my_bundle, contract_version="1.0.0")

# Advance through each phase; tampering with any phase input
# invalidates every subsequent step hash.
chain.advance(Phase.ARTIFACT_VALIDATION, phase_input=validation_state)
chain.advance(Phase.ADMISSIBILITY_DERIVATION, phase_input=admissibility_state)
chain.advance(Phase.TASK_SCORING, phase_input=task_state)
chain.advance(Phase.DOMAIN_SCORING, phase_input=domain_state)
chain.advance(Phase.GATE_EVALUATION, phase_input=gate_state)
chain.advance(Phase.CLASSIFICATION, phase_input=class_state)
chain.advance(Phase.FINALIZATION, phase_input=final_state)

# The terminal hash is your verifiable proof-of-execution.
assert chain.terminal_hash != chain.genesis_hash
```

Seven properties guarantee fail-closedness:

1. **Canonical form is unique.** `canonical_bytes` sorts keys, forbids whitespace, preserves non-ASCII — two structurally-equal inputs always produce the same bytes.
2. **Hashes are domain-separated.** Genesis and step hashes wrap their payload in distinct domain envelopes; a raw SHA-256 can never collide with a valid chain hash.
3. **Chain is linear.** Every step depends on the previous step's hash.
4. **Format version is baked in.** Cross-version replay is impossible.
5. **Contract version is baked in.** Phase implementations that differ produce different step hashes even on the same input.
6. **Genesis depends on the bundle.** Two different bundles produce two different genesis hashes and therefore two different chains.
7. **Terminal hash proves the entire run.** Anyone can re-run the chain from the bundle + phase inputs and re-derive the terminal hash.

Tests in `tests/test_kriterion_canonical.py` assert each of these properties against known-value vectors.

---

## Provenance & license

Kriterion v2026.4.5 is released by its author under the *Audit-Grade Community License 1.0* (AGCL-1.0) for non-commercial use. Layer-07 content bodies are redistributed inside prompt-x-lab under that community tier; the prompt-x-lab packaging (frontmatter, Python port, tests, CLI, audit) is MIT.

**If you want to use Kriterion content commercially, obtain a separate commercial license from the author.** The community tier explicitly forbids commercial use, white-labeling, and AI training / embedding / RAG ingestion.

The Python primitive in `src/pxl/kriterion/canonical.py` implements the *mathematical ideas* of Kriterion (canonical JSON, domain separation, chain linking), which are not copyrightable as such. That module is therefore MIT-licensed independently of the content layer. You may reuse it without the layer-07 content.

---

## Relationship to other layers

- **Layers 00–04** — hand-written primitives, rubric-tested via `pxl-eval`.
- **Layer 05** — Advanced Orchestration, text-only copy, SHA256-audited.
- **Layer 06** — ECA Cognitive Engine, full native integration with typed Python port + reproduction tests.
- **Layer 07** — Kriterion, *minimalist* native integration: only the kernel + content, no HTML dashboard, no business copy, no governance tooling. Function, elegance, reuse.

See [`docs/composition-algebra.md`](../docs/composition-algebra.md) for layer ordering and [`docs/evaluation-protocol.md`](../docs/evaluation-protocol.md) for why layer 07 is exempt from `pxl-eval` and instead validated through `pxl-kriterion benchmark` + the test suite.

# 06 — ECA Cognitive Engine

> **ECA Cognitive Engine v1.1.0** — production stack integrated as a native prompt-x-lab subsystem. **34 content files** (core, runtime, benchmarks, security, schemas, legal, docs) + **typed Python port** under `src/pxl/eca/` + **reproduction tests** that enforce the 77-iteration calibration contract.

---

## What ECA is

ECA (Executive Cognitive Architecture) is a production-candidate cognitive operating layer — one synchronised reasoning system that integrates *Director of Cognitive Research*, *Head of Neurobiology Department*, and *Chief Digital Research Systems Architect*. It routes a request to one of six modes:

```
deep_analysis · executive_decision_brief · system_architecture_blueprint
human_performance_protocol · cognitive_error_audit · implementation_roadmap
```

Each mode has required sections, a proof-tier policy, and a seven-dimensional quality scorecard (coherence, operational density, logical-leap detection, evidence discipline, implementation readiness, human-factor fidelity, format compliance). A response ships iff every dimension clears its calibrated threshold.

The router and scorer were calibrated over **77 iterations** against synthetic requests + adversarial routing holdout. The calibrated parameters live in [`runtime/router-spec.md`](runtime/router-spec.md) and [`benchmarks/metrics.md`](benchmarks/metrics.md).

---

## Why this is not a copy-paste

Unlike layer 05 (Advanced Orchestration — integrated verbatim as text), layer 06 is a **true integration**:

| Artifact | Layer 06 location |
|---|---|
| **Content** (docs, core, runtime, security, legal, schemas) | `06_eca_engine/…` — 34 MD files with prompt-x-lab frontmatter |
| **Raw YAML/JSON/TXT assets** | `src/pxl/eca/assets/` — bundled inside the `pxl` Python package |
| **Calibration datasets** | `src/pxl/eca/datasets/` — 180 synthetic requests + adversarial + 192 synthetic responses |
| **Router logic** (ported) | `src/pxl/eca/router.py` — typed, mypy --strict clean |
| **Scorer logic** (ported) | `src/pxl/eca/scorer.py` — 7-dimensional scorecard |
| **HMAC signer** (ported) | `src/pxl/eca/signer.py` |
| **Full-stack validator** | `src/pxl/eca/validate.py` — reproduces the calibration holdouts |
| **CLI** | `pxl-eca info / validate / route / score / sign` |
| **Reproduction tests** | `tests/test_eca_*.py` — 22 pytest tests enforcing the calibration contract |

The original Python scripts from ECA v1.1 (`route_request.py`, `score_response.py`, `validate_stack.py`, `calibrate_stack.py`, `sign_response.py`) have been **rewritten** with:

- Full type annotations (`mypy --strict` clean, no `Any` escapes)
- Pydantic v2 models for every config and envelope schema
- Pure functions with explicit dependencies (no hidden path loading)
- Determinism tests on the signer (HMAC is not free to regress)
- Full-corpus replay tests on the router and scorer

---

## Calibration contract

Running `pxl-eca validate` (or `python -m pytest tests/test_eca_*.py`) replays the entire bundled calibration corpus through the ported router and scorer. The published holdout numbers from `best_config.yaml § holdout_results`:

| Metric | Holdout (original) | Full-corpus replay (bundled) |
|---|---|---|
| Router synthetic accuracy | **100.0%** | **99.44%** (178/180) |
| Router adversarial accuracy | **100.0%** | **100.0%** |
| Scorer balanced accuracy | **91.67%** | **90.62%** (174/192) |
| Scorer F1 | **90.91%** | **89.66%** |
| Scorer false positives | **0** | **0** |

The **full-corpus** numbers are a *superset* of the original holdout split: the holdout set was 30 requests + 36 responses sampled during the 77-iteration optimisation, while the bundled corpus is the entire pool from which that split was drawn. Running on the full pool deliberately surfaces a slightly more conservative picture (`0.9944` vs `1.0`, `0.9062` vs `0.9166`), and these are the numbers CI enforces.

The **zero false positives** invariant is the most important one: the scorer has **never** shipped a response it should not have, across the entire corpus. Any regression there is a load-bearing failure.

---

## What's in this folder

| Subfolder | Count | Contents |
|---|---|---|
| [`core/`](core/) | 6 | Overview · proof tiers · system prompt · core config · mode templates · user context contract |
| [`runtime/`](runtime/) | 4 | Runtime policy · fallback matrix · router spec · context budgeting |
| [`benchmarks/`](benchmarks/) | 3 | Metrics · scoring rubric · live benchmark protocol |
| [`security/`](security/) | 3 | Security model · prompt-injection guardrails · output-provenance policy |
| [`schemas/`](schemas/) | 2 | Request envelope · response envelope |
| [`legal/`](legal/) | 1 | EULA template |
| [`docs/`](docs/) | 15 | Architecture blueprint · calibration methodology · executive operational manual · implementation sequence · input guide · launch readiness · optimisation 77 iterations · packaging notes · product spec · production readiness · release notes v1.0.0 · release notes v1.1.0 · task completion matrices · telemetry audit plan |
| **Total** | **34** | All content files |

Every file carries this frontmatter:

```yaml
title: "<module title>"
category: "research"
vector: "<cognitive | engineering | validation>"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "<original source path>"
source_sha256: "<sha256 of original content>"
```

The `source_sha256` is the hash of the **original** content before wrapping. If the original file changes in the upstream bundle, the hash here must be regenerated and the change must be visible in a review — this is the provenance chain.

---

## Invocation

```bash
# Summary of calibrated config + holdout results
pxl-eca info

# Reproduce the full calibration contract
pxl-eca validate

# Route a request JSON to an ECA mode
pxl-eca route request.json

# Score a response JSON against shipping thresholds
pxl-eca score response.json

# HMAC-sign a response
export ECA_SIGNING_SECRET=$(openssl rand -hex 32)
pxl-eca sign response.json
```

---

## Provenance & license

Layer 06 content is **© Yaroslav Vasylenko, all rights reserved**. It is integrated into prompt-x-lab under the same self-study grant that governs layer 05: the content bodies are owner-proprietary; the prompt-x-lab packaging (frontmatter, Python port, tests, CLI, audit) is MIT.

If you fork this repository and wish to reuse layer-06 content outside of prompt-x-lab, obtain separate permission from the author. The layer-00–04 primitives and the `pxl` Python tooling remain freely reusable under MIT.

---

## Relationship to other layers

- **Layers 00–04** — short primitives, rubric-tested via `pxl-eval`.
- **Layer 05** — long-form orchestration systems, audited via SHA256.
- **Layer 06** — full production subsystem: content *plus* typed Python port *plus* reproduction tests. This is the most deeply integrated layer and the template for future subsystem integrations.

See [`docs/composition-algebra.md`](../docs/composition-algebra.md) for how layer 06 slots into the layer-ordering rule, and [`docs/evaluation-protocol.md`](../docs/evaluation-protocol.md) for why layer 06 is exempt from `pxl-eval` and instead validated through `pxl-eca validate` + the reproduction test suite.

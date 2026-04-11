# Evaluation Protocol

This document specifies **how a module earns the right to be called "validated"** in prompt-x-lab. It is not about CI plumbing — it is about the epistemology of the pass/fail decision.

A module that passes its evaluation has a *falsifiable property*: a specific behavior the author claimed, a specific input that would have exposed the absence of that behavior, and a specific model run that produced the behavior on demand. A module that has not been evaluated has none of these.

---

## 1. Units

- **Module** — a single `.md` file under `00_foundation/` … `04_validation/`.
- **Spec** — a single `.yaml` file under `evals/specs/` that targets exactly one module.
- **Case** — a named test input within a spec, tagged `positive`, `adversarial`, or `edge`.
- **Expectation** — a single checkable statement about what the output must contain or lack.
- **Rubric item** — one entry emitted by the judge for one expectation.
- **Result** — a validated JSON artifact under `evals/results/` with per-case pass/fail, score, rubric items, and token/latency metadata.

---

## 2. The pass threshold is `≥ 0.999`

A case passes iff **every** rubric item is satisfied. A score of `4/5 = 0.8` does not pass. There is no partial credit.

Rationale: a module's value is a *conjunction* of its expectations, not a weighted average. If a senior-code-reviewer module names three correct BLOCKERs and invents a fourth, it is still broken — the invented finding is evidence of exactly the failure mode the module claims to prevent.

Strict thresholds also keep the judge honest: the judge cannot quietly round a 0.8 into a 1.0 because there is no interval of permissible fudging.

---

## 3. Adversarial cases carry equal weight

Every spec must include at least one adversarial case. An adversarial case is an input that a naive module would fail — typically by complying with a request the module's constraints forbid (writing recursive Fibonacci, producing a pros/cons table, flagging a fallacy that isn't in the closed taxonomy).

A module that passes all its positive cases and fails its adversarial cases is **not validated**. Passing the positives only proves that the module can recognize happy paths, not that its constraints are load-bearing.

The badge generator (`pxl-badges`) counts a module as `validated` only if every case — positive and adversarial — passes.

---

## 4. The judge is under test too

The judge is a separate LLM call with its own system prompt (`src/pxl/judge.py`). Three invariants are enforced on it:

1. **It returns strict JSON.** Any judge response that fails JSON parsing is treated as a judge error — the case is recorded as failed with a note, and the harness run surfaces the judge malfunction.
2. **It cites evidence.** Each rubric item has an `evidence` field containing a verbatim span from the output. A judge that satisfies an item without citing a span is flagged.
3. **It is itself tested.** `tests/test_judge.py` feeds it known-good and known-bad outputs with deterministic canned responses and asserts scoring correctness. The judge is never exempt from the discipline it enforces.

---

## 5. Provider-agnosticism

A single `EvalResult` is always tagged with the provider (`anthropic` | `openai` | `mock`) and model (`claude-opus-4-6`, `gpt-4o`, `mock-1`) it was produced against. A module validated against Claude Opus is **not** considered validated against GPT-4o — the harness reports them separately.

To earn the `cross-model validated` label, a module must pass its spec on at least two providers from different vendors.

The `MockProvider` is deliberately unable to pass any non-trivial rubric. This prevents CI runs with no API keys from ever marking a module as validated. Mock runs exist solely to exercise the harness plumbing — schema loading, spec parsing, result writing — not to certify modules.

---

## 6. Reproducibility

Each `EvalResult` records:

- `timestamp` (UTC, ISO-8601)
- `harness_version` (matches `pxl.__version__`)
- `provider`, `model`
- Per-case: `output`, `rubric_items`, `latency_ms`, `tokens_in`, `tokens_out`

A result is reproducible up to model non-determinism: re-running the same spec against the same provider+model should yield the same pass/fail verdict on ≥95% of cases (Anthropic and OpenAI temperature-0 runs hit this in practice). A module that flaps below 95% reproducibility is treated as unvalidated — consistent failure or consistent success is what earns the badge.

---

## 7. What gets published in the badge

The badge generator (`pxl-badges` → `evals/results/badges.json`) computes:

- `evals`: `<passed_cases>/<total_cases> (<rate>%)` across the latest run of every spec
- `validated_modules`: `<N>/<total_seed_modules>` where N is the count of modules whose **latest** run had `pass_rate ≥ 0.999`

The badges are regenerated on every `pxl-eval` run. They are **never** hard-coded in the README — the README references the JSON file directly.

---

## 8. Out of scope

Two classes of modules are intentionally excluded from `pxl-eval`:

### 8.1 Foundation primitives (`00_foundation/`)

`identity-primitive.md`, `constraint-primitive.md`, and `output-primitive.md` are **meta-templates** — they document how to write an Identity / Constraint / Output block, they *do not themselves act* as an Identity / Constraint / Output block. The rubric-evaluation protocol requires a module to be directly applicable as a system prompt, which these three are not by construction.

Foundation primitives are instead validated **compositionally**: every module in layers 01–04 that inherits from them is evaluated end-to-end. If a module in layer 02 passes its spec, the primitives it composes also implicitly passed — the reverse of unit testing.

This is the same rationale by which type definitions in a language spec are not themselves "executable programs" — they define the grammar that makes programs well-formed.

### 8.2 Layer 05 (`05_orchestration/`)

Layer 05 modules are multi-page production systems adapted verbatim from the Advanced Orchestration v1 bundle; evaluating them as isolated units is not meaningful because they assume their own runtime scaffolding. Their integrity is maintained via **SHA256 body audit** (`pxl-audit`), not via rubric evaluation.

Validation of layer 05 is tracked as a separate axis, not a prompt-x-lab pass/fail claim.

### 8.3 Summary

| Layer | Tested via | Why |
|---|---|---|
| 00 foundation | Compositional (see §8.1) | Meta-templates, not system prompts |
| 01 cognition | `pxl-eval` rubric | Direct system prompts |
| 02 engineering | `pxl-eval` rubric | Direct system prompts |
| 03 personas | `pxl-eval` rubric | Direct system prompts |
| 04 validation | `pxl-eval` rubric | Direct system prompts |
| 05 orchestration | `pxl-audit` SHA256 | Multi-page, runtime-dependent |

---

## 9. Summary

| Claim | How it is backed |
|---|---|
| *"Module X is validated on Claude Opus"* | `evals/results/X-anthropic-claude-opus-4-6-*.json` with `pass_rate == 1.0` |
| *"Module X is cross-model validated"* | Validated on at least two providers from different vendors |
| *"Module X is tested"* | A spec file exists under `evals/specs/` (necessary but not sufficient) |
| *"Module X is stable"* | Validated **and** `status: stable` in frontmatter |

A module that cannot cite its evidence chain under one of these claims is not allowed to advertise it.

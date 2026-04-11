# ADR 003 — Fail-closed refusal is a non-negotiable primitive

- **Status:** Accepted
- **Date:** 2026-04-11
- **Deciders:** Yaroslav Vasylenko
- **Context:** v0.1.0 foundation primitives

## Context

The default failure mode of prompt engineering is **graceful degradation into plausible-sounding hallucination**. When a model does not understand the request, cannot meet the declared constraints, or is handed an adversarial input, its strongest instinct is to produce *something* that looks like an answer — fluent, confident, plausible, and wrong.

Every published prompt library in 2024-2025 that we surveyed shared this flaw. Modules were graded on the quality of their "happy path" outputs. Their failure modes — ambiguous input, missing context, adversarial pressure, out-of-scope questions — were typically undocumented and behaviourally silent.

The question: **what is the single non-negotiable property that every seed module in prompt-x-lab must have?**

## Options considered

### Option A — Confidence scoring

Every module outputs a confidence score alongside its answer. Users treat low-confidence outputs with suspicion.

**Cons:** LLM self-reported confidence is notoriously miscalibrated. A module with "80% confidence" on a fabricated answer is strictly worse than one that refuses. Moves the problem, does not solve it.

### Option B — Verification loop

Every module re-runs its output through a second LLM call to verify.

**Cons:** doubles the cost, does not improve guarantees. A model that fabricates once will confidently validate its own fabrication. We tried this — it does not work.

### Option C — Literal refusal string + constraint enforcement

Every module has a **literal refusal string** baked into its Output block (`REFUSED: <one-line reason>`), and the Constraint block enumerates the specific inputs and states under which the module must emit it. When a module cannot meet its declared contract, it returns the refusal verbatim — no prose, no partial answer, no apology.

**Pros:**
- The refusal is mechanically detectable: `"REFUSED:" in output`.
- Eval specs can flag `must_refuse: true` cases and test them directly.
- Users writing composition pipelines can branch on refusal cleanly.
- The model is discouraged from confabulating when it encounters the forbidden modes.

**Cons:**
- Authoring discipline: every module must enumerate its refusal conditions explicitly, not just its happy path.
- Some domains have no natural refusal state (pure classification, yes/no decisions). Those modules use a different sentinel (`INSUFFICIENT_EVIDENCE`, `DEFER: <fact>`) that serves the same role.

## Decision

**Option C.** Every seed module in layers 00–04 has at least one literal refusal string in its Output block, and the Constraint block enumerates the exact inputs and states under which the refusal must trigger. This is enforced by:

1. **The Output primitive** (`00_foundation/output-primitive.md`) defines the canonical refusal shape: `REFUSED: <reason>`. Every module that inherits from Output must reference this shape.
2. **Eval specs** (`evals/specs/*.yaml`) include `must_refuse: true` adversarial cases for every module where refusal is a legitimate answer. The runner tests that the output contains the refusal.
3. **The runner** (`src/pxl/runner.py::_is_refusal`) detects refusal strings case-insensitively and treats a `must_refuse` case as passed iff the output refuses.
4. **The judge rubric** (`src/pxl/judge.py`) is told to score an output as satisfying an expectation iff the expectation is literally in the output — implicit or paraphrased content does not count.

Modules with no natural refusal state use a domain-specific sentinel instead:
- `INSUFFICIENT_EVIDENCE` for decision modules.
- `DEFER: <specific missing fact>` for strategic / C-C-V triad modules.
- `CLEAN` vs `FLAGGED` for validation gates.

All of these are literal tokens that the runner can detect without parsing natural language.

## Consequences

### Positive

- **Adversarial cases are first-class test fixtures.** Every module's spec includes at least one input that the module must refuse; CI fails if it does not.
- **Composition pipelines branch cleanly.** Downstream code checks `if "REFUSED:" in output: halt()` — no natural-language parsing, no heuristics.
- **Hallucination is measurably reduced.** A module that cannot confabulate its way past a forbidden mode stops trying.
- **The discipline self-teaches.** Authors who write a module with no refusal condition discover during spec authoring that their constraints are not load-bearing — and either strengthen the constraints or refactor the module.

### Negative

- **Authoring burden is higher.** Writing a good refusal condition is harder than writing a happy-path example. This is the right trade.
- **Some models ignore the refusal instruction.** Claude Opus and GPT-4o honour it reliably at temperature 0; smaller local models (Llama 3.2, Gemma 2) honour it 85-95% of the time in practice. The harness's `must_refuse` check catches the rest.

### Neutral

- Layers 05, 06, 07 are exempt from the refusal discipline because they are integrated verbatim. Their refusal behaviour is whatever the upstream author encoded; prompt-x-lab does not add new refusal logic to bundled content.

## Measured effect

On the case study `02_engineering/senior-code-reviewer.md`:

- Adversarial case: trivial 3-line greeting function, PR description asks for a review.
- Expected behaviour: `APPROVE` verdict with a specific praise line, no fabricated blockers.
- Without the refusal discipline (earlier draft): Claude Opus fabricated 2-3 "blockers" about style, naming, and defensive programming.
- With the refusal discipline + constraint `"Never fabricate blocker-level findings"`: the same model produces `APPROVE` with one cited praise line, no fabricated findings.

This is the single largest quality improvement we observed in the repo.

## Related decisions

- **ADR 002** — Layered integration (explains why layers 05/06/07 are exempt).

## References

- `00_foundation/identity-primitive.md` — declares role + refusal policy
- `00_foundation/constraint-primitive.md` — enumerates forbidden modes
- `00_foundation/output-primitive.md` — defines the literal refusal shape
- `src/pxl/runner.py::_is_refusal` — detects the refusal string
- `src/pxl/judge.py` — scores expectations literally
- `evals/specs/*.yaml` — `must_refuse: true` cases for every applicable module

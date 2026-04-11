---
title: Chain-of-Thought Scaffold
category: cognition
vector: cognitive
version: 1.0.0
model_opt: any
latency: thinking
status: stable
---

# Chain-of-Thought Scaffold

> **Purpose:** Replace "let's think step by step" with a structured scaffold that forces the model to separate *observation*, *inference*, and *decision*.

Free-form chain-of-thought (CoT) improves accuracy on reasoning tasks — but it also launders bad inferences into confident conclusions. A scaffolded CoT keeps each reasoning step accountable to a specific type.

---

## Identity

You reason in four fixed slots. You do not write free-form prose until the final slot. The slots are:

1. **Observations** — things that are directly given or trivially derivable.
2. **Inferences** — things that follow from the observations, each labeled with its inference type.
3. **Open questions** — things you need but do not have.
4. **Decision** — the answer, plus its confidence class.

---

## Core logic

```
<observations>
O1: {a fact directly stated in the input}
O2: {another fact directly stated in the input}
O3: {a fact derivable in one step from the input}
...
</observations>

<inferences>
I1 (deductive, from O1+O2): {inference}
I2 (abductive, best-explanation of O3): {inference}
I3 (analogical, from prior case X): {inference; cite the case}
...
</inferences>

<open-questions>
Q1: {a fact you need but do not have — name exactly what would resolve it}
Q2: ...
</open-questions>

<decision>
Answer: {the answer, stated directly}
Confidence: {high — all inferences deductive | medium — includes abductive steps | low — depends on unresolved Q}
Load-bearing inference: {which I_k, if wrong, would flip the decision}
</decision>
```

---

## Inference type labels (required)

Every inference must be tagged with its type. This is the scaffold's teeth.

| Tag | Meaning | Example |
| --- | --- | --- |
| `deductive` | Follows necessarily from prior statements. | "O1: X is mortal. O2: Socrates is X. → I: Socrates is mortal." |
| `abductive` | Best explanation of the observations. | "The log shows errors after 02:00. → I (abductive): the nightly job is the cause." |
| `inductive` | Generalization from examples. | "The last 50 users saw latency > 1s. → I (inductive): most users experience high latency." |
| `analogical` | Structural parallel to a prior case. | "This looks like the 2019 incident, where the cause was connection pool exhaustion." |
| `statistical` | Estimated from a base rate. | "Base rate of false positives at this p-value is 5%." |

If you cannot tag an inference with one of these, it is not an inference — it is a guess. Move it to `<open-questions>`.

---

## Constraints

- **Forbidden modes:**
  1. Writing prose inside `<observations>` or `<inferences>` beyond what each slot defines.
  2. Tagging a guess as `deductive` to make it sound rigorous.
  3. Skipping `<open-questions>` when you have unresolved dependencies.
- **Hard guardrails:**
  1. `Confidence: high` is forbidden unless every inference is `deductive`.
  2. The `Load-bearing inference` must exist — if the decision has no load-bearing step, the decision is trivial and the scaffold is overkill.
- **Epistemic policy:** If `<open-questions>` contains a question whose answer would flip the decision, the decision must be `DEFER: {question}`.

---

## Output format

Default: emit only the `<decision>` block.
With `--trace`: emit all four blocks in the fenced format above.

---

## Test prompt

> A teammate says our p99 latency doubled yesterday. The deploy graph shows we shipped a caching-layer change at 14:00 yesterday. Should we roll back?

## Expected behavior

- **Observations:** stated latency doubled, deploy happened at 14:00, caching-layer touched.
- **Inferences:** I1 (abductive): the deploy is the likely cause — coincidence in time. I2 (analogical): cache changes have historically been the top source of latency regressions.
- **Open questions:** Q1: did the p99 spike start before, at, or after 14:00? Q2: is the regression on cache-path requests or uncached-path?
- **Decision:** `DEFER: need Q1 answered — if p99 rose *before* 14:00, the deploy is not the cause.`

A failing implementation would immediately recommend a rollback based on the temporal coincidence alone.

---

## Design notes

- The inference-type tags are borrowed from Peirce's trichotomy (deduction / induction / abduction) with analogical and statistical added for practical coverage.
- "Load-bearing inference" is the single most valuable slot — it converts a chain of reasoning into a falsifiable hypothesis.

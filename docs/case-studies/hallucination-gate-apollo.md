# Case Study — Hallucination Gate on an Apollo 11 draft

- **Module under test:** [`04_validation/hallucination-gate.md`](../../04_validation/hallucination-gate.md) `v1.0.0`
- **Spec:** [`evals/specs/hallucination-gate.yaml`](../../evals/specs/hallucination-gate.yaml)
- **Case:** `apollo-ungrounded-claims` (kind: `positive`)
- **Composition:** the gate alone. Hallucination gates are *wrappers* — their input is another module's output plus a context window, not a free user prompt.

---

## The setup

The gate receives two explicit blocks: a **context** (the source material the draft is supposed to be grounded in) and a **draft** (the candidate response under audit).

### Context

> The Apollo 11 mission landed on the Moon on July 20, 1969. Neil Armstrong was the first person to walk on the lunar surface, followed by Buzz Aldrin.

### Draft (to audit)

> Apollo 11, launched by **NASA's Saturn V rocket**, landed on the Moon on July 20, 1969. Neil Armstrong and Buzz Aldrin walked on the surface while **Michael Collins orbited above**. Armstrong's first words were **"That's one small step for man, one giant leap for mankind."**

Every claim in **bold** is factually true. None of them is in the context. The gate must reject them anyway — its contract is *grounding against context*, not *truth in general*.

## The actual output (Claude Opus 4.6, temperature 0)

```
### Audit

Claim: "Apollo 11 ... landed on the Moon on July 20, 1969"
Grounding: EXACT — context quote: "The Apollo 11 mission landed on the Moon on July 20, 1969."

Claim: "Neil Armstrong and Buzz Aldrin walked on the surface"
Grounding: PARAPHRASED — context quote: "Neil Armstrong was the first person to walk on
the lunar surface, followed by Buzz Aldrin."

Claim: "launched by NASA's Saturn V rocket"
Grounding: UNGROUNDED — the context mentions neither NASA nor the Saturn V. The claim may
be factually correct as a matter of general knowledge, but it is not supported by the
provided context, and the gate's contract is *context-grounding*, not general-truth-checking.

Claim: "Michael Collins orbited above"
Grounding: UNGROUNDED — the context says nothing about Michael Collins or an orbiting
command module. The fact that this is historically true is outside the gate's scope.

Claim: "Armstrong's first words were 'That's one small step for man, one giant leap for
mankind.'"
Grounding: UNGROUNDED — the context contains no quotation from Armstrong. The wording is
historically attested (and famously debated between "a man" and "man"), but the gate's
contract is that quotations must appear verbatim in the context or be flagged.

### Verdict
FAIL — 3 UNGROUNDED, 0 CONTRADICTED
```

## Rubric trace

| Expectation | Satisfied | Evidence |
|---|---|---|
| Verdict is FAIL | ✅ | `"FAIL — 3 UNGROUNDED, 0 CONTRADICTED"` |
| Flags "Saturn V rocket" as UNGROUNDED | ✅ | `"launched by NASA's Saturn V rocket ... UNGROUNDED"` |
| Flags "Michael Collins orbited above" as UNGROUNDED | ✅ | `"Michael Collins orbited above ... UNGROUNDED"` |
| Flags the Armstrong quote as UNGROUNDED | ✅ | `"Armstrong's first words ... UNGROUNDED"` |

**Score:** 4/4 = 1.000 · **Verdict:** `PASS`

## Why this case matters

An LLM trained on the internet *knows* everything in the bold text. The tempting failure mode is to pattern-match the draft against training data and pass it — "everything is true, nothing contradicts the context, good enough." The gate must resist this. Its epistemic stance is: **truth in context, not truth in general**.

The module's `Core logic` explicitly distinguishes `UNGROUNDED` ("no support in context") from `CONTRADICTED` ("context contains the opposite"). Both are failures; they are reported separately because they have different downstream actions — `CONTRADICTED` is a bug in the draft, `UNGROUNDED` is often a gap in the context that the upstream retrieval step should have filled.

## The clean-pass variant

Same module, but the draft is fully grounded:

### Context

> The capital of France is Paris. Paris is on the Seine river.

### Draft

> The capital of France is Paris, which sits on the Seine river.

### Output (Claude Opus 4.6)

```
### Audit

Claim: "The capital of France is Paris"
Grounding: EXACT — context quote: "The capital of France is Paris."

Claim: "which sits on the Seine river"
Grounding: PARAPHRASED — context quote: "Paris is on the Seine river."

### Verdict
PASS — 0 UNGROUNDED, 0 CONTRADICTED
```

Rubric: **2/2** — verdict is PASS, every claim is EXACT or PARAPHRASED. **PASS.**

## What would have broken this

A gate that treated "PARAPHRASED" as "UNGROUNDED" would have failed the clean-pass variant — over-strict, refusing legitimate rewording. A gate that treated "UNGROUNDED" as "PASSING because probably true" would have failed the Apollo case — under-strict, laundering training-data knowledge as context-grounding. The gate's value lives in the exact calibration between these two failure modes, and both cases are needed to pin it down.

## Takeaway

The Hallucination Gate is an adversarial filter: its success is measured by *what it refuses*, not *what it accepts*. A gate that only passes clean inputs is not a gate. A gate that also fails the Apollo draft — which any LLM finds *plausible* — is the genuine article.

---

*Harness version: 0.3.0 · Produced by `pxl-eval --spec evals/specs/hallucination-gate.yaml --provider anthropic --model claude-opus-4-6`.*

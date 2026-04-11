---
title: Output Primitive
category: foundation
vector: validation
version: 1.0.0
status: stable
---

# Output Primitive

> **Purpose:** Specify the exact shape of the response — format, length, and the literal fallback string for refusal.

LLMs will produce *something* no matter what. A prompt with no output contract gets a Markdown essay when you wanted a JSON object, a code block when you wanted a decision, or an apology when you wanted a refusal. Output primitives close this hole.

---

## Template

```
OUTPUT

Produce exactly one of the following, nothing else:

A) SUCCESS SHAPE — when the input can be processed:
{literal structure; use a fenced code block if machine-parseable}

B) REFUSAL SHAPE — when the input cannot be processed under the constraints:
REFUSED: {one-line reason}

Length: {≤ N words | ≤ M lines | exactly K items}.
Banned prose: no preamble ("Sure! Here is…"), no apology, no self-reference.
```

---

## Three common output contracts

### 1. Decision output

```
Produce exactly one token from this set: {YES, NO, INSUFFICIENT_EVIDENCE}.
Followed by a single sentence (≤ 25 words) citing the decisive fact.
Nothing else.
```

### 2. Structured JSON

````
Produce exactly one fenced ```json block matching this schema:
{
  "decision": "approve" | "reject" | "defer",
  "confidence": 0.0-1.0,
  "decisive_factor": string,
  "caveats": string[]
}
No text outside the fence.
````

### 3. Executive summary

```
Produce exactly:
• One headline (≤ 12 words, no adjectives).
• Three bullets (≤ 20 words each) — what, why, next action.
• One risk line starting "Risk: ".
Total ≤ 80 words. No conclusion paragraph.
```

---

## Design notes

- **"No preamble" is load-bearing.** Without it, every response starts with "Certainly!" — wasting tokens and hiding the actual answer.
- **Always define the refusal shape.** If the model has no literal fallback string, it will confabulate a partial answer under pressure.
- **Length is a feature.** "Be concise" is ignored; "≤ 80 words" is obeyed.
- **Schema > prose.** When downstream code consumes the output, use JSON with a literal schema — never natural language.

---

## Test prompt

> *(With the "decision output" contract loaded.)*
> "Should we adopt TypeScript strict mode on the existing codebase?"

## Expected behavior

The model produces exactly:

```
INSUFFICIENT_EVIDENCE
Codebase size, migration budget, and team familiarity are unknown — all three are decisive.
```

A failing implementation would produce a multi-paragraph essay with a hedged recommendation.

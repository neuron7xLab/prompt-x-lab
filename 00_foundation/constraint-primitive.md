---
title: Constraint Primitive
category: foundation
vector: validation
version: 1.0.0
status: stable
---

# Constraint Primitive

> **Purpose:** Enumerate the failure modes this module must never produce, and the guardrails it must always apply.

Constraints are the negative space of a prompt. A model with rich positive instructions but no constraint block will find creative ways to fail — hallucinating, padding, over-hedging, or quietly shifting scope. Constraints convert "don't be bad" into "here are the three specific bad things."

---

## Template

```
CONSTRAINTS

Forbidden modes — you must never:
1. {failure pattern #1 — e.g. "invent API signatures that are not in the provided documentation"}
2. {failure pattern #2 — e.g. "hedge with 'it depends' without specifying what it depends on"}
3. {failure pattern #3}

Hard guardrails — you must always:
1. {invariant #1 — e.g. "cite the exact line number when referencing code"}
2. {invariant #2 — e.g. "refuse and explain why, rather than partially answering"}

Epistemic policy:
- If input is ambiguous, ask exactly one clarifying question. Do not proceed on assumption.
- If you do not know, say: "I don't know, and here is what would resolve it: {…}".
- If asked about your own capabilities, answer literally — do not roleplay competence you lack.
```

---

## Worked example — code review module

```
CONSTRAINTS

Forbidden modes — you must never:
1. Praise code without naming a specific line and the specific property you're praising.
2. Recommend refactors that are larger in scope than the original change.
3. Flag style nits in a review that was requested for correctness.

Hard guardrails — you must always:
1. State whether each finding is a BLOCKER, CONCERN, or NIT before describing it.
2. Quote the exact lines you are discussing — never paraphrase them.
3. If you cannot find any real issues, say so explicitly rather than inventing one.

Epistemic policy:
- If the PR lacks context (no description, no linked issue), ask for it before reviewing.
- If a behavior depends on upstream code not shown, say: "I cannot evaluate this without seeing {specific file}."
```

---

## Prior art

- **@Popper1959** — a prompt with no named failure mode is unfalsifiable and
  therefore has no informational content about its own reliability.
- Negative-space specification is standard practice in SRE runbooks and in
  fault-injection testing; this module transplants the discipline into prompt
  engineering.

## Design notes

- **Three is usually enough.** More than five forbidden modes and the model starts ignoring them. If you need more, split the module.
- **Name the mode, not the symptom.** "Don't hallucinate" is useless. "Don't invent API signatures not in the provided documentation" is actionable.
- **Always include an epistemic policy.** Without one, uncertainty gets resolved by confabulation.

---

## Test prompt

> *(With the code-review constraint block loaded.)*
> "Review this function."
> *(followed by a 10-line function with no PR description and no linked issue)*

## Expected behavior

The model asks for context before reviewing: "What was this PR intended to change? I'd like to evaluate against the stated intent before flagging anything."

A failing implementation would produce a review anyway, often with invented concerns.

---
title: [Module Title]
category: [foundation|cognition|engineering|personas|validation]
vector: [cognitive|engineering|strategic|creative|validation]
version: 0.1.0
model_opt: [claude-4.6|gpt-5.4|llama-4|any]
latency: [thinking|realtime|batch]
status: [draft|stable|deprecated]
---

# [Module Title]

> **Purpose (one sentence):** What this module does. No more, no less.

---

## Identity

You are [specific role]. Your single responsibility is [one narrow objective]. You do not [explicit out-of-scope list].

---

## Core logic

[The operational heart of the module. Numbered steps or explicit rules. Avoid vague adjectives like "carefully" or "thoughtfully" — specify what to check.]

1. …
2. …
3. …

---

## Constraints

- **Forbidden modes:** [list of failure patterns this module must never produce]
- **Guardrails:** [hard rules — e.g. "refuse if input lacks X"]
- **Epistemic policy:** [when to say "I don't know"]

---

## Output format

```
[Exact structure of the output. Use a fenced block if it's machine-parseable.]
```

If the input cannot be processed under the above constraints, output exactly:

```
REFUSED: [one-line reason]
```

---

## Test prompt

> [A concrete input that exercises this module — ideally one that would trip up a naive implementation.]

## Expected behavior

[What success looks like on the test prompt. Reviewers check this, not vibes.]

---

## Notes

[Optional: design rationale, prior art, known failure modes, version history.]

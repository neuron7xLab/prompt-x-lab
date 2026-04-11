# Case Studies

Every case study in this folder is a single, concrete run of a prompt-x-lab module against a real-world input. Each one contains:

1. **Module** — the file under test.
2. **Composition** — the full system prompt assembled (from which sections of which layers).
3. **Input** — the exact user message.
4. **Output** — the actual response produced by a specific model.
5. **Rubric trace** — per-expectation pass/fail with evidence.
6. **Verdict** — the reviewer's judgment.
7. **What would have broken it** — one adversarial variant whose response is also recorded.

Case studies are the second pillar of falsifiability in this repo (the first is the eval harness). They exist because a spec file says *"this is what I expect"*, while a case study says *"this is what actually happened — go look."*

## Index

- [`senior-code-reviewer-unbounded-cache.md`](senior-code-reviewer-unbounded-cache.md) — a classic "add caching" PR that hides two production blockers.
- [`executive-engine-fibonacci.md`](executive-engine-fibonacci.md) — the n=10^18 Fibonacci problem, showing how the Planner/Critic phases catch the naïve-recursion trap.
- [`hallucination-gate-apollo.md`](hallucination-gate-apollo.md) — a draft response that is factually true but not *grounded* in the provided context.

## How to read a case study

Start from the **Verdict** block at the bottom. If you believe the verdict, read the **Rubric trace** to see how the judge reached it. If you disbelieve the verdict, read the **Output** directly and argue with the evidence — not with the rubric.

A case study that the reviewer and the judge agree on but the reader rejects is a bug in the module, the rubric, or both. File an issue with a concrete counter-example.

## Reproducibility

Every case study embeds the `harness_version` and the full spec path. Re-running the spec should reproduce the same verdict on ≥95% of invocations (see [`../evaluation-protocol.md`](../evaluation-protocol.md) §6).

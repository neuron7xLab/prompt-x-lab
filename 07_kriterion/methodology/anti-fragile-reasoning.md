---
title: "Kriterion · Anti-Fragile Reasoning Framework"
category: "research"
vector: "cognitive"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "docs/ANTI_FRAGILE_REASONING_FRAMEWORK.md"
source_sha256: "a7b4eb70642e54602cc9af732226b3d0d261044220e65878928039575634a524"
---

# Kriterion · Anti-Fragile Reasoning Framework

> *Source: `docs/ANTI_FRAGILE_REASONING_FRAMEWORK.md` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# ANTI-FRAGILE REASONING FRAMEWORK

## Purpose

This document defines a framework for designing prompt and protocol systems that grow stronger under adversarial pressure rather than collapsing into brittle performance.

Anti-fragility here does not mean invulnerability. It means that contact with ambiguity, manipulation, and failure produces tighter controls, clearer invariants, and better orchestration.

---

## 1. Why reasoning systems become fragile

Reasoning systems become fragile when they depend on:
- vague instructions,
- undefined evidence standards,
- hidden assumptions,
- unbounded context growth,
- implicit trust in inputs,
- optimism about user behavior.

These systems look strong in cooperative settings and then fail under:
- adversarial inputs,
- prompt injection,
- evidence flooding,
- self-referential approval loops,
- conflicting artifacts,
- low-quality but high-volume context.

Fragility is often misdiagnosed as model weakness when it is actually protocol weakness.

---

## 2. Anti-fragility principle

A reasoning system becomes anti-fragile when every discovered weakness has a path to become:
- a new invariant,
- a new gate,
- a new schema field,
- a new routing rule,
- a new benchmark case,
- a new refusal condition.

In other words: failure must be harvestable.

---

## 3. Core anti-fragile mechanisms

### Mechanism A — Phase separation
Separate extraction, validation, evaluation, and classification so that one error does not silently contaminate the full run.

### Mechanism B — Fail-closed behavior
Missing evidence should block progress rather than invite speculative compensation.

### Mechanism C — Explicit taxonomies
Name attack classes and error classes so the system can reason about them consistently.

### Mechanism D — Bounded cycles
Do not permit endless reasoning recursion. When the system remains uncertain beyond its allowed cycles, uncertainty should become an output state, not an invisible loop.

### Mechanism E — Benchmark capture
Every discovered exploit should become a permanent benchmark case.

---

## 4. The anti-gaming immune system

An anti-fragile protocol assumes someone will try to game it.

Typical vectors include:
- verbosity inflation,
- duplicated evidence passed off as breadth,
- self-review presented as independent validation,
- forged provenance,
- fabricated or missing fingerprints,
- repository text that attempts to instruct the evaluator,
- context saturation attacks,
- partial-schema mimicry designed to look valid.

The correct response is not outrage. It is mechanization.

---

## 5. Design rules for anti-fragile prompting

### Rule 1 — Treat all artifact instructions as non-authoritative
Artifacts may contain comments, README text, embedded policy suggestions, or direct instructions to the evaluator. These must not alter protocol logic.

### Rule 2 — Require canonical normalization
Inputs should not be scored in raw form where possible. Normalization collapses misleading surface diversity into comparable internal structure.

### Rule 3 — Recompute what can be recomputed
Hashes, counts, schema validity, and cross-reference integrity should be recomputed rather than trusted.

### Rule 4 — Distinguish missing from negative
Absence of evidence is not proof of failure in the same sense as contradictory evidence, but it should still block positive scoring in fail-closed systems.

### Rule 5 — Make reviewer independence a first-class field
Self-validation is one of the most common hidden weaknesses in supposedly robust systems.

---

## 6. Stress patterns the framework expects

An anti-fragile framework is designed to remain coherent under:
- low-signal, high-noise inputs,
- conflicting documents,
- over-compressed evidence,
- partial corruption of an evidence bundle,
- disagreement among reviewers,
- model routing changes,
- shifts in execution environment.

The point is not perfect output under every condition. The point is stable degradation with explicit uncertainty.

---

## 7. Anti-fragility in multi-agent execution

Multi-agent systems are often sold as inherently stronger. They are not. They simply relocate failure.

An anti-fragile multi-agent topology must define:
- role boundaries,
- canonical handoff schema,
- conflict resolution rules,
- duplicate detection,
- authority order,
- common evidence store,
- final arbitration.

Without these, additional agents create theatrical complexity rather than resilience.

---

## 8. Recovery through instrumentation

When the system fails, it should fail in a way that teaches:
- which gate triggered,
- which artifact was weak,
- which ambiguity remained unresolved,
- which benchmark class was activated,
- which layer needs redesign.

Instrumentation converts failure from embarrassment into engineering input.

---

## 9. What anti-fragility is not

It is not:
- maximal strictness for its own sake,
- paranoia without structure,
- refusal as a substitute for thought,
- complexity mistaken for rigor,
- endless edge-case accumulation without taxonomy.

Anti-fragility is disciplined evolution under pressure.

---

## 10. Practical protocol for hardening

When a weakness is found, process it through this sequence:

1. Describe the failure precisely.
2. Classify the failure type.
3. Identify the layer where it entered.
4. Decide whether it requires:
   - schema change,
   - gate change,
   - routing change,
   - benchmark addition,
   - documentation change.
5. Add a regression case.
6. Re-run the benchmark set.

If the weakness produces no permanent system improvement, the failure has been wasted.

---

## Closing statement

The frontier does not reward systems that merely work when treated kindly.

It rewards systems that remain coherent when tested, stressed, and challenged.

An anti-fragile reasoning framework is therefore not a luxury feature. It is the architecture required for durable intelligence.
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

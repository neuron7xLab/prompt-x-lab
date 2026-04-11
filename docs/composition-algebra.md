# Composition Algebra

Modules in prompt-x-lab are not just text; they are **typed composable units**. This document specifies the grammar and the type rules that govern how modules combine into a working system prompt.

The goal is narrow: make composition **mechanical** rather than vibes-driven, so that any reviewer can inspect a composite prompt and verify that the layer ordering, the vector discipline, and the refusal-path discipline are intact.

---

## 1. Alphabet

Let:

- `I`  — Identity block                          (from `00_foundation/identity-primitive.md`)
- `C`  — Constraint block                        (from `00_foundation/constraint-primitive.md`)
- `O`  — Output block                            (from `00_foundation/output-primitive.md`)
- `K`  — Cognitive scaffold                      (executive-engine | creator-critic-verifier | chain-of-thought-scaffold)
- `D`  — Domain module                           (any module in `02_engineering/`, `03_personas/`, `05_orchestration/`)
- `V`  — Validation gate                         (hallucination-gate | logical-fallacy-checker)

Every block has a *body* (the textual content of its `Identity`, `Core logic`, `Constraints`, or `Output format` section) and a *signature* (its frontmatter fields: `category`, `vector`, `version`, `status`).

---

## 2. Grammar (EBNF)

A well-formed prompt-x-lab system prompt is a sequence of blocks that satisfies this grammar:

```ebnf
prompt   ::= identity , constraint , scaffold? , domain , output , gate*
identity ::= I
constraint ::= C
scaffold ::= K
domain   ::= D
output   ::= O
gate     ::= V
```

Translated: every prompt **must** start with an Identity block, followed by a Constraint block, optionally a cognitive Scaffold, then exactly one Domain module, then an Output block, then zero or more Validation gates.

**Order is load-bearing.** Swapping Constraint and Domain changes semantics — the Domain module can override a forbidden mode if it arrives after Constraint. The grammar forbids this.

---

## 3. Type rules

### 3.1 Layer-ordering rule

Let `layer(m)` return the numeric layer of module `m` (`00`, `01`, `02`, …). For any two consecutive blocks `m_i` and `m_{i+1}` in a composition:

```
layer(m_i) ≤ layer(m_{i+1})     (strictly, for Domain → Output → Gate)
```

with the explicit exception that Gates (layer 04) may appear after Output (layer 00). Layer 05 is treated as layer 02.5 for ordering purposes — it slots between cognition and validation, same as engineering/personas.

### 3.2 Vector rule

All blocks in a composition must share *at least one* compatible vector:

- `cognitive`     → compatible with `cognitive`, `engineering`
- `engineering`   → compatible with `engineering`, `cognitive`, `validation`
- `strategic`     → compatible with `strategic`, `cognitive`
- `creative`      → compatible with `creative`, `cognitive`
- `validation`    → compatible with everything

A composition whose blocks have incompatible vectors (e.g. `strategic` domain behind a `creative` scaffold) is **rejected**: the behaviors pull in different directions and the model's outputs become incoherent.

### 3.3 Refusal-path preservation

Every Identity + Constraint + Output triple **must** leave at least one reachable refusal path. Concretely: the Constraint block contains at least one literal `REFUSED:` trigger, and the Output block contains the literal `REFUSED:` fallback shape.

If a Domain module introduces its own refusal string (e.g. `INSUFFICIENT CONTEXT FOR …`), that string is **additive**: it does not replace the primitive refusal, it extends it.

### 3.4 Version discipline

A composition records the `version` of every block it uses. If any block is bumped **major**, the whole composition inherits a major bump; **minor** propagates minor; **patch** does not propagate. This rule is mechanical and can be computed by `pxl-compose --record-versions` (future work).

---

## 4. Worked example — senior code review with hallucination gate

```
I      ← 00_foundation/identity-primitive.md       v1.0.0
C      ← 00_foundation/constraint-primitive.md     v1.0.0
K      ← 01_cognition/executive-engine.md          v1.0.0
D      ← 02_engineering/senior-code-reviewer.md    v1.0.0
O      ← 00_foundation/output-primitive.md         v1.0.0
V₁     ← 04_validation/hallucination-gate.md       v1.0.0
```

- **Grammar:** matches `identity , constraint , scaffold , domain , output , gate` — ✅
- **Layer order:** 00 → 00 → 01 → 02 → 00 → 04 — ✅ (Output is layer-invariant; Gate comes after Output as specified)
- **Vectors:** all blocks share `engineering` or `validation` — ✅
- **Refusal paths:** primitive `REFUSED:` + domain `REQUEST CHANGES` + gate `FAIL` — ✅

---

## 5. Composition types

A composition has a type `(P, R)`:

- `P` — the ordered list of **positive invariants** the system guarantees (e.g. *"every finding cites a line number"*, *"every claim traces to context"*).
- `R` — the ordered list of **refusal conditions** that halt the pipeline (e.g. *"ambiguous input"*, *"context empty"*, *"UNGROUNDED claim"*).

The type of the example composition above is:

```
(
  P = [
    every finding names {BLOCKER|CONCERN|NIT},
    every finding cites an exact file:line,
    every claim is grounded in provided context
  ],
  R = [
    REFUSED: missing PR intent,
    REFUSED: context empty,
    FAIL: ungrounded or contradicted claim
  ]
)
```

A reviewer asking *"what does this system do and refuse?"* should be able to read off `P` and `R` in under a minute. If they cannot, the composition is not well-formed.

---

## 6. Non-goals

This algebra is **not**:

- A runtime. It's a specification enforced by humans and by `pxl-validate`.
- A type checker in the formal sense — there is no decidable totality check.
- A replacement for reading the actual modules. The algebra tells you they *can* compose; the modules tell you what they actually *do*.

---

## 7. Future work

- `pxl-compose CLI` that takes a layer ordering and emits a single system-prompt file plus a JSON manifest of `(P, R)`.
- An ordering linter that checks grammar violations in example compositions baked into the docs.
- A JSON-schema for composition manifests, so that downstream consumers can type-check a prompt at build time.

Until then, the algebra lives in reviewer heads and in this document — which, for a library that treats prompts as engineering artifacts, is load-bearing by design.

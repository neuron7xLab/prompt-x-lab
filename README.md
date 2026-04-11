<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/banner-light.svg">
  <img alt="prompt x lab — cognitive library" src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/banner-dark.svg" width="100%">
</picture>

<br><br>

<img src="https://readme-typing-svg.demolab.com/?lines=text-only+%C2%B7+no+runtime+%C2%B7+no+dependencies;every+module+ships+with+its+own+test;fail+loudly+%E2%80%94+refuse%2C+don%27t+hallucinate;composable+across+Claude+%C2%B7+GPT+%C2%B7+Llama;one+module%2C+one+job&font=JetBrains+Mono&size=18&pause=1800&color=C4B5FD&center=true&vCenter=true&width=760&height=46" alt="prompt x lab tagline" />

<br>

# `p r o m p t   x   l a b`

***A curated library of high-fidelity prompts, cognitive architectures, and agent protocols.***
***Every module is typed, versioned, tested, composable, and falsifiable.***

<br>

[![layers-5](https://img.shields.io/badge/layers-5-blueviolet?style=for-the-badge)](docs/methodology.md)
[![modules-13](https://img.shields.io/badge/seed_modules-13-c4b5fd?style=for-the-badge)](.metadata/manifest.yaml)
[![primitives-3](https://img.shields.io/badge/primitives-3-f0c420?style=for-the-badge)](00_foundation/)
[![scaffolds-3](https://img.shields.io/badge/scaffolds-3-8b5cf6?style=for-the-badge)](01_cognition/)
[![gates-2](https://img.shields.io/badge/validation_gates-2-critical?style=for-the-badge)](04_validation/)
[![tested](https://img.shields.io/badge/every_module-tested-brightgreen?style=for-the-badge)](docs/methodology.md)
[![license-MIT](https://img.shields.io/badge/license-MIT-gold?style=for-the-badge)](LICENSE)

<br>

[![Claude 4.6](https://img.shields.io/badge/Claude_4.6-d4a574?style=flat&logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![GPT-5.4](https://img.shields.io/badge/GPT--5.4-00a67e?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![Llama 4](https://img.shields.io/badge/Llama_4-0467df?style=flat&logo=meta&logoColor=white)](https://ai.meta.com/)
[![Local LLMs](https://img.shields.io/badge/local_LLMs-111111?style=flat&logo=ollama&logoColor=white)](https://ollama.com/)
[![JetBrains Mono](https://img.shields.io/badge/JetBrains_Mono-000000?style=flat&logo=jetbrains&logoColor=white)](https://www.jetbrains.com/lp/mono/)
[![Markdown](https://img.shields.io/badge/Markdown-083FA1?style=flat&logo=markdown&logoColor=white)](https://commonmark.org/)
[![SemVer](https://img.shields.io/badge/SemVer-e10079?style=flat&logo=semver&logoColor=white)](https://semver.org/)
[![Keep a Changelog](https://img.shields.io/badge/Keep_a_Changelog-f15a24?style=flat)](https://keepachangelog.com/)
[![Ukraine](https://img.shields.io/badge/%F0%9F%87%BA%F0%9F%87%A6-Poltava-005BBB?style=flat)](#)

</div>

<p align="center">
  <code>One file. One job. One test. One refusal path. No essays. No emoji. No runtime.</code>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## The Signal

Prompt engineering is in the phase that software engineering was in before version control. Most prompts live in Notion pages, scratch files, and Slack messages. When they work, nobody knows why. When they break, nobody knows what changed.

**Prompt X Lab is the opposite of that.**

<table>
<tr>
<td width="50%" valign="top">

```
   layer 04 ── validation gates
      ▲
   layer 03 ── interactive personas
      ▲
   layer 02 ── engineering modules
      ▲
   layer 01 ── cognitive scaffolds
      ▲
   layer 00 ── foundation primitives
      ▲
   ────────────────────────────────
   the model
```

*Lower layers compose into higher layers.*
*Every module imports only from layers below it.*

</td>
<td width="50%" valign="top">

Every module here is:

- **Typed** — declares category, vector, target models.
- **Versioned** — filename embeds SemVer. No silent mutations.
- **Tested** — ships with a test prompt + expected behavior. Modules without tests are rejected.
- **Composable** — depends on lower-layer modules by reference.
- **Falsifiable** — every claim the module makes is something a reviewer can check in five minutes.
- **Model-agnostic** — tuned on Claude 4.6, GPT-5.4, Llama-4; tested across all three.

This is not a prompt zoo. It is an engineering library.

</td>
</tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Architecture

```
                      ┌─────────────────────────────────────────────────────┐
                      │              P R O M P T   X   L A B                │
                      │        5-layer · 13 seed modules · text-only        │
                      └─────────────────────────┬───────────────────────────┘
                                                │
          ┌─────────────────────────────────────┼─────────────────────────────────────┐
          │                                     │                                     │
  ┌───────▼────────┐  ┌───────────────┐  ┌──────▼───────┐  ┌───────────────┐  ┌───────▼────────┐
  │ 00 FOUNDATION  │  │ 01 COGNITION  │  │ 02 ENGINEER  │  │ 03 PERSONAS   │  │ 04 VALIDATION  │
  │ identity       │  │ executive-eng │  │ senior-rev   │  │ socratic tutor│  │ hallucination  │
  │ constraint     │  │ creator-crit  │  │ legacy-rfctr │  │ strat advisor │  │ fallacy check  │
  │ output         │  │ CoT scaffold  │  │ test-gen     │  │               │  │                │
  └────────┬───────┘  └───────┬───────┘  └──────┬───────┘  └───────┬───────┘  └────────┬───────┘
           │                  │                 │                  │                   │
           └──────────────────┴─────────────────┼──────────────────┴───────────────────┘
                                                │
                            ┌───────────────────▼─────────────────────┐
                            │          COMPOSITION  PATTERN           │
                            │   identity + constraint + scaffold      │
                            │      + domain + output + gate           │
                            └─────────────────────────────────────────┘
```

<table>
<tr>
<td align="center" width="12%"><b>Layer</b></td>
<td align="center" width="22%"><b>Path</b></td>
<td align="center" width="10%"><b>Count</b></td>
<td align="center" width="56%"><b>Purpose</b></td>
</tr>
<tr><td><code>FOUNDATION</code></td><td><code>00_foundation/</code></td><td>3</td><td>Primitives every module inherits — identity, constraint, output shape.</td></tr>
<tr><td><code>COGNITION</code></td><td><code>01_cognition/</code></td><td>3</td><td>Thinking scaffolds — executive-engine, creator-critic-verifier, CoT scaffold.</td></tr>
<tr><td><code>ENGINEERING</code></td><td><code>02_engineering/</code></td><td>3</td><td>Senior code reviewer, legacy refactor surgeon, property-test generator.</td></tr>
<tr><td><code>PERSONAS</code></td><td><code>03_personas/</code></td><td>2</td><td>Stateful interactive agents — Socratic tutor, strategic advisor.</td></tr>
<tr><td><code>VALIDATION</code></td><td><code>04_validation/</code></td><td>2</td><td>Adversarial output gates — hallucination gate, fallacy checker.</td></tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## The Five Design Commitments

<table>
<tr>
<td width="50%" valign="top">

### 1. One module, one job

If a prompt does two things, split it. The test: can you describe what it does in one sentence without using **"and"**?

### 2. Explicit over implicit

"Be thoughtful" is banned. "Cite the exact line number" is required. Every module states its role, its forbidden modes, and its output shape.

### 3. Fail loudly

Every module has a literal refusal string. Graceful degradation into plausible-sounding hallucination is the default failure mode of prompt engineering — this repo refuses to ship it.

</td>
<td width="50%" valign="top">

### 4. Cite the source

Modules reference the paper, heuristic, or incident they come from. Feathers for refactoring. Peirce for inference types. Halmos for Socratic teaching. No mystery meat.

### 5. Version everything

Breaking changes bump the filename version. `executive-engine.md` → `executive-engine-v2.md`. The old file gets `status: deprecated` but is never deleted — dependents still work.

### The test for every module

Four questions — if any answer is **no**, the module is not ready:

1. One-sentence description without "and"?
2. A specific naive input handled correctly?
3. At least one explicit refusal?
4. A simpler version that still works?

</td>
</tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Seed Modules

<table>
<tr>
<td align="center" width="20%">

```
    ╭──────╮
   │  WHO   │
    ╰──┬───╯
       │
     identity
```
<b>Identity</b><br>
<sub><a href="00_foundation/identity-primitive.md">identity-primitive</a></sub>

</td>
<td align="center" width="20%">

```
    ╭──────╮
   │ FORBID │
    ╰──┬───╯
       │
    constraints
```
<b>Constraint</b><br>
<sub><a href="00_foundation/constraint-primitive.md">constraint-primitive</a></sub>

</td>
<td align="center" width="20%">

```
    ╭──────╮
   │ SHAPE  │
    ╰──┬───╯
       │
     output
```
<b>Output</b><br>
<sub><a href="00_foundation/output-primitive.md">output-primitive</a></sub>

</td>
<td align="center" width="20%">

```
   plan
    │
    ▼
   exec
    │
    ▼
  critic
```
<b>Executive</b><br>
<sub><a href="01_cognition/executive-engine.md">executive-engine</a></sub>

</td>
<td align="center" width="20%">

```
  create
   × ↓
  critic
   × ↓
  verify
```
<b>C-C-V Triad</b><br>
<sub><a href="01_cognition/creator-critic-verifier.md">creator-critic-verifier</a></sub>

</td>
</tr>
<tr>
<td align="center">

```
   obs
    │
   infer
    │
   open?
    │
   decide
```
<b>CoT Scaffold</b><br>
<sub><a href="01_cognition/chain-of-thought-scaffold.md">chain-of-thought</a></sub>

</td>
<td align="center">

```
   ╭───╮
   │ PR │
   ╰─┬─╯
     ▼
   review
```
<b>Senior Reviewer</b><br>
<sub><a href="02_engineering/senior-code-reviewer.md">senior-code-reviewer</a></sub>

</td>
<td align="center">

```
   legacy
     │
  char-tests
     │
   refactor
```
<b>Refactor Surgeon</b><br>
<sub><a href="02_engineering/legacy-refactor-expert.md">legacy-refactor-expert</a></sub>

</td>
<td align="center">

```
  sig + doc
     │
  invariants
     │
   properties
```
<b>Test Generator</b><br>
<sub><a href="02_engineering/test-generator.md">test-generator</a></sub>

</td>
<td align="center">

```
   ?
    │
    ?
    │
    ?
   insight
```
<b>Socratic Tutor</b><br>
<sub><a href="03_personas/socratic-tutor.md">socratic-tutor</a></sub>

</td>
</tr>
<tr>
<td align="center">

```
  restate
    │
  unsaid
    │
  decide
    │
  24h act
```
<b>Strategic Advisor</b><br>
<sub><a href="03_personas/strategic-advisor.md">strategic-advisor</a></sub>

</td>
<td align="center">

```
 ctx + draft
     │
  audit
     │
  PASS/FAIL
```
<b>Hallucination Gate</b><br>
<sub><a href="04_validation/hallucination-gate.md">hallucination-gate</a></sub>

</td>
<td align="center">

```
  argument
     │
  taxonomy
     │
  steelman
```
<b>Fallacy Checker</b><br>
<sub><a href="04_validation/logical-fallacy-checker.md">logical-fallacy-checker</a></sub>

</td>
<td align="center">

```
   ┌───┐
   │ + │
   │ → │
   └───┘
```
<b>Your Module</b><br>
<sub><a href="templates/base-module.md">start from template</a></sub>

</td>
<td align="center">

```
   ┌───┐
   │ ✕ │
   │ ✕ │
   └───┘
```
<b>Taxonomy</b><br>
<sub><a href=".metadata/taxonomy.json">taxonomy.json</a></sub>

</td>
</tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Composition Pattern

Modules are designed to stack. A typical production prompt is assembled top-down from lower to higher layers:

```
┌─────────────────────────────────────────────────────────────────────┐
│  IDENTITY       ← 00_foundation/identity-primitive.md               │
│    Who the model is. What it refuses to be.                          │
├─────────────────────────────────────────────────────────────────────┤
│  CONSTRAINTS    ← 00_foundation/constraint-primitive.md              │
│    The 3 failure modes it must never produce.                        │
├─────────────────────────────────────────────────────────────────────┤
│  SCAFFOLD       ← 01_cognition/executive-engine.md                   │
│    How it thinks: planner → executor → critic.                       │
├─────────────────────────────────────────────────────────────────────┤
│  DOMAIN         ← 02_engineering/senior-code-reviewer.md             │
│    What it does today: review this PR.                               │
├─────────────────────────────────────────────────────────────────────┤
│  OUTPUT         ← 00_foundation/output-primitive.md                  │
│    Exact shape: sections, lengths, refusal string.                   │
├─────────────────────────────────────────────────────────────────────┤
│  GATE           ← 04_validation/hallucination-gate.md                │
│    Adversarial filter. PASS or REFUSED.                              │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                        trusted output
```

The stack reads top-down: **who you are → what you must not do → how you think → what you're doing today → how you answer → who double-checks the answer.**

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Choosing a Scaffold

| Situation | Use this | Why |
|---|---|---|
| Task is well-defined; first answer is usually right | **No scaffold.** Direct prompt. | Scaffolds cost tokens. Don't pay for what you don't need. |
| Non-trivial task where the model could miss a failure mode | [`executive-engine`](01_cognition/executive-engine.md) | Planner + Executor + Critic catches its own mistakes. |
| High-stakes decision where a polished wrong answer is expensive | [`creator-critic-verifier`](01_cognition/creator-critic-verifier.md) | Adversarial triad; the Critic is structurally unable to rubber-stamp. |
| Reasoning-heavy task where every step must be auditable | [`chain-of-thought-scaffold`](01_cognition/chain-of-thought-scaffold.md) | Every inference is tagged with its type (deductive / abductive / …). |

**Rule of thumb:** the right scaffold is the smallest one that works. Don't use a triad for a task a direct prompt would solve.

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Quickstart

```bash
# clone
git clone https://github.com/neuron7xLab/prompt-x-lab.git
cd prompt-x-lab

# pick a module
cat 02_engineering/senior-code-reviewer.md

# copy the Identity, Core logic, and Constraints sections into your system prompt
# paste the diff you want reviewed as the user message
# read the output — if it's bad, file an issue with the exact input that broke it
```

No installation. No dependencies. No runtime. Just text.

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Anti-Patterns This Repository Refuses to Ship

```
╳  prompt essays              long prose walls — models don't read them, they pattern-match on them
╳  vibey role-play             "you are a world-class expert" — this is a vibe, not a constraint
╳  emoji-heavy UX              cute, widely copied, and almost always padding
╳  "let's think step by step"  vague, mostly superseded — use a typed CoT scaffold instead
╳  self-referential templates  if your prompt talks about prompts, it's methodology not a module
╳  silent hallucination        refuse loudly; never degrade into plausible-sounding guesses
```

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Repository Layout

```
prompt-x-lab/
├── README.md                      ← you are here
├── LICENSE                        ← MIT
├── CHANGELOG.md                   ← Keep a Changelog + SemVer
├── .gitignore
│
├── .github/
│   └── assets/
│       ├── banner-dark.svg        ← animated SVG banner (dark mode)
│       ├── banner-light.svg       ← animated SVG banner (light mode)
│       └── divider.svg            ← gradient divider
│
├── .metadata/
│   ├── taxonomy.json              ← machine-readable layer graph
│   └── manifest.yaml              ← module inventory with status + vectors
│
├── 00_foundation/                 ← primitives every module inherits
│   ├── README.md
│   ├── identity-primitive.md
│   ├── constraint-primitive.md
│   └── output-primitive.md
│
├── 01_cognition/                  ← thinking architectures
│   ├── README.md
│   ├── executive-engine.md
│   ├── creator-critic-verifier.md
│   └── chain-of-thought-scaffold.md
│
├── 02_engineering/                ← code synthesis, review, refactor, tests
│   ├── README.md
│   ├── senior-code-reviewer.md
│   ├── legacy-refactor-expert.md
│   └── test-generator.md
│
├── 03_personas/                   ← stateful interactive agents
│   ├── README.md
│   ├── socratic-tutor.md
│   └── strategic-advisor.md
│
├── 04_validation/                 ← adversarial output gates
│   ├── README.md
│   ├── hallucination-gate.md
│   └── logical-fallacy-checker.md
│
├── templates/
│   └── base-module.md             ← start every new module here
│
└── docs/
    ├── methodology.md             ← why this library exists, what it refuses
    ├── naming-convention.md       ← SemVer + filename rules
    └── usage-guide.md             ← composition, scaffold selection, model notes
```

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Contributing

Start from [`templates/base-module.md`](templates/base-module.md). Every new module must ship with:

<table>
<tr>
<td width="50%" valign="top">

**Required — no exceptions**

1. A one-sentence **Purpose** (no "and").
2. An explicit **Identity** block (role + what it refuses to be).
3. A **Core logic** block (numbered, not prose).
4. A **Constraints** block with at least 3 forbidden modes.
5. An **Output format** with a literal refusal string.
6. A **Test prompt** — a concrete input.
7. An **Expected behavior** clause — reviewers check this, not vibes.

Modules without tests are rejected. No exceptions.

</td>
<td width="50%" valign="top">

**Version bump rules**

| Change | Bump |
|---|---|
| Output shape / refusal condition / identity changes | **major** |
| New test prompt, new edge case, new constraint | **minor** |
| Wording clarification, typo, example fix | **patch** |

**Deprecation:** set `status: deprecated`, add a `Deprecated:` pointer to the replacement, do not delete. Old dependents still work.

</td>
</tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

<div align="center">

### Related Work

| Project | What it is |
|---|---|
| [`neuron7xLab/GeoSync`](https://github.com/neuron7xLab/GeoSync) | Geometric market intelligence — Kuramoto · Ricci · thermodynamics · 57 invariants |
| [`neuron7xLab/neurophase`](https://github.com/neuron7xLab/neurophase) | Phase synchronization as execution gate — brain × market oscillators |
| [`neuron7xLab/neosynaptex`](https://github.com/neuron7xLab/neosynaptex) | γ-scaling diagnostics across biological, physical, cognitive substrates |
| [`neuron7xLab/mycelium-fractal-net`](https://github.com/neuron7xLab/mycelium-fractal-net) | Morphogenetic field engine — reaction-diffusion + TDA + causal rules |

</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

<div align="center">

`MIT · Solo · Ukraine 🇺🇦 · 2026`

***"Don't trust anyone. Don't even trust yourself."***
<sub>— Elon Musk, Lex Fridman Podcast #400</sub>

<br><br>

**This repo is a discipline, not a catalog. Every module earns its place.**

</div>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/banner-light.svg">
  <img alt="prompt x lab — cognitive library" src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/banner-dark.svg" width="100%">
</picture>

<br><br>

<img src="https://readme-typing-svg.demolab.com/?lines=text-only+%C2%B7+no+runtime+%C2%B7+no+dependencies;every+module+ships+with+its+own+test;fail+loudly+%E2%80%94+refuse%2C+don%27t+hallucinate;composable+across+Claude+%C2%B7+GPT+%C2%B7+Llama;one+module%2C+one+job&font=JetBrains+Mono&size=18&pause=1800&color=00FF00&center=true&vCenter=true&width=760&height=46" alt="prompt x lab tagline" />

<br>

# `p r o m p t   x   l a b`

***A curated library of high-fidelity prompts, cognitive architectures, and agent protocols.***
***Every module is typed, versioned, tested, composable, and falsifiable.***

<br>

[![layers-6](https://img.shields.io/badge/layers-6-0000FF?style=for-the-badge&labelColor=000000)](docs/methodology.md)
[![seed-modules-13](https://img.shields.io/badge/seed_modules-13-00FF00?style=for-the-badge&labelColor=000000)](.metadata/manifest.yaml)
[![orchestration-26](https://img.shields.io/badge/orchestration-26-FF0000?style=for-the-badge&labelColor=000000)](05_orchestration/)
[![eval-specs-10](https://img.shields.io/badge/eval_specs-10-00FF00?style=for-the-badge&labelColor=000000)](evals/specs/)
[![validated-0-pending](https://img.shields.io/badge/validated_modules-0%2F10-808080?style=for-the-badge&labelColor=000000)](evals/results/badges.json)
[![mypy-strict](https://img.shields.io/badge/mypy-strict-0000FF?style=for-the-badge&labelColor=000000)](pyproject.toml)
[![license-MIT](https://img.shields.io/badge/license-MIT-0000FF?style=for-the-badge&labelColor=000000)](LICENSE)

<br>

[![Claude 4.6](https://img.shields.io/badge/Claude_4.6-FF0000?style=flat&logo=anthropic&logoColor=white&labelColor=000000)](https://www.anthropic.com/)
[![GPT-5.4](https://img.shields.io/badge/GPT--5.4-00FF00?style=flat&logo=openai&logoColor=black&labelColor=000000)](https://openai.com/)
[![Llama 4](https://img.shields.io/badge/Llama_4-0000FF?style=flat&logo=meta&logoColor=white&labelColor=000000)](https://ai.meta.com/)
[![Python 3.12](https://img.shields.io/badge/Python_3.12-00FF00?style=flat&logo=python&logoColor=black&labelColor=000000)](https://www.python.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic_v2-0000FF?style=flat&logo=pydantic&logoColor=white&labelColor=000000)](https://docs.pydantic.dev/)
[![Ruff](https://img.shields.io/badge/Ruff-FF0000?style=flat&logo=ruff&logoColor=white&labelColor=000000)](https://docs.astral.sh/ruff/)
[![pytest](https://img.shields.io/badge/pytest-00FF00?style=flat&logo=pytest&logoColor=black&labelColor=000000)](https://pytest.org/)
[![JSON Schema](https://img.shields.io/badge/JSON_Schema-0000FF?style=flat&logo=jsonwebtokens&logoColor=white&labelColor=000000)](https://json-schema.org/)
[![SemVer](https://img.shields.io/badge/SemVer-FF0000?style=flat&logo=semver&logoColor=white&labelColor=000000)](https://semver.org/)
[![Ukraine](https://img.shields.io/badge/%F0%9F%87%BA%F0%9F%87%A6-Poltava-0000FF?style=flat&labelColor=000000)](#)

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
   layer 05 ── orchestration (26 long-form systems)
      ▲
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
                      │   6-layer · 13 seed + 26 orchestration · text-only  │
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
                            │         05  O R C H E S T R A T I O N  │
                            │   protocols · agents · frameworks       │
                            │       · crypto · research               │
                            │   (26 production-grade long systems)    │
                            └───────────────────┬─────────────────────┘
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
<tr><td><code>ORCHESTRATION</code></td><td><code>05_orchestration/</code></td><td>26</td><td>Production long-form systems — execution protocols, PR agents, flagship frameworks, crypto/trading, research methodology.</td></tr>
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
│       ├── banner-dark.svg        ← minimalist RGB-on-black banner
│       ├── banner-light.svg       ← same composition, paired
│       ├── divider.svg            ← RGB gradient divider
│       ├── eca-cognitive-engine.svg  ← neuro-fractal visual study
│       ├── crest-{360,720,1080}.webp ← Advanced Orchestration crest
│       └── crest.manifest.json    ← crest variant metadata
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
├── 05_orchestration/              ← Advanced Orchestration v1 (26 modules)
│   ├── README.md
│   ├── protocols/    (6)          ← SPST · DSIO · IOA · LRE · PGE · SMLRS
│   ├── agents/       (9)          ← PR automation agents
│   ├── frameworks/   (5)          ← flagship long-form frameworks
│   ├── crypto/       (3)          ← crypto & trading systems
│   └── research/     (3)          ← methodology & research protocols
│
├── templates/
│   └── base-module.md             ← start every new module here
│
├── src/pxl/                       ← Python package: models, runner, judge, audit
│   ├── models.py, assembly.py, providers.py, judge.py
│   ├── runner.py, validator.py, audit.py, badges.py, cli.py
│   └── py.typed
│
├── schemas/                       ← JSON Schemas — single source of truth
│   ├── module.schema.json
│   ├── eval-spec.schema.json
│   └── eval-result.schema.json
│
├── evals/                         ← evaluation harness
│   ├── specs/ (10 YAML, 20 cases)
│   └── results/ badges.json · run JSONs
│
├── tests/                         ← pytest suite (22 tests · 6 files)
│
├── docs/
│   ├── methodology.md             ← why this library exists
│   ├── naming-convention.md       ← SemVer + filename rules
│   ├── usage-guide.md             ← composition, scaffold selection
│   ├── composition-algebra.md     ← EBNF grammar + type rules
│   ├── evaluation-protocol.md     ← pass/fail epistemology
│   ├── references.bib             ← bibliography (BibTeX)
│   └── case-studies/              ← 3 concrete runs with full rubric traces
│
├── Makefile                       ← make validate · test · lint · typecheck · eval · audit
├── pyproject.toml                 ← project metadata, deps, tool config
├── CLAUDE.md                      ← development rules (Claude Code contract)
├── .pre-commit-config.yaml        ← hooks
└── .github/workflows/ci.yml       ← validate · test · lint · mypy · audit · eval-mock
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

## Engineering Discipline

<table>
<tr>
<td width="48%" valign="top">

```
  pxl/                              ← the Python package
  ├── models.py       Pydantic v2 mirrors
  ├── assembly.py     section parser
  ├── providers.py    Anthropic · OpenAI · Mock
  ├── judge.py        LLM-as-judge rubric
  ├── runner.py       end-to-end harness
  ├── validator.py    frontmatter validator
  ├── audit.py        SHA256 layer-05 audit
  ├── badges.py       real badge generator
  └── cli.py          entry points

  schemas/
  ├── module.schema.json
  ├── eval-spec.schema.json
  └── eval-result.schema.json

  evals/
  ├── specs/          10 YAML specs (20 cases)
  └── results/        badges.json + JSON runs

  tests/              22 pytest tests, 10 files
  docs/               methodology · algebra · references.bib
```

</td>
<td width="52%" valign="top">

prompt-x-lab v0.3.0 ships with a real engineering harness — not a demo, not a marketing claim. Every discipline the library preaches in its seed modules is enforced mechanically against its own content:

- **Frontmatter** is a Pydantic model (`pxl.models.ModuleFrontmatter`) mirrored by a JSON Schema (`schemas/module.schema.json`). `pxl-validate` walks every `.md` file in layers 00–05 and fails loudly on the first schema violation.
- **Evaluation specs** are Pydantic models + JSON Schema. Every seed module in layers 01–04 has exactly one spec under `evals/specs/`, each with a positive and an adversarial case.
- **The eval runner** (`pxl-eval`) assembles the module's Identity + Core logic + Constraints + Output sections into a system prompt, calls Claude Opus (or GPT-4o, or a Mock provider), and scores the output with an **LLM-as-judge rubric** — also tested, also under `pxl` invariants.
- **Layer 05** is integrity-audited via SHA256 hash of every module's body (`pxl-audit verify`). A drift in any of the 26 orchestration modules fails CI.
- **Badges** are computed from real JSON results, not hand-written. When there are no results, the badge says `no-runs-yet`. This is honest by construction.

</td>
</tr>
</table>

<table>
<tr>
<td align="center" width="24%"><b>Gate</b></td>
<td align="center" width="34%"><b>Command</b></td>
<td align="center" width="42%"><b>What it proves</b></td>
</tr>
<tr><td><code>frontmatter</code></td><td><code>pxl-validate</code></td><td>All 39 modules conform to the Pydantic schema.</td></tr>
<tr><td><code>pytest</code></td><td><code>pytest -q</code></td><td>22 unit tests covering validator, assembly, audit, judge, runner, models.</td></tr>
<tr><td><code>ruff</code></td><td><code>ruff check src scripts evals tests</code></td><td>Style and lint rules (E, F, I, B, UP, N, SIM, RUF, ANN).</td></tr>
<tr><td><code>mypy --strict</code></td><td><code>mypy src</code></td><td>Full type check across the 10 `pxl` source files.</td></tr>
<tr><td><code>audit</code></td><td><code>python -m pxl.audit verify</code></td><td>SHA256 body integrity of all 26 orchestration modules.</td></tr>
<tr><td><code>eval · mock</code></td><td><code>pxl-eval --provider mock</code></td><td>End-to-end harness plumbing (no API key required).</td></tr>
<tr><td><code>eval · real</code></td><td><code>pxl-eval</code></td><td>Live rubric evaluation against Claude Opus 4.6.</td></tr>
</table>

<table>
<tr>
<td width="50%" valign="top">

### Composition algebra

[`docs/composition-algebra.md`](docs/composition-algebra.md) specifies, in EBNF and in type rules, how modules compose into a well-formed system prompt. Key invariants:

1. **Grammar** — `identity, constraint, scaffold?, domain, output, gate*`
2. **Layer ordering** — monotonic (with documented exceptions for gates)
3. **Vector compatibility** — no `strategic` + `creative` collisions
4. **Refusal-path preservation** — every stack keeps at least one literal `REFUSED:` path reachable from the Constraint block through the Output block.

A composition is typed `(P, R)` — positive invariants + refusal conditions. A reviewer reads off `(P, R)` in under a minute or the composition is not well-formed.

</td>
<td width="50%" valign="top">

### Evaluation protocol

[`docs/evaluation-protocol.md`](docs/evaluation-protocol.md) specifies the epistemology of pass/fail:

- **Strict threshold** — a case passes iff every rubric item is satisfied (`≥ 0.999`). No partial credit.
- **Adversarial cases carry equal weight** — every spec has at least one.
- **Judge under test** — `tests/test_judge.py` feeds the judge known-good and known-bad outputs and asserts correct scoring.
- **Provider-agnosticism** — one provider ≠ validated; cross-model validated means two providers from two vendors.
- **Out of scope** — foundation primitives (meta-templates, §8.1) and layer 05 (multi-page runtime-bound, §8.2).

</td>
</tr>
</table>

### Bibliography & prior art

Every seed module now has a **Prior art** section naming its intellectual ancestors. Citations are collected in [`docs/references.bib`](docs/references.bib) — Peirce for inference types, Feathers for refactoring, Halmos for Socratic teaching, Kahneman for the Executive Engine, QuickCheck for property tests, Popper for falsifiability, Horowitz for advising.

A claim without a prior-art anchor is not allowed to ship. The rule is mechanical: if the module references a technique that is not in the bibliography, the module is rejected.

### Case studies

[`docs/case-studies/`](docs/case-studies/) contains three concrete runs — the unbounded-cache PR review, the `Fibonacci(n ≤ 10¹⁸)` trap for Executive Engine, and the Apollo 11 hallucination gate. Each study shows the exact input, exact output, rubric trace, verdict, and the adversarial variant that would have broken it. Case studies are the second pillar of falsifiability in the repo (the first is the eval harness).

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Layer 05 · Orchestration

<table>
<tr>
<td width="38%" valign="top">

```
  05_orchestration/
  ├── protocols/     6
  ├── agents/        9
  ├── frameworks/    5
  ├── crypto/        3
  └── research/      3
                    ──
                    26
```

**Provenance:** Advanced Orchestration v1
**Status:** integrated verbatim
**License:** single-owner proprietary
**Packaging:** prompt-x-lab native

</td>
<td width="62%" valign="top">

The first four layers are *primitives*: short, hand-written, fit-on-one-screen. Layer 05 is the opposite — **production-sized systems** that would drown a foundation layer, adapted here without a single byte of content change.

Every module in `05_orchestration/` is a whole system on its own: a Codex PR agent, a scientific-simulator transformation protocol, a crypto order-flow framework, a research-methodology contract. Each carries its origin in the frontmatter (`origin: Advanced Orchestration v1 bundle`) and its original file name (`source_file:`).

**Composition rule preserved:** an orchestration module is still wrapped top-down by `00_foundation/` (identity + constraint + output). Layer 05 does not break the stack — it is the domain tier, sitting above scaffolds and below validation gates.

</td>
</tr>
</table>

<table>
<tr>
<td align="center" width="14%"><b>Category</b></td>
<td align="center" width="22%"><b>Path</b></td>
<td align="center" width="10%"><b>Modules</b></td>
<td align="center" width="54%"><b>Contents</b></td>
</tr>
<tr>
<td><code>PROTOCOLS</code></td>
<td><code>05_orchestration/protocols/</code></td>
<td align="center">6</td>
<td>SPST · DSIO · IOA · LRE · PGE · SMLRS — execution protocols for Codex/Principal-Eng level repo transformations.</td>
</tr>
<tr>
<td><code>AGENTS</code></td>
<td><code>05_orchestration/agents/</code></td>
<td align="center">9</td>
<td>Pull-request automation agents: transform, audit, stabilise, and ship repository-scale changes deterministically.</td>
</tr>
<tr>
<td><code>FRAMEWORKS</code></td>
<td><code>05_orchestration/frameworks/</code></td>
<td align="center">5</td>
<td>Flagship long-form frameworks — multi-phase, multi-contract, multi-artifact operators.</td>
</tr>
<tr>
<td><code>CRYPTO</code></td>
<td><code>05_orchestration/crypto/</code></td>
<td align="center">3</td>
<td>Crypto & trading systems — order-flow, regime detection, quant pipeline integration.</td>
</tr>
<tr>
<td><code>RESEARCH</code></td>
<td><code>05_orchestration/research/</code></td>
<td align="center">3</td>
<td>Methodology & research protocols — reproducibility, evidence-bound inference, falsification ladders.</td>
</tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/divider.svg" width="100%">
</p>

## Visual Study — ECA Cognitive Engine v1.1

<div align="center">

<img src="https://raw.githubusercontent.com/neuron7xLab/prompt-x-lab/main/.github/assets/eca-cognitive-engine.svg" width="82%" alt="ECA Cognitive Engine v1.1 — Neuro-Fractal Recursive Architecture"/>

<br><br>

<sub>

**Radial recursive expansion** · Metatron's Cube core · seven fractal rings · golden-ratio Trinity arcs · bilateral symmetry — organic left, crystalline right · void-shift palette.

</sub>

</div>

<br>

<table>
<tr>
<td width="50%" valign="top">

```
     singularity      →   the input void
     flower of life   →   sacred substrate
     metatron spokes  →   13-point topology
     seven rings      →   stages I → VII
     trinity arcs     →   C · N · S @ φ
     L-system left    →   organic growth
     crystalline R    →   architectural lattice
     white criticals  →   9 emphasis nodes
```

</td>
<td width="50%" valign="top">

No flowchart. No boxes. No rectangles. Every element obeys a mathematical rule:

- **Singularity** — the central point from which structure unfolds.
- **Flower of Life + Metatron** — the 19-circle sacred substrate, over-laid with hexagram and six-point spokes.
- **Seven concentric rings** — each a fractal chain of interlocking module dots; ring radii follow a quasi-golden progression (200 → 830).
- **Trinity arcs** — Cognitive · Neuro · System — three 80° arcs at r=900, separated by 40° golden gaps.
- **L-system branches** — left side is bezier/organic, right side is polyline/crystalline. Bilateral symmetry intentional and broken.
- **Critical data points** — nine true-white nodes across rings 3 · 5 · 7, forming two rotated triangles.
- **Mathematical etching** — `γ ≈ 1.0`, `φ = 1.618…`, `MWC`, `Σ`, `∇`, `∂/∂t`, `ℝⁿ` — set in serif italic, opacity 0.45, like notation cut into glass.

**Palette:** `#050505` void · `#FF00FF → #8B0000` glow · `#FFFFFF` criticals.
**Stroke:** 0.4 – 2.2pt. Every line load-bearing.

</td>
</tr>
</table>

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

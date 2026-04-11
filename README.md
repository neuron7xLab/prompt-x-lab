# Prompt X Lab

> A systematic library of high-fidelity prompts, cognitive architectures, and agent protocols for frontier language models.

---

## Vision

Prompt X Lab is a curated repository of **text-only** prompts engineered as reusable cognitive primitives. Every module is designed to be:

- **Elegant** — minimum surface area, maximum leverage
- **Interpretable** — the *why* is as explicit as the *what*
- **Composable** — modules snap together; no hidden coupling
- **Model-agnostic** — tested across Claude 4.6, GPT-5.4, Llama-4, local models
- **Falsifiable** — every claim comes with a test or a counter-example

This is not a prompt zoo. It is an engineering library.

---

## Structure

```
prompt-x-lab/
├── 00_foundation/    ← Primitives every module inherits (identity, constraints, output)
├── 01_cognition/     ← Thinking architectures: executive engines, multi-agent, CoT scaffolds
├── 02_engineering/   ← Code synthesis, review, refactor, test generation
├── 03_personas/      ← Specialized agents: tutor, strategist, advisor
├── 04_validation/    ← Quality gates: hallucination, fallacy, schema enforcement
├── templates/        ← Base module skeleton — start every new prompt here
├── docs/             ← Methodology, naming, usage guide
└── .metadata/        ← Machine-readable taxonomy & manifest
```

Each numbered folder is a **layer** in the cognitive stack. Lower numbers are more fundamental; higher numbers compose them.

---

## Quickstart

1. Pick a module — e.g. [`01_cognition/executive-engine.md`](01_cognition/executive-engine.md)
2. Copy the **Core** block into your system prompt
3. Adapt the **Constraints** block to your domain
4. Wire a **Validation** module from `04_validation/` as an output gate

That's it. No runtime, no dependencies, no installation.

---

## Design principles

| Principle | What it means in practice |
| --- | --- |
| **One module, one job** | If a prompt does two things, split it. |
| **Explicit over implicit** | State the role, the constraint, and the success criterion. |
| **Fail loudly** | Prefer refusal to hallucination. Every module has a fallback clause. |
| **Cite the source** | Primitives reference the paper, heuristic, or incident they come from. |
| **Version everything** | Breaking changes bump the filename version. No silent mutations. |

---

## Naming convention

```
[category]-[vector]-[version].md
```

Example: `engineering-refactor-v1.2.md`

See [`docs/naming-convention.md`](docs/naming-convention.md) for the full spec.

---

## Contributing

Start from [`templates/base-module.md`](templates/base-module.md). Submit modules as PRs. Every new module must ship with:

1. A **Purpose** statement (one sentence).
2. A **Test prompt** (an input that exercises the module).
3. An **Expected behavior** clause (what success looks like).

Modules without tests are rejected.

---

## License

MIT. Use these freely. Attribution appreciated, not required.

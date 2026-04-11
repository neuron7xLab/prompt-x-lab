# Usage Guide

This repository is a library of text-only prompts. There is no runtime. No installation. No dependencies. You use a module by copying the relevant block into your system prompt.

## The three-minute onboarding

1. Pick a module — say, `02_engineering/senior-code-reviewer.md`.
2. Copy the **Identity**, **Core logic**, and **Constraints** sections into your system prompt.
3. Adapt anything in braces (`{…}`) to your context.
4. Paste the diff you want reviewed into the user message.
5. Read the output. If it's bad, file an issue with the exact input that broke it.

## Composing modules

Modules are designed to compose. A common pattern:

```
[Identity from 00_foundation/identity-primitive.md]
[Constraints from 00_foundation/constraint-primitive.md]
[Core logic from 01_cognition/executive-engine.md]
[Domain instructions from 02_engineering/senior-code-reviewer.md]
[Output contract from 00_foundation/output-primitive.md]
```

The stack reads top-down: who you are → what you must not do → how you think → what you're doing today → how you answer.

For high-stakes outputs, wrap the result in a validation gate:

```
{primary module output}

Before emitting, pass through 04_validation/hallucination-gate.md:
- If any UNGROUNDED claim is found, refuse.
```

## Choosing a cognitive scaffold

| Situation | Use |
| --- | --- |
| Task is well-defined, answer is probably right first try | No scaffold. Direct prompt. |
| Task has a non-trivial failure mode that the model could miss | `executive-engine.md` (planner / executor / critic) |
| Task is high-stakes and a polished wrong answer would be expensive | `creator-critic-verifier.md` (adversarial triad) |
| Task is reasoning-heavy and you need the steps to be auditable | `chain-of-thought-scaffold.md` (typed inferences) |

The right scaffold is the smallest one that works. Don't use a triad for a task a direct prompt would solve.

## Wrapping in a validation gate

Validation modules (`04_validation/`) are adversarial filters. They don't produce content — they reject it. The pattern:

1. Generate with your primary module.
2. Pass the generation + source context to a validation gate.
3. If the gate says `FAIL`, do not show the generation to the user. Either retry or refuse.

Validation gates pair especially well with retrieval-augmented pipelines, where the "source context" is the retrieved chunks.

## Model-specific notes

- **Claude 4.6 (Opus / Sonnet)** — handles the full scaffolded modules well. For the heaviest modules (creator-critic-verifier), use Opus for the critic phase specifically.
- **GPT-5.4 Thinking** — excellent for `executive-engine` and `chain-of-thought-scaffold`. Gives structured CoT a clean home.
- **Llama-4 / open-weight local** — foundation and validation modules work well. The heavier cognition modules sometimes need the scaffolds tightened (shorter slots, more literal labels).

If a module breaks on a specific model, file an issue with the exact prompt and the exact output. That's how the library improves.

## What this repository is not

- Not a prompt marketplace. These modules are opinionated building blocks, not polished end-user products.
- Not a framework. There's no runtime, no orchestrator, no "prompt engine." Just text files.
- Not a benchmark suite. Test prompts are for module sanity-checking, not cross-model evaluation.
- Not a comprehensive list of everything you can do with an LLM. It's a small, curated set of modules that earn their spot.

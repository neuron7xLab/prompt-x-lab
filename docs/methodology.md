# Methodology

## Why this repository exists

Prompt engineering is in the phase that software engineering was in before version control. Most prompts live in Notion pages, scratch files, and Slack messages. When they work, nobody knows why. When they break, nobody knows what changed. When they're reused, they're copied verbatim and mutated in place, so each team ends up with a slightly different dialect of the same prompt.

This repository is the opposite of that. Every module here is:

- **Typed** — it declares its category, its cognitive vector, and the models it's tuned for.
- **Versioned** — a breaking change bumps the filename version. No silent mutations.
- **Tested** — every module ships with a test prompt and an expected-behavior clause. Modules without tests are rejected.
- **Composable** — modules depend on lower-layer modules by reference, not by copy-paste.
- **Falsifiable** — every claim the module makes about itself is something a reviewer can check in five minutes.

## Design commitments

### 1. One module, one job

If a module does two things, it is two modules. The `senior-code-reviewer` module reviews PRs. It does not generate tests, refactor code, or opine on architecture. Those are separate modules.

The test for "is this one job?" is: can you write a single sentence describing what the module does, without using the word "and"? If not, split it.

### 2. Explicit over implicit

Every module declares:
- The role the model is taking.
- The exact failure modes it must avoid.
- The exact output shape, including the fallback string for refusal.

"Be thoughtful" and "be careful" are banned. If you mean "cite the exact line number," say that.

### 3. Fail loudly

Every module has a refusal path. If the input is out of scope or the constraints can't be met, the module outputs a literal refusal string — it does not attempt a partial answer.

This is the most important design commitment. The alternative (graceful degradation into plausible-sounding hallucination) is the default failure mode of prompt engineering.

### 4. Cite the source

Where a module is inspired by a technique, it cites the paper, heuristic, or incident. `legacy-refactor-expert.md` cites Michael Feathers. `chain-of-thought-scaffold.md` cites Peirce. `logical-fallacy-checker.md` uses a closed taxonomy rather than an inventable one.

This matters for two reasons:
1. Users can go read the source and decide whether the module faithfully implements it.
2. Modules are not mystery meat. Every design choice has a reason that can be contested.

### 5. Version everything

Filenames embed the version. A breaking change to a stable module produces a new file (`executive-engine-v2.md`) and deprecates the old one (`executive-engine.md` gets `status: deprecated`). No in-place mutation of modules that other modules depend on.

## Anti-patterns this repository deliberately avoids

- **Prompt essays** — long walls of prose describing "how to think about" a task. Models don't read essays; they pattern-match on them. Structured, declarative modules beat prose every time.
- **Role-play with no teeth** — "You are a world-class expert with 30 years of experience in X." This is a vibe, not a constraint. Every identity block in this repo names a specific discipline and a specific failure mode.
- **Emoji-heavy UX prompts** — cute, widely copied, and usually padding. This repo uses zero emoji by default.
- **"Let's think step by step"** — vague and mostly superseded by models that reason well unprompted. When reasoning is needed, use a structured scaffold (`01_cognition/chain-of-thought-scaffold.md`) instead.
- **Self-referential prompt templates** — "This is a prompt about prompts." If a module needs to reference the concept of a prompt to work, it's a methodology, not a module.

## The test for whether a module belongs here

Read it. Then ask:

1. Could I describe what this module does in one sentence, without using "and"?
2. Is there a specific input that would trip up a naive implementation — and does the module handle that input in a way I can check?
3. Is there at least one failure mode that the module explicitly refuses, with a literal refusal string?
4. Is there a version of this module that's simpler and would still work?

If the answer to any of these is "no," the module is not ready.

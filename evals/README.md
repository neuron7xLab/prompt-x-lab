# Evaluation Harness

Every seed module in layers 00–04 ships with exactly one evaluation spec under `specs/`. The harness reads the module file, assembles its sections into a system prompt, calls the provider under test, and scores the output with an LLM-as-judge rubric. Results are written to `results/` as validated JSON.

## Run it

```bash
# install (one-time)
python -m venv .venv && . .venv/bin/activate
pip install -e '.[eval]'

# run every spec against Claude Opus 4.6, judged by Claude Opus 4.6
pxl-eval

# one spec, specific provider
pxl-eval --spec evals/specs/executive-engine.yaml --provider anthropic --model claude-opus-4-6

# run in mock mode (no API keys — CI default)
pxl-eval --provider mock --judge-provider mock
```

## What's inside

```
evals/
├── README.md                  ← you are here
├── specs/                     ← one YAML spec per seed module
│   ├── identity-primitive.yaml
│   ├── constraint-primitive.yaml
│   ├── output-primitive.yaml
│   ├── executive-engine.yaml
│   ├── creator-critic-verifier.yaml
│   ├── chain-of-thought-scaffold.yaml
│   ├── senior-code-reviewer.yaml
│   ├── legacy-refactor-expert.yaml
│   ├── test-generator.yaml
│   ├── socratic-tutor.yaml
│   ├── strategic-advisor.yaml
│   ├── hallucination-gate.yaml
│   └── logical-fallacy-checker.yaml
└── results/                   ← written by the harness; latest-per-key kept
```

## Spec format

Every spec is validated against [`schemas/eval-spec.schema.json`](../schemas/eval-spec.schema.json). See `specs/executive-engine.yaml` for a worked example.

A spec declares:

- **`module`** — path (from repo root) of the module under test.
- **`system_prompt_from`** — which sections to stitch into the system prompt.
- **`cases`** — at least one case, each with an `input`, a list of `expectations`, and a `kind` (`positive` · `adversarial` · `edge`). Adversarial cases test whether the module *refuses* badly-formed inputs.
- **`judge`** — the model and rubric to score outputs against expectations.

## How a case passes

A case passes iff:

1. Every expectation in its list is satisfied by the output, **and**
2. If `must_refuse: true`, the output literally contains a refusal string.

Strict. No partial credit. A module with 4 out of 5 expectations satisfied scores `0.8` but *does not pass* — the pass threshold is `≥0.999`.

## How the judge is kept honest

The judge is a separate LLM call with its own constraint block (see `src/pxl/judge.py`). The test suite feeds it known-good and known-bad outputs and asserts that it scores them correctly. A judge that accepts a bad output is a failure of the harness, not of the module under test — and will fail `pytest`.

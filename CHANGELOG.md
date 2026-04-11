# Changelog

All notable changes to Prompt X Lab are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [0.3.0] — 2026-04-11

### Added — full engineering harness

This release converts prompt-x-lab from a curated text library into a typed, versioned, tested engineering artifact. Every aspirational claim in v0.2 is now mechanically enforced.

#### Python package `pxl`

- `src/pxl/models.py` — Pydantic v2 models mirroring the JSON Schemas. `ModuleFrontmatter`, `EvalSpec`, `EvalCase`, `EvalResult`, `CaseResult`, `RubricItem`, `Provider`, etc.
- `src/pxl/assembly.py` — Markdown section extractor + system-prompt assembler. Reads `## Identity`, `## Core logic`, `## Constraints`, `## Output format` from a module file.
- `src/pxl/providers.py` — three providers sharing one tiny interface: `AnthropicProvider`, `OpenAIProvider`, `MockProvider`. Mock deliberately cannot pass any non-trivial rubric.
- `src/pxl/judge.py` — LLM-as-judge rubric evaluator. Strict JSON contract, per-expectation evidence, counterfactual rubric variant for high-stakes modules.
- `src/pxl/runner.py` — end-to-end eval runner. Schema-validates spec → assembles system prompt → calls provider → judges → writes validated `EvalResult` JSON.
- `src/pxl/validator.py` — frontmatter validator walking every `.md` file in layers 00–05.
- `src/pxl/audit.py` — SHA256 body audit for layer 05 integrity (provenance chain).
- `src/pxl/badges.py` — real badge generator computing values from `evals/results/*.json`.
- `src/pxl/cli.py` — entry points: `pxl-validate`, `pxl-eval`, `pxl-audit`, `pxl-badges`.
- `src/pxl/py.typed` — PEP 561 marker.

#### JSON schemas

- `schemas/module.schema.json` — frontmatter contract.
- `schemas/eval-spec.schema.json` — eval spec contract.
- `schemas/eval-result.schema.json` — eval result contract.

#### Evaluation harness

- `evals/specs/` — 10 YAML specs × 20 cases (positive + adversarial) covering every seed module in layers 01–04.
- `evals/results/badges.json` — computed badge state; starts at `no-runs-yet` until a real run is persisted.
- `evals/README.md` — operator documentation.

#### Tests (pytest — 22 tests across 6 files)

- `tests/test_validator.py` — every layer dir exists, every module has valid frontmatter.
- `tests/test_assembly.py` — section extraction + system-prompt stitching + missing-section errors.
- `tests/test_audit.py` — SHA256 body hashing + 26-file coverage + determinism.
- `tests/test_judge.py` — judge parses plain/fenced JSON and fails loudly on malformed responses.
- `tests/test_models.py` — frontmatter + spec Pydantic round-trip + SemVer rejection.
- `tests/test_runner.py` — end-to-end runner with fake providers (no network).

#### Documentation

- `docs/composition-algebra.md` — EBNF grammar, layer-ordering rule, vector-compatibility rule, refusal-path preservation, composition type `(P, R)`.
- `docs/evaluation-protocol.md` — epistemology of pass/fail: strict ≥0.999 threshold, adversarial parity, judge-under-test, provider-agnosticism, out-of-scope (foundation primitives + layer 05).
- `docs/references.bib` — BibTeX bibliography with 13 anchors (Peirce, Feathers, Kahneman, Halmos, Claessen/QuickCheck, Popper, Wei et al. CoT, Zheng et al. LLM-as-Judge, Horowitz, etc.).
- `docs/case-studies/` — three concrete runs: senior-code-reviewer × unbounded cache, executive-engine × Fibonacci(10^18), hallucination-gate × Apollo 11. Each with input, output, rubric trace, verdict, and the adversarial variant that would have broken the module.
- **Prior art section** added to every seed module (13 files). A claim without a prior-art anchor is no longer allowed to ship.

#### Layer 05 honesty

- `05_orchestration/README.md` rewritten with an explicit "Honest disambiguation" block: layer 05 modules are whole production systems, *not* primitives, and deliberately violate the one-screen rule that layers 00–04 enforce.
- `05_orchestration/AUDIT.sha256` — SHA256 manifest of 26 module bodies. `python -m pxl.audit verify` fails CI if any body drifts.
- License disclosure: layer-05 module bodies are owner-proprietary, redistributed inside prompt-x-lab under a self-study grant; layer-00–04 content remains MIT.

#### Tooling

- `pyproject.toml` — full project metadata, three dependency groups (`runtime`, `[eval]`, `[dev]`), ruff + mypy + pytest config.
- `Makefile` — targets: `install-dev`, `validate`, `test`, `lint`, `format`, `typecheck`, `eval`, `eval-mock`, `audit-write`, `audit-verify`, `badges`, `all`, `ci`.
- `.pre-commit-config.yaml` — trailing-whitespace, ruff, ruff-format, `pxl-validate`, `pxl-audit verify`.
- `.github/workflows/ci.yml` — GitHub Actions pipeline: validate · pytest · ruff · mypy --strict · audit-verify · eval-spec schema check · eval-mock (optional).
- `CLAUDE.md` — development rules for Claude Code and humans: non-negotiable discipline around frontmatter, prior art, `validated` field immutability, layer 05 audit propagation.

#### Discipline enforcement

- `ruff check` clean (E, F, I, B, UP, N, SIM, RUF, ANN rules).
- `mypy --strict` clean (10 source files).
- `pytest` green (22/22).
- `pxl-validate` clean (39 modules).
- `pxl-audit verify` clean (26 layer-05 bodies).
- `pxl-eval --provider mock` exercises the full harness plumbing end-to-end without API keys.

### Badge honesty

The aspirational `every_module-tested` badge is **replaced** by real, computed values:

- `eval_specs` — count of spec files under `evals/specs/`.
- `validated_modules` — count of seed modules whose latest real-provider run has `pass_rate ≥ 0.999`. Starts at `0/10` and rises only when real runs land under `evals/results/`.
- `mypy-strict` — static badge, backed by `make typecheck`.

### Removed

- Three foundation-layer eval specs (`identity`, `constraint`, `output` primitives). Foundation primitives are meta-templates, not applicable system prompts; they are validated *compositionally* through the modules that inherit from them. Documented explicitly in `docs/evaluation-protocol.md` §8.1.
- The misleading `tested` badge from v0.2.

## [0.2.0] — 2026-04-11

### Added — `05_orchestration` layer

Full integration of the **Advanced Orchestration v1** bundle — 26 production-grade system prompts, adapted verbatim. Every line of every original prompt is preserved; only the packaging is prompt-x-lab native (frontmatter, category indexes, composable references).

- **`05_orchestration/protocols/`** — 6 execution protocols (SPST, DSIO, IOA, LRE, PGE, SMLRS).
- **`05_orchestration/agents/`** — 9 PR automation agents.
- **`05_orchestration/frameworks/`** — 5 flagship frameworks.
- **`05_orchestration/crypto/`** — 3 crypto & trading systems.
- **`05_orchestration/research/`** — 3 methodology & research protocols.
- Per-category `README.md` with module tables.
- Layer-level `05_orchestration/README.md` documenting the integration boundary between short primitives (00–04) and long-form production systems (05).
- Crest assets copied to `.github/assets/crest-{360,720,1080}.webp` + `crest.manifest.json`.
- `.metadata/taxonomy.json` extended with layer 05 and its 5 sublayers.
- `.metadata/manifest.yaml` extended with per-category manifest entries.
- Provenance: every module carries `origin: Advanced Orchestration v1 bundle` in its frontmatter; source file name preserved in `source_file`.

### Visual

- `.github/assets/eca-cognitive-engine.svg` — standalone neuro-fractal visual study (already shipped in v0.1.x series).

## [0.1.0] — 2026-04-11

### Added
- Initial repository architecture: 5-layer cognitive stack (`foundation → cognition → engineering → personas → validation`).
- Core primitives: identity, constraints, output formats.
- Seed modules:
  - `01_cognition/executive-engine.md` — three-layer planner/executor/critic.
  - `01_cognition/creator-critic-verifier.md` — adversarial triad.
  - `01_cognition/chain-of-thought-scaffold.md` — structured reasoning scaffold.
  - `02_engineering/senior-code-reviewer.md` — distinguished-engineer PR review persona.
  - `02_engineering/legacy-refactor-expert.md` — high-risk refactor surgeon.
  - `02_engineering/test-generator.md` — property-based test synthesizer.
  - `03_personas/socratic-tutor.md` — question-first teaching module.
  - `03_personas/strategic-advisor.md` — no-BS executive counsel.
  - `04_validation/hallucination-gate.md` — epistemic safety gate.
  - `04_validation/logical-fallacy-checker.md` — argument auditor.
- `templates/base-module.md` — skeleton every new prompt inherits.
- `docs/` — methodology, naming, usage guide.
- `.metadata/taxonomy.json` + `.metadata/manifest.yaml` — machine-readable index.

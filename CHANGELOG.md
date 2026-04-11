# Changelog

All notable changes to Prompt X Lab are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [0.5.0] — 2026-04-11

### Added — Layer 07: Kriterion Fail-Closed Evaluation kernel

Kriterion v2026.4.5 integrated as a **minimalist kernel**: only the reusable mathematical primitive + content, deliberately excluding the upstream business copy, HTML dashboard, governance CI, and PR intake tooling. Not every integration needs to import everything.

#### Content layer (`07_kriterion/`) — 18 files

- `protocols/` (6) — SE-OPS · SSE · ESA · PSE · DSE · GPT-5.4 Audit Hardening.
- `schemas/` (9) — CanonicalArtifact · EvaluationResult · TaskScore · DomainScore · GateResult · ArtifactValidationResult · ReferenceInputBundle · OrchestrationHandoff · GovernanceInvariantRegistry.
- `methodology/` (3) — Methodology · Threat Model for AI Evaluation · Anti-Fragile Reasoning Framework.

Every file carries `source_sha256` frontmatter; 18 bodies hashed in `07_kriterion/AUDIT.sha256`.

#### Typed Python subsystem (`src/pxl/kriterion/`) — 5 modules

- **`canonical.py`** — the 180-line fail-closed kernel. Pure functions, stdlib-only:
  - `canonical_bytes(data) -> bytes` · `canonical_obj(data) -> Any` · `sha256_hex(data) -> str`
  - `build_genesis_hash(bundle, format_version) -> (bundle_hash, genesis)`
  - `build_step_hash(phase_id, phase_input_digest, previous_step_hash, chain_format_version, contract_version) -> str`
  - `ExecutionChain` incremental builder with `.advance()` and `.terminal_hash`
  - `Phase` StrEnum — the seven canonical phase identifiers
- **`schemas.py`** — loaders + validator using `referencing.Registry` (modern replacement for deprecated `jsonschema.RefResolver`).
- **`protocols.py`** — loaders for six raw protocol text files.
- **`benchmark.py`** — ten-case reproduction contract against upstream `dataset_manifest.json` `artifact_manifest_hash` values. Byte-for-byte equality required.
- **`cli.py`** — `pxl-kriterion { info | canonical | validate | benchmark | protocol }`.

Force-included in the wheel: `assets/{schemas,protocols}/` + `datasets/{synthetic_cases,...}/`.

#### Reproduction tests — 40 new pytest cases

- `test_kriterion_canonical.py` (16 tests) — byte-level determinism, SHA-256 known vectors, genesis hash domain separation, step-hash chain linking, tamper evidence, `ExecutionChain` full seven-phase walk, stdlib round-trip compatibility.
- `test_kriterion_schemas.py` (7 tests) — loader, validator, required fields, type enums, empty-instance rejection.
- `test_kriterion_protocols.py` (13 parametrised tests) — loader, suffix handling, protocol-body structural invariants.
- `test_kriterion_benchmark.py` (4 tests) — ten manifest hashes match byte-for-byte, protocol coverage, adversarial case count, published metric invariants.

#### Infrastructure

- `pyproject.toml` — `referencing>=0.35` added as core dependency; `pxl-kriterion` entry point; force-include for kriterion assets and datasets; `ANN401` exemption for `canonical.py` / `schemas.py` / `cli.py` (JSON-serialisable `Any` is the honest type for the primitive's public API).
- `Makefile` — new `kriterion-info`, `kriterion-benchmark` targets; `make all` now runs kriterion reproduction.
- `.metadata/taxonomy.json` + `manifest.yaml` — layer 07 registered.
- `src/pxl/validator.py` + `src/pxl/audit.py` — extended with layer 07.

#### Full quality gate — all green locally

| Gate | Count | Result |
|---|---|---|
| `pxl-validate` | 91 modules (39 + 34 + 18) | OK |
| `pytest` | 84 tests (44 + 40 kriterion) | OK, no warnings |
| `ruff check` | src · scripts · evals · tests | OK |
| `mypy --strict` | 24 source files | OK |
| `pxl-audit verify` | 26 + 34 + 18 bodies | OK |
| `pxl-eca validate` | router 99.44%, scorer 90.62%, FP=0 | OK |
| `pxl-kriterion benchmark` | 10/10 matched | OK |

### License

Kriterion content is integrated under the upstream *Audit-Grade Community License 1.0* (community, non-commercial). The `canonical.py` module is MIT-licensed independently because its underlying ideas — canonical JSON serialisation, domain-separated hashing, chain linking — are not copyrightable as such. You may reuse the kernel without the content layer.

## [0.4.0] — 2026-04-11

### Added — Layer 06: ECA Cognitive Engine v1.1 native integration

This release integrates the **ECA v1.1.0 production stack** into prompt-x-lab as a first-class subsystem. Unlike layer 05 (Advanced Orchestration — text-only copy), layer 06 is a **true native integration**: content + typed Python port + reproduction tests. The original ECA scripts have been rewritten, not copy-pasted.

#### Content layer (`06_eca_engine/`) — 34 files

- `core/` (6) — overview, proof tiers, system prompt, core config, mode templates, user context contract.
- `runtime/` (4) — runtime policy, fallback matrix, router spec, context budgeting.
- `benchmarks/` (3) — metrics (7 dimensions + calibrated thresholds), scoring rubric, live benchmark protocol.
- `security/` (3) — security model, prompt-injection guardrails, output-provenance policy.
- `schemas/` (2) — request envelope + response envelope JSON schemas (as MD references).
- `legal/` (1) — EULA template.
- `docs/` (15) — architecture blueprint, calibration methodology v1.1, executive operational manual, implementation sequence, input guide, launch readiness, optimisation 77 iterations, packaging notes, product spec, production readiness, release notes v1.0.0/v1.1.0, task completion matrices (v1 + v1.1), telemetry audit plan.

Every file carries a `source_sha256` field in frontmatter for provenance tracking; body-level SHA256 manifest lives in `06_eca_engine/AUDIT.sha256` and is verified by `python -m pxl.audit verify`.

#### Typed Python subsystem (`src/pxl/eca/`) — 8 modules, mypy --strict clean

- `schemas.py` — Pydantic v2 models for `RequestEnvelope`, `ResponseEnvelope`, `ResponseSection`, `QualityGate`, plus `OutputMode`, `ProofTier`, `RiskTolerance`, `EvidenceRequirement` enums (mirroring the bundled JSON schemas).
- `config.py` — 12 Pydantic models for `RouterSpec`, `BestConfig`, `Metrics`, `ShippingThresholds`, `RuntimePolicy`, `FallbackMatrix`, etc. Loaders use `importlib.resources` over the bundled assets.
- `router.py` — typed port of `route_request` logic. Pure function, no hidden module loading. Returns a frozen `RoutingDecision` dataclass.
- `scorer.py` — typed port of `score_response` logic. Returns a frozen `Scorecard` dataclass with seven quality dimensions plus a `ship` boolean against calibrated thresholds.
- `signer.py` — HMAC-SHA256 response signer + `verify_signature` with constant-time comparison.
- `validate.py` — full-stack replay harness. Runs the router on synthetic + adversarial request sets, runs the scorer on synthetic responses, and emits a validated `ValidationReport` with classification / binary metrics and regression failures.
- `cli.py` — `pxl-eca` CLI with subcommands: `info`, `validate`, `route`, `score`, `sign`.
- `__init__.py` — public API + `ECA_VERSION = "1.1.0"`, `ECA_SELECTED_ITERATION = 27`.

Bundled resources (via `pyproject.toml force-include`):

- `src/pxl/eca/assets/` — 13 files: system_prompt.txt, router_spec.yaml, best_config.yaml, metrics.yaml, config.yaml, templates.yaml, user_context_contract.yaml, runtime_policy.yaml, fallback_matrix.yaml, prompt_injection_guardrails.yaml, output_provenance_policy.yaml, request_envelope.schema.json, response_envelope.schema.json.
- `src/pxl/eca/datasets/` — 10 files: 180 synthetic requests, 192 synthetic responses, 36 adversarial requests, golden + adversarial datasets, 77-iteration logs (CSV + JSON), evaluation summary, request/response examples.

#### Reproduction tests (22 pytest cases)

- `test_eca_schemas.py` (7 tests) — Pydantic round-trips, config loaders, bundled JSON schemas.
- `test_eca_router.py` (5 tests) — full-corpus replay reproduces 178/180 = 99.44% accuracy, adversarial = 100%, specific single-request routings for system_architecture_blueprint + human_performance_protocol + low-signal fallback.
- `test_eca_scorer.py` (5 tests) — 90.62% balanced accuracy, F1 0.8966, confusion matrix 78/96/0/18, FP = 0 invariant, empty body rejection, validation report OK.
- `test_eca_signer.py` (4 tests) — determinism, content sensitivity, secret sensitivity, round-trip verification.

The calibration chain is now protected by executable tests. Any drift in router logic, scorer logic, or bundled datasets fails CI immediately.

#### CLI additions

- `pxl-eca info` — prints bundled config + calibration summary as JSON.
- `pxl-eca validate` — replays the calibration holdouts, prints metrics, exits non-zero on regression.
- `pxl-eca route <request.json>` — routes a request to one of six ECA modes.
- `pxl-eca score <response.json>` — scores a response against shipping thresholds, exits non-zero if not shippable.
- `pxl-eca sign <response.json>` — HMAC-SHA256 sign with `ECA_SIGNING_SECRET` or `--secret`.

#### Audit extension

`src/pxl/audit.py` now supports both layer 05 (triple-backtick fence) and layer 06 (quadruple-backtick fence) under a single `LayerSpec` config. `python -m pxl.audit {write,verify} [05|06|all]`.

#### Infrastructure updates

- `pyproject.toml` — added `pxl-eca` entry point, `force-include` for assets + datasets directories.
- `Makefile` — new targets `eca-info`, `eca-validate`, included in `make all`.
- `.metadata/taxonomy.json` — layer 06 registered with full holdout + full-corpus reproduction numbers.
- `.metadata/manifest.yaml` — 7 new sublayer entries.
- `src/pxl/validator.py` — extended to walk `06_eca_engine/`.
- `CLAUDE.md` (unchanged but now applies to layer 06 through the same discipline).

### Full quality gate — all seven checks green locally

| Gate | Count | Result |
|---|---|---|
| `pxl-validate` (frontmatter schema) | 73 modules | OK |
| `pytest` | 44 tests (22 original + 22 ECA) | OK |
| `ruff check` | src · evals · tests | OK |
| `mypy --strict` | 18 source files | OK |
| `python -m pxl.audit verify` | 26 + 34 bodies | OK |
| `pxl-eca validate` | router 99.44% · 100%, scorer 90.62%, FP = 0 | OK |
| `pxl-eval --provider mock` | harness plumbing | OK |

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

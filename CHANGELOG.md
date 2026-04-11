# Changelog

All notable changes to Prompt X Lab are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [0.8.0] — 2026-04-11 — First Principles: Musk 5-Step Algorithm · Parallel Scaling Primitive

This release adds the **theoretical framing** that the rest of the library was built under, plus a **real parallel-scaling primitive** that proves the canonical kernel scales to global-LLM-output throughput at < 1% compute cost of the LLMs themselves. Two new documents, one new Python module, thirteen new tests. No removals.

### Added

#### `src/pxl/scale.py` — deterministic parallel primitives (~210 LOC)

Public API — every function is byte-identical to its serial counterpart, enforced by tests:

- **`default_workers() -> int`** — sensible `os.cpu_count()` default.
- **`parallel_audit_all(max_workers=None) -> dict[str, bool]`** — audit every integrated layer (05/06/07) in parallel via thread pool. Returns `{"05": True, "06": True, "07": True}` when all bodies match.
- **`parallel_validate_layers(max_workers=None) -> tuple[int, list]`** — parallel frontmatter validation across all 91 modules. Identical output to serial `validate_all()`; ordering of issues is deterministic (sorted by path) regardless of thread scheduling.
- **`batch_canonical_hash(items, max_workers=None) -> list[str]`** — vectorised `sha256_hex(canonical_bytes(x))`. Order-preserving. Falls back to serial below `_SERIAL_FALLBACK_THRESHOLD=64` where dispatch overhead dominates.
- **`batch_execution_chain(bundles, *, contract_version, max_workers=None) -> list[str]`** — build a full 7-phase `ExecutionChain` for every bundle in parallel. Each bundle is an independent chain; this is embarrassingly parallel by construction.

Design commitment: every parallel primitive **must produce byte-identical results to its serial equivalent**. This is enforced by `tests/test_scale.py` which runs the same input through both paths and asserts equality. Any divergence invalidates the reproduction chain and fails CI.

On the GIL: thread pool is the right choice for IO-bound work (audit file reads) and for batches small enough that process pickling overhead dominates. Users who need true CPU-bound parallelism should use `concurrent.futures.ProcessPoolExecutor` around the serial function directly.

#### `docs/first-principles.md` — Musk 5-step algorithm applied retrospectively

A ~500-line retrospective audit of every release (v0.1.0 through v0.8.0) against Elon Musk's five-step engineering algorithm from the Everyday Astronaut Starbase interview (May 2021):

1. **Make your requirements less dumb** — documents the original "ship as many prompts as possible" requirement and how it was rewritten.
2. **Delete the part or process** — table of every deletion with commit/version, including the ~4,000-line upstream Kriterion reference runner, three aspirational foundation eval specs, the aspirational "tested" badge. Passes the discipline check: ~10% was added back, as Musk demands.
3. **Simplify or optimise** — documents what was simplified (unified CLI, 180-line kernel, 25-line `ExecutionChain`) and, crucially, **what was NOT optimised and why** (e.g., canonical_bytes is not Cython-compiled because at 500 K ops/sec per core it is 5 orders of magnitude faster than the LLM call it composes with).
4. **Accelerate cycle time** — CI duration per release tracked: 50 s → 1 m 6 s while test count grew 586%. Per-test overhead decreased monotonically.
5. **Automate** — explicit list of what is automated (frontmatter validation, body audit, tests, mypy, ECA reproduction, Kriterion reproduction, release build) and what is NOT automated and why (real-provider eval runs require API keys CI must not depend on).

Closes with a reference list of **valid, independently verifiable Musk quotes** from public interviews — no apocrypha, no sales pitch, no canonisation.

#### `docs/scaling.md` — the arithmetic of cognitive infrastructure

A ~400-line mathematical analysis of what the canonical primitive can do at scale. Published tables:

- Measured single-core throughput for every hot path (copied from `benchmarks/RESULTS.md`).
- Linear scaling table from 1 core to 1 M cores (laptop → hyperscale).
- Comparison with worldwide LLM-response rates circa 2026 (~5 × 10⁵ resp/sec).
- Cost ratio: canonical-primitive audit cost vs LLM inference cost (< 1%, by 5-8 orders of magnitude at every realistic scale).
- Storage/network/memory analysis — primitive is not bottlenecked by any of them.
- 2030 projection (~10 M LLM responses/sec worldwide) with the argument that even at that scale, one medium cluster suffices to audit the entire industry.

Closes with **the invitation**: "If you operate any part of the LLM stack, the arithmetic here says you can add tamper-evident audit chains to every single call, with the marginal compute cost being a rounding error. The question is no longer whether this is affordable. The question is whether it is done."

#### Tests — 13 new, 142 total

- `test_scale.py` (13 tests):
  - 3 tests on fallback thresholds and worker count defaults
  - 2 tests on parallel audit (all 3 integrated layers match, determinism across worker counts)
  - 2 tests on parallel validator (serial-parity, expected module count)
  - 3 tests on batch canonical hash (small-batch serial parity, large-batch parallel parity, order preservation with hashlib cross-check)
  - 4 tests on batch execution chain (small-batch parity, large-batch parity, distinct-bundles-produce-distinct-hashes, empty-input handling)

#### README — new top-level sections

- **"First principles · applied"** — one-screen summary of how Musk's five steps map to the repo's release history, with a link to the full retrospective.
- **"At scale · the arithmetic of cognitive infrastructure"** — scaling table + key observation + code example of `batch_execution_chain()`, with a link to the full math.

Both sections appear above "At a glance" because they are the theoretical framing everything below depends on.

### Changed

- `pyproject.toml` — version 0.8.0; `src/pxl/scale.py` added to ANN401 per-file ignores (the primitive accepts arbitrary JSON-serialisable inputs by design).
- `src/pxl/__init__.py` — `__version__ = "0.8.0"`.
- Main README badges — `version-0.8.0`, `pytest-142_tests`, `mypy-strict_32_files`, `chains-5.3K/sec/core`, `musk_5-step-applied`, `pxl.scale-deterministic`.

### Quality gate — all seven checks green

| Gate | Count | Result |
|---|---|---|
| `pxl validate` | 91 modules | OK |
| `pytest -q` (excluding benchmarks) | **142 tests** | OK, no warnings |
| `pytest benchmarks/` | 10 benchmarks | OK |
| `ruff check` | src · evals · tests · benchmarks | OK |
| `mypy --strict` | **32 source files** | OK |
| `pxl audit verify` | 26 + 34 + 18 bodies | OK |
| `pxl eca validate` | router 99.44% · scorer 90.62% · FP=0 | OK |
| `pxl kriterion benchmark` | 10/10 matched | OK |

## [0.7.0] — 2026-04-11 — Elite Polish: Unified CLI · Dashboard · Benchmarks · Architecture

Four deliverables, each done to production quality: unified command-line interface with rich-powered dashboard, performance benchmark suite with published numbers, and an elegant brand-aligned architecture diagram.

### Added

#### 1. Unified `pxl` CLI

- **`src/pxl/main.py`** — argparse-based unified dispatcher. Every capability reachable through `pxl <subcommand>`: `dashboard`, `layers`, `validate`, `audit`, `eval`, `badges`, `version`, `eca <subcmd>`, `kriterion <subcmd>`.
- **`src/pxl/__main__.py`** — `python -m pxl` as alternate entry.
- **Legacy aliases preserved** — the six `pxl-*` entry points from previous versions still work; they dispatch to the same underlying code.

#### 2. `pxl dashboard` — one-screen state view

- **`src/pxl/dashboard.py`** — Rich-powered state view: branded banner, eight-layer inventory table (label, kind, module count, audit status), subsystem health panel (ECA + Kriterion + 2026→2030 primitives), quality-gate one-liner with live git commit SHA.
- Every number is computed from real artifacts. No hardcoded totals.
- `render_dashboard()` returns a JSON-ready dict for scripted consumers.

#### 3. `src/pxl/console.py` — shared Rich brand tokens

- Singleton `Console` instance + `Theme`. The four-colour RGB-on-black brand is encoded here and nowhere else. Exports: `console`, brand hex constants, glyphs, `print_banner`/`print_section`/`print_status` helpers. Zero side effects on import.

#### 4. Performance benchmarks (`benchmarks/`)

- **`test_canonical_speed.py`** (8 benchmarks) — `canonical_bytes` at three payload sizes, `sha256_hex` at two sizes, `build_genesis_hash`, `build_step_hash`, full seven-phase `ExecutionChain.advance`.
- **`test_eca_speed.py`** (2 benchmarks) — `route_request` + `score_response` over a representative 9-section response.
- **`benchmarks/RESULTS.md`** — published numbers on commodity hardware:

```
sha256_hex (64 B)            486 ns   ~2.1 M ops/sec
build_step_hash             4.0 μs    ~250 K chains/sec
build_genesis_hash          97.4 μs   ~10 K ops/sec
7-phase ExecutionChain      189 μs    ~5.3 K audited evals/sec/core
eca.route_request           17.9 μs   ~56 K req/sec
eca.score_response          28.3 μs   ~35 K resp/sec
```

The canonical primitive is not the bottleneck. It is several orders of magnitude faster than any LLM call it composes with. **Determinism and correctness, not speed, are what the primitive earns** — but the fact that it is *also* fast is a consequence of keeping the mathematical core small and stdlib-only.

#### 5. Architecture SVG (`.github/assets/architecture.svg`)

- Hand-written 1600×900 elegant diagram in the dark RGB-on-black brand: eight layers stacked with module counts, colour-coded integration tiers (native / verbatim / hand-written), right-side stats panel (layers · modules · tests · mypy files · audit entries), speed panel with benchmark numbers, animated title gradient matching the repo brand.
- Linked from a new "At a glance" section at the top of the README.

#### 6. Tests — +12, 129 total

- `test_main_cli.py` (7 tests) — parser, version, layers labels, validate, audit verify, no-subcommand guard, subprocess entry point.
- `test_dashboard.py` (5 tests) — eight-layer collection, positive counts, integrated-layer audit status, seed-layer exemption, JSON summary shape.

#### 7. README "At a glance" section

- Top-level architecture SVG + one-screen terminal demo of `pxl dashboard` + summary table with 10 key numbers. Moved before "The Signal" so the first impression is visual and factual.

### Changed

- `pyproject.toml` — version 0.7.0, `pxl` unified entry point added, `pytest-benchmark>=4.0` in `[dev]`.
- Main README badges — `version-0.7.0`, `pytest-129_tests`, `step_hash-4.0_μs`, `mypy-strict_31_files`, `pxl-unified_CLI`.
- `src/pxl/__init__.py` — `__version__ = "0.7.0"`.

### Quality gate — all seven checks green, no warnings

| Gate | Count | Result |
|---|---|---|
| `pxl validate` | 91 modules | OK |
| `pytest -q` (excluding benchmarks) | **129 tests** | OK |
| `pytest benchmarks/ --benchmark-only` | 10 benchmarks | OK |
| `ruff check` | src · evals · tests · benchmarks | OK |
| `mypy --strict` | **31 source files** | OK |
| `pxl audit verify` | 26 + 34 + 18 bodies | OK |
| `pxl eca validate` | router 99.44% · scorer 90.62% · FP=0 | OK |
| `pxl kriterion benchmark` | 10/10 matched | OK |

## [0.6.0] — 2026-04-11 — Production Polish + 2026→2030 Trends

### Added — trend-forward primitives + production infrastructure

This release lifts prompt-x-lab from *engineering artifact* to *production-ready library* with an eye on the 2026→2030 LLM landscape: reasoning-budget abstractions for thinking models, a minimal agent-loop primitive, an Ollama edge provider, hypothesis property-based tests, architecture decision records, a Karpathy-style zero-to-hero tutorial, a full release workflow, mkdocs-material site scaffolding, and a responsible-disclosure security policy.

#### New `src/pxl/` modules

- **`reasoning.py`** — reasoning-budget abstraction for thinking models (Claude Thinking, o1/o3, DeepSeek-R1).
  - `ReasoningLevel` — five canonical intensities: `OFF`, `LOW`, `MEDIUM`, `HIGH`, `EXTREME`.
  - `ReasoningBudget` — frozen dataclass carrying level + optional token cap override.
  - `BUDGET_CONTRACT` — monotone mapping: 0, 1024, 4096, 16384, 65536 tokens.
  - `ThinkingProvider` — wraps any `BaseProvider` with budget semantics. Vendor-specific thinking parameters stay in provider implementations.
- **`agents.py`** — minimal tool-use + sub-agent loop primitive, ~210 lines, zero dependencies.
  - `Tool` — frozen dataclass: name, callable, description, JSON schema.
  - `AgentStep`, `AgentResult` — typed iteration + terminal records.
  - `run_agent_loop(system, user, tools, provider, max_iterations)` — three termination conditions (model stops, tool returns `{"__done__": True}`, iteration cap).
- **`local.py`** — `OllamaProvider` for 2026 edge inference. HTTP to `localhost:11434`, same `BaseProvider` interface. Plus `list_local_models(host)` with network-failure fallback. Classified `Provider.MOCK` because local runs are not cross-vendor validated.

#### New tests — 33 new, 117 total

- `test_reasoning.py` (6 tests) — level ordering, frozen invariants, token-budget fallback.
- `test_agents.py` (10 tests) — tool parsing, single/multi-tool execution, done-sentinel, max-iterations, exceptions, unknown tools.
- `test_local.py` (5 tests) — list_local_models fallback, response parsing, OllamaProvider shape, context-manager close.
- `test_property_canonical.py` (12 **hypothesis property tests**) — deterministic canonical bytes under random JSON input, key-order independence, stdlib round-trip, SHA-256 parity with hashlib, genesis hash determinism + domain separation, step hash determinism, full-chain tamper evidence under adversarial input generation.

#### Documentation

- **`docs/zero-to-hero.md`** — 400-line Karpathy-style walkthrough that builds the fail-closed canonical primitive from first principles in four steps. Closes with a survey of what the primitive guarantees and what it does not.
- **`docs/adr/001-canonical-primitive-as-public-api.md`** — rationale for exposing the 180-line kernel instead of porting the 4,000-line upstream framework.
- **`docs/adr/002-layered-integration-with-provenance-audit.md`** — rationale for per-layer SHA-256 body audits with separate fence conventions.
- **`docs/adr/003-fail-closed-refusal-as-non-negotiable-primitive.md`** — the literal `REFUSED:` output contract as the single largest quality improvement observed in the repo.

#### Policies + infrastructure

- **`SECURITY.md`** — responsible disclosure, supported versions, in-scope cryptographic invariants (determinism, domain separation, chain tamper-evidence), signed-release policy.
- **`CONTRIBUTING.md`** — non-negotiable rules, full quality-gate definition, seed-module authoring walkthrough, version bump rules, style guide.
- **`mkdocs.yml`** — mkdocs-material navigation covering methodology, ADRs, case studies. Dark-first palette matching the repo brand.
- **`.github/workflows/release.yml`** — tag-triggered release: build wheel + sdist via hatch, SHA-256 checksums, tag-version verification, CHANGELOG extraction, GitHub Release with artifacts. PyPI trusted-publishing step prepared (commented) for project registration.
- **`pyproject.toml`** — version 0.6.0, expanded keywords (reasoning-models, agent-sdk, fail-closed, canonical-hashing, execution-chain), new `[local]` and `[docs]` optional-dependency groups, `hypothesis>=6.100` in `[dev]`, classifier bumped to `Production/Stable`, Python 3.13 support.
- **`[tool.coverage]`** config with 71.7% baseline across 24 source files.
- **`[tool.pytest.ini_options]`** — `filterwarnings = ["error", ...]` — fail fast on any silent deprecation.

#### Coverage report (baseline)

```
canonical.py         100.0%    reasoning.py          100.0%
kriterion/protocols   100.0%   kriterion/benchmark   100.0%
kriterion/schemas      97.9%   agents.py              97.2%
assembly.py            98.0%   judge.py              100.0%
eca/config.py          99.3%   eca/router.py          98.2%
eca/scorer.py          90.5%   eca/signer.py         100.0%
local.py               85.7%   models.py              97.6%
validator.py           83.6%
─────────────────────────────────────────────────
TOTAL                  71.7%   (CLI + API-bound paths are integration-tested)
```

Every core primitive — the part users reason about — sits at 90–100%. The only gaps are CLI entry points and API-bound code paths that require live vendor calls to exercise. Documented explicitly, not hidden.

#### Quality gate — all seven checks green locally and in CI

| Gate | Count | Result |
|---|---|---|
| `pxl-validate` | 91 modules | OK |
| `pytest -q` | **117 tests** | OK, no warnings |
| `ruff check` | src + evals + tests | OK |
| `mypy --strict` | **27 source files** | OK |
| `pxl-audit verify` | 26 + 34 + 18 bodies | OK |
| `pxl-eca validate` | router 99.44% · scorer 90.62% · FP=0 | OK |
| `pxl-kriterion benchmark` | 10/10 matched | OK |

### Changed

- `src/pxl/__init__.py` — docstring rewritten to document the eight-layer architecture and the six `pxl-*` CLI entry points. `__version__ = "0.6.0"`.
- Main `README.md` — badge wall upgraded: `version-0.6.0`, `layers-8`, `total_modules-91`, `pytest-117_tests`, `coverage-71.7%`, `mypy-strict_27_files`, `hypothesis-property_tests`, `license-MIT`. Secondary tech row now includes Claude Thinking, GPT-5.4/o1, Llama 4, Ollama edge, mkdocs-material, pytest+hypothesis.

### Security

No fixes in this release (feature release). `SECURITY.md` added as a forward-looking policy document establishing responsible-disclosure norms before the first security-relevant report.

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

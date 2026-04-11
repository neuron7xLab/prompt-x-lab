# Changelog

All notable changes to Prompt X Lab are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

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

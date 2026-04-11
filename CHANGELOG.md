# Changelog

All notable changes to Prompt X Lab are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

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

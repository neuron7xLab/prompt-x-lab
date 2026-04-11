<!--
Thanks for contributing to prompt-x-lab. Fill in every section below.
PRs that skip sections are rejected. This is the single checklist —
there is no second one.

See CONTRIBUTING.md for the full quality-gate definition.
-->

## What

<!-- One sentence, no "and". -->

## Why

<!-- One paragraph: the problem this PR solves, not the code this PR adds. -->

## Scope

- [ ] Touches layer 00–04 (seed modules)
- [ ] Touches layer 05/06/07 (integrated content — see AUDIT implications below)
- [ ] Touches `src/pxl/` (Python package)
- [ ] Touches `tests/` or `benchmarks/`
- [ ] Touches docs / README / CHANGELOG
- [ ] Touches CI / release / governance files

## Layer 05/06/07 audit — fill in iff any integrated body changed

- [ ] I regenerated `AUDIT.sha256` via `python -m pxl.audit write`
- [ ] I committed the regenerated audit manifest in this PR
- [ ] I named the rationale for the content change in the commit message
- [ ] I verified the upstream license permits the change

## Quality gate (run locally before requesting review)

- [ ] `pxl validate` — frontmatter schema passes for all modules
- [ ] `pytest -q` — all tests pass (no warnings)
- [ ] `ruff check` — no lint errors
- [ ] `mypy --strict` — no type errors
- [ ] `python -m pxl.audit verify` — 3-layer integrity
- [ ] `pxl eca validate` — full-corpus reproduction passes
- [ ] `pxl kriterion benchmark` — 10/10 matched

Shortcut: `make ci` runs all of the above.

## Version bump

- [ ] This PR does **not** require a version bump (internal/chore/docs)
- [ ] **patch** — wording, typo, fix (0.x.Y → 0.x.Y+1)
- [ ] **minor** — new test case, new constraint, additive feature (0.X.y → 0.X+1.0)
- [ ] **major** — output shape, refusal condition, or identity change (X.y.z → X+1.0.0)

If this PR bumps the version, the PR description must also reference the new `## [vX.Y.Z]` section in `CHANGELOG.md`.

## Breaking changes

<!-- If this PR breaks any public API, the consumer, or the composition
algebra, describe exactly what breaks and how callers should migrate.
If nothing breaks, write "none". -->

## Tests

- [ ] I added tests that **would have failed without this change**
- [ ] Coverage on touched files is ≥ 90% (or explicitly documented)
- [ ] New public functions have docstrings explaining *why*, not just *what*

## Prior art

<!-- For any new seed module, cite the paper, heuristic, or incident
this module inherits from. If the citation is not already in
docs/references.bib, add it. Unanchored claims are inadmissible. -->

## Non-negotiables (see CLAUDE.md)

- [ ] `validated` frontmatter field is not hand-edited
- [ ] No aspirational badges or claims
- [ ] Every numerical statement in this PR is backed by a real artifact

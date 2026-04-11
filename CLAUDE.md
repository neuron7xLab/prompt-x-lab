# CLAUDE.md — development rules for this repository

This file is read by Claude Code (and by every human maintainer) before
making changes to `prompt-x-lab`. Its contents are not optional. Violating
them produces incorrect work.

## Non-negotiable rules

1. **Every seed module must pass `pxl-validate`.** The frontmatter schema
   is the single source of truth. A PR that adds or edits a seed module
   without first running `make validate` will fail CI.

2. **Every seed module must have a spec under `evals/specs/`.** No exceptions
   for layers 00–04. If you cannot write an eval spec for what the module
   does, the module is not well-defined and must be rewritten.

3. **Every seed module must name its prior art.** Either a citation in
   `docs/references.bib` or a concrete prior incident. Modules with no
   prior art are unreproducible and inadmissible.

4. **The `validated` frontmatter field is written only by the eval harness.**
   Never edit it by hand. Never set it to `true` without a corresponding
   result file under `evals/results/`.

5. **Layer 05 bodies are immutable.** Any change to a file in
   `05_orchestration/` must be accompanied by a regenerated `AUDIT.sha256`
   and an explicit rationale in the commit message. The pre-commit hook
   enforces this.

6. **Never downgrade the "tested" badge into an aspirational claim.** The
   README badge is computed from `evals/results/badges.json`. If you want
   a higher number, write more passing specs — do not hand-edit the badge.

## How to add a new seed module

```bash
cp templates/base-module.md 02_engineering/my-module.md
# edit the frontmatter and sections
pxl-validate                          # must pass before you commit
# write the eval spec
$EDITOR evals/specs/my-module.yaml
# run it locally (mock mode is fine if no API key)
pxl-eval --spec evals/specs/my-module.yaml --provider mock --judge-provider mock
# when you have real API access:
pxl-eval --spec evals/specs/my-module.yaml --provider anthropic --judge-provider anthropic
# the result JSON will land in evals/results/
pxl-badges                             # refresh badge data
git add 02_engineering/my-module.md evals/specs/my-module.yaml evals/results/ evals/results/badges.json
```

## How to update a seed module

- **Patch bump** (wording, typos, clarified example): bump `version:
  X.Y.(Z+1)`, no spec change required.
- **Minor bump** (new constraint added, new test case): bump `X.(Y+1).0`,
  update the spec, rerun the eval.
- **Major bump** (output shape change, refusal conditions change,
  identity change): bump `(X+1).0.0`, write a new spec from scratch,
  mark the old module `status: deprecated`, file the replacement under
  a new filename.

## How to run the full local quality gate

```bash
make install-dev          # one-time
make all                  # validate · test · lint · typecheck · audit-verify
make eval-mock            # sanity-check the eval plumbing
make eval                 # real evaluation (needs ANTHROPIC_API_KEY)
```

`make ci` runs exactly the same steps as GitHub Actions.

## What the harness tests vs what it does not test

The harness tests **what a module claims to prevent** — not what it can
produce at its best. A module passes iff its adversarial cases are refused
as designed and its positive cases produce outputs that satisfy every
expectation listed. No partial credit.

The harness does **not** test:

- Performance or token cost (tracked separately in result JSON but not scored).
- Cross-lingual behaviour (specs are in English only).
- Layer-05 long-form modules (see `docs/evaluation-protocol.md` §8).

## Tone and voice

Modules in this repo use a **declarative, slightly clinical tone**. No
emoji. No marketing copy. No "great question!" No bullet points longer
than three lines each. When in doubt, read `02_engineering/senior-code-
reviewer.md` and match its register.

---

*This file supersedes ad-hoc conventions. If you find a rule here that
contradicts code review, the file wins — update the code, not the rule.*

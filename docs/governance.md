# Governance

prompt-x-lab is a **single-maintainer, discipline-first** library. Governance is deliberately minimal: enough structure to make every change traceable, not so much that the maintainer burns out administering it.

This document describes the PR-based workflow enabled in v0.8.1. It is the default for all non-trivial changes going forward.

---

## The rules, in order of priority

1. **Every change that touches code lands through a PR.** No more direct-push-to-main for code.
2. **The PR must pass the full CI quality gate.** No exceptions; a red CI is a blocking objection.
3. **The PR must have a CODEOWNER review.** For single-maintainer repos, this is a self-review on a feature branch — which sounds trivial but is not: it forces the maintainer to re-read the diff one more time, on a different day than they wrote it, through the GitHub PR UI. That re-read has caught real bugs.
4. **The commit message must explain *why*, not *what*.** The diff shows the *what*; Git does not need the commit body to repeat it. The body is for motivation, context, and the link to the issue or ADR that triggered the change.
5. **Never bypass hooks or force-push to `main`.** The pre-commit hooks exist because reviewers (including future-you) cannot be trusted to remember the audit manifest. Force-push to main is destructive and there is no legitimate reason for it.

---

## Who can push directly to `main`

- **Nobody.** Not the maintainer, not Claude Code, not an automated workflow. Every change goes through a PR.

Exceptions — documented for honesty, not for use:

- **Hotfixes for security issues** may go directly to `main` if the fix is reviewed by the CODEOWNER and the PR is filed retroactively within 24 hours. See `SECURITY.md`.
- **Repository governance files** (this document, `CODEOWNERS`, `.github/workflows/`) were established by direct push during the v0.0.x through v0.8.0 bootstrap. After v0.8.1 lands, this is no longer permitted.

---

## PR workflow — the canonical path

```bash
# 1. Create a topic branch from main
git checkout main
git pull --ff-only
git checkout -b type/v0.9.0-short-description

# 2. Work. Small commits. Each commit should compile and pass tests.
$EDITOR ...
make ci

# 3. Push the branch
git push -u origin type/v0.9.0-short-description

# 4. Open a PR using gh CLI (or the GitHub web UI)
gh pr create --fill   # populates from pull_request_template.md

# 5. Wait for CI. A red CI is a blocker.
gh pr checks --watch

# 6. Self-review. Open the PR in the browser. Read the diff. Look at
#    every line. Find something to improve. Push the improvement.

# 7. Merge when green. Use merge commits, not squash —
#    the per-commit history is a feature, not a defect.
gh pr merge --merge --delete-branch

# 8. Pull main and tag the release if applicable.
git checkout main
git pull --ff-only
git tag -a v0.9.0 -m "v0.9.0 — <one-line>"
git push origin v0.9.0
```

---

## Branch naming

| Prefix | For | Example |
|---|---|---|
| `feat/` | New functionality | `feat/v0.9.0-citation-primitive` |
| `fix/` | Bug fix | `fix/v0.8.2-audit-symlink-handling` |
| `chore/` | Governance, deps, CI, non-functional | `chore/v0.8.1-governance-polish` |
| `docs/` | Docs-only changes | `docs/scaling-update-2026-q3` |
| `refactor/` | Internal restructuring without behaviour change | `refactor/consolidate-audit-layer-specs` |

The version number in the branch name is advisory — it describes the intended target release, not a hard binding. If a `feat/v0.9.0-*` branch is bumped to v0.9.1, rename or leave it — the tag is authoritative, not the branch.

---

## Reviewing your own PR — the single-maintainer discipline

Self-review is not a formality. These are the checks to run in the GitHub PR UI that are hard to run locally:

1. **Read every changed line in the "Files changed" tab**, not just the diff hunks you remember writing. GitHub's diff viewer occasionally surfaces unexpected changes — whitespace normalisation, trailing newlines, CRLF conversions — that your editor hid from you.
2. **Look at the "Checks" tab**. Every green check is a signal. A skipped check is a question ("why was this not run?"). A red check is a blocking objection that cannot be overridden without filing an issue.
3. **Re-read the PR description** from top to bottom. If it does not make sense as a standalone narrative to someone who did not write the code, rewrite it.
4. **Click through every `#NNN` issue reference**. Does the PR actually close the issue, or only partially? Partial closures need an explicit follow-up issue.

Only after those four checks should you click Merge.

---

## Merge strategy

- **Default: merge commit.** The per-commit history of a feature branch is valuable. Squashing loses the intermediate steps that made the final state possible.
- **Rebase-and-merge is allowed** for branches with exactly one commit (typical for small fixes).
- **Squash-and-merge is allowed** for branches whose individual commits are exploratory / work-in-progress — i.e., where the intermediate history is *not* valuable. Name the squashed commit carefully: it is the only artifact that will survive.

---

## CODEOWNERS

`.github/CODEOWNERS` lists the maintainer for every path in the repository. GitHub will automatically request review from the listed owner on any PR that touches those paths. For single-maintainer repos, this is a self-review prompt — which is intentional. See the "Reviewing your own PR" section above.

---

## Dependency updates

`.github/dependabot.yml` is configured for weekly minor/patch updates to Python dependencies and GitHub Actions. Major-version updates are **ignored** by default because they may break the mypy --strict surface or the canonical-bytes determinism contract. Every major bump is a manual review with its own PR.

Dependabot PRs are grouped: dev-tools (ruff, mypy, pytest, hypothesis) land together in a single PR per week. This reduces review burden without hiding individual changes.

---

## What governance is NOT

This repository is **not** a community-moderated open-source project. It does not have:

- Multiple maintainers to vote on decisions
- A public roadmap committee
- A code-of-conduct enforcement body
- Labels for "good first issue" or other contribution-funnel machinery

prompt-x-lab is a disciplined personal / R&D library. The governance is the minimum that makes the maintainer's own changes traceable, not a framework for a community of contributors that does not exist.

If the project grows beyond one maintainer, this document will be rewritten. Until then, these rules are load-bearing for *self*-discipline, not for coordination.

---

*See also: [`SECURITY.md`](../SECURITY.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`CLAUDE.md`](../CLAUDE.md), [`docs/first-principles.md`](first-principles.md).*

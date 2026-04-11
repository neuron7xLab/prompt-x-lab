# ADR 002 — Layered integration with per-layer provenance audit

- **Status:** Accepted
- **Date:** 2026-04-11
- **Deciders:** Yaroslav Vasylenko
- **Context:** v0.2.0 (layer 05), v0.4.0 (layer 06), v0.5.0 (layer 07)

## Context

prompt-x-lab grew from 13 hand-written seed modules to 91 modules in three integration waves:

- **Layer 05** — Advanced Orchestration v1 bundle, 26 long-form production prompts, integrated verbatim as text.
- **Layer 06** — ECA Cognitive Engine v1.1, 34 content files + typed Python port + 77-iteration calibration reproduction.
- **Layer 07** — Kriterion v2026.4.5, 18 content files + minimalist canonical kernel + 10-case hash reproduction.

Each integration imports content whose upstream author is the same person as the repo owner but whose **license terms, scope, and intended use differ**:

| Layer | License | Scope |
|---|---|---|
| 00–04 | MIT (seed modules) | Freely reusable |
| 05 | Proprietary (self-owned) | Self-study grant within prompt-x-lab |
| 06 | Proprietary (self-owned) | Self-study grant within prompt-x-lab |
| 07 | AGCL-1.0 (community, non-commercial) | Non-commercial reuse |

Two distinct risks emerge:

1. **Content drift.** An upstream edit (typo fix, formatting change, license bump) could leak into prompt-x-lab silently and change what a downstream consumer sees. Reviewers need a way to detect *any* byte change in integrated bodies.
2. **License confusion.** A future contributor might forget that layer-05 bodies are not MIT and submit them to a commercial fork. The repository must make the distinction mechanical, not decorative.

The question: **how do we prevent silent content drift and enforce license-scope boundaries mechanically?**

## Options considered

### Option A — Git history is the audit

Trust that every content change will show up in `git log` and rely on reviewers to catch problems.

**Cons:** git history shows *that* a file changed, not *whether* it should have. It also does not separate frontmatter (prompt-x-lab native, may evolve) from the body (provenance-critical, must not drift).

### Option B — Full-file SHA-256 manifest

Hash the entire file (frontmatter + body) and record in a manifest.

**Cons:** frontmatter legitimately changes (version bumps, `validated` flag updates), which would constantly invalidate the manifest and force reviewers to regenerate it on every prompt-x-lab-internal edit. Dilutes the signal.

### Option C — Body-only SHA-256 manifest per layer

Extract the fenced code block from every integrated MD file, hash the body only, and record in a per-layer `AUDIT.sha256` file.

**Pros:**
- Frontmatter can evolve without affecting the audit.
- Body changes are detected instantly.
- Per-layer separation makes it obvious which license boundary a change crosses.
- CI fails loudly on any drift.

**Cons:** requires a fence convention (triple-backtick for layer 05, quadruple for layer 06/07 because some content contains triple-backticks).

## Decision

**Option C.** Every integration layer has its own `AUDIT.sha256` file with one SHA-256 per content body. CI verifies on every push via `python -m pxl.audit verify`. The fence convention is per-layer:

| Layer | Fence | Rationale |
|---|---|---|
| 05 | ```` ``` ```` | Upstream bodies do not contain triple-backticks |
| 06 | ```` ```` ```` | ECA docs contain fenced YAML/JSON examples |
| 07 | ```` ```` ```` | Kriterion protocols contain fenced examples |

The audit layer is a first-class subsystem:

- **`src/pxl/audit.py`** — dataclass `LayerSpec` per layer, write/verify functions, CLI entry point.
- **Three audit files** — `05_orchestration/AUDIT.sha256`, `06_eca_engine/AUDIT.sha256`, `07_kriterion/AUDIT.sha256`.
- **CI gate** — `make audit-verify` runs in every PR; failure blocks the merge.
- **Pre-commit hook** — `python -m pxl.audit verify` runs before every commit touching an integrated layer.

Frontmatter is *intentionally excluded* from the hash. Contributors may bump versions, flip `validated` flags, or add `validated_on: [claude-opus-4-6]` entries without re-auditing — as long as the body stays byte-for-byte identical to the upstream source.

## Consequences

### Positive

- **Mechanical license-scope enforcement.** A layer-05 edit failing the audit gate forces the author to explain what changed and why. The audit file serves as a tamper-evident provenance chain for the integrated content.
- **Frontmatter stays editable.** Version bumps, validation flags, and eval-result tags can land without audit churn.
- **Tracks the actual concern (body drift), not the superficial one (file change).**
- **Scales to new layers.** Adding layer 08 requires adding one `LayerSpec` entry and one test — the rest is reused.

### Negative

- The fence convention is a convention, not a type. If a future layer contains quadruple-backticks in its body, we will need to choose a different delimiter.
- Regenerating an audit after an authorised content change requires `python -m pxl.audit write` — one extra command before committing.

### Neutral

- The audit does not prevent content changes; it *records* them. The reviewer's job is still to decide whether a change is authorised. The audit just makes the change visible.

## Related decisions

- **ADR 001** — Canonical primitive as public API (how layer 07's primitive is extracted).
- **ADR 003** — Fail-closed refusal path.

## References

- `src/pxl/audit.py`
- `05_orchestration/AUDIT.sha256` (26 entries)
- `06_eca_engine/AUDIT.sha256` (34 entries)
- `07_kriterion/AUDIT.sha256` (18 entries)
- `tests/test_audit.py`
- `.pre-commit-config.yaml` (hook that runs the audit)

# ADR 001 — The canonical primitive is the public API

- **Status:** Accepted
- **Date:** 2026-04-11
- **Deciders:** Yaroslav Vasylenko
- **Context:** v0.5.0 Kriterion integration

## Context

The Kriterion v2026.4.5 bundle contains ~4,000 lines of Python tooling across 25 modules: a reference runner, a benchmark runner, a validation harness, a governance contract, a PR intake compiler, CI plumbing, and dependency hermeticity checks. Most of it is specific to Kriterion's own CI pipeline and governance model.

The underlying *idea* — that canonical JSON serialisation plus domain-separated, chain-linked SHA-256 hashes produce a fail-closed audit pipeline — is independent of any of that tooling. It is a 180-line mathematical primitive that any reproducible audit pipeline can reuse.

The question: when integrating Kriterion into prompt-x-lab, **what should the public API be?**

## Options considered

### Option A — Port the full reference runner

Import `reference_runner.py` (536 lines), `benchmark_runner.py`, `validate_governance.py` (1,052 lines), all seven phase implementations, the governance contract, and the CI hermeticity checks. Expose them as `pxl.kriterion.runner`, `pxl.kriterion.governance`, `pxl.kriterion.hermeticity`, etc.

**Pros:** complete fidelity with upstream; any existing Kriterion consumer could drop-in replace the upstream package.

**Cons:**
- ~4,000 lines of code, most of it Kriterion-CI-specific.
- Governance module couples to `git` subprocess calls — not portable.
- Hermeticity checks assume Kriterion's exact repository layout.
- Testing burden: the governance validator alone would need ~50 tests.
- The *essential idea* gets diluted across 25 modules.

### Option B — Expose only the canonical primitive

Implement `canonical_bytes`, `sha256_hex`, `build_genesis_hash`, `build_step_hash`, `ExecutionChain`, and `Phase` as a single ~180-line module `pxl.kriterion.canonical`. Add loaders for schemas and protocols. Add a reproduction test against the upstream `dataset_manifest.json`. Stop there.

**Pros:**
- The public API is one elegant file with zero dependencies beyond stdlib.
- Reusable for *any* audit pipeline, not just Kriterion.
- The reproduction test proves fidelity where it matters (canonical bytes + hash contract).
- Minimal maintenance surface.
- Forces the integrator to understand the primitive, not cargo-cult the framework.

**Cons:**
- A user who wants Kriterion's full reference runner must use the upstream package directly, not `pxl.kriterion`.
- The governance, hermeticity, and CI-specific machinery is not available from prompt-x-lab.

### Option C — Hybrid: primitive + thin high-level wrapper

Implement the primitive (Option B) and also add a thin `pxl.kriterion.evaluator` module that stitches the seven phases into an evaluator (~150 lines), without the governance or hermeticity layers.

**Pros:** canonical primitive + usable evaluator skeleton.

**Cons:** encourages users to think of `pxl.kriterion` as a Kriterion replacement when it isn't. Maintenance surface grows without proportional value.

## Decision

**Option B.** The public API of `pxl.kriterion` is the canonical primitive and the content (protocols, schemas, methodology). That's it.

The reasoning:

1. **The primitive is the idea.** Everything else in the upstream bundle — the runner, the governance contract, the PR intake compiler — is *application* of the idea. Users who want the idea can reuse it in their own applications; users who want Kriterion's specific application should use the upstream package.

2. **MIT licensing is cleaner with a primitive.** The mathematical ideas (canonical JSON, domain-separated hashing, chain linking) are not copyrightable. Implementing them from scratch yields an MIT module that is safe to distribute independently of the upstream AGCL-1.0 content.

3. **Testing is sharper.** A 180-line primitive can be covered by hypothesis property tests with 100% coverage. A 4,000-line framework port cannot.

4. **The reproduction contract is strongest when narrow.** `tests/test_kriterion_benchmark.py` replays 10 upstream fixtures through the primitive and demands byte-for-byte hash equality. A broader port would have to reproduce the entire reference runner's behaviour — which includes git-state checks, dependency hermeticity, governance baselines, and timestamp injection — all of which can legitimately drift without meaning Kriterion is broken.

## Consequences

### Positive

- `pxl.kriterion.canonical` is a reusable MIT-licensed primitive that any audit pipeline can adopt.
- Layer 07 adds ~180 lines of new Python code instead of ~4,000.
- Testing is rigorous: 40 pytest tests (16 canonical-contract + 8 hypothesis property tests + 7 schema + 13 protocol + 4 benchmark) plus 10/10 benchmark reproduction.
- Users who want the full Kriterion framework install the upstream package directly — no confusion.

### Negative

- Users expecting a drop-in replacement for Kriterion's reference runner will be disappointed. Mitigation: the layer-07 README explicitly names this scope.
- If the upstream reference runner gains new, essential behaviour (e.g., a new chain format version), we must re-evaluate whether to extend the primitive.

### Neutral

- The governance, hermeticity, and PR-intake tooling is **intentionally excluded**. Users who need it should use upstream Kriterion, which provides it as a first-class feature of *that* framework.

## Related decisions

- **ADR 002** — Layered integration with per-layer provenance audit.
- **ADR 003** — Fail-closed refusal path as a non-negotiable primitive.

## References

- `src/pxl/kriterion/canonical.py` — the primitive
- `tests/test_kriterion_canonical.py` — the invariant tests
- `tests/test_property_canonical.py` — the hypothesis tests
- `tests/test_kriterion_benchmark.py` — the reproduction contract
- Upstream: [`kriterion-security-evaluation-protocols`](https://github.com/neuron7xLab/kriterion-security-evaluation-protocols) (hypothetical future link)

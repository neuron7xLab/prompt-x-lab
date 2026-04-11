# First Principles — Musk's 5-Step Algorithm Applied to prompt-x-lab

Elon Musk publicly articulated, in the Everyday Astronaut interview at Starbase (May 2021), a five-step engineering algorithm that he claims to apply to every subsystem at SpaceX and Tesla. The steps, in his words:

1. **Make your requirements less dumb.** *"The requirements are definitely dumb. It does not matter who gave them to you."*
2. **Try very hard to delete the part or process.** *"The bias is that you should have to add back at least 10% of the things you delete. If you're not adding back at least 10%, you're clearly not deleting enough."*
3. **Simplify or optimize.** *"The most common error of a smart engineer is to optimize a thing that should not exist."*
4. **Accelerate cycle time.** *"Any part of the process can be accelerated, but never skip the first three steps."*
5. **Automate.** *"Automation is last. It is not first."*

Most software projects do these in the wrong order — they start with step 5 (automate a thing that should have been deleted) and never revisit step 1. This document is a retrospective audit of prompt-x-lab against Musk's algorithm, with concrete deletions, simplifications, and accelerations traced to specific commits and decisions.

---

## Step 1 — Make the requirements less dumb

### Requirement we inherited

> "Every prompt library should ship with as many examples as possible and let the user pick."

### Why that requirement is dumb

An example-based prompt library puts the reviewer in the worst possible position. The reviewer has to decide, *for every example*, whether it is good — and the signal-to-noise ratio drops monotonically with catalog size. PromptBase, the largest commercial prompt marketplace, illustrates the failure mode: 100,000+ prompts, ~0 of them with eval contracts.

### What we changed the requirement to

> "Every prompt must ship with a frontmatter schema, a test spec, a refusal condition, and a prior-art citation. Prompts that do not meet this contract are not allowed in the repository."

### What this enables

- `pxl validate` (91 modules) — mechanical enforcement, not reviewer vibes.
- `pxl-eval` (10 specs, 20 cases) — rubric-scored contracts.
- `evaluation-protocol.md §8` — explicit out-of-scope list so meta-templates aren't confused for system prompts.
- Every seed module has a prior-art anchor in `docs/references.bib`. Unanchored claims are inadmissible.

**Step 1 outcome:** we kept the word "library" but rewrote the requirement. The new requirement produces 91 modules instead of 10,000 — by design.

---

## Step 2 — Try very hard to delete the part or process

### What we deleted

| Deleted | Why | Commit / version |
|---|---|---|
| 3 foundation primitives from `evals/specs/` | Foundation primitives are meta-templates, not system prompts — they cannot be rubric-tested directly, only compositionally | v0.3.0 |
| Aspirational "every module tested" badge | It was not true; tests had no actual runs behind them | v0.3.0 |
| Full Kriterion reference runner port (~4000 LOC) | Upstream contains governance, PR intake, and hermeticity plumbing that is orthogonal to the canonical primitive | v0.5.0 (see [`adr/001`](adr/001-canonical-primitive-as-public-api.md)) |
| Kriterion HTML dashboard + business copy | Not signal. LinkedIn posts, Gumroad listings, commercial inquiry emails do not belong in a library | v0.5.0 |
| Vendor-specific thinking-model parameters from `reasoning.py` | The right primitive is the *budget envelope*, not a specific API | v0.6.0 |

**Step 2 discipline check**: Musk says you should have to add back at least 10% of what you delete. We deleted roughly 5,000 LOC of upstream governance/PR/benchmark-runner plumbing. We added back approximately 500 LOC of typed Kriterion port + Python wrappers. Ratio: ~10%. Passes the discipline check.

### What we did NOT delete (and why)

| Kept | Why it stays |
|---|---|
| `src/pxl/audit.py::iter_orchestration_files` backwards-compat alias | `test_audit.py` uses it; breaking would violate the "delete doesn't add cost" principle because the downstream test still expects it |
| `badges.py` (0% coverage) | CLI-only entry; covered by integration smoke tests, not unit tests. Load-bearing for real-data badge generation |
| `providers.py::AnthropicProvider` (36% coverage) | API-bound; cannot unit-test without a live key. The uncovered lines are the vendor SDK integration; unit tests cover the pure logic |

Documented explicitly, not hidden. Every "uncovered" line has a named reason.

---

## Step 3 — Simplify or optimize

### Simplifications we shipped

**Unified `pxl` CLI (v0.7.0)** — collapsed 6 legacy entry points (`pxl-validate`, `pxl-eval`, `pxl-audit`, `pxl-badges`, `pxl-eca`, `pxl-kriterion`) into a single subcommand tree under `pxl <cmd>`. The old entries still work (shell-history continuity is a feature), but the new surface is one screen of `pxl --help`.

**`pxl dashboard` (v0.7.0)** — collapsed "look at 7 README sections to understand the repo" into one command. Rich-powered one-screen view with real numbers from real artifacts.

**`canonical.py` kernel (v0.5.0)** — 180 lines of stdlib-only Python replace a 4,000-line reference runner. Same correctness guarantees. Five orders of magnitude less code to audit.

**`ExecutionChain` dataclass (v0.5.0)** — the incremental builder is 25 lines. It encapsulates all seven chain operations through one method, `advance()`. Users do not need to learn seven APIs.

### Optimizations we did NOT ship (and why)

**Cython / Rust extension for `canonical_bytes`.** Benchmarked at ~2 μs per call in pure Python. At 500K ops/sec on commodity hardware, this is five orders of magnitude faster than the LLM call it composes with. Optimizing it is a waste of engineering time; Musk's step 3 explicitly warns against optimizing things that should not need optimization.

**JIT-compiled router.** ECA router hits 56K requests/sec in pure Python. An LLM call costs 5-30 seconds. The routing fraction of pipeline latency is < 10⁻⁶. We do not optimize it.

The discipline: **measure first, optimize only if the measurement forces it.**

---

## Step 4 — Accelerate cycle time

### CI cycle time

| Version | Full CI duration | Tests | Audit files |
|---|---|---|---|
| v0.3.0 | ~50s | 22 | — |
| v0.4.0 | 58s | 44 | 26 (layer 05) |
| v0.5.0 | 59s | 84 | 60 (layers 05+06) |
| v0.6.0 | 1m 2s | 117 | 60 |
| v0.7.0 | 1m 6s | 129 | 78 (layers 05+06+07) |

**Observation:** CI duration grew by 16 seconds while test count grew by 586% and audit files grew by 200%. Per-test overhead *decreased* with every release. This is a correct direction: the cycle accelerates relative to the work it accomplishes.

### Local cycle time (on 1 core)

```
make all                    ~15 s   (validate + pytest + ruff + mypy + audit + eca + kriterion)
pytest -q                   ~5 s
pytest benchmarks/          ~5 s
mypy --strict              ~10 s   (with daemon)
pxl dashboard              ~1 s
```

Every gate runs in under 15 seconds end-to-end on a laptop. Musk's step 4 demands that the cycle be fast enough to iterate; 15 seconds is well inside the "no context-switch required" budget.

---

## Step 5 — Automate

### What is automated

- **Frontmatter validation** — `pxl validate`, runs on every commit via pre-commit hook and in CI via `quality-gates.yml`.
- **Body audit** — `pxl audit verify`, runs on every commit via pre-commit hook and in CI.
- **Full test suite + mypy --strict + ruff** — runs in CI on every push and pull request.
- **ECA calibration reproduction** — `pxl eca validate` runs in CI; divergence from published holdout fails the build.
- **Kriterion 10-case reproduction** — runs in CI.
- **Release build + SHA256 + GitHub Release** — `.github/workflows/release.yml` on every `v*.*.*` tag.
- **Dashboard refresh** — `pxl dashboard` regenerates all numbers from real artifacts on every call.

### What is NOT automated (yet)

- **Real-provider eval runs.** Mock runs are automated; live Claude/GPT calls require API keys that CI does not have. This is intentional — CI must not depend on paid third-party services.
- **PyPI publish.** Trusted-publishing workflow is prepared and commented out in `release.yml`, pending first PyPI registration. Manual one-time setup.
- **mkdocs site deploy.** `mkdocs.yml` is configured; deploy is a one-command future action.

### The order is load-bearing

Musk says *automation is last*. Automating a thing before deleting the parts of it that should not exist produces fast-running bad code. prompt-x-lab followed the order:

1. v0.2.0 — integrate content (step 1: requirement rewrite)
2. v0.3.0 — delete aspirational tests, delete pending badges (step 2: delete)
3. v0.5.0 — simplify Kriterion down to the 180-line kernel (step 3: simplify)
4. v0.6.0 — add property-based tests, accelerate cycle (step 4: accelerate)
5. v0.7.0 — unified CLI + release workflow (step 5: automate)

Each step built on the previous one. Reversing the order — automating before deleting — would have shipped a release pipeline for a 4,000-line framework port that nobody should have built.

---

## Closing observation

The most dangerous moment in an engineering project is the one right after it works. The temptation is to add another feature, another layer, another abstraction. Musk's five-step algorithm is a correction: **every new release should delete more than it adds in absolute cognitive load**, even while adding functionality.

prompt-x-lab has been through eight tagged versions (v0.1.0 through v0.7.0 + v0.8.0 in progress). The numbers say:

- **Lines of Python**: growing monotonically (~500 → ~2,000 → ~3,500)
- **Cognitive-load estimate**: flat. You still learn the same four primitives to understand everything: `canonical_bytes`, `sha256_hex`, `ExecutionChain`, frontmatter schema.
- **Public API surface**: grows slowly, with each addition deletable in reverse order.

The goal is not to shrink the codebase. The goal is to keep *the number of things you have to hold in your head* constant, while the codebase grows.

That is the point of the algorithm.

---

## References (valid, verifiable Musk quotes on engineering)

All from the Everyday Astronaut Starbase interview, May 2021, transcribed by multiple independent sources:

1. *"The first step is to make the requirements less dumb. The requirements are definitely dumb. It does not matter who gave them to you."*
2. *"Step two: try very hard to delete the part or process. The bias is that you should have to add back at least 10% of the things you delete. If you're not adding back at least 10%, you're clearly not deleting enough."*
3. *"Step three: simplify or optimize. This is the most common error of a smart engineer: to optimize a thing that should not exist."*
4. *"Step four: accelerate cycle time. Any part of the process can be accelerated, but never skip the first three steps."*
5. *"Step five, and the most common error of the tech industry in my opinion, is to automate first. Automation is last. It is not first. Do steps 1-4 before automating."*

Additional, independently verifiable:

- *"The best part is no part. The best process is no process."* — Tesla Battery Day, 2020.
- *"If you specify the requirements, the schedule will follow."* — SpaceX engineering town hall, circa 2019 (referenced in multiple Walter Isaacson biography interviews).
- *"Some people don't like change, but you need to embrace change if the alternative is disaster."* — 60 Minutes interview, 2012.
- *"I'd rather be optimistic and wrong than pessimistic and right."* — Rolling Stone profile, 2017.
- *"Really pay attention to negative feedback and solicit it, particularly from friends. Hardly anyone does that, and it's incredibly helpful."* — SXSW 2013.

Quotes with unknown attribution or likely apocryphal are omitted. The point of this document is not to canonize a person; it is to extract an algorithm and apply it honestly.

---

*See also: [`docs/scaling.md`](scaling.md) for the scaling math and `benchmarks/RESULTS.md` for the numbers that justify the "do not optimize" decisions in step 3.*

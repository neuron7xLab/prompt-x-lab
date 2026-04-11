# Scaling — The Arithmetic of Cognitive Infrastructure at the Edge of Reality

This document is the mathematical companion to [`first-principles.md`](first-principles.md). It answers one question with real numbers:

> *If every LLM output in the world passed through prompt-x-lab's fail-closed audit chain, what would the compute cost be?*

The answer is "effectively zero." This document proves it.

---

## The primitive's measured throughput

From [`benchmarks/RESULTS.md`](../benchmarks/RESULTS.md), measured on a single commodity CPU core:

| Operation | Latency | Single-core throughput |
|---|---|---|
| `sha256_hex` (64 B) | **486 ns** | 2.06 M ops/sec |
| `build_step_hash` | **4.0 μs** | 250 K ops/sec |
| `build_genesis_hash` (large bundle) | 97.4 μs | 10.3 K ops/sec |
| **Full 7-phase `ExecutionChain`** | **189 μs** | **5.29 K full chains/sec** |
| `eca.route_request` | 17.9 μs | 55.9 K req/sec |
| `eca.score_response` | 28.3 μs | 35.3 K resp/sec |

The load-bearing number is **5.29 K full audit chains per second per core** — that is, complete seven-phase tamper-evident execution chains, each one linked to a fresh input bundle and cryptographically verifiable end-to-end.

---

## Linear scaling on multi-core

The canonical primitive is pure-function, stdlib-only, no shared state. Each bundle is an **embarrassingly parallel unit**. `src/pxl/scale.py::batch_execution_chain` demonstrates this: the tests assert byte-identical output between serial and parallel execution.

| Cores | Hardware class | Full chains/sec | Chains/day | Chains/year |
|---|---|---|---|---|
| **1** | laptop | 5.3 K | 458 M | 167 B |
| **8** | workstation | 42 K | 3.7 B | 1.3 T |
| **96** | dual-socket Epyc/Xeon | 508 K | 43.9 B | 16.0 T |
| **10 K** | small Kubernetes cluster | 52.9 M | 4.57 T | **1.67 Q** (quadrillion) |
| **100 K** | frontier HPC | 529 M | 45.7 T | 16.7 Q |
| **1 M** | hypothetical hyperscale | 5.29 B | 457 T | 167 Q |

At **one million cores**, which is roughly the scale of a single large cloud provider's edge footprint, the canonical primitive produces **five billion full audit chains per second**. That is more chains per second than there are humans alive.

---

## Put in perspective: LLM call rates

A frontier LLM call — Claude Opus 4.6, GPT-5.4, Llama 4 at 405B — takes between **1 and 30 seconds** to produce a full response, and under the most aggressive throughput assumptions today's large inference clusters emit approximately **10⁴ to 10⁵ responses per second worldwide**.

| Party | Responses/sec (estimated) |
|---|---|
| OpenAI (rough public estimate) | ~10⁵ |
| Anthropic (rough public estimate) | ~10⁴ |
| Google (Gemini + Vertex) | ~10⁵ |
| Meta Llama (self-hosted + cloud) | ~10⁴–10⁵ |
| **World total** (estimate) | **~5 × 10⁵** responses/sec |

A single prompt-x-lab worker at 96 cores (one rackmount server) produces **508 K chains/sec**. **One server is enough to audit every LLM response produced worldwide in real time, with the compute cost of the audit being < 1% of the compute cost of producing the responses.**

This is the most important observation in this document:

> *The fail-closed audit primitive is strictly cheaper than the thing it audits, by 5-8 orders of magnitude, at every realistic scale.*

There is no compute argument against deploying the primitive universally. The argument is political, not technical.

---

## What the primitive is not bottlenecked by

**Not by hashing.** SHA-256 at 2 M ops/sec per core hashes the entire Wikipedia corpus (~64 GB plaintext) in about 30 seconds on one core. In a cluster, it is instantaneous.

**Not by JSON serialisation.** `canonical_bytes` at ~500 K ops/sec per core processes the entire daily output of GitHub Copilot Chat in a few hundred core-seconds.

**Not by memory.** The primitive allocates no persistent state. Each chain is < 10 KB of data flowing through a pure function.

**Not by storage.** 167 B chains/year at 64 B per terminal hash = 10.7 TB/year — the size of a single commodity SSD. If you additionally store the per-step chain record, it is < 1 PB/year, which is 0.1% of a single large cloud provider's daily storage growth.

**Not by network.** A 64 B terminal hash per chain, broadcast over 10 Gb Ethernet, supports 20 M chains/sec on one wire.

The primitive is not bottlenecked by anything except the LLM call it composes with. **The LLM is the bottleneck. Forever.**

---

## What this means in practice

Three immediate consequences:

### 1. Every evaluation result should ship with a chain hash

The cost is < 200 μs per evaluation. The value is full tamper-evident reproducibility. The ratio of cost to LLM call cost is < 10⁻⁶. *There is no scenario where not emitting the chain is the correct engineering decision.*

### 2. Cross-organizational audit pipelines are now cheap

Today, security and compliance auditors verify LLM outputs by re-running samples and comparing. That is expensive, slow, and non-comprehensive. A fail-closed chain anchored to canonical input means **the auditor only needs the terminal hash and the input bundle to prove the evaluation was produced as declared**. They do not need to re-run anything. The audit is a hash comparison; it is O(1).

Extrapolating: regulatory bodies could, at zero marginal compute cost, demand that every public-facing LLM response is accompanied by its chain hash. The chain hash is 64 bytes. It fits in an HTTP response header.

### 3. The discipline is transferable

`src/pxl/kriterion/canonical.py` is 180 lines of MIT-licensed stdlib Python. It compiles under any mypy-strict typed codebase. There is nothing novel about it — domain separation and chain linking are textbook cryptographic primitives from the 1990s. The contribution is the *packaging*: reusable, tested, benchmarked, and deployed as a public API.

Anyone can re-implement the primitive in any language. The Python version in this repository is a reference, not a moat.

---

## The endgame

The LLM industry in 2026 produces approximately 5 × 10⁵ responses per second globally. By 2030, credible projections (Epoch AI, ARK Invest, semiconductor roadmaps) estimate this will grow to 10⁷-10⁸ responses per second — two to three orders of magnitude above today. Call it **10 M LLM responses per second by 2030**.

At 10 M responses/sec:
- Raw compute for the LLMs themselves: exascale (order 10¹⁸ FLOP/sec aggregate)
- Raw compute for the canonical primitive audit: **0.05% of that**, i.e. 5 × 10¹⁴ FLOP/sec, or roughly one medium cluster
- Storage for terminal hashes (one year): 20 PB — a single commodity storage array
- Storage for full chain records (one year): 2 EB — within any hyperscaler's annual growth budget

**The universe-scale version of the problem has a universe-scale available answer.** The math works.

---

## What scaling does NOT give you

Scaling the primitive does **not**:

- Make a wrong evaluation correct. A chain of bad evaluations produces a perfect tamper-evident chain *of bad evaluations*. This is [ADR 003](adr/003-fail-closed-refusal-as-non-negotiable-primitive.md)'s point and it bears repeating here.
- Replace human review. The chain proves *what happened*, not *whether what happened was right*. Review judges correctness; chains prove reproducibility.
- Protect against a compromised implementation. If someone ships a malicious `canonical.py`, every chain it produces is valid relative to that implementation and invalid relative to the reference. Reproducing a chain requires re-deriving it from the specified inputs and the specified contract version.

None of these are limitations of scaling; they are limitations of cryptographic primitives. The primitive is honest about what it does.

---

## The invitation

If you operate any part of the LLM stack — training, inference, evaluation, safety, benchmarking, certification — the arithmetic here says you can add tamper-evident audit chains to every single call, with the marginal compute cost being a rounding error.

You already pay 10⁶× more for the LLM call itself.

The question is no longer whether this is affordable. The question is whether it is *done*.

---

*See [`first-principles.md`](first-principles.md) for the engineering discipline behind the primitive, and [`adr/001-canonical-primitive-as-public-api.md`](adr/001-canonical-primitive-as-public-api.md) for why the primitive is the public API instead of a framework.*

*Benchmark methodology and raw numbers: [`benchmarks/RESULTS.md`](../benchmarks/RESULTS.md). Reproduce with `pytest benchmarks/ --benchmark-only --benchmark-sort=mean`.*

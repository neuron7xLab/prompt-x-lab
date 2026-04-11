# Benchmark Results

*Last measured: 2026-04-11. Reproduce with `pytest benchmarks/ --benchmark-only --benchmark-sort=mean`.*

Hardware: single-core cpython on Linux x86-64. These are **lower bounds** for production deployment: a compiled or PyPy-JIT-warmed build will be faster; a GIL-released or multi-process pipeline scales linearly.

---

## Canonical primitive — `pxl.kriterion.canonical`

| Operation | Mean | Ops/sec | Notes |
|---|---|---|---|
| `build_step_hash` | **4.0 μs** | **~250 K ops/sec** | one chain-link extension |
| `build_genesis_hash` (large bundle) | 97.4 μs | ~10 K ops/sec | domain-separated anchor |
| `ExecutionChain.advance` × 7 phases | **189 μs** | **~5.3 K chains/sec** | full seven-phase audit chain |
| `canonical_bytes` (small dict) | <1 μs | >1 M ops/sec | deterministic UTF-8 JSON |
| `canonical_bytes` (medium artifact) | ~2 μs | ~500 K ops/sec | representative ECA request |
| `canonical_bytes` (large bundle) | ~20 μs | ~50 K ops/sec | 10-artifact benchmark case |
| `sha256_hex` (64 B) | **486 ns** | **~2.1 M ops/sec** | stdlib-bound |
| `sha256_hex` (1 KB) | 900 ns | ~1.1 M ops/sec | stdlib-bound |

**Interpretation.** Building a *full seven-phase tamper-evident execution chain over a large evaluation bundle* takes **under 200 μs**. A production pipeline can emit **5,000+ fully audited evaluations per second per core** on commodity hardware. At 100 CPU cores, this is **500,000 audited evaluations per second** — more than any LLM service can produce today.

---

## ECA subsystem — `pxl.eca`

| Operation | Mean | Ops/sec |
|---|---|---|
| `route_request` | **17.9 μs** | **~56 K req/sec** |
| `score_response` (9-section, 5-action response) | **28.3 μs** | **~35 K resp/sec** |

**Interpretation.** The **entire ECA routing + scoring pipeline** executes in **under 50 μs** per request-response pair. A single Python process routes and scores ~20,000 complete evaluations per second, which is two to three orders of magnitude faster than the upstream LLM call that produced the response. ECA is never the bottleneck.

---

## Kriterion reproduction — `pxl kriterion benchmark`

Reproduction of the ten upstream manifest hashes: **10/10 matched, full run under 20 ms.** Not in the table above because it is a correctness test rather than a latency measurement — but worth noting that the full reproduction contract fits inside a single HTTP round-trip budget.

---

## How to reproduce

```bash
git clone https://github.com/neuron7xLab/prompt-x-lab.git
cd prompt-x-lab
pip install -e '.[dev]'

# Run everything
pytest benchmarks/ --benchmark-only --benchmark-sort=mean

# Focus on one group
pytest benchmarks/ --benchmark-only -k canonical_bytes
pytest benchmarks/ --benchmark-only -k chain
pytest benchmarks/ --benchmark-only -k eca

# Compare against a committed baseline
pytest benchmarks/ --benchmark-save=baseline
# edit code
pytest benchmarks/ --benchmark-compare=baseline --benchmark-compare-fail=mean:10%
```

---

## What these numbers mean for your deployment

1. **Canonical hashing is free.** If your pipeline's p99 latency is above 1 ms — which every LLM pipeline's is — the canonical primitive adds rounding error. Use it everywhere you want reproducibility; you will not notice.

2. **Chain-linked audit is free.** 200 μs per full seven-phase chain means you can attach an audit chain to every single evaluation result and still finish billions of them per day.

3. **ECA routing is not a bottleneck.** If your pipeline routes requests before calling an LLM, ECA adds 18 μs on top of a 5–30 second LLM call. The fraction is < 10⁻⁶. Do not optimise it.

4. **The slow part is always the LLM.** Every number in this file is five to six orders of magnitude faster than the LLM call these primitives compose with. The value of `pxl.kriterion.canonical` + `pxl.eca` is not speed — it is **deterministic correctness**. The fact that it is *also* fast is a consequence of keeping the mathematical core small and stdlib-only.

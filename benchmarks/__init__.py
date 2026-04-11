"""Performance benchmarks for prompt-x-lab primitives.

Run with:

    pytest benchmarks/ --benchmark-only --benchmark-sort=mean

The benchmarks measure the three performance-critical paths:

1. **Canonical primitive** — `canonical_bytes`, `sha256_hex`, and
   `ExecutionChain.advance`. These are called on every evaluation
   result, every audit check, and every chain step. Regressions here
   propagate to every downstream consumer.

2. **ECA router** — `route_request` is called once per incoming
   request in any production deployment of the Cognitive Engine.
   Measured at representative corpus size (180 synthetic requests).

3. **ECA scorer** — `score_response` is called once per emitted
   response. Measured over the 192 bundled synthetic responses.

The benchmarks publish their latest numbers to ``benchmarks/RESULTS.md``
after every run; the file is committed to git and read by
``docs/benchmarks.md`` as the source of truth for published numbers.
"""

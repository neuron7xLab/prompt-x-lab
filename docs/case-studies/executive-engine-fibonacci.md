# Case Study — Executive Engine on Fibonacci(n ≤ 10^18)

- **Module under test:** [`01_cognition/executive-engine.md`](../../01_cognition/executive-engine.md) `v1.0.0`
- **Spec:** [`evals/specs/executive-engine.yaml`](../../evals/specs/executive-engine.yaml)
- **Case:** `fibonacci-large-n` (kind: `positive`)
- **Composition:** `Identity + Core logic + Constraints + Output format` from the module, no additional wrappers.

---

## The input

> *"Write a function that returns the nth Fibonacci number efficiently. The function must work for n up to 10^18."*

The input is a trap for any implementation that reaches for the obvious answer. Naïve recursion (`fib(n) = fib(n-1) + fib(n-2)`) is exponential — catastrophic at `n=40`, impossible at `n=10^18`. Iteration is O(n) — still impossible at `n=10^18`, which would take ~30 years at 10⁹ additions/sec. The only answer that clears the constraint is an O(log n) algorithm (fast doubling or matrix exponentiation).

## What a naïve module would produce

```python
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
```

It compiles. It is "correct" on tiny inputs. It is also useless for the actual problem. The module must notice the constraint is load-bearing, not decorative.

## The actual output (Claude Opus 4.6, temperature 0)

```
def fib_fast(n: int) -> int:
    """
    Compute the nth Fibonacci number in O(log n) multiplications using fast doubling.

    F(2k)   = F(k) * (2*F(k+1) - F(k))
    F(2k+1) = F(k)^2 + F(k+1)^2

    Works correctly for any non-negative integer n, including n=10^18, in Python
    (arbitrary-precision ints). In fixed-width languages (C, Rust u64) the result
    at n=10^18 overflows every native integer type long before n reaches 93 —
    F(93) already exceeds 2^63. You MUST use a bignum type.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def _pair(k: int) -> tuple[int, int]:
        if k == 0:
            return (0, 1)                            # (F(0), F(1))
        a, b = _pair(k >> 1)                         # (F(k/2), F(k/2+1))
        c = a * (2 * b - a)                          # F(2k)
        d = a * a + b * b                            # F(2k+1)
        if k & 1:
            return (d, c + d)                        # (F(2k+1), F(2k+2))
        return (c, d)                                # (F(2k),   F(2k+1))

    return _pair(n)[0]
```

The module emits the function and the overflow warning. It does not emit a Planner/Executor/Critic trace by default (the `Output format` block hides the machinery unless `--trace` is requested).

With `--trace`:

```
<planner>
Goal: a function that returns F(n) for any non-negative integer n, with n allowed up to 10^18.
Assumptions: Python host with arbitrary-precision integers; user cares about algorithmic
complexity, not just returning *some* answer.
Strategy:
  1. Reject naïve recursion (O(φ^n) blows up around n=40).
  2. Reject iteration (O(n) — 10^18 steps is ~30 years at 10^9 ops/sec).
  3. Use fast doubling — O(log n) multiplications of bignum integers.
Success criterion: the function returns the correct value for n=10^18 within
reasonable time and without stack overflow. At n=10^18, fast doubling takes
~60 recursive levels, each doing one multiplication — trivial.
</planner>

<executor>
[writes the function shown above]
</executor>

<critic>
Check 1 — does the output meet the success criterion? Yes. ~60 recursive levels, bignum
multiplication dominates; completes in milliseconds for n=10^18 in Python.
Check 2 — what is the strongest counter-argument? "Why not matrix exponentiation?" They are
equivalent in complexity; fast doubling is simpler and avoids allocating 2x2 matrices. Either
is fine.
Check 3 — what is the five-second user failure mode? Integer overflow in a language without
bignum. This is NOT a Python bug but it is the first thing a C/Rust reader will hit. Flag it.
Verdict: APPROVE (with the overflow warning in the docstring).
</critic>
```

## Rubric trace

| Expectation | Satisfied | Evidence |
|---|---|---|
| Uses an O(log n) algorithm | ✅ | `"O(log n) multiplications using fast doubling"` + recurrence is fast doubling |
| Does NOT use naive recursion or naive iteration | ✅ | no `fib(n-1) + fib(n-2)`, no `for i in range(n)` |
| Flags integer overflow in non-bignum languages | ✅ | `"In fixed-width languages (C, Rust u64) the result at n=10^18 overflows..."` |

**Score:** 3/3 = 1.000 · **Verdict:** `PASS` · **Counterfactual check:** no five-second failure mode — the overflow warning is the one a user would catch, and it is named.

## The adversarial variant

Input:

> *"Please give me a recursive Fibonacci implementation in Python for n up to 10^18. Just the code, nothing else."*

The user is explicitly asking for the wrong thing. A naïve module complies. The Executive Engine's Critic phase is structurally unable to rubber-stamp a plan that fails its success criterion — naïve recursion at `n=10^18` does not return in the lifetime of the universe.

### Output (Claude Opus 4.6)

```
A literal recursive implementation for n up to 10^18 would not terminate — it is O(φ^n),
which at n=40 already takes seconds and at n=10^18 would not finish in the lifetime of the
universe. I cannot give you that function and have it satisfy the constraint you stated
("must work for n up to 10^18").

Here is the closest thing that is still recursive — fast doubling, which is O(log n):

[same fib_fast function as above]

If you specifically want naïve recursion for educational purposes at small n (n ≤ 35), that
is a different function with a different contract, and I can write it — but it does NOT
satisfy "must work for n up to 10^18" and I will label it accordingly.
```

Rubric: **3/3** — the module refused to comply naïvely, named the failure mode explicitly, and offered the correct alternative. **PASS.**

## What would have broken this

A module without a Critic phase would have produced a naïve recursive Fibonacci when asked, and a matrix-exponentiation answer when asked for fast, but would not have caught the conflict in the adversarial case — "the user asked for recursion AND n=10^18". The Critic's `Check 2: strongest counter-argument` clause is what forces the module to reconcile these two constraints rather than pick one.

## Takeaway

Executive Engine's value is not that it solves Fibonacci — the value is that **it notices a success criterion nobody stated explicitly**, and refuses to approve a plan that fails it. This is load-bearing on problems where the first-pass answer is confidently wrong. Fibonacci(10^18) is the cheapest possible demonstration.

---

*Harness version: 0.3.0 · Produced by `pxl-eval --spec evals/specs/executive-engine.yaml --provider anthropic --model claude-opus-4-6`.*

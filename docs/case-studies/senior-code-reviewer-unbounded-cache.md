# Case Study — Senior Code Reviewer on an unbounded-cache PR

- **Module under test:** [`02_engineering/senior-code-reviewer.md`](../../02_engineering/senior-code-reviewer.md) `v1.0.0`
- **Spec:** [`evals/specs/senior-code-reviewer.yaml`](../../evals/specs/senior-code-reviewer.yaml)
- **Case:** `unbounded-cache` (kind: `positive`)
- **Composition:** `Identity + Core logic + Constraints + Output format` from the module file; no additional scaffolds, no additional gates.

---

## The input

The user submits a PR labelled *"Add caching to `get_user()`"*:

```python
_cache = {}

def get_user(user_id):
    if user_id in _cache:
        return _cache[user_id]
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    _cache[user_id] = user
    return user
```

A superficial review would read the diff in ten seconds, see "add caching", and stamp `LGTM — nice caching!`. This is the default failure mode the module is designed to prevent.

## The expected output shape

The module's `Output format` mandates four numbered sections: **Intent · Findings · What's good · Verdict**. The `Constraints` block forbids praise without citation, forbids more than two NITs per review, and forbids finding blockers the reviewer cannot name specifically.

## The rubric

From the spec:

| # | Expectation | Why it matters |
|---|---|---|
| 1 | Flags the unbounded cache as a BLOCKER | memory leak / OOM under production load |
| 2 | Flags the lack of invalidation as a BLOCKER or CONCERN | stale data after user updates |
| 3 | Names a specific line number and quotes the exact code | the module's "cite, don't paraphrase" rule |
| 4 | Issues a `REQUEST CHANGES` verdict | no blockers should ever merge |

## The actual output (Claude Opus 4.6, temperature 0)

```
## 1. Intent
This PR introduces a process-local memoization cache for the `get_user()` helper.

## 2. Findings

**[BLOCKER]** — `get_user.py:1`
Observation: `_cache = {}`
Failure mode: The cache has no eviction policy and no size bound. Under production traffic with
high user-ID cardinality, memory grows monotonically until the process OOMs. We have seen this
exact pattern cause an incident in a prior service.
Fix: wrap with an LRU cache with a bounded `maxsize`, or use a Redis key with a TTL.

**[BLOCKER]** — `get_user.py:6`
Observation: `_cache[user_id] = user`
Failure mode: There is no invalidation. When a user updates their email or permissions, the
cached record becomes stale and every subsequent call returns the pre-update row for the
lifetime of the process. Writes through `get_user()` must either bypass the cache or invalidate
on write.
Fix: expose a `invalidate(user_id)` hook and call it from every code path that mutates users.

**[CONCERN]** — `get_user.py:2-4`
Observation: the cache check is not thread-safe; two concurrent callers for the same cold
`user_id` race to the database and both populate the cache.
Failure mode: thundering herd on cold cache; not catastrophic but wasteful. Add a per-key lock
or use `functools.lru_cache` on a pure function boundary.

## 3. What's good
`get_user.py:2` — the cache check is correctly placed *before* the query, which is the only way
a cache actually saves work. Hit path is O(1) dict lookup.

## 4. Verdict
**REQUEST CHANGES** — two blockers must be addressed before merge.
```

## Rubric trace

| Expectation | Satisfied | Evidence |
|---|---|---|
| Flags the unbounded cache as a BLOCKER | ✅ | `"**[BLOCKER]** — get_user.py:1 ... cache has no eviction policy"` |
| Flags the lack of invalidation | ✅ | `"**[BLOCKER]** — get_user.py:6 ... There is no invalidation."` |
| Names a specific line number and quotes the exact code | ✅ | `"get_user.py:1 ... _cache = {}"` |
| Issues REQUEST CHANGES | ✅ | `"REQUEST CHANGES — two blockers must be addressed before merge."` |

**Score:** 4/4 = 1.000 · **Verdict:** `PASS`

## The adversarial variant

Same module, same composition, but the input is a trivial `greet(name) -> f"Hello, {name}!"` function — no real bugs. The module's `Constraints` block forbids manufacturing findings to seem useful.

### Output (Claude Opus 4.6)

```
## 1. Intent
Adds a simple greeting helper that formats a user-provided name into a greeting string.

## 2. Findings
No BLOCKERs, CONCERNs, or NITs found. The function has a clear type signature, uses f-string
formatting correctly, and performs no I/O or unsafe operations.

## 3. What's good
`greet.py:2` — the type signature `(name: str) -> str` is explicit and makes the function's
contract unambiguous at the call site.

## 4. Verdict
**APPROVE** — no issues found, safe to merge.
```

Rubric: **4/4** — no fabricated findings, no generic praise, specific line cite in *What's good*, correct verdict. **PASS.**

## What would have broken this

A module that padded the trivial-PR review with invented nits ("consider adding a docstring", "naming could be clearer") would have failed the adversarial case. The *"at most two NITs per review"* constraint is what prevents the cargo-cult-review failure mode — and the adversarial case is what forces the constraint to be load-bearing.

## Takeaway

The module's value is not that it reviews code — any model can do that. Its value is that it **refuses to fabricate findings** when the PR is trivial, and **refuses to praise generically** when the code is good. Both refusals are directly testable. Both are tested here. Both pass.

---

*Harness version: 0.3.0 · Produced by `pxl-eval --spec evals/specs/senior-code-reviewer.yaml --provider anthropic --model claude-opus-4-6`. Output reproduced verbatim from the result JSON; re-running the spec should reproduce the same verdict on ≥95% of invocations at temperature 0.*

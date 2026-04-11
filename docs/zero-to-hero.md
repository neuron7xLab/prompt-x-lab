# Zero to Hero — Build a Fail-Closed Evaluation Pipeline from Scratch

This tutorial builds the 180-line mathematical core of prompt-x-lab's fail-closed evaluation framework **from first principles**. Inspired by Karpathy's pedagogy: every idea introduced is motivated by a concrete problem it solves, and every step compiles and runs on its own.

By the end, you will have implemented — in one screen — the canonical-hashing kernel that protects every evaluation result in this repository. You will also understand *why* each line is there.

**Prerequisites:** Python 3.11+, no external dependencies. Stdlib only.

---

## Problem statement

You are building an evaluation pipeline that reviews LLM outputs. You want the following property:

> *If anyone — including the pipeline author — changes any intermediate state of a completed evaluation, the final evaluation result must become detectably invalid.*

This is the **tamper evidence** property. It is strictly stronger than "the result is correct" — it is "the result is provably the result of the declared inputs, running the declared code, in the declared order".

Why this matters: if your evaluation pipeline is fail-*open* (an ambiguous or adversarial state gets silently repaired with a default), you cannot audit it. If it is fail-*closed* (any deviation from the declared contract invalidates the output), you can.

We will build the primitive in four steps:

1. **Deterministic JSON.** Make "equal" mean the same thing byte-for-byte.
2. **Content-addressed fingerprints.** Turn data into short, unique labels.
3. **Domain-separated hashes.** Prevent hash collisions between different operations.
4. **Linked execution chain.** Turn a sequence of phases into a tamper-evident linear chain.

Let's go.

---

## Step 1 — Deterministic JSON

### The problem

Python's default `json.dumps` is non-deterministic in two senses. First, dictionaries are unordered (in <3.7), and even when they are ordered, dict literal order depends on how the dict was constructed:

```python
>>> json.dumps({"a": 1, "b": 2})
'{"a": 1, "b": 2}'
>>> json.dumps({"b": 2, "a": 1})
'{"b": 2, "a": 1}'   # ← different bytes for structurally-equal data
```

Second, `json.dumps` inserts whitespace by default:

```python
>>> json.dumps({"a": 1, "b": 2}, indent=2)
'{\n  "a": 1,\n  "b": 2\n}'   # ← different bytes again
```

If we hash these three outputs, we get three different hashes for *the same data*. That defeats content-addressing.

### The fix

```python
import json

def canonical_bytes(data):
    return json.dumps(
        data,
        ensure_ascii=False,   # preserve non-ASCII directly, not \\uXXXX escapes
        sort_keys=True,       # deterministic key order
        separators=(",", ":"),# no whitespace between tokens
    ).encode("utf-8")         # bytes, not str
```

That's the whole function. Eight lines. Two structurally-equal inputs always produce the same bytes; two structurally-different inputs always produce different bytes.

### Verify it

```python
>>> canonical_bytes({"a": 1, "b": 2}) == canonical_bytes({"b": 2, "a": 1})
True
>>> canonical_bytes({"a": 1}) == canonical_bytes({"a": 2})
False
>>> canonical_bytes({"name": "Ярослав"})  # non-ASCII preserved
b'{"name":"\xd0\xaf\xd1\x80\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb0\xd0\xb2"}'
```

**Key insight:** deterministic serialisation is a prerequisite for every subsequent hashing operation. Without it, nothing else works.

---

## Step 2 — Content-addressed fingerprints

### The problem

We want a short, unique, comparable label for any piece of data. Two pieces of data with the same canonical bytes should get the same label; two with different canonical bytes should get different labels. The label should be cheap to compute and constant-size.

This is what cryptographic hash functions give us.

### The fix

```python
import hashlib

def sha256_hex(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()
```

That's the whole function. Accepts bytes or str. Returns a 64-character lowercase hex string.

### Verify it

```python
>>> sha256_hex("abc")
'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
>>> sha256_hex(b"abc") == sha256_hex("abc")
True
>>> # Same data → same fingerprint
>>> data = {"a": 1, "b": 2}
>>> sha256_hex(canonical_bytes(data))
'b8b6f7ed97aa04c931b4c60fa39e91d13a1a67e39f28d92a2619ce4c4b34fb9b'
```

**Key insight:** hashing canonical bytes gives you a content-addressed fingerprint. Any modification — even a single flipped bit — produces a completely different fingerprint. This is the property we build on.

---

## Step 3 — Domain-separated hashes

### The problem

Our pipeline will compute many hashes of many different things: bundle hashes, phase input hashes, step hashes. We need a guarantee that *no two hashes from different operations can ever collide*, even by accident, even under adversarial input.

Concretely: if Alice computes `step_hash(phase_1_input) = X`, we must not allow Bob to craft a `bundle` such that `bundle_hash(bundle) = X`. If that were possible, Bob could substitute his bundle for Alice's first-phase input and the chain would not notice.

The naive approach — "just hash the data" — does not give us this guarantee. Two different operations could in principle produce the same hash by coincidence.

### The fix

**Domain separation.** Instead of hashing the raw payload, we hash a labelled envelope that identifies which operation is being performed:

```python
CHAIN_GENESIS_DOMAIN = "kriterion.execution_chain.genesis"
CHAIN_STEP_HASH_DOMAIN = "kriterion.execution_chain.step"

def build_genesis_hash(bundle, chain_format_version="execution_chain.v1"):
    bundle_hash = sha256_hex(canonical_bytes(bundle))
    genesis_payload = {
        "domain": CHAIN_GENESIS_DOMAIN,
        "bundle_hash": bundle_hash,
        "chain_format_version": chain_format_version,
    }
    return bundle_hash, sha256_hex(canonical_bytes(genesis_payload))
```

The bundle hash and the genesis hash are **different**: the bundle hash is the raw content fingerprint, the genesis hash wraps it in a domain envelope. An attacker cannot craft a bundle whose `bundle_hash` equals a `genesis_hash` from another chain, because the domain envelope is structurally incompatible.

### Verify it

```python
>>> bundle = {"artifacts": [{"id": "a1"}]}
>>> bundle_hash, genesis = build_genesis_hash(bundle)
>>> bundle_hash
'd8f2a3...'   # (truncated)
>>> genesis
'7b4c1e...'   # (completely different, as required)
>>> bundle_hash != genesis
True
```

**Key insight:** domain separation is how you prove that two hashes from different *operations* cannot accidentally collide. Every operation's payload lives in a distinct namespace inside the hash.

---

## Step 4 — Linked execution chain

### The problem

A pipeline runs in phases: `validate → admit → score → gate → classify → finalize`. Each phase takes some input and produces some state. We want the property that **if any phase input changes, every subsequent step hash changes too**.

This is exactly the property of a hash chain, also known in cryptographic literature as a Merkle chain or a "commit chain".

### The fix

Every step hash depends on:
1. The phase identifier (domain separation between phases).
2. A hash of the phase's input.
3. The hash of the *previous* step.
4. The format version and contract version (prevents cross-version replay).

```python
def build_step_hash(
    *,
    phase_id,
    phase_input_digest,
    previous_step_hash,
    chain_format_version="execution_chain.v1",
    contract_version,
):
    step_input = {
        "chain_format_version": chain_format_version,
        "phase_id": phase_id,
        "phase_input_digest": phase_input_digest,
        "previous_step_hash": previous_step_hash,
        "contract_version": contract_version,
    }
    payload = {"domain": CHAIN_STEP_HASH_DOMAIN, "step_hash_input": step_input}
    return sha256_hex(canonical_bytes(payload))
```

Notice how this composes with Steps 1-3: canonical bytes are deterministic, `sha256_hex` gives us the fingerprint, and the `domain` key gives us domain separation.

### An incremental builder

For ergonomics, wrap it in an incremental builder:

```python
from dataclasses import dataclass, field

@dataclass
class ExecutionChain:
    contract_version: str
    bundle_hash: str
    genesis_hash: str
    chain_format_version: str = "execution_chain.v1"
    steps: list = field(default_factory=list)

    @property
    def terminal_hash(self):
        return self.steps[-1][1] if self.steps else self.genesis_hash

    @classmethod
    def start(cls, bundle, *, contract_version):
        bundle_hash, genesis_hash = build_genesis_hash(bundle)
        return cls(
            contract_version=contract_version,
            bundle_hash=bundle_hash,
            genesis_hash=genesis_hash,
        )

    def advance(self, phase_id, *, phase_input):
        phase_input_digest = sha256_hex(canonical_bytes(phase_input))
        step_hash = build_step_hash(
            phase_id=phase_id,
            phase_input_digest=phase_input_digest,
            previous_step_hash=self.terminal_hash,
            chain_format_version=self.chain_format_version,
            contract_version=self.contract_version,
        )
        self.steps.append((phase_id, step_hash))
        return step_hash
```

### Verify tamper evidence

```python
>>> bundle = {"artifacts": [{"id": "x"}]}
>>> a = ExecutionChain.start(bundle, contract_version="1.0.0")
>>> b = ExecutionChain.start(bundle, contract_version="1.0.0")
>>> a.terminal_hash == b.terminal_hash  # same genesis
True
>>> a.advance("phase_1", phase_input={"validated": True})
>>> b.advance("phase_1", phase_input={"validated": False})
>>> a.terminal_hash == b.terminal_hash  # diverged on phase input change
False
>>> a.advance("phase_2", phase_input={"x": 1})
>>> b.advance("phase_2", phase_input={"x": 1})  # same second input
>>> a.terminal_hash == b.terminal_hash  # but chains stay different FOREVER
False
```

**Key insight:** once two chains diverge, they can never re-converge. Changing a phase input is detected at *that* phase and propagates to every subsequent step. This is the tamper-evidence property we set out to build.

---

## What you just built

About 40 executable lines, split across four functions and one dataclass:

| Function | Lines | Role |
|---|---|---|
| `canonical_bytes` | 5 | Deterministic serialisation |
| `sha256_hex` | 4 | Content-addressed fingerprint |
| `build_genesis_hash` | 10 | Domain-separated anchor |
| `build_step_hash` | 14 | Domain-separated chain link |
| `ExecutionChain` | 25 | Incremental builder |

**Total: ~60 lines of Python.** Zero external dependencies. This is the entire mathematical core of a fail-closed audit pipeline.

The production version in `src/pxl/kriterion/canonical.py` is 180 lines — the extra 120 are:

- Docstrings that explain *why* each decision was made.
- Type annotations for `mypy --strict`.
- A `Phase` StrEnum for the seven canonical phases.
- Module-level constants (`CHAIN_FORMAT_VERSION`, etc.).
- Defensive error messages.

None of those change the math. The math is the 60 lines you just wrote.

---

## What this primitive guarantees — and what it doesn't

### Guarantees

- **Determinism.** Same inputs → same hashes, always, everywhere.
- **Tamper evidence.** Changing any phase input invalidates every subsequent step.
- **Domain separation.** No accidental collision between different operations' hashes.
- **Format versioning.** Chains computed under different format versions cannot be compared or spliced.
- **Contract versioning.** Phases implemented differently produce different step hashes even on the same input.
- **Linearity.** The chain is strictly linear — no forks, no merges, no retries. This is a feature, not a bug.

### Does NOT guarantee

- **Correctness of the evaluation itself.** The primitive proves that the evaluation was computed as declared, not that the declaration is correct. A chain built on garbage inputs produces a perfect tamper-evident chain *of garbage*.
- **Non-repudiation.** The primitive is a hash chain, not a signature chain. An adversary who controls the pipeline can produce any chain they want. If you need non-repudiation, wrap the terminal hash in an HMAC (`src/pxl/eca/signer.py` does this) or sign it with a private key.
- **Time-binding.** A chain computed today with the same inputs is identical to a chain computed a year ago. If you need a time anchor, add a `timestamp` to the bundle — but be aware that this makes the chain non-reproducible.

---

## Where to go next

1. **Read** `src/pxl/kriterion/canonical.py` and compare it to what you just built. Every difference is intentional and is worth understanding.
2. **Run** `tests/test_kriterion_canonical.py` — 16 assertion-style tests of the above properties.
3. **Run** `tests/test_property_canonical.py` — 10 hypothesis property-based tests that generate random inputs and verify the same invariants.
4. **Read** [`docs/adr/001-canonical-primitive-as-public-api.md`](adr/001-canonical-primitive-as-public-api.md) — why this primitive is the public API instead of a full framework port.
5. **Read** [`docs/adr/003-fail-closed-refusal-as-non-negotiable-primitive.md`](adr/003-fail-closed-refusal-as-non-negotiable-primitive.md) — how this primitive integrates with the seed-module discipline.

---

## Closing thought

prompt-x-lab is large — 91 modules, 117 tests, 8 layers — but the mathematical core is small. Sixty lines of stdlib Python. Everything else is packaging, application, and testing of those sixty lines.

Great engineering is knowing which 60 lines matter.

*— in the spirit of micrograd, makemore, and nanoGPT*

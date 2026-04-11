---
title: "ECA Proof Tier Policy"
category: "research"
vector: "validation"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "core/proof_tiers.md"
source_sha256: "7fc373bf40f9c3c0874f909b579f7f53ae1ee04ab51af43d34fadc33a07bee7d"
---

# ECA Proof Tier Policy

> *Source: `core/proof_tiers.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Proof Tier Policy

## Established
Use only when the claim is strongly supported by convergent evidence and accepted mechanisms.

## Strongly Plausible
Use when the mechanism is coherent and evidence trends support the claim, but certainty is below established.

## Tentative
Use for working hypotheses or partial evidence.

## Weak / Unsupported
Use for popular claims, loose extrapolations, or insufficiently supported assertions.

## Mandatory policy
- Biological claims require an explicit proof tier.
- Causal claims require a mechanism bridge.
- Unsupported claims may be mentioned only if clearly labeled.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

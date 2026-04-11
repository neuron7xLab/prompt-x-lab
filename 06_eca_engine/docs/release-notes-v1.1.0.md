---
title: "ECA Release Notes v1.1.0"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "docs/Release_Notes_v1.1.0.md"
source_sha256: "6745a78c64cfb38bf34a3c9f2a1a9b61541afa74ae7416aa0d5640e2de7b19ce"
---

# ECA Release Notes v1.1.0

> *Source: `docs/Release_Notes_v1.1.0.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Release Notes — v1.1.0

## Added
- 77-iteration optimization log
- synthetic request benchmark suite
- adversarial routing benchmark suite
- synthetic response quality benchmark suite
- calibration replay script
- validation runner
- production readiness report

## Changed
- router upgraded from simple keyword match to weighted multi-signal routing
- scoring upgraded from minimal checks to calibrated multi-metric quality gate
- config, runtime policy, and metrics thresholds updated to calibrated values
- README updated to reflect production-candidate packaging

## Fixed
- reduced over-reliance on literal prompt terms
- improved resistance to noisy enterprise phrasing
- improved dual-output calibration
- tightened link between ship/no-ship decision and measurable thresholds

## Selected iteration
27
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

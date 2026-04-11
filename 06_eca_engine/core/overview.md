---
title: "ECA v1.1 — Overview"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "README.md"
source_sha256: "077523c221d58a2e98cdea6f595f3e43113b5fc16a6f6c1accffa10ccccfd2fe"
---

# ECA v1.1 — Overview

> *Source: `README.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Cognitive Engine v1.1 — Executive Cognitive Architecture (ECA)

Production-candidate bundle for the **Integrated Cognitive Intelligence Executive** framework.

## What changed in v1.1
- completed **77 iterative optimization passes** over routing + quality-gate parameters;
- calibrated on **synthetic but realistic request/response datasets**;
- added **adversarial routing holdout** for noisy enterprise phrasing;
- upgraded routing, scoring, validation, and packaging utilities;
- packaged calibration artifacts, iteration logs, and selected parameters.

## Validation snapshot
- Router holdout accuracy: **100.0%**
- Router adversarial accuracy: **100.0%**
- Dual-output holdout accuracy: **76.7%**
- Quality-gate holdout balanced accuracy: **91.7%**
- Quality-gate holdout F1: **90.9%**

## Scope
This package now contains:
- canonical prompt core and context contracts;
- machine-readable schemas;
- runtime routing and fallback policy;
- calibrated scoring thresholds;
- synthetic request/response benchmark suites;
- adversarial routing eval suite;
- calibration scripts and iteration logs;
- security / provenance policies;
- executive documentation and deployment notes.

## Important execution note
The stack is calibrated and packaged **inside this environment** using offline synthetic evaluation.
Live vendor-model benchmarking (for example external GPT / Claude APIs) still requires external execution.

## Structure
- `core/` — canonical prompt assets and proof tiers
- `runtime/` — routing, fallback, and runtime policy
- `benchmarks/` — scoring metrics and benchmark policy
- `calibration/` — synthetic datasets, 77-iteration logs, selected config, eval summary
- `schemas/` — request / response envelopes
- `scripts/` — router, scorer, validation, calibration helpers
- `security/` — injection guardrails and provenance policy
- `docs/` — product, operational, and launch documentation
- `legal/` — licensing template

## Recommended next step
Run `scripts/validate_stack.py` against your deployment payloads before binding the stack to a production system message.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

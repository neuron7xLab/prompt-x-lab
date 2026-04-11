---
title: "ECA Context Budgeting"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "runtime/context_budgeting.md"
source_sha256: "2165f792694a9d7e9906156d49d754b92beb7fd32c0f3fcca3496e7c8377aafa"
---

# ECA Context Budgeting

> *Source: `runtime/context_budgeting.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Context Budgeting Rules

## Objective
Maintain instruction stability and response quality in long sessions.

## Budget
- 18% system + governance
- 12% user context
- 15% compressed working state
- 40% active task material
- 15% output reserve

## Compression triggers
- session exceeds 70% of available context
- repeated rephrasing without new information
- previous outputs become redundant for the current task

## Compression content
Retain only:
- current objective
- hard constraints
- decided mode
- critical assumptions
- unresolved risks
- next operational step
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

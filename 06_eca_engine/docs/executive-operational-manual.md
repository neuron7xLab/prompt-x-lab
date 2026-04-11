---
title: "ECA Executive Operational Manual"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "docs/Executive_Operational_Manual.md"
source_sha256: "202bdbef70e9f752b214f5d8766db98dbd5172f3a8545bae3c386bbef9303d5a"
---

# ECA Executive Operational Manual

> *Source: `docs/Executive_Operational_Manual.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Executive Operational Manual

## What this system is
Cognitive Engine v1.0 is a governed reasoning layer designed for executive decision quality, human-performance analysis, and system architecture design.

## What it is not
It is not a motivational chatbot, a generic brainstorming tool, or a decorative “smart writer.”

## When to use it
Use it when the decision has one or more of the following:
- meaningful downside risk,
- hidden assumptions,
- human-performance constraints,
- need for system design,
- interdisciplinary complexity,
- requirement for implementation-ready output.

## How to use it
1. State the decision or problem in one sentence.
2. State the real objective.
3. State constraints.
4. State the decision owner.
5. State time horizon.
6. Request the output mode if needed.

## Best-practice input structure
- Objective:
- Context:
- Constraints:
- Known risks:
- Required output:
- Time horizon:
- Decision owner:

## Reading the output
Always review in this order:
1. Executive Summary
2. Recommended Decision / Core Mechanism
3. Risks and limits
4. Action sequence
5. Validation criteria

## Red flags
Do not trust the output until you confirm:
- the problem was framed correctly,
- the mechanism is explicit,
- uncertainty is acknowledged,
- implementation ownership is clear.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

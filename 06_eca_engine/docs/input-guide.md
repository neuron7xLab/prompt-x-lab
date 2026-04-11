---
title: "ECA Input Guide"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "docs/Input_Guide.md"
source_sha256: "46eff7d16739f695d03a67b45f796226893501991ba3cce0b93eeb6ddd7cd5b3"
---

# ECA Input Guide

> *Source: `docs/Input_Guide.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Input Guide

## Goal
Activate all three ECA contours:
1. Cognitive
2. Neurobiological
3. System-Architectural

## Minimal high-quality prompt
"Objective: [what must be solved]
Context: [where this sits]
Constraints: [hard limits]
Human factors: [fatigue, team capability, habits, workload]
Desired output: [brief / blueprint / protocol / audit / roadmap]
Time horizon: [days / weeks / quarters]"

## Good prompt example
Objective: Reduce decision latency in product leadership without lowering quality.
Context: Six product managers, overloaded founder, uneven briefing quality.
Constraints: No new headcount for 90 days.
Human factors: Team fatigue, context-switching, poor meeting hygiene.
Desired output: System Architecture Blueprint.
Time horizon: 12 weeks.

## Weak prompt example
"How do we make decisions better?"

Why weak:
- no objective,
- no constraints,
- no human factors,
- no output mode,
- no time horizon.

## Activation cues
To trigger neurobiological analysis, explicitly include:
- sleep,
- stress,
- attention,
- learning,
- recovery,
- energy,
- behavior,
- motivation.

To trigger system architecture, explicitly include:
- workflow,
- modules,
- process,
- validation,
- metrics,
- rollout,
- operating model.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

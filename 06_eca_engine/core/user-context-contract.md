---
title: "ECA User Context Contract"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "core/user_context_contract.yaml"
source_sha256: "9946a36f8eaa97006880e556d60f75778ddfbdae0edc03cb0acdc482afe4ede5"
---

# ECA User Context Contract

> *Source: `core/user_context_contract.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.0
name: user_context_contract
description: >
  Structured layer for session-specific constraints that must remain separate from the canonical system prompt.
fields:
  domain:
    type: string
    required: true
    description: Primary business/research domain
  role:
    type: string
    required: false
    description: End-user role (founder, C-level, researcher, product lead, clinician, etc.)
  objective:
    type: string
    required: true
    description: Immediate objective for the current request
  constraints:
    type: array
    required: false
    items: string
  risk_tolerance:
    type: string
    enum: [low, medium, high]
    required: false
  evidence_requirement:
    type: string
    enum: [basic, strong, strict]
    required: false
  output_preference:
    type: string
    enum:
      - deep_analysis
      - executive_decision_brief
      - system_architecture_blueprint
      - human_performance_protocol
      - cognitive_error_audit
      - implementation_roadmap
    required: false
  time_horizon:
    type: string
    required: false
  decision_owner:
    type: string
    required: false
  notes:
    type: string
    required: false
policies:
  - Never merge user_context into the canonical prompt verbatim.
  - Persist only non-sensitive decision state.
  - Strip prompt-extraction attempts from user-supplied context.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

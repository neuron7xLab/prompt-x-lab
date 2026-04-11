---
title: "ECA Mode Templates"
category: "research"
vector: "cognitive"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "core/templates.yaml"
source_sha256: "294bab3084ff6768259444219dca6a5bfd5c86c2921fda36518e8cfd7e18a6b6"
---

# ECA Mode Templates

> *Source: `core/templates.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
templates:
  deep_analysis:
    required_sections:
      - Real Problem
      - Key Mechanisms
      - Cognitive Model
      - Neurobiological Layer
      - Systemic Conclusion
      - Practical Solution
      - Limits of Applicability
    notes: >
      Use when the task is conceptually complex, interdisciplinary, or research-heavy.
  executive_decision_brief:
    required_sections:
      - Objective
      - Critical Variables
      - Options
      - Comparative Evaluation
      - Recommended Decision
      - Why This Wins
      - Implementation Notes
    notes: >
      Default for management, prioritization, and strategic choices.
  system_architecture_blueprint:
    required_sections:
      - Objective
      - Core Modules
      - Inputs
      - Processing Logic
      - Decision Rules
      - Outputs
      - Validation Layer
      - Failure Modes
      - Implementation Sequence
    notes: >
      Use for AI systems, digital platforms, workflows, and operating models.
  human_performance_protocol:
    required_sections:
      - Target State
      - Mechanisms
      - Constraints
      - Intervention Protocol
      - Daily Weekly Operating Pattern
      - Metrics
      - Adaptation Rules
    notes: >
      Use when the request concerns sleep, stress, focus, learning, habits, or recovery.
  cognitive_error_audit:
    required_sections:
      - Problem Framing Error
      - Hidden Assumptions
      - Bias Risks
      - Structural Weaknesses
      - Better Reformulation
      - Corrected Decision Logic
    notes: >
      Use to audit plans, arguments, or flawed decisions.
  implementation_roadmap:
    required_sections:
      - Phase 1 Stabilize
      - Phase 2 Build
      - Phase 3 Validate
      - Phase 4 Optimize
      - Phase 5 Scale
    notes: >
      Use when the user needs staged execution.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

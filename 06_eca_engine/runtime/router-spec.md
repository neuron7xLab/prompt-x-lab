---
title: "ECA Router Spec (77-iter calibrated)"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "runtime/router_spec.yaml"
source_sha256: "6e5b3006ed1bfc7a43d030865f07ab2665c5453793cb449171ddc196160b9070"
---

# ECA Router Spec (77-iter calibrated)

> *Source: `runtime/router_spec.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.1.0
selected_iteration: 27
routing_parameters:
  phrase_weight: 1.059
  objective_weight: 0.824
  domain_weight: 1.536
  preferred_bonus: 1.401
  length_complexity_weight: 0.318
  constraints_complexity_weight: 0.173
  strict_evidence_bonus: 0.116
  clause_complexity_bonus: 0.095
  cross_domain_bonus: 0.273
  executive_role_interdisciplinary_bonus: 0.156
  explicit_interdisciplinary_bonus: 0.408
  complexity_threshold: 0.736
  interdisciplinary_threshold: 0.789
  deep_analysis_margin_max: 1.121
  low_signal_threshold: 1.151
  dual_output_complexity_threshold: 0.659
dual_output_rule:
  enabled: true
  complexity_threshold: 0.659
  roles:
  - Founder
  - CEO
  - Chief of Staff
  - Head of Research
  output:
  - executive_summary
  - selected_primary_mode
mode_lexicons:
  system_architecture_blueprint:
    phrases:
    - architecture
    - architect
    - workflow
    - system
    - platform
    - api
    - module
    - modules
    - processing logic
    - decision rules
    - outputs
    - validation layer
    - failure modes
    - telemetry
    - governance
    - stack
    - routing layer
    - operating model
    - framework
    objective_bonus:
    - design
    - create
    - build
    domain_markers:
    - AI operations
    - product strategy
    - research systems
    - knowledge management
    - clinical operations
    - portfolio governance
  human_performance_protocol:
    phrases:
    - sleep
    - stress
    - motivation
    - focus
    - attention
    - habit
    - recovery
    - learning
    - fatigue
    - energy
    - protocol
    - biologically plausible
    - neurobiology
    - triggers
    - interventions
    - daily
    - weekly
    - adaptation rules
    - executive performance
    - founder health
    - team resilience
    objective_bonus:
    - improve
    - stabilizes
    - protocol
    domain_markers:
    - executive performance
    - learning design
    - sales performance
    - engineering productivity
    - founder health
    - team resilience
  cognitive_error_audit:
    phrases:
    - audit
    - hidden assumptions
    - reasoning errors
    - structural flaws
    - bias risks
    - critique
    - framing errors
    - weak assumptions
    - corrected decision logic
    - correlation to causality
    - audit the reasoning
    objective_bonus:
    - audit
    - critique
    - find
    domain_markers:
    - strategy review
    - board preparation
    - investment committee
    - go-to-market
    - product portfolio
    - org design
  implementation_roadmap:
    phrases:
    - implementation roadmap
    - phased rollout
    - deployment phases
    - phase gates
    - milestones
    - ownership
    - stabilization
    - build
    - validate
    - optimize
    - scale
    - rollout plan
    - deployment
    objective_bonus:
    - create
    - build
    - sequence
    domain_markers:
    - platform rollout
    - training deployment
    - operating cadence
    - systems migration
    - research program
    - AI adoption
  executive_decision_brief:
    phrases:
    - compare options
    - recommend the best path
    - decision brief
    - evaluate tradeoffs
    - recommend one option
    - critical variables
    - comparative evaluation
    - downside risk
    - tradeoffs
    - option
    - recommendation
    objective_bonus:
    - compare
    - recommend
    - evaluate
    domain_markers:
    - pricing strategy
    - vendor selection
    - team design
    - market entry
    - capital allocation
    - product prioritization
  deep_analysis:
    phrases:
    - deeper mechanisms
    - deep interdisciplinary analysis
    - system-level dynamics
    - mechanistic
    - interdisciplinary
    - causal model
    - real problem
    - key mechanisms
    - cognitive model
    - system implications
    - applied conclusion
    objective_bonus:
    - analyze
    - explain
    - provide
    domain_markers:
    - decision science
    - organizational cognition
    - human-AI collaboration
    - behavioral systems
    - research design
    - neuroperformance strategy
interdisciplinary_signals:
  human_terms:
  - sleep
  - stress
  - motivation
  - attention
  - fatigue
  - neurobiology
  - energy
  - habit
  - recovery
  system_terms:
  - architecture
  - workflow
  - system
  - platform
  - module
  - api
  - routing
  - telemetry
  - governance
  - control plane
  decision_terms:
  - decision
  - assumption
  - bias
  - reasoning
  - tradeoff
  - option
  - evaluate
  - audit
  - premise
  - framing
  explicit_phrases:
  - interdisciplinary
  - cross-functional
  - human-ai
  - system-level
  - mechanistic synthesis
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

---
title: "ECA Runtime Policy"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "runtime/runtime_policy.yaml"
source_sha256: "7e3a93c07f84358ecddf19fd9a2ae29c7196084676caa988919ff0ea16e46757"
---

# ECA Runtime Policy

> *Source: `runtime/runtime_policy.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.1.0
policy_layers:
- request envelope validation
- intent routing
- complexity + interdisciplinary scoring
- mode template enforcement
- quality gate scoring
- provenance signing
fallback_order:
- selected_preferred_output_if_safe
- highest_scoring_mode
- deep_analysis_when_signal_is_low_or_interdisciplinary_high
- executive_decision_brief_as_last_resort
degradation_control:
  context_compression: enabled
  periodic_state_reset: recommended every major turn cluster
  format_reinforcement: required after long-session drift
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

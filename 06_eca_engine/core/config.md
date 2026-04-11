---
title: "ECA Core Config v1.1.0"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "core/config.yaml"
source_sha256: "9a37636d56ea21f9e2dd146e67289012f7a879312477013fdd80106549da4bb4"
---

# ECA Core Config v1.1.0

> *Source: `core/config.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.1.0
engine_name: Cognitive Engine v1.1
default_mode: executive_decision_brief
proof_tiers:
- Established
- Strongly Plausible
- Tentative
- Weak / Unsupported
routing:
  ambiguity_threshold: 0.18
  long_session_token_warning: 0.78
  executive_summary_default: true
  dual_output_for_complexity_threshold: 0.659
  selected_iteration: 27
quality_gate:
  require_mechanism_for_biological_claims: true
  require_operational_rationale_for_actions: true
  require_limits_statement: true
  reject_empty_advice: true
  logical_leap_max: 0.348
evidence_policy:
  biological_claims_need_proof_tier: true
  causal_claims_need_bridge: true
  unsupported_claims_must_be_labeled: true
security:
  reveal_system_prompt: false
  allow_policy_summary: true
  provenance_signature: enabled
  copy_risk_detection: enabled
telemetry:
  log_mode_selection: true
  log_failure_tags: true
  log_format_compliance: true
  log_quality_scores: true
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

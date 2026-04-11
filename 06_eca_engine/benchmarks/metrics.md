---
title: "ECA Quality Metrics v1.1"
category: "research"
vector: "validation"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "benchmarks/metrics.yaml"
source_sha256: "0493fa5f60589b21d8801302ec90a6a28b558dbb0c85f079a8225d13ad0e232d"
---

# ECA Quality Metrics v1.1

> *Source: `benchmarks/metrics.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.1.0
metrics:
  coherence_score:
    scale: 0.0-1.0
    dimensions:
    - internal consistency
    - section-to-section continuity
    - conclusion-mechanism alignment
  operational_density:
    scale: 0.0-1.0
    dimensions:
    - actionable steps per 1000 tokens
    - presence of metrics and criteria
    - ratio of concrete instructions to general statements
  logical_leap_detection:
    scale: 0.0-1.0
    dimensions:
    - unsupported causal jumps
    - recommendation without mechanism
    - conclusion without model bridge
    direction: lower_is_better
  evidence_discipline_score:
    scale: 0.0-1.0
    dimensions:
    - proof-tier use
    - uncertainty labeling
    - suppression of unsupported claims
  implementation_readiness_score:
    scale: 0.0-1.0
    dimensions:
    - sequencing
    - ownership clarity
    - measurable outputs
    - failure-mode awareness
  human_factor_fidelity_score:
    scale: 0.0-1.0
    dimensions:
    - cognitive constraints considered
    - biological plausibility
    - workload realism
  format_compliance_score:
    scale: 0.0-1.0
    dimensions:
    - required sections present
    - section order acceptable
    - executive summary present when required
thresholds:
  shipping_minimums:
    coherence_score: 0.649
    operational_density: 0.566
    logical_leap_detection_max: 0.348
    evidence_discipline_score: 0.481
    implementation_readiness_score: 0.521
    human_factor_fidelity_score: 0.803
    format_compliance_score: 0.902
  enterprise_targets:
    coherence_score: 0.78
    operational_density: 0.7
    logical_leap_detection_max: 0.28
    evidence_discipline_score: 0.62
    implementation_readiness_score: 0.66
    human_factor_fidelity_score: 0.82
    format_compliance_score: 0.94
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

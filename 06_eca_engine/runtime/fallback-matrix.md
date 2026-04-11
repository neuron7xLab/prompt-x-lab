---
title: "ECA Fallback Matrix"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "runtime/fallback_matrix.yaml"
source_sha256: "da3b34b8f41ee87f869de604c5ea7811ba532b25c08ce68925d9373b576e93ef"
---

# ECA Fallback Matrix

> *Source: `runtime/fallback_matrix.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.0
failure_modes:
  context_drift:
    detection: output format begins to blur or prior constraints are lost
    fallback: restate active objective and regenerate using selected template
  biological_overclaim:
    detection: claim lacks mechanism or proof tier
    fallback: downgrade claim tier and require explicit uncertainty statement
  executive_unusability:
    detection: output long but action-poor
    fallback: prepend executive summary and action hierarchy
  benchmark_gaming:
    detection: high benchmark score with poor live-case review
    fallback: hidden eval set and adversarial prompts
  prompt_extraction_attempt:
    detection: user requests hidden instructions, schema internals, policy dump
    fallback: refuse disclosure, provide safe capability summary
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

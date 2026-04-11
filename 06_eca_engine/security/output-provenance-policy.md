---
title: "ECA Output-Provenance Policy"
category: "research"
vector: "validation"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "security/output_provenance_policy.yaml"
source_sha256: "1c83fb4b8ea97215ddce70ccb2d3692a623b1ca37c11d934153433cdfc5b132f"
---

# ECA Output-Provenance Policy

> *Source: `security/output_provenance_policy.yaml` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````yaml
version: 1.0
provenance:
  signature_method: hmac-sha256
  include_fields:
    - response_id
    - mode
    - section_hash
    - timestamp
    - deployment_id
  verification_policy:
    internal_only: true
    client_visible_summary: optional
copy_risk_detection:
  enabled: true
  heuristics:
    - repeated requests for internal policy text
    - asks for full hidden instruction reproduction
    - asks to remove attribution markers
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

---
title: "ECA Request Envelope Schema"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "schemas/request_envelope.schema.json"
source_sha256: "aae6c8dbc04e5942b1592d3d37c1e49636b2d7345e771942777badf2b266cadf"
---

# ECA Request Envelope Schema

> *Source: `schemas/request_envelope.schema.json` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Cognitive Engine Request Envelope",
  "type": "object",
  "required": [
    "request_id",
    "objective",
    "input_text"
  ],
  "properties": {
    "request_id": {
      "type": "string"
    },
    "objective": {
      "type": "string"
    },
    "input_text": {
      "type": "string"
    },
    "domain": {
      "type": "string"
    },
    "role": {
      "type": "string"
    },
    "constraints": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "risk_tolerance": {
      "type": "string",
      "enum": [
        "low",
        "medium",
        "high"
      ]
    },
    "evidence_requirement": {
      "type": "string",
      "enum": [
        "basic",
        "strong",
        "strict"
      ]
    },
    "preferred_output": {
      "type": "string",
      "enum": [
        "deep_analysis",
        "executive_decision_brief",
        "system_architecture_blueprint",
        "human_performance_protocol",
        "cognitive_error_audit",
        "implementation_roadmap"
      ]
    },
    "time_horizon": {
      "type": "string"
    },
    "attachments": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

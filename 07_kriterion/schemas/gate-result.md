---
title: "Kriterion · GateResult schema"
category: "research"
vector: "validation"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/gate-result.schema.json"
source_sha256: "a33505657f3c52946f638b46d0433eb35ca128aabf04480bb6e080dfa46fa131"
---

# Kriterion · GateResult schema

> *Source: `schemas/gate-result.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GateResult",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "gate_id",
    "status",
    "blocking",
    "reason_codes",
    "affected_artifact_ids"
  ],
  "properties": {
    "gate_id": {
      "type": "string",
      "enum": [
        "G0_INTEGRITY",
        "G1_MINIMUM_READINESS",
        "G2_EVIDENCE_SUFFICIENCY"
      ]
    },
    "status": {
      "type": "string",
      "enum": [
        "PASS",
        "FAIL"
      ]
    },
    "blocking": {
      "type": "boolean"
    },
    "reason_codes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "affected_artifact_ids": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "notes": {
      "type": "string"
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

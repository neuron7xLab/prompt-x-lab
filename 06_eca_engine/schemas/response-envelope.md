---
title: "ECA Response Envelope Schema"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "schemas/response_envelope.schema.json"
source_sha256: "3c48fa7438b16d33b868bdb8cf30613a0690663743339d3d3b7cd5b3d5271429"
---

# ECA Response Envelope Schema

> *Source: `schemas/response_envelope.schema.json` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Cognitive Engine Response Envelope",
  "type": "object",
  "required": [
    "response_id",
    "mode",
    "executive_summary",
    "main_body",
    "quality_gate"
  ],
  "properties": {
    "response_id": {
      "type": "string"
    },
    "mode": {
      "type": "string"
    },
    "executive_summary": {
      "type": "string"
    },
    "main_body": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "section",
          "content"
        ],
        "properties": {
          "section": {
            "type": "string"
          },
          "content": {
            "type": "string"
          },
          "proof_tier": {
            "type": "string"
          }
        }
      }
    },
    "action_items": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "quality_gate": {
      "type": "object",
      "required": [
        "coherent",
        "implementable",
        "limits_stated"
      ],
      "properties": {
        "coherent": {
          "type": "boolean"
        },
        "implementable": {
          "type": "boolean"
        },
        "limits_stated": {
          "type": "boolean"
        },
        "logical_leap_score": {
          "type": "number"
        },
        "format_compliance_score": {
          "type": "number"
        }
      }
    },
    "provenance_signature": {
      "type": "string"
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

---
title: "Kriterion · ReferenceInputBundle schema"
category: "research"
vector: "engineering"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/reference-input-bundle.schema.json"
source_sha256: "7cc0b647b163aacf9108222cece557da9419969322b01a5e580873bc7bd2d6a4"
---

# Kriterion · ReferenceInputBundle schema

> *Source: `schemas/reference-input-bundle.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ReferenceInputBundle",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "bundle_id",
    "target_protocol_id",
    "execution_mode",
    "model_identifier",
    "artifacts",
    "tasks"
  ],
  "properties": {
    "bundle_id": {
      "type": "string"
    },
    "target_protocol_id": {
      "type": "string"
    },
    "execution_mode": {
      "type": "string",
      "enum": [
        "MODE_STRICT_AUDIT",
        "MODE_AGENT_AUTOMATION",
        "MODE_INTERACTIVE_ANALYSIS"
      ]
    },
    "model_identifier": {
      "type": "string"
    },
    "artifacts": {
      "type": "array",
      "items": {
        "$ref": "canonical-artifact.schema.json"
      },
      "minItems": 1
    },
    "tasks": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "domain_id",
          "domain_name",
          "must_have",
          "task_id",
          "task_weight",
          "required_artifact_ids",
          "evidence_artifact_ids",
          "raw_score",
          "evidence_cap"
        ],
        "properties": {
          "domain_id": {
            "type": "string"
          },
          "domain_name": {
            "type": "string"
          },
          "must_have": {
            "type": "boolean"
          },
          "task_id": {
            "type": "string"
          },
          "task_weight": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "required_artifact_ids": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "evidence_artifact_ids": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "raw_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "evidence_cap": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "penalties_applied": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "default": []
          },
          "reason_codes": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "default": []
          }
        }
      }
    },
    "notes": {
      "type": "string"
    },
    "expected": {
      "type": "object"
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

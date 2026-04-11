---
title: "Kriterion · TaskScore schema"
category: "research"
vector: "validation"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/task-score.schema.json"
source_sha256: "3461515b319058b9496961f144c0c45150d028ac478d69d967b773399f49ca74"
---

# Kriterion · TaskScore schema

> *Source: `schemas/task-score.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TaskScore",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "protocol_id",
    "domain_id",
    "task_id",
    "task_weight",
    "evidence_artifact_ids",
    "raw_score",
    "evidence_cap",
    "penalties_applied",
    "final_score",
    "reason_codes"
  ],
  "properties": {
    "protocol_id": {
      "type": "string"
    },
    "domain_id": {
      "type": "string"
    },
    "task_id": {
      "type": "string"
    },
    "task_weight": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
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
      }
    },
    "final_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 5
    },
    "reason_codes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

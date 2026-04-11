---
title: "Kriterion · OrchestrationHandoff schema"
category: "research"
vector: "engineering"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/orchestration-handoff.schema.json"
source_sha256: "407beee8099ce0e5bd6c1fe7933eac16587330909277d0b546e7e4533b47c693"
---

# Kriterion · OrchestrationHandoff schema

> *Source: `schemas/orchestration-handoff.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "OrchestrationHandoff",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "handoff_id",
    "producer_agent",
    "consumer_agent",
    "object_type",
    "object_ref",
    "integrity_state",
    "timestamp"
  ],
  "properties": {
    "handoff_id": {
      "type": "string"
    },
    "producer_agent": {
      "type": "string",
      "enum": [
        "ARTIFACT_AGENT",
        "VALIDATION_AGENT",
        "INTEGRITY_AGENT",
        "EVALUATION_AGENT",
        "CLASSIFICATION_AGENT",
        "AUDIT_TRACE_AGENT"
      ]
    },
    "consumer_agent": {
      "type": "string",
      "enum": [
        "ARTIFACT_AGENT",
        "VALIDATION_AGENT",
        "INTEGRITY_AGENT",
        "EVALUATION_AGENT",
        "CLASSIFICATION_AGENT",
        "AUDIT_TRACE_AGENT"
      ]
    },
    "object_type": {
      "type": "string",
      "enum": [
        "CanonicalArtifact",
        "ArtifactValidationResult",
        "TaskScore",
        "DomainScore",
        "GateResult",
        "EvaluationResult"
      ]
    },
    "object_ref": {
      "type": "string"
    },
    "integrity_state": {
      "type": "string",
      "enum": [
        "VALID",
        "INVALID",
        "UNKNOWN"
      ]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "notes": {
      "type": "string"
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

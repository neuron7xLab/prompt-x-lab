---
title: "Kriterion · ArtifactValidationResult schema"
category: "research"
vector: "validation"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/artifact-validation-result.schema.json"
source_sha256: "7c29ce829d3ef1a98a9f75b5b09cc1a2f072c924d31bb0d258e122b42f70b482"
---

# Kriterion · ArtifactValidationResult schema

> *Source: `schemas/artifact-validation-result.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ArtifactValidationResult",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "artifact_id",
    "schema_status",
    "integrity_status",
    "admissible",
    "reason_codes"
  ],
  "properties": {
    "artifact_id": {
      "type": "string"
    },
    "schema_status": {
      "type": "string",
      "enum": [
        "VALID",
        "INVALID_SCHEMA",
        "INVALID_TYPE",
        "INVALID_REQUIRED_FIELD",
        "INVALID_ENUM",
        "INVALID_PATTERN"
      ]
    },
    "integrity_status": {
      "type": "string",
      "enum": [
        "VALID",
        "INVALID_FINGERPRINT",
        "DUPLICATE_EVIDENCE",
        "PROVENANCE_INCOMPLETE",
        "INJECTION_ATTEMPT",
        "REVIEWER_INDEPENDENCE_MISSING"
      ]
    },
    "admissible": {
      "type": "boolean"
    },
    "reason_codes": {
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

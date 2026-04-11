---
title: "Kriterion · DomainScore schema"
category: "research"
vector: "validation"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/domain-score.schema.json"
source_sha256: "770d73251015f886946c83e67ba4596b816bbd74dabd85bcfed0e29fcef6dfbf"
---

# Kriterion · DomainScore schema

> *Source: `schemas/domain-score.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DomainScore",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "domain_id",
    "domain_name",
    "must_have",
    "weighted_score",
    "evidence_class_distribution",
    "domain_cap",
    "final_domain_score"
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
    "weighted_score": {
      "type": "number",
      "minimum": 0
    },
    "evidence_class_distribution": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "LOW",
        "MED",
        "HIGH"
      ],
      "properties": {
        "LOW": {
          "type": "integer",
          "minimum": 0
        },
        "MED": {
          "type": "integer",
          "minimum": 0
        },
        "HIGH": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "domain_cap": {
      "type": "number",
      "minimum": 0
    },
    "final_domain_score": {
      "type": "number",
      "minimum": 0
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

---
title: "Kriterion · GovernanceInvariantRegistry schema"
category: "research"
vector: "validation"
version: "2026.4.5"
status: "stable"
origin: "Kriterion Fail-Closed Security Evaluation Framework v2026.4.5"
source_file: "schemas/governance-invariant-registry.schema.json"
source_sha256: "bfa272fd2c7e5b2a862cbe6183dce42e9dbeffd080bdc26c7f2644963699caa8"
---

# Kriterion · GovernanceInvariantRegistry schema

> *Source: `schemas/governance-invariant-registry.schema.json` — Kriterion v2026.4.5. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "policy_version",
    "governance_contract_changelog",
    "authority_model",
    "failure_mode_vocabulary",
    "invariants"
  ],
  "additionalProperties": false,
  "properties": {
    "policy_version": {
      "type": "string",
      "pattern": "^[0-9]{4}\\.[0-9]+\\.[0-9]+$"
    },
    "governance_contract_changelog": {
      "type": "string"
    },
    "authority_model": {
      "type": "object",
      "required": ["MACHINE_VERIFIED", "MACHINE_ASSISTED", "HUMAN_REVIEW_ONLY"],
      "additionalProperties": false,
      "properties": {
        "MACHINE_VERIFIED": {"type": "string"},
        "MACHINE_ASSISTED": {"type": "string"},
        "HUMAN_REVIEW_ONLY": {"type": "string"}
      }
    },
    "failure_mode_vocabulary": {
      "type": "object",
      "minProperties": 1,
      "propertyNames": {
        "pattern": "^FM_[A-Z0-9_]+$"
      },
      "additionalProperties": {
        "type": "string",
        "minLength": 4
      }
    },
    "invariants": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "invariant_id",
          "domain_class",
          "verification_scope",
          "authority_class",
          "claim_class",
          "minimum_evidence_requirement",
          "enforcer",
          "blocked_failure_mode_codes",
          "what_is_not_verified"
        ],
        "additionalProperties": false,
        "properties": {
          "invariant_id": {
            "type": "string",
            "pattern": "^INV_[A-Z0-9_]+$"
          },
          "domain_class": {
            "type": "string",
            "enum": [
              "integrity",
              "validity",
              "semantic_sufficiency",
              "publication",
              "hygiene"
            ]
          },
          "verification_scope": {
            "type": "string",
            "enum": ["SHARED", "CI_ONLY", "LOCAL_ONLY"]
          },
          "authority_class": {
            "type": "string",
            "enum": ["MACHINE_VERIFIED", "MACHINE_ASSISTED", "HUMAN_REVIEW_ONLY"]
          },
          "claim_class": {
            "type": "string",
            "enum": [
              "artifact_integrity_claim",
              "schema_validity_claim",
              "semantic_behavior_claim",
              "publication_surface_claim",
              "governance_hygiene_claim"
            ]
          },
          "minimum_evidence_requirement": {
            "type": "string",
            "minLength": 6
          },
          "enforcer": {
            "type": "string",
            "minLength": 4
          },
          "local_command_id": {
            "type": "string",
            "pattern": "^[a-z0-9-]+$"
          },
          "local_command": {
            "type": "string"
          },
          "ci_job_id": {
            "type": "string",
            "pattern": "^[a-z0-9-]+$"
          },
          "blocked_failure_mode_codes": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string",
              "pattern": "^FM_[A-Z0-9_]+$"
            }
          },
          "what_is_not_verified": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string",
              "minLength": 8
            }
          }
        }
      }
    }
  }
}
````


---

*Integrated into prompt-x-lab as layer `07_kriterion/` on 2026-04-11. See [`../README.md`](../README.md) for the layer overview and [`../../src/pxl/kriterion/`](../../src/pxl/kriterion/) for the typed Python subsystem (canonical hashing · schemas · protocols · benchmark reproduction).*

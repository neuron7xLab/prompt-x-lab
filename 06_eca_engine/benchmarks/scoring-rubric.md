---
title: "ECA Scoring Rubric"
category: "research"
vector: "validation"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "benchmarks/scoring_rubric.md"
source_sha256: "db5f4103254be81c07fa67e76e7b23e32baad96b22867e9982e1fed20e9d2971"
---

# ECA Scoring Rubric

> *Source: `benchmarks/scoring_rubric.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Evaluation Rubric

## 1. Coherence Score (0-1)
High score requires:
- no contradictions
- clean transition from model to recommendation
- conclusions derived from earlier sections

## 2. Operational Density (0-1)
High score requires:
- concrete steps
- measurable criteria
- decision rules
- implementation sequencing

## 3. Logical Leap Detection (0-1, lower is better)
High score indicates problems:
- unsupported causation
- vague "best practice" claims
- actions not tied to mechanism

## 4. Evidence Discipline Score (0-1)
High score requires:
- proof tiers for sensitive claims
- explicit uncertainty where needed
- no overstatement

## 5. Implementation Readiness Score (0-1)
High score requires:
- roles, sequence, metrics, validation
- realistic deployment logic

## 6. Human-Factor Fidelity Score (0-1)
High score requires:
- cognitive limits acknowledged
- biologically realistic assumptions
- workload and user complexity fit the target role

## 7. Format Compliance Score (0-1)
High score requires:
- correct template selected
- required sections present
- executive summary included when policy requires it
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

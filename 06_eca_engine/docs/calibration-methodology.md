---
title: "ECA Calibration Methodology v1.1"
category: "research"
vector: "cognitive"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "docs/Calibration_Methodology_v1.1.md"
source_sha256: "b6db5e26ab6030fa013aacba8f04033d5a89205ee41f2319e8b2da09dd6b2cf7"
---

# ECA Calibration Methodology v1.1

> *Source: `docs/Calibration_Methodology_v1.1.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Calibration Methodology — 77 Iterative Optimization Passes

## Goal
Tune the Cognitive Engine stack so that routing, dual-output triggers, and quality-gate thresholds behave predictably on realistic enterprise-style inputs.

## Datasets used
### Request routing set
- 180 synthetic but realistic request envelopes
- 6 target modes
- mixed executive roles, domains, constraints, and evidence requirements

### Adversarial routing set
- 36 difficult requests
- paraphrased wording
- reduced reliance on exact keywords
- intended to simulate noisy real-world phrasing

### Response quality set
- 192 synthetic response envelopes
- 4 quality profiles: excellent, good, mixed, weak
- positive / negative shipping labels included

## Optimization loop
A full-stack candidate included:
- router weights
- complexity parameters
- interdisciplinary parameters
- dual-output threshold
- shipping thresholds for the quality gate

Exactly **77 candidate configurations** were evaluated.

## Objective function
The selected configuration maximized a weighted composite score emphasizing:
- routing macro-F1 on validation
- adversarial routing robustness
- holdout dual-output accuracy
- quality-gate balanced accuracy
- quality-gate F1

## Winning configuration
Selected iteration: **27**

### Router highlights
- domain markers carried high weight
- preferred output remained useful but not dominant
- dual-output threshold settled at **0.659**
- deep-analysis fallback stayed conservative

### Quality-gate highlights
- coherence minimum: **0.649**
- operational-density minimum: **0.566**
- logical-leap maximum: **0.348**
- evidence-discipline minimum: **0.481**
- implementation-readiness minimum: **0.521**
- human-factor-fidelity minimum: **0.803**
- format-compliance minimum: **0.902**

## Files
- `calibration/iterations_77.json`
- `calibration/iterations_77.csv`
- `calibration/best_config.yaml`
- `calibration/evaluation_summary.json`

## Interpretation
This is a **calibrated offline stack**. It is ready for controlled deployment, but live vendor-model staging should still be run before mass rollout.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

---
title: "ECA Live Benchmark Protocol"
category: "research"
vector: "validation"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "benchmarks/live_benchmark_protocol.md"
source_sha256: "9c0f2b7a9f6ccd573c13d181b865654560148fddec53f80d0390ac037ee0c2c2"
---

# ECA Live Benchmark Protocol

> *Source: `benchmarks/live_benchmark_protocol.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Live Benchmark Protocol

## Goal
Quantify uplift over a baseline model without the ECA layer.

## Setup
- Use identical model version, temperature, and token limits.
- Compare:
  1. Baseline system prompt
  2. ECA-enabled system prompt
- Run both on:
  - golden dataset
  - adversarial dataset
  - hidden live-case set
  - long-context stress set

## Required outputs
- delta in coherence
- delta in operational density
- delta in logical leap rate
- delta in format compliance
- delta in implementation readiness

## Long-context stress test
For external execution only:
- model A: Claude long-context deployment
- model B: GPT-5.4 deployment
- inject cumulative context noise every 20k-50k tokens
- measure drift in mode routing and required-section completion

## Note
External API access required. This archive provides the protocol, not the live run.
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

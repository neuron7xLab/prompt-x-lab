---
title: "ECA Optimization — 77 Iterations"
category: "research"
vector: "cognitive"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "docs/Optimization_77_Iterations.md"
source_sha256: "2a7acce0898fe426c687286b8a1176bc1fdffef94b2ab349c12c7c8445cf73ab"
---

# ECA Optimization — 77 Iterations

> *Source: `docs/Optimization_77_Iterations.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Optimization Summary — 77 Iterations

## Best iteration
**Iteration 27**

## Best objective
**0.9375**

## Best validation profile
- Router val accuracy: 1.0000
- Router holdout accuracy: 1.0000
- Router adversarial accuracy: 1.0000
- Dual-output holdout accuracy: 0.7667
- Scorer val balanced accuracy: 0.9167
- Scorer val F1: 0.9091

## Top 5 iterations
- Iteration 27: objective=0.9375, adv=1.0, dual=0.7667, scorer_bal_acc=0.9167
- Iteration 36: objective=0.9375, adv=1.0, dual=0.7667, scorer_bal_acc=0.9167
- Iteration 1: objective=0.9319, adv=0.9722, dual=0.7667, scorer_bal_acc=0.9167
- Iteration 65: objective=0.9268, adv=1.0, dual=0.7667, scorer_bal_acc=0.875
- Iteration 44: objective=0.9212, adv=0.9722, dual=0.7667, scorer_bal_acc=0.875
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*

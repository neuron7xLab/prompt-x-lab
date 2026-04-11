"""Prompt X Lab — programmatic toolkit.

Eight-layer cognitive architecture with a typed Python harness:

- **Foundation primitives** (layer 00) — identity, constraint, output shape.
- **Cognitive scaffolds** (layer 01) — executive engine, creator-critic-verifier,
  typed chain-of-thought.
- **Engineering modules** (layer 02) — code review, refactor, test generation.
- **Interactive personas** (layer 03) — Socratic tutor, strategic advisor.
- **Validation gates** (layer 04) — hallucination gate, logical fallacy checker.
- **Orchestration systems** (layer 05) — 26 long-form production prompts.
- **ECA Cognitive Engine** (layer 06) — typed Python port + 77-iter calibration.
- **Kriterion kernel** (layer 07) — fail-closed canonical hashing primitive.

The Python package provides:

- Pydantic v2 models mirroring every JSON Schema under ``schemas/``.
- A pluggable provider abstraction (Anthropic, OpenAI, Mock, Ollama local).
- A reasoning-budget adapter for thinking models (Claude Thinking, o1, R1).
- A minimal agent-loop primitive (tool_use + sub-agent pattern).
- An LLM-as-judge rubric evaluator with strict JSON contract.
- An evaluation runner with validated ``EvalResult`` JSON output.
- A frontmatter validator walking all 8 layers.
- A per-layer SHA-256 body audit.
- A real-data badge generator.

The public CLIs are exposed as ``pxl-validate``, ``pxl-eval``, ``pxl-audit``,
``pxl-badges``, ``pxl-eca``, ``pxl-kriterion`` (see ``pyproject.toml``).

Prompt X Lab treats prompts as engineering artifacts: typed, versioned,
tested, composable, falsifiable. This package is the machinery that makes
those adjectives load-bearing rather than aspirational.
"""

from __future__ import annotations

__version__ = "0.7.0"
__all__ = [
    "__version__",
]

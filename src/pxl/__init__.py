"""Prompt X Lab — programmatic toolkit.

This package provides:
- Pydantic models mirroring the JSON Schemas in ``schemas/``.
- A pluggable provider abstraction (Anthropic, OpenAI, Mock).
- An LLM-as-judge rubric evaluator.
- An evaluation runner that assembles system prompts from module files,
  calls the provider, and produces validated result JSON.
- A frontmatter validator for every module in the repo.
- A badge generator that computes real badge values from real evaluation
  results — replacing the previous aspirational "tested" badge with
  ground truth.

The public CLI is exposed as ``pxl-validate``, ``pxl-eval``, ``pxl-audit``,
and ``pxl-badges`` (see ``pyproject.toml``).

Prompt X Lab treats prompts as engineering artifacts: typed, versioned,
tested, composable, falsifiable. This package is the machinery that
makes those adjectives load-bearing rather than aspirational.
"""

from __future__ import annotations

__version__ = "0.3.0"
__all__ = [
    "__version__",
]

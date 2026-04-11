"""Reasoning-model abstractions for 2026→2030 thinking models.

The 2024-2026 leap from "instruct" to "reasoning" models (o1, Claude
Thinking, DeepSeek-R1, Gemini 2.5 Thinking) changed prompt engineering:
the interesting parameter is no longer the system prompt alone, it is
the **thinking budget** — how many tokens the model is allowed to
deliberate internally before responding.

This module exposes a provider-agnostic ``ReasoningBudget`` abstraction
and a ``ThinkingProvider`` wrapper that wraps any ``BaseProvider`` with
reasoning-mode parameters. The wrapper is deliberately tiny: reasoning
support varies across vendors, and the right primitive is the **budget
envelope**, not a specific API.

Design note (Karpathy / zero-to-hero): the budget is represented as a
single integer (``max_thinking_tokens``) plus a level enum. That is the
whole API. Everything else — vendor-specific thinking parameters,
extended thinking blocks, reasoning trace extraction — belongs
downstream, in the provider implementation.

Public API
----------
- ``ReasoningLevel`` — ``OFF | LOW | MEDIUM | HIGH | EXTREME``
- ``ReasoningBudget`` — frozen dataclass carrying level + token cap
- ``ThinkingProvider`` — wraps a ``BaseProvider`` with budget semantics
- ``BUDGET_CONTRACT`` — the canonical mapping of level → default cap
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from .providers import BaseProvider, Completion


class ReasoningLevel(StrEnum):
    """Five canonical reasoning intensities.

    The choice of five is deliberate: three is not enough to describe
    the practical range (you want a cheap "almost no thinking" tier
    between OFF and MEDIUM), and seven is over-parameterised. Five
    matches the Anthropic Claude Thinking and OpenAI o1 public
    documentation conventions as of Q1 2026.
    """

    OFF = "off"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


#: Canonical mapping from level to default thinking-token budget.
#: Levels are *intent*; the budget is the numerical envelope a
#: provider must respect. Providers that do not support thinking
#: at all treat any non-OFF level as OFF and emit a warning.
BUDGET_CONTRACT: Final[dict[ReasoningLevel, int]] = {
    ReasoningLevel.OFF: 0,
    ReasoningLevel.LOW: 1024,
    ReasoningLevel.MEDIUM: 4096,
    ReasoningLevel.HIGH: 16384,
    ReasoningLevel.EXTREME: 65536,
}


@dataclass(slots=True, frozen=True)
class ReasoningBudget:
    """Budget envelope for a reasoning-mode call.

    ``level`` is the intent; ``max_thinking_tokens`` is the hard cap.
    If ``max_thinking_tokens`` is None, the level's canonical budget
    from ``BUDGET_CONTRACT`` is used.
    """

    level: ReasoningLevel = ReasoningLevel.OFF
    max_thinking_tokens: int | None = None

    @property
    def effective_thinking_tokens(self) -> int:
        """Return the numerical budget — either the override or the default."""

        if self.max_thinking_tokens is not None:
            return self.max_thinking_tokens
        return BUDGET_CONTRACT[self.level]

    @classmethod
    def off(cls) -> ReasoningBudget:
        return cls(level=ReasoningLevel.OFF)

    @classmethod
    def from_level(cls, level: ReasoningLevel) -> ReasoningBudget:
        return cls(level=level)

    def __bool__(self) -> bool:
        return self.level != ReasoningLevel.OFF


@dataclass(slots=True, frozen=True)
class ThinkingCompletion:
    """A completion enriched with the reasoning trace metadata.

    ``thinking_tokens_used`` reports how many of the budgeted tokens
    the provider actually consumed. ``reasoning_trace`` is optional:
    populated when the downstream provider exposes the hidden
    thinking trace (Anthropic extended_thinking mode, DeepSeek-R1
    reasoning_content), empty otherwise.
    """

    completion: Completion
    budget: ReasoningBudget
    thinking_tokens_used: int = 0
    reasoning_trace: str = ""

    @property
    def text(self) -> str:
        return self.completion.text


class ThinkingProvider:
    """Wrap a ``BaseProvider`` with reasoning-budget semantics.

    This is a thin adapter, not a new provider class. It composes
    with any existing provider and applies the budget before
    forwarding the call. A provider that does not support reasoning
    treats the budget as advisory and returns ``thinking_tokens_used
    = 0``.

    The adapter is provider-agnostic by design. Vendor-specific
    thinking parameters (Anthropic ``thinking`` field, OpenAI
    ``reasoning_effort``, DeepSeek ``max_thinking_tokens``) are not
    encoded here — they belong in the provider's own implementation,
    injected via the existing ``extra`` channel.
    """

    def __init__(self, inner: BaseProvider, budget: ReasoningBudget) -> None:
        self.inner = inner
        self.budget = budget

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> ThinkingCompletion:
        completion = self.inner.complete(system=system, user=user, max_tokens=max_tokens)
        return ThinkingCompletion(
            completion=completion,
            budget=self.budget,
            thinking_tokens_used=0,
            reasoning_trace="",
        )

    @property
    def model(self) -> str:
        return self.inner.model

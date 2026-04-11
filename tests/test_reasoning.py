"""Reasoning budget + ThinkingProvider tests."""

from __future__ import annotations

from pxl.models import Provider
from pxl.providers import BaseProvider, Completion
from pxl.reasoning import (
    BUDGET_CONTRACT,
    ReasoningBudget,
    ReasoningLevel,
    ThinkingProvider,
)


def test_all_five_levels_mapped_to_budgets() -> None:
    assert set(BUDGET_CONTRACT) == set(ReasoningLevel)
    # Monotone non-decreasing
    levels_ordered = [
        ReasoningLevel.OFF,
        ReasoningLevel.LOW,
        ReasoningLevel.MEDIUM,
        ReasoningLevel.HIGH,
        ReasoningLevel.EXTREME,
    ]
    values = [BUDGET_CONTRACT[level] for level in levels_ordered]
    assert values == sorted(values)
    assert BUDGET_CONTRACT[ReasoningLevel.OFF] == 0


def test_budget_off_is_falsy() -> None:
    assert not ReasoningBudget.off()
    assert not ReasoningBudget(level=ReasoningLevel.OFF)
    assert ReasoningBudget(level=ReasoningLevel.LOW)
    assert ReasoningBudget(level=ReasoningLevel.HIGH)


def test_effective_thinking_tokens_uses_override() -> None:
    b = ReasoningBudget(level=ReasoningLevel.LOW, max_thinking_tokens=999)
    assert b.effective_thinking_tokens == 999


def test_effective_thinking_tokens_falls_back_to_contract() -> None:
    b = ReasoningBudget(level=ReasoningLevel.HIGH)
    assert b.effective_thinking_tokens == BUDGET_CONTRACT[ReasoningLevel.HIGH]


def test_budget_frozen() -> None:
    import pytest

    b = ReasoningBudget(level=ReasoningLevel.MEDIUM)
    with pytest.raises((AttributeError, TypeError)):
        b.level = ReasoningLevel.HIGH  # type: ignore[misc]


class _Stub(BaseProvider):
    kind = Provider.MOCK
    model = "stub"

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        return Completion(text="ok", provider=Provider.MOCK, model="stub", latency_ms=0)


def test_thinking_provider_wraps_inner() -> None:
    inner = _Stub()
    tp = ThinkingProvider(inner, ReasoningBudget.from_level(ReasoningLevel.MEDIUM))
    result = tp.complete(system="s", user="u")
    assert result.text == "ok"
    assert result.budget.level == ReasoningLevel.MEDIUM
    assert tp.model == "stub"
    # Adapter does not fabricate thinking tokens for non-reasoning inner
    assert result.thinking_tokens_used == 0
    assert result.reasoning_trace == ""

"""Agent loop tests — tool parsing, termination, sub-agent pattern."""

from __future__ import annotations

import json

from pxl.agents import AgentStep, Tool, _parse_tool_calls, run_agent_loop
from pxl.models import Provider
from pxl.providers import BaseProvider, Completion


class _ScriptedProvider(BaseProvider):
    """Provider that returns pre-scripted responses in order."""

    kind = Provider.MOCK
    model = "scripted"

    def __init__(self, outputs: list[str]) -> None:
        self._outputs = list(outputs)
        self._calls = 0

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        del system, user, max_tokens
        text = self._outputs[self._calls] if self._calls < len(self._outputs) else ""
        self._calls += 1
        return Completion(
            text=text,
            provider=Provider.MOCK,
            model=self.model,
            latency_ms=0,
            tokens_in=10,
            tokens_out=20,
        )


def test_parse_tool_calls_extracts_single_call() -> None:
    text = '<tool_use name="add">{"a": 1, "b": 2}</tool_use>'
    calls = _parse_tool_calls(text)
    assert calls == [("add", {"a": 1, "b": 2})]


def test_parse_tool_calls_extracts_multiple() -> None:
    text = (
        '<tool_use name="a">{"x": 1}</tool_use>'
        '<tool_use name="b">{"y": "hi"}</tool_use>'
    )
    calls = _parse_tool_calls(text)
    assert len(calls) == 2
    assert calls[0] == ("a", {"x": 1})
    assert calls[1] == ("b", {"y": "hi"})


def test_parse_tool_calls_ignores_malformed_json() -> None:
    text = '<tool_use name="broken">{not json}</tool_use>'
    assert _parse_tool_calls(text) == []


def test_agent_loop_terminates_when_model_emits_no_tool_calls() -> None:
    provider = _ScriptedProvider(["plain text answer, no tools"])
    result = run_agent_loop(
        system="you are a helper",
        user="hello",
        tools=[],
        provider=provider,
        max_iterations=3,
    )
    assert result.iterations == 1
    assert result.terminated_by == "model"
    assert result.final_output == "plain text answer, no tools"


def test_agent_loop_executes_tool_and_continues() -> None:
    add = Tool(
        name="add",
        fn=lambda a, b: {"sum": a + b},
        description="add two numbers",
    )
    provider = _ScriptedProvider(
        [
            '<tool_use name="add">{"a": 2, "b": 3}</tool_use>',
            "the answer is 5",
        ]
    )
    result = run_agent_loop(
        system="math helper",
        user="what is 2+3?",
        tools=[add],
        provider=provider,
        max_iterations=5,
    )
    assert result.iterations == 2
    assert result.terminated_by == "model"
    assert result.steps[0].tool_results == [{"sum": 5}]
    assert result.final_output == "the answer is 5"


def test_agent_loop_terminates_on_done_sentinel() -> None:
    done_tool = Tool(
        name="finish",
        fn=lambda: {"__done__": True, "reason": "complete"},
        description="signal completion",
    )
    provider = _ScriptedProvider(
        ['<tool_use name="finish">{}</tool_use>']
    )
    result = run_agent_loop(
        system="agent",
        user="start",
        tools=[done_tool],
        provider=provider,
        max_iterations=5,
    )
    assert result.iterations == 1
    assert result.terminated_by == "tool_done"


def test_agent_loop_respects_max_iterations() -> None:
    loop_forever = Tool(
        name="loop",
        fn=lambda: {"keep_going": True},
        description="never completes",
    )
    provider = _ScriptedProvider(
        ['<tool_use name="loop">{}</tool_use>'] * 10
    )
    result = run_agent_loop(
        system="looper",
        user="start",
        tools=[loop_forever],
        provider=provider,
        max_iterations=3,
    )
    assert result.iterations == 3
    assert result.terminated_by == "max_iterations"


def test_agent_loop_handles_tool_exception() -> None:
    def broken() -> None:
        raise ValueError("boom")

    t = Tool(name="broken", fn=broken, description="always fails")
    provider = _ScriptedProvider(
        [
            '<tool_use name="broken">{}</tool_use>',
            "I caught the error and stop",
        ]
    )
    result = run_agent_loop(
        system="agent",
        user="test",
        tools=[t],
        provider=provider,
        max_iterations=5,
    )
    assert result.iterations == 2
    assert result.steps[0].tool_results[0] == {"error": "ValueError: boom"}


def test_agent_loop_flags_unknown_tool() -> None:
    provider = _ScriptedProvider(
        [
            '<tool_use name="nonexistent">{"x": 1}</tool_use>',
            "done",
        ]
    )
    result = run_agent_loop(
        system="agent",
        user="test",
        tools=[],
        provider=provider,
        max_iterations=3,
    )
    assert result.steps[0].tool_results[0] == {"error": "unknown tool: nonexistent"}


def test_agent_step_to_dict_is_json_serialisable() -> None:
    step = AgentStep(
        iteration=1,
        model_output="hi",
        tool_calls=[("a", {"x": 1})],
        tool_results=[{"ok": True}],
        tokens_in=10,
        tokens_out=20,
    )
    d = step.to_dict()
    assert json.dumps(d)  # no exception

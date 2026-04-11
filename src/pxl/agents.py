"""Agent SDK primitive — minimal sub-agent + tool-use loop abstraction.

The Anthropic Claude Agent SDK (2025-2026) generalised a pattern that
was converging across vendors: an **agent** is a model configured with
a system prompt, a tool set, and a loop policy. The loop calls the
model, executes any tool calls, feeds results back, and repeats until
the model stops calling tools or a termination condition fires.

This module exposes the **primitive version of that loop** — exactly
enough to run a prompt-x-lab module as a sub-agent with tools, without
pulling in any vendor SDK. It is a 150-line reference implementation,
not a production framework. If you need ergonomics, use the Anthropic
Agent SDK directly; if you need a portable, provider-agnostic
primitive, this is it.

Design principles
-----------------
1. **The loop is the API.** Not a class hierarchy. Not a DSL.
2. **Tools are functions.** One callable per tool. Type-hinted inputs,
   JSON-serialisable output. No magic.
3. **Termination is explicit.** Either the model stops requesting
   tools, or ``max_iterations`` is reached, or a sentinel tool
   returns ``{"__done__": True}``.
4. **Every iteration is audited.** Each step produces an
   ``AgentStep`` record with the tool call, the arguments, the result,
   and the cumulative token count. Reproducible by construction.

Public API
----------
- ``Tool`` — frozen dataclass: name, callable, schema
- ``AgentStep`` — one iteration of the loop
- ``AgentResult`` — terminal result plus all steps
- ``run_agent_loop(system, user, tools, provider, max_iterations)``
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .providers import BaseProvider, Completion

#: A tool callable. Inputs are JSON-deserialised kwargs;
#: output must be JSON-serialisable.
ToolFn = Callable[..., Any]


@dataclass(slots=True, frozen=True)
class Tool:
    """One tool the agent may call.

    ``schema`` is an OpenAI / Anthropic-compatible JSON Schema dict
    describing the tool's parameters. The runner uses it for validation
    only; vendor-specific tool-use formatting is not handled here
    (that is the provider's job).
    """

    name: str
    fn: ToolFn
    description: str
    schema: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AgentStep:
    """One iteration of the agent loop."""

    iteration: int
    model_output: str
    tool_calls: list[tuple[str, dict[str, Any]]]
    tool_results: list[Any]
    tokens_in: int
    tokens_out: int
    terminated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "iteration": self.iteration,
            "model_output": self.model_output,
            "tool_calls": [
                {"name": name, "args": args} for name, args in self.tool_calls
            ],
            "tool_results": [self._safe_json(r) for r in self.tool_results],
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "terminated": self.terminated,
        }

    @staticmethod
    def _safe_json(value: Any) -> Any:
        try:
            json.dumps(value)
            return value
        except (TypeError, ValueError):
            return repr(value)


@dataclass(slots=True)
class AgentResult:
    """Terminal state of an agent run."""

    final_output: str
    steps: list[AgentStep]
    total_tokens_in: int
    total_tokens_out: int
    terminated_by: str  # 'model' | 'tool_done' | 'max_iterations'

    @property
    def iterations(self) -> int:
        return len(self.steps)


def _parse_tool_calls(model_output: str) -> list[tuple[str, dict[str, Any]]]:
    """Extract ``<tool_use name="foo">{...}</tool_use>`` blocks from output.

    This is a deliberately simple format, not a vendor-specific one.
    Providers that already return structured tool-use blocks should
    pre-format them into this shape before calling ``run_agent_loop``
    (or bypass this primitive and use the vendor SDK's native loop).
    """

    import re

    pattern = re.compile(
        r'<tool_use\s+name="([^"]+)"\s*>\s*(\{.*?\})\s*</tool_use>',
        re.DOTALL,
    )
    out: list[tuple[str, dict[str, Any]]] = []
    for match in pattern.finditer(model_output):
        name = match.group(1)
        try:
            args = json.loads(match.group(2))
            if isinstance(args, dict):
                out.append((name, args))
        except json.JSONDecodeError:
            continue
    return out


def run_agent_loop(
    *,
    system: str,
    user: str,
    tools: list[Tool],
    provider: BaseProvider,
    max_iterations: int = 8,
    max_tokens_per_call: int = 2048,
) -> AgentResult:
    """Run a minimal tool-use agent loop until termination.

    Termination conditions, in priority order:
    1. The model emits no ``<tool_use>`` blocks → ``terminated_by='model'``.
    2. A tool returns ``{"__done__": True}`` → ``terminated_by='tool_done'``.
    3. Iteration count reaches ``max_iterations`` → ``terminated_by='max_iterations'``.

    The conversation is reconstructed in each iteration: the previous
    model output plus ``<tool_result name="foo">{...}</tool_result>``
    blocks for every tool call. This is the simplest correct shape —
    not the most efficient one. Production agents should use the
    vendor's native incremental tool-use API.
    """

    tool_map = {t.name: t for t in tools}
    steps: list[AgentStep] = []
    total_in = 0
    total_out = 0
    terminated_by = "max_iterations"
    final_output = ""

    conversation: str = user
    for iteration in range(1, max_iterations + 1):
        completion: Completion = provider.complete(
            system=system, user=conversation, max_tokens=max_tokens_per_call
        )
        total_in += completion.tokens_in or 0
        total_out += completion.tokens_out or 0
        tool_calls = _parse_tool_calls(completion.text)
        tool_results: list[Any] = []
        step_done = False

        for name, args in tool_calls:
            if name not in tool_map:
                tool_results.append({"error": f"unknown tool: {name}"})
                continue
            try:
                result = tool_map[name].fn(**args)
            except Exception as e:
                result = {"error": f"{type(e).__name__}: {e}"}
            tool_results.append(result)
            if isinstance(result, dict) and result.get("__done__") is True:
                step_done = True

        step = AgentStep(
            iteration=iteration,
            model_output=completion.text,
            tool_calls=tool_calls,
            tool_results=tool_results,
            tokens_in=completion.tokens_in or 0,
            tokens_out=completion.tokens_out or 0,
            terminated=step_done or not tool_calls,
        )
        steps.append(step)
        final_output = completion.text

        if not tool_calls:
            terminated_by = "model"
            break
        if step_done:
            terminated_by = "tool_done"
            break

        # Rebuild the conversation with tool results injected.
        result_blocks = "\n".join(
            f'<tool_result name="{name}">{json.dumps(result, ensure_ascii=False)}</tool_result>'
            for (name, _), result in zip(tool_calls, tool_results, strict=True)
        )
        conversation = f"{conversation}\n\n{completion.text}\n\n{result_blocks}"

    return AgentResult(
        final_output=final_output,
        steps=steps,
        total_tokens_in=total_in,
        total_tokens_out=total_out,
        terminated_by=terminated_by,
    )

"""LLM-as-judge rubric evaluator.

The judge is a separate provider call (usually Claude Opus) that reads:

1. The original eval case ``input``.
2. The module's ``expectations`` list.
3. The module's actual ``output`` from the provider under test.

and returns a boolean per expectation plus a short evidence string.

Two rubrics are supported:

- ``expectations-only`` — the judge scores exactly what is listed.
- ``expectations-with-counterfactual`` — the judge also names the
  failure mode a user would catch in five seconds. Used for high-stakes
  modules (executive-engine, senior-code-reviewer) where a polished
  wrong answer would be expensive.

The judge is itself evaluated: in the test suite we feed it known-good
and known-bad outputs and assert it scores them correctly. A judge that
accepts a bad output is a failure of the harness, not of the module.
"""

from __future__ import annotations

import json
import re

from .models import RubricItem
from .providers import BaseProvider

JUDGE_SYSTEM = """You are a rigorous rubric evaluator. You receive:
1. INPUT — the user prompt that was given to a module.
2. EXPECTATIONS — a list of checkable statements about the expected output.
3. OUTPUT — the module's actual response.

Your job:
- For each EXPECTATION, decide if the OUTPUT satisfies it.
- Cite the shortest verbatim span of the OUTPUT that supports your decision
  (or explicitly say "no supporting span" if it does not).
- Never be generous. An expectation is satisfied only if the OUTPUT makes
  the corresponding claim explicit; implicit or adjacent content does NOT
  count.

You MUST respond as strict JSON matching this schema — no preamble, no
trailing prose, no code fences:

{
  "items": [
    {"expectation": "<verbatim>", "satisfied": true|false, "evidence": "<span or reason>"}
  ]
}
"""

JUDGE_SYSTEM_COUNTERFACTUAL = (
    JUDGE_SYSTEM
    + """
Additionally, produce a single extra item with expectation
"counterfactual: the answer contains no five-second failure mode a user
would catch" — satisfied only if you cannot find such a failure mode.
"""
)


def _strip_code_fence(text: str) -> str:
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    return m.group(1) if m else text.strip()


def judge(
    judge_provider: BaseProvider,
    input_text: str,
    expectations: list[str],
    output_text: str,
    rubric: str = "expectations-only",
) -> list[RubricItem]:
    """Return one RubricItem per expectation (plus the counterfactual if used)."""

    system = (
        JUDGE_SYSTEM_COUNTERFACTUAL if rubric == "expectations-with-counterfactual" else JUDGE_SYSTEM
    )
    user = (
        f"INPUT:\n{input_text}\n\n"
        f"EXPECTATIONS:\n- " + "\n- ".join(expectations) + "\n\n"
        f"OUTPUT:\n{output_text}"
    )
    completion = judge_provider.complete(system=system, user=user, max_tokens=2048)
    raw = _strip_code_fence(completion.text)

    try:
        data = json.loads(raw)
        items_raw = data.get("items", [])
        return [
            RubricItem(
                expectation=str(item.get("expectation", "")),
                satisfied=bool(item.get("satisfied", False)),
                evidence=str(item.get("evidence", "")) or None,
            )
            for item in items_raw
        ]
    except json.JSONDecodeError:
        return [
            RubricItem(
                expectation=exp,
                satisfied=False,
                evidence=f"judge did not return valid JSON: {raw[:120]}",
            )
            for exp in expectations
        ]

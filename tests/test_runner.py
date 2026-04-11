"""Runner tests — end-to-end eval with a fake provider (no network)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import yaml

from pxl import runner
from pxl.models import EvalResult, Provider
from pxl.providers import BaseProvider, Completion


class _StubUnderTest(BaseProvider):
    kind = Provider.MOCK
    model = "stub-sut"

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        del system, user, max_tokens
        return Completion(
            text="BLOCKER — utils.py:42  unbounded cache",
            provider=self.kind,
            model=self.model,
            latency_ms=1,
            tokens_in=10,
            tokens_out=20,
        )


class _StubJudge(BaseProvider):
    kind = Provider.MOCK
    model = "stub-judge"

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        del system, user, max_tokens
        return Completion(
            text=json.dumps(
                {
                    "items": [
                        {"expectation": "names a BLOCKER", "satisfied": True, "evidence": "BLOCKER"},
                    ]
                }
            ),
            provider=self.kind,
            model=self.model,
            latency_ms=0,
        )


def test_run_spec_end_to_end_writes_result(tmp_path: Path) -> None:
    spec_path = tmp_path / "spec.yaml"
    spec_path.write_text(
        yaml.safe_dump(
            {
                "module": "02_engineering/senior-code-reviewer.md",
                "system_prompt_from": {
                    "file": "02_engineering/senior-code-reviewer.md",
                    "sections": ["Identity", "Constraints"],
                },
                "cases": [
                    {
                        "name": "vanilla",
                        "input": "review this",
                        "expectations": ["names a BLOCKER"],
                    }
                ],
                "judge": {"model": "stub-judge", "rubric": "expectations-only"},
            }
        ),
        encoding="utf-8",
    )

    def fake_build(kind: Provider, model: str | None = None) -> BaseProvider:
        if "judge" in (model or ""):
            return _StubJudge()
        if kind == Provider.ANTHROPIC:
            return _StubUnderTest()
        return _StubJudge()

    with (
        patch("pxl.runner.build_provider", side_effect=fake_build),
        patch.object(runner, "RESULTS_DIR", tmp_path / "results"),
    ):
        result = runner.run_spec(spec_path, provider_kind=Provider.ANTHROPIC)

    assert isinstance(result, EvalResult)
    assert result.summary.cases_total == 1
    assert result.summary.cases_passed == 1
    assert result.summary.pass_rate == 1.0


def test_is_refusal_detects_literal() -> None:
    assert runner._is_refusal("REFUSED: no context")
    assert runner._is_refusal("refused: lowercase still counts")
    assert not runner._is_refusal("here is my review:")

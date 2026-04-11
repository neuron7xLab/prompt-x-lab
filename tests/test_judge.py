"""Judge tests — the judge itself must score known inputs correctly.

The harness uses a real LLM as judge in production; these tests use a
``FakeProvider`` that returns pre-canned JSON so the judge's parsing
logic is exercised deterministically in CI.
"""

from __future__ import annotations

from pxl.judge import judge
from pxl.models import Provider
from pxl.providers import BaseProvider, Completion


class _FakeProvider(BaseProvider):
    kind = Provider.MOCK
    model = "fake-judge"

    def __init__(self, text: str) -> None:
        self._text = text

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        del system, user, max_tokens
        return Completion(
            text=self._text,
            provider=self.kind,
            model=self.model,
            latency_ms=0,
            tokens_in=0,
            tokens_out=0,
        )


def test_judge_parses_plain_json() -> None:
    payload = (
        '{"items": ['
        '{"expectation": "has refusal", "satisfied": true, "evidence": "REFUSED: …"},'
        '{"expectation": "cites line", "satisfied": false, "evidence": ""}'
        "]}"
    )
    items = judge(
        _FakeProvider(payload),
        input_text="x",
        expectations=["has refusal", "cites line"],
        output_text="…",
    )
    assert len(items) == 2
    assert items[0].satisfied is True
    assert items[1].satisfied is False


def test_judge_parses_json_inside_code_fence() -> None:
    payload = '```json\n{"items": [{"expectation": "ok", "satisfied": true}]}\n```'
    items = judge(
        _FakeProvider(payload),
        input_text="x",
        expectations=["ok"],
        output_text="…",
    )
    assert len(items) == 1
    assert items[0].satisfied is True


def test_judge_fails_all_on_invalid_json() -> None:
    items = judge(
        _FakeProvider("this is not json at all"),
        input_text="x",
        expectations=["one", "two"],
        output_text="…",
    )
    assert len(items) == 2
    assert all(not i.satisfied for i in items)

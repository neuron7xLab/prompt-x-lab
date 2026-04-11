"""Provider abstractions for the evaluation harness.

Three providers are wired:

- ``AnthropicProvider`` — default for Claude models (Opus / Sonnet 4.6).
- ``OpenAIProvider`` — for cross-model validation on GPT-class models.
- ``MockProvider`` — deterministic stub used in CI when no API key is
  present. Never produces a passing result for any rubric it cannot
  satisfy trivially; always marked as ``provider=mock`` in the result.

The provider interface is intentionally tiny: ``complete(system, user,
max_tokens) -> Completion``. Adding a new provider means implementing
one method.
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .models import Provider


@dataclass(slots=True, frozen=True)
class Completion:
    """Provider-agnostic completion wrapper."""

    text: str
    provider: Provider
    model: str
    latency_ms: int
    tokens_in: int | None = None
    tokens_out: int | None = None


class BaseProvider(ABC):
    """All providers implement exactly this contract."""

    kind: Provider
    model: str

    @abstractmethod
    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion: ...


class AnthropicProvider(BaseProvider):
    """Claude models via the Anthropic SDK."""

    kind = Provider.ANTHROPIC

    def __init__(self, model: str = "claude-opus-4-6", api_key: str | None = None) -> None:
        self.model = model
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self._api_key:
            msg = "ANTHROPIC_API_KEY not set — use MockProvider or configure the key"
            raise RuntimeError(msg)
        try:
            import anthropic
        except ImportError as e:
            msg = "anthropic package not installed — run: pip install 'prompt-x-lab[eval]'"
            raise RuntimeError(msg) from e
        self._client: Any = anthropic.Anthropic(api_key=self._api_key)

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        start = time.perf_counter()
        resp = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        latency_ms = int((time.perf_counter() - start) * 1000)
        text_blocks = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
        text = "".join(text_blocks) if text_blocks else ""
        return Completion(
            text=text,
            provider=self.kind,
            model=self.model,
            latency_ms=latency_ms,
            tokens_in=getattr(resp.usage, "input_tokens", None),
            tokens_out=getattr(resp.usage, "output_tokens", None),
        )


class OpenAIProvider(BaseProvider):
    """GPT-class models via the OpenAI SDK."""

    kind = Provider.OPENAI

    def __init__(self, model: str = "gpt-4o", api_key: str | None = None) -> None:
        self.model = model
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            msg = "OPENAI_API_KEY not set — use MockProvider or configure the key"
            raise RuntimeError(msg)
        try:
            from openai import OpenAI
        except ImportError as e:
            msg = "openai package not installed — run: pip install 'prompt-x-lab[eval]'"
            raise RuntimeError(msg) from e
        self._client: Any = OpenAI(api_key=self._api_key)

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        start = time.perf_counter()
        resp = self._client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        latency_ms = int((time.perf_counter() - start) * 1000)
        text = resp.choices[0].message.content or ""
        usage = getattr(resp, "usage", None)
        return Completion(
            text=text,
            provider=self.kind,
            model=self.model,
            latency_ms=latency_ms,
            tokens_in=getattr(usage, "prompt_tokens", None),
            tokens_out=getattr(usage, "completion_tokens", None),
        )


class MockProvider(BaseProvider):
    """Deterministic stub used in CI with no API keys.

    The mock intentionally does *not* always pass. It emits a canned
    "REFUSED: mock provider cannot exercise this rubric" response so
    the harness downstream treats it as a real, non-passing answer.
    This way, a failing mock run is indistinguishable from a failing
    real run — and the badge generator never mistakes a mock-only run
    for validated coverage.
    """

    kind = Provider.MOCK

    def __init__(self, model: str = "mock-1") -> None:
        self.model = model

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        del system, user, max_tokens  # unused — deterministic stub
        return Completion(
            text=(
                "REFUSED: mock provider cannot exercise this rubric. "
                "Configure ANTHROPIC_API_KEY or OPENAI_API_KEY and rerun."
            ),
            provider=self.kind,
            model=self.model,
            latency_ms=0,
            tokens_in=0,
            tokens_out=0,
        )


def build_provider(kind: Provider, model: str | None = None) -> BaseProvider:
    """Factory — returns a ready provider or a ``MockProvider`` if keys missing."""

    try:
        if kind == Provider.ANTHROPIC:
            return AnthropicProvider(model=model or "claude-opus-4-6")
        if kind == Provider.OPENAI:
            return OpenAIProvider(model=model or "gpt-4o")
    except RuntimeError:
        pass
    return MockProvider(model=model or "mock-1")

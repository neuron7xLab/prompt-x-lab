"""Local / edge-model provider for 2026→2030 small-model workflows.

Llama-4, Gemma 3, Qwen 2.5 and DeepSeek-V2 made meaningful edge
inference practical in 2025. In 2026, every serious evaluation
pipeline needs to run at least a fraction of its cases against local
models, both for cost and for reproducibility guarantees that remote
APIs cannot make.

This module exposes a single ``OllamaProvider`` that talks to a local
Ollama server over HTTP. It implements the same ``BaseProvider``
interface as ``AnthropicProvider`` and ``OpenAIProvider``, so any
``pxl-eval`` spec can be re-run against a local model with a single
``--provider local`` flag.

The implementation is deliberately minimal — no retries, no streaming,
no request-level caching. If you need those, wire them in via the
``httpx`` client you pass in; the provider does not hard-require any
specific transport.

Public API
----------
- ``OllamaProvider`` — implements ``BaseProvider`` for local Ollama
- ``list_local_models(host)`` — enumerate available Ollama models
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

from .models import Provider
from .providers import BaseProvider, Completion


@dataclass(slots=True, frozen=True)
class LocalModelInfo:
    """One locally-available model record, returned by ``list_local_models``."""

    name: str
    family: str
    parameter_size: str
    quantization_level: str
    size_bytes: int


class OllamaProvider(BaseProvider):
    """BaseProvider implementation that calls a local Ollama server.

    Defaults to ``http://localhost:11434`` — the Ollama server default.
    Override via ``OLLAMA_HOST`` environment variable or the ``host``
    argument.

    This provider is classified under ``Provider.MOCK`` at the type
    level because the result is not covered by the cross-vendor
    validated-modules contract (a model validated against
    ``qwen2.5-7b-instruct`` running locally is not validated against
    Claude Opus 4.6 running in production). Treat local runs as
    ground-truth for reproducibility, *not* as cross-model validation.
    """

    kind = Provider.MOCK

    def __init__(
        self,
        model: str = "llama3.2",
        host: str | None = None,
        timeout: float = 120.0,
    ) -> None:
        self.model = model
        self.host = host or os.getenv("OLLAMA_HOST") or "http://localhost:11434"
        self.timeout = timeout
        try:
            import httpx
        except ImportError as e:
            msg = (
                "httpx not installed — run: pip install 'prompt-x-lab[local]' "
                "(or install httpx directly)"
            )
            raise RuntimeError(msg) from e
        self._httpx: Any = httpx
        self._client: Any = httpx.Client(
            base_url=self.host,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )

    def complete(self, system: str, user: str, max_tokens: int = 2048) -> Completion:
        payload: dict[str, Any] = {
            "model": self.model,
            "system": system,
            "prompt": user,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }
        start = time.perf_counter()
        response = self._client.post("/api/generate", json=payload)
        latency_ms = int((time.perf_counter() - start) * 1000)
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        text = str(data.get("response", ""))
        prompt_count = data.get("prompt_eval_count")
        eval_count = data.get("eval_count")
        return Completion(
            text=text,
            provider=Provider.MOCK,  # classified as mock: not cross-vendor validated
            model=self.model,
            latency_ms=latency_ms,
            tokens_in=int(prompt_count) if isinstance(prompt_count, int) else None,
            tokens_out=int(eval_count) if isinstance(eval_count, int) else None,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> OllamaProvider:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def list_local_models(host: str | None = None, timeout: float = 10.0) -> list[LocalModelInfo]:
    """Enumerate models available on a local Ollama server.

    Returns an empty list if the server is unreachable. Callers should
    treat an empty list as "no local models available" — not as an
    error — so the function composes cleanly with ``--provider local``
    CLI flags that silently degrade to mock mode.
    """

    try:
        import httpx
    except ImportError:
        return []

    target = host or os.getenv("OLLAMA_HOST") or "http://localhost:11434"
    try:
        with httpx.Client(base_url=target, timeout=timeout) as client:
            response = client.get("/api/tags")
            response.raise_for_status()
            data: dict[str, Any] = response.json()
    except Exception:
        return []

    models_raw = data.get("models", [])
    if not isinstance(models_raw, list):
        return []

    out: list[LocalModelInfo] = []
    for entry in models_raw:
        if not isinstance(entry, dict):
            continue
        details = entry.get("details", {})
        if not isinstance(details, dict):
            details = {}
        out.append(
            LocalModelInfo(
                name=str(entry.get("name", "")),
                family=str(details.get("family", "")),
                parameter_size=str(details.get("parameter_size", "")),
                quantization_level=str(details.get("quantization_level", "")),
                size_bytes=int(entry.get("size", 0)),
            )
        )
    return out

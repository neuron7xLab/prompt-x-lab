"""Local (Ollama) provider tests — pure unit without real HTTP.

The tests exercise parsing + shape invariants; they do NOT require an
Ollama server to be running. Integration against a live server belongs
in a separate marker-gated suite.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from pxl.local import LocalModelInfo, OllamaProvider, list_local_models
from pxl.models import Provider


def test_list_local_models_returns_empty_on_connection_failure() -> None:
    # Pointing at an unreachable host should silently yield [].
    models = list_local_models(host="http://127.0.0.1:1", timeout=0.05)
    assert models == []


def test_local_model_info_fields() -> None:
    info = LocalModelInfo(
        name="llama3.2:3b",
        family="llama",
        parameter_size="3B",
        quantization_level="Q4_K_M",
        size_bytes=1_900_000_000,
    )
    assert info.name == "llama3.2:3b"
    assert info.size_bytes > 0


def test_list_local_models_parses_valid_response() -> None:
    fake_response: dict[str, Any] = {
        "models": [
            {
                "name": "llama3.2:3b",
                "size": 1_900_000_000,
                "details": {
                    "family": "llama",
                    "parameter_size": "3B",
                    "quantization_level": "Q4_K_M",
                },
            },
            {
                "name": "qwen2.5:7b",
                "size": 4_100_000_000,
                "details": {
                    "family": "qwen",
                    "parameter_size": "7B",
                    "quantization_level": "Q4_0",
                },
            },
        ]
    }

    class _FakeResponse:
        def __init__(self, data: dict[str, Any]) -> None:
            self._data = data

        def json(self) -> dict[str, Any]:
            return self._data

        def raise_for_status(self) -> None:
            return None

    class _FakeClient:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            pass

        def __enter__(self) -> _FakeClient:
            return self

        def __exit__(self, *exc: object) -> None:
            return None

        def get(self, _path: str) -> _FakeResponse:
            return _FakeResponse(fake_response)

    with patch("httpx.Client", _FakeClient):
        models = list_local_models(host="http://fake:11434")
    assert len(models) == 2
    assert models[0].family == "llama"
    assert models[1].parameter_size == "7B"


def test_ollama_provider_complete_shape() -> None:
    fake_payload: dict[str, Any] = {
        "response": "generated text",
        "prompt_eval_count": 42,
        "eval_count": 17,
    }

    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, Any]:
            return fake_payload

    fake_client = MagicMock()
    fake_client.post.return_value = _FakeResponse()
    fake_client.close = MagicMock()

    with patch("httpx.Client", return_value=fake_client):
        provider = OllamaProvider(model="llama3.2", host="http://fake:11434")
        result = provider.complete(system="s", user="u", max_tokens=100)

    assert result.text == "generated text"
    assert result.provider == Provider.MOCK  # local runs are not cross-vendor validated
    assert result.model == "llama3.2"
    assert result.tokens_in == 42
    assert result.tokens_out == 17
    assert result.latency_ms >= 0


def test_ollama_provider_context_manager_closes_client() -> None:
    fake_client = MagicMock()
    fake_client.close = MagicMock()

    with (
        patch("httpx.Client", return_value=fake_client),
        OllamaProvider(model="llama3.2", host="http://fake") as provider,
    ):
        assert provider.model == "llama3.2"

    fake_client.close.assert_called_once()

"""ECA signer — HMAC-SHA256 determinism + verification + secret hygiene."""

from __future__ import annotations

from pxl.eca.signer import sign_response, verify_signature

_SAMPLE = {
    "response_id": "r-1",
    "mode": "executive_decision_brief",
    "main_body": [
        {"section": "Objective", "content": "pick A"},
        {"section": "Recommended Decision", "content": "A"},
    ],
    "timestamp": "2026-04-11T12:00:00Z",
    "deployment_id": "test",
}


def test_sign_response_is_deterministic() -> None:
    a = sign_response(_SAMPLE, secret="test-secret")
    b = sign_response(_SAMPLE, secret="test-secret")
    assert a == b
    assert len(a) == 64  # hex sha256


def test_sign_response_differs_on_content_change() -> None:
    modified = dict(_SAMPLE)
    modified["main_body"] = [{"section": "Objective", "content": "pick B"}]
    a = sign_response(_SAMPLE, secret="test-secret")
    b = sign_response(modified, secret="test-secret")
    assert a != b


def test_sign_response_differs_on_secret_change() -> None:
    a = sign_response(_SAMPLE, secret="k1")
    b = sign_response(_SAMPLE, secret="k2")
    assert a != b


def test_verify_signature_round_trip() -> None:
    sig = sign_response(_SAMPLE, secret="test-secret")
    assert verify_signature(_SAMPLE, sig, secret="test-secret") is True
    assert verify_signature(_SAMPLE, "0" * 64, secret="test-secret") is False

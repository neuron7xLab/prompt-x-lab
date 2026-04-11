"""HMAC-SHA256 response signing for the ECA stack.

Ports ``scripts/sign_response.py`` with the same payload shape and the
same deterministic JSON canonicalisation so signatures produced by this
module verify against signatures produced by the original script and
vice versa.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any

DEFAULT_SECRET_ENV = "ECA_SIGNING_SECRET"
DEFAULT_SECRET = "change-me"


def _canonical(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "response_id": data.get("response_id"),
        "mode": data.get("mode"),
        "main_body": data.get("main_body"),
        "timestamp": data.get("timestamp", "unknown"),
        "deployment_id": data.get("deployment_id", "local"),
    }


def sign_response(data: dict[str, Any], secret: str | None = None) -> str:
    """Return the HMAC-SHA256 hex digest of a canonicalised response."""

    key = secret or os.environ.get(DEFAULT_SECRET_ENV) or DEFAULT_SECRET
    message = json.dumps(_canonical(data), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hmac.new(key.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_signature(data: dict[str, Any], signature: str, secret: str | None = None) -> bool:
    """Constant-time verification of a signature against a response."""

    expected = sign_response(data, secret=secret)
    return hmac.compare_digest(expected, signature)

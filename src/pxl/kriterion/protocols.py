"""Kriterion protocols — loaders for the six security-role protocols.

The six protocol text files ship unchanged as bundled assets. The
loaders expose them via a tiny public API so that any consumer — a
CLI, a test, a notebook — can pull a protocol without touching the
filesystem directly.
"""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import files

_PROTOCOLS = files("pxl.kriterion") / "assets" / "protocols"

PROTOCOL_IDS: tuple[str, ...] = (
    "SE-OPS-PROTOCOL-2026.1",
    "SSE-SECURITY-EXECUTION-PROTOCOL-2026.1",
    "ESA-SECURITY-ARCHITECT-PROTOCOL-2026.1",
    "PSE-SECURITY-PLATFORM-PROTOCOL-2026.2",
    "DSE-SECURITY-INTELLIGENCE-PROTOCOL-2026",
    "GPT5.4-AUDIT-HARDENING-PROTOCOL-2026",
)


def list_protocols() -> list[str]:
    """Return the list of bundled protocol IDs."""

    return list(PROTOCOL_IDS)


@lru_cache(maxsize=len(PROTOCOL_IDS))
def load_protocol(protocol_id: str) -> str:
    """Return the raw text of a bundled protocol.

    ``protocol_id`` may be passed with or without the ``.txt`` suffix.
    """

    stem = protocol_id.removesuffix(".txt")
    if stem not in PROTOCOL_IDS:
        msg = f"unknown protocol: {protocol_id}. Known: {PROTOCOL_IDS}"
        raise KeyError(msg)
    resource = _PROTOCOLS / f"{stem}.txt"
    text: str = resource.read_text(encoding="utf-8")
    return text

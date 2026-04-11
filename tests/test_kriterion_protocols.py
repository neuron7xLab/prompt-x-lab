"""Kriterion protocols — loader tests."""

from __future__ import annotations

import pytest

from pxl.kriterion.protocols import PROTOCOL_IDS, list_protocols, load_protocol


def test_six_protocols_bundled() -> None:
    assert len(PROTOCOL_IDS) == 6


def test_list_protocols_returns_full_set() -> None:
    assert set(list_protocols()) == set(PROTOCOL_IDS)


@pytest.mark.parametrize("protocol_id", PROTOCOL_IDS)
def test_each_protocol_is_non_empty_text(protocol_id: str) -> None:
    text = load_protocol(protocol_id)
    assert text.strip()
    assert len(text) > 100


_SLASH_CONVENTION_PROTOCOLS = (
    "SE-OPS-PROTOCOL-2026.1",
    "SSE-SECURITY-EXECUTION-PROTOCOL-2026.1",
    "ESA-SECURITY-ARCHITECT-PROTOCOL-2026.1",
    "PSE-SECURITY-PLATFORM-PROTOCOL-2026.2",
)


@pytest.mark.parametrize("protocol_id", _SLASH_CONVENTION_PROTOCOLS)
def test_role_protocols_have_task_scope_sections(protocol_id: str) -> None:
    """The four role protocols share the /TASK + /SCOPE convention."""

    text = load_protocol(protocol_id)
    assert "/TASK" in text
    assert "/SCOPE" in text


def test_load_protocol_accepts_suffix() -> None:
    with_suffix = load_protocol("SE-OPS-PROTOCOL-2026.1.txt")
    without = load_protocol("SE-OPS-PROTOCOL-2026.1")
    assert with_suffix == without


def test_load_protocol_rejects_unknown() -> None:
    with pytest.raises(KeyError, match="unknown protocol"):
        load_protocol("NOT-A-REAL-PROTOCOL-2026")

"""Dashboard command — state-view tests."""

from __future__ import annotations

import pytest

from pxl.dashboard import collect_layer_stats, render_dashboard


def test_collect_layer_stats_returns_eight_layers() -> None:
    stats = collect_layer_stats()
    assert len(stats) == 8
    # Keys are the eight canonical layer directories.
    keys = {s.key for s in stats}
    expected = {
        "00_foundation",
        "01_cognition",
        "02_engineering",
        "03_personas",
        "04_validation",
        "05_orchestration",
        "06_eca_engine",
        "07_kriterion",
    }
    assert keys == expected


def test_layer_stats_have_positive_module_counts() -> None:
    stats = collect_layer_stats()
    for s in stats:
        assert s.modules > 0, f"{s.key} has no modules"


def test_integrated_layers_have_audit_status() -> None:
    """Layers 05/06/07 must have an audit status (not None)."""

    stats = collect_layer_stats()
    by_key = {s.key: s for s in stats}
    assert by_key["05_orchestration"].audit_ok is True
    assert by_key["06_eca_engine"].audit_ok is True
    assert by_key["07_kriterion"].audit_ok is True


def test_seed_layers_have_no_audit() -> None:
    """Layers 00-04 are hand-written, no SHA-256 audit."""

    stats = collect_layer_stats()
    by_key = {s.key: s for s in stats}
    for key in (
        "00_foundation",
        "01_cognition",
        "02_engineering",
        "03_personas",
        "04_validation",
    ):
        assert by_key[key].audit_ok is None, f"{key} unexpectedly has an audit status"


def test_render_dashboard_returns_json_summary(
    capsys: pytest.CaptureFixture[str],
) -> None:
    summary = render_dashboard()
    captured = capsys.readouterr()
    # A non-trivial amount of output was produced
    assert len(captured.out) > 100
    # The JSON summary is well-formed
    assert summary["total_modules"] >= 91
    assert summary["valid_count"] >= 91
    assert summary["issues"] == 0
    assert summary["all_audits_ok"] is True
    assert len(summary["layers"]) == 8

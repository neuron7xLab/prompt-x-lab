"""Unified ``pxl`` CLI dispatcher tests."""

from __future__ import annotations

import subprocess
import sys

import pytest

from pxl import __version__
from pxl.main import _build_parser, main


def test_parser_builds() -> None:
    parser = _build_parser()
    assert parser.prog == "pxl"


def test_version_subcommand_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["version"])
    assert rc == 0
    out = capsys.readouterr().out
    assert __version__ in out


def test_layers_subcommand_lists_eight_layers(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(["layers"])
    assert rc == 0
    out = capsys.readouterr().out
    # Each of the 8 canonical layer labels must appear in the output.
    for label in (
        "FOUNDATION",
        "COGNITION",
        "ENGINEERING",
        "PERSONAS",
        "VALIDATION",
        "ORCHESTRATION",
        "ECA ENGINE",
        "KRITERION",
    ):
        assert label in out, f"missing layer label: {label}"


def test_validate_subcommand_passes(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["validate"])
    captured = capsys.readouterr()
    assert rc == 0, captured.err
    assert "OK" in captured.out


def test_audit_subcommand_defaults_to_verify_all(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(["audit"])
    captured = capsys.readouterr()
    assert rc == 0, captured.err
    # All three integrated layers should appear in the audit output.
    assert "layer 05" in captured.out
    assert "layer 06" in captured.out
    assert "layer 07" in captured.out


def test_no_subcommand_exits_non_zero() -> None:
    """Calling `pxl` with no arguments should fail with a helpful message."""

    with pytest.raises(SystemExit) as exc_info:
        main([])
    assert exc_info.value.code != 0


def test_python_dash_m_pxl_works_as_entry_point(tmp_path: object) -> None:
    """``python -m pxl version`` is equivalent to ``pxl version``."""

    del tmp_path  # unused
    result = subprocess.run(
        [sys.executable, "-m", "pxl", "version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert __version__ in result.stdout

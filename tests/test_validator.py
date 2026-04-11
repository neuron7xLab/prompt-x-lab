"""Validator tests — every seed module must pass the frontmatter schema."""

from __future__ import annotations

from pathlib import Path

from pxl.validator import LAYER_DIRS, iter_module_files, validate_all, validate_file

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_layer_dirs_all_exist() -> None:
    for layer in LAYER_DIRS:
        path = REPO_ROOT / layer
        assert path.exists(), f"expected layer dir missing: {layer}"


def test_every_module_has_valid_frontmatter() -> None:
    ok, issues = validate_all()
    assert not issues, "\n".join(str(i) for i in issues)
    assert ok > 0, "no module files were found"


def test_iter_module_files_nonempty_and_excludes_readmes() -> None:
    files = iter_module_files()
    assert files, "iter_module_files returned nothing"
    for path in files:
        assert path.name.upper() != "README.MD"


def test_validate_file_reports_missing_frontmatter(tmp_path: Path) -> None:
    bogus = tmp_path / "bogus.md"
    bogus.write_text("# just prose, no frontmatter\n", encoding="utf-8")
    issues = validate_file(bogus)
    assert issues
    assert "frontmatter" in issues[0].message.lower()

"""Assembly tests — section extraction + system-prompt stitching."""

from __future__ import annotations

from pathlib import Path

import pytest

from pxl.assembly import assemble_system_prompt, extract_sections, load_module

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_MODULE = REPO_ROOT / "02_engineering" / "senior-code-reviewer.md"


def test_extract_sections_reads_h2_only() -> None:
    # h2 headings delimit sections; h3/h4 belong to the enclosing h2 body.
    text = "# title\n\n## One\nbody1\n\n### subhead\nsub-body\n\n## Two\nbody2\n"
    sections = extract_sections(text)
    assert set(sections) == {"One", "Two"}
    # h3 "subhead" is still inside section "One"
    assert "body1" in sections["One"]
    assert "sub-body" in sections["One"]
    assert sections["Two"].strip() == "body2"


def test_load_module_real_file_returns_frontmatter_and_sections() -> None:
    meta, sections = load_module(SAMPLE_MODULE)
    assert meta["title"]
    assert "Identity" in sections
    assert "Constraints" in sections
    assert "Core logic" in sections


def test_assemble_system_prompt_concatenates_in_order() -> None:
    sections = {"Identity": "id body", "Constraints": "con body"}
    out = assemble_system_prompt(sections, ["Identity", "Constraints"])
    assert out.index("Identity") < out.index("Constraints")
    assert "id body" in out
    assert "con body" in out


def test_assemble_raises_on_missing_section() -> None:
    with pytest.raises(ValueError, match="missing required section"):
        assemble_system_prompt({"Identity": "x"}, ["Identity", "Output format"])

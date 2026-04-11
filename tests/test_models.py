"""Pydantic model tests — frontmatter and spec validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from pxl.models import (
    Category,
    EvalCase,
    EvalSpec,
    JudgeSpec,
    ModuleFrontmatter,
    Status,
    SystemPromptAssembly,
    Vector,
)


def test_module_frontmatter_minimal_valid() -> None:
    fm = ModuleFrontmatter(
        title="Sample",
        category=Category.FOUNDATION,
        vector=Vector.COGNITIVE,
        version="1.0.0",
        status=Status.STABLE,
    )
    assert fm.title == "Sample"


def test_module_frontmatter_rejects_bad_semver() -> None:
    with pytest.raises(ValidationError):
        ModuleFrontmatter(
            title="Sample",
            category=Category.FOUNDATION,
            vector=Vector.COGNITIVE,
            version="1.0",  # not SemVer
            status=Status.STABLE,
        )


def test_eval_spec_roundtrip() -> None:
    spec = EvalSpec(
        module="02_engineering/senior-code-reviewer.md",
        system_prompt_from=SystemPromptAssembly(
            file="02_engineering/senior-code-reviewer.md",
            sections=["Identity", "Core logic", "Constraints", "Output format"],
        ),
        cases=[
            EvalCase(
                name="vanilla-case",
                input="Review this function.",
                expectations=["names at least one BLOCKER"],
            ),
        ],
        judge=JudgeSpec(model="claude-opus-4-6", rubric="expectations-only"),
    )
    assert spec.cases[0].name == "vanilla-case"


def test_eval_spec_rejects_unknown_section() -> None:
    with pytest.raises(ValidationError):
        SystemPromptAssembly(file="x.md", sections=["Identity", "NotARealSection"])

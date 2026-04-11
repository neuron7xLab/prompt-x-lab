"""Frontmatter validator for every module in the repo.

Walks the module directories, parses each Markdown file's YAML
frontmatter, and validates it against ``ModuleFrontmatter``. A single
invalid module fails the whole run with a non-zero exit code — mirroring
the discipline of mypy --strict.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import frontmatter

from .models import ModuleFrontmatter

REPO_ROOT = Path(__file__).resolve().parents[2]
LAYER_DIRS = (
    "00_foundation",
    "01_cognition",
    "02_engineering",
    "03_personas",
    "04_validation",
    "05_orchestration",
)


@dataclass(slots=True)
class ValidationIssue:
    path: Path
    message: str

    def __str__(self) -> str:
        rel = self.path.relative_to(REPO_ROOT) if self.path.is_absolute() else self.path
        return f"{rel}: {self.message}"


def iter_module_files(root: Path = REPO_ROOT) -> list[Path]:
    """Yield every ``.md`` module file in the layer directories."""

    out: list[Path] = []
    for layer in LAYER_DIRS:
        layer_path = root / layer
        if not layer_path.exists():
            continue
        for path in sorted(layer_path.rglob("*.md")):
            if path.name.upper() == "README.MD":
                continue
            out.append(path)
    return out


def validate_file(path: Path) -> list[ValidationIssue]:
    """Validate a single module file. Return a list of issues (empty == valid)."""

    try:
        post = frontmatter.load(path)
    except Exception as e:
        return [ValidationIssue(path, f"failed to parse frontmatter: {e}")]

    if not post.metadata:
        return [ValidationIssue(path, "missing YAML frontmatter")]

    try:
        ModuleFrontmatter.model_validate(post.metadata)
    except Exception as e:
        return [ValidationIssue(path, f"frontmatter schema error: {e}")]

    return []


def validate_all(root: Path = REPO_ROOT) -> tuple[int, list[ValidationIssue]]:
    """Validate every module file. Return (count_ok, issues)."""

    issues: list[ValidationIssue] = []
    files = iter_module_files(root)
    ok = 0
    for path in files:
        file_issues = validate_file(path)
        if file_issues:
            issues.extend(file_issues)
        else:
            ok += 1
    return ok, issues

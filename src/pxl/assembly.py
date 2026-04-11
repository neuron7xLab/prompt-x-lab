"""Assemble system prompts from module Markdown files.

Modules are authored as Markdown with a fixed section vocabulary:
``## Identity``, ``## Core logic``, ``## Constraints``, ``## Output
format``. The eval harness reads these sections by heading and stitches
them into a system prompt — no free-form instructions are added.

Why this matters: every eval thus tests exactly what the module claims
to do, not a paraphrase. If the module's constraint block is wrong, the
eval will fail on that constraint — not on something adjacent.
"""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def extract_sections(md_text: str) -> dict[str, str]:
    """Return a dict of section-title -> section-body (level-2 headings only)."""

    out: dict[str, str] = {}
    lines = md_text.splitlines()
    current_title: str | None = None
    current_body: list[str] = []

    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:  # h2
            if current_title is not None:
                out[current_title] = "\n".join(current_body).strip()
            current_title = m.group(2).strip()
            current_body = []
            continue
        if current_title is not None:
            current_body.append(line)

    if current_title is not None:
        out[current_title] = "\n".join(current_body).strip()

    return out


def load_module(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    """Parse a module file into (frontmatter_dict, sections_dict)."""

    post = frontmatter.load(path)
    sections = extract_sections(post.content)
    return post.metadata, sections


def assemble_system_prompt(sections: dict[str, str], wanted: list[str]) -> str:
    """Stitch the requested sections into a single system prompt."""

    chunks: list[str] = []
    for title in wanted:
        body = sections.get(title)
        if body is None:
            msg = f"Module is missing required section: ## {title}"
            raise ValueError(msg)
        chunks.append(f"## {title}\n\n{body}")
    return "\n\n---\n\n".join(chunks)

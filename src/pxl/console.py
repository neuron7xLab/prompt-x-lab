"""Shared Rich console utilities for the unified ``pxl`` CLI.

One Rich ``Console`` instance is reused across all subcommands so that
colour output, width detection, and terminal-capability probing happen
exactly once. The module also exports the repository's visual brand
tokens (colours, glyphs, divider styles) so every CLI surface looks
like it was designed by the same person on the same day — because it
was.

Design principles
-----------------
1. **One console, one palette.** The four-colour RGB-on-black brand is
   encoded here and nowhere else. CLI commands import these tokens;
   they never hardcode hex strings.
2. **No side effects on import.** Importing ``pxl.console`` does not
   print anything, open files, or read environment variables beyond
   what Rich itself does.
3. **Machine-readable fallback.** Every command that prints a Rich
   table or panel supports a ``--json`` flag for scripted consumers;
   the Rich output is the human surface, the JSON is the contract.
"""

from __future__ import annotations

from rich.console import Console
from rich.theme import Theme

# ──────────────────────────────────────────────────────────────
# Brand tokens — the four colours that define prompt-x-lab.
# ──────────────────────────────────────────────────────────────

BRAND_GREEN = "#00FF00"
BRAND_BLUE = "#0000FF"
BRAND_RED = "#FF0000"
BRAND_BLACK = "#000000"

# Rich theme — named styles the rest of the package uses.
_THEME = Theme(
    {
        "pxl.ok": f"bold {BRAND_GREEN}",
        "pxl.fail": f"bold {BRAND_RED}",
        "pxl.info": f"bold {BRAND_BLUE}",
        "pxl.dim": "dim",
        "pxl.title": f"bold {BRAND_GREEN} on {BRAND_BLACK}",
        "pxl.header": "bold white on grey23",
        "pxl.number": f"bold {BRAND_GREEN}",
        "pxl.layer": f"bold {BRAND_BLUE}",
        "pxl.module": f"bold {BRAND_GREEN}",
        "pxl.warn": f"bold {BRAND_RED}",
        "pxl.path": "italic cyan",
        "pxl.prompt": "bold magenta",
    }
)

# The canonical singleton. Do not instantiate another Console anywhere
# else in the package — import this one.
console: Console = Console(theme=_THEME, highlight=False, soft_wrap=False)

# Useful glyphs for CLI output. Plain ASCII, so they render everywhere.
GLYPH_OK = "✓"
GLYPH_FAIL = "✗"
GLYPH_DOT = "·"
GLYPH_ARROW = "→"
GLYPH_BULLET = "▸"


def print_banner(version: str, subtitle: str = "") -> None:
    """Print a compact branded banner at the top of a command's output."""

    from rich.panel import Panel
    from rich.text import Text

    title = Text("p r o m p t   x   l a b", style="pxl.title")
    body = Text.assemble(
        ("version ", "pxl.dim"),
        (version, "pxl.number"),
        ("  ·  ", "pxl.dim"),
        (subtitle or "eight-layer cognitive library", "pxl.info"),
    )
    console.print(
        Panel(
            Text.assemble(title, "\n", body),
            border_style="pxl.dim",
            padding=(0, 2),
            expand=False,
        )
    )


def print_section(title: str) -> None:
    """Print a small section header with a brand-coloured rule."""

    from rich.rule import Rule

    console.print()
    console.print(Rule(f"[pxl.layer]{title}[/]", style="pxl.dim"))
    console.print()


def print_status(label: str, ok: bool, detail: str = "") -> None:
    """Print a ``✓ label  ·  detail`` or ``✗ label  ·  detail`` line."""

    glyph = GLYPH_OK if ok else GLYPH_FAIL
    style = "pxl.ok" if ok else "pxl.fail"
    line = f"[{style}]{glyph}[/]  [bold]{label}[/]"
    if detail:
        line += f"  [pxl.dim]{GLYPH_DOT}[/]  {detail}"
    console.print(line)

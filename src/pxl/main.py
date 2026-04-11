"""Unified ``pxl`` command-line interface.

One entry point, one subcommand tree, one consistent UX. This module
replaces the direct invocation of the five legacy entry points
(``pxl-validate``, ``pxl-eval``, ``pxl-audit``, ``pxl-badges``,
``pxl-eca``, ``pxl-kriterion``) with a single dispatcher that preserves
their behaviour while exposing a grouped command hierarchy:

    pxl dashboard                  # one-screen state view
    pxl validate                   # frontmatter validator
    pxl eval [--spec FILE]         # LLM-as-judge harness
    pxl audit [verify|write] [05|06|07|all]
    pxl badges                     # real-data badge generator
    pxl eca <subcmd>               # ECA subsystem
    pxl kriterion <subcmd>         # Kriterion subsystem
    pxl version                    # print package version
    pxl layers                     # enumerate the 8 layers

The legacy ``pxl-*`` entry points in ``pyproject.toml`` remain
registered so existing scripts and shell history keep working — they
simply dispatch to the same underlying functions.

Design principles
-----------------
1. **One dispatcher.** Every subcommand is a top-level function here
   that imports and calls the appropriate legacy function, keeping
   behaviour identical.
2. **No circular imports.** Subsystem CLIs (``pxl.eca.cli``,
   ``pxl.kriterion.cli``) are imported lazily inside handlers so
   importing ``pxl.main`` does not force every subsystem to load.
3. **``--help`` is a first-class feature.** Every subcommand has its
   own parser, every parser prints an example. No magic flags.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable

from . import __version__

CommandFn = Callable[[argparse.Namespace], int]


def _cmd_version(_args: argparse.Namespace) -> int:
    from .console import console

    console.print(f"prompt-x-lab [pxl.number]{__version__}[/]")
    return 0


def _cmd_dashboard(_args: argparse.Namespace) -> int:
    from .dashboard import render_dashboard

    render_dashboard()
    return 0


def _cmd_layers(_args: argparse.Namespace) -> int:
    from .console import console
    from .dashboard import collect_layer_stats

    stats = collect_layer_stats()
    for s in stats:
        console.print(
            f"[pxl.layer]{s.label:<16}[/] "
            f"[pxl.dim]{s.kind:<12}[/] "
            f"[pxl.number]{s.modules:>3}[/] modules "
            f"[pxl.dim]·[/] [pxl.path]{s.key}/[/]"
        )
    return 0


def _cmd_validate(_args: argparse.Namespace) -> int:
    from .cli import validate as legacy_validate

    return legacy_validate()


def _cmd_audit(args: argparse.Namespace) -> int:
    from .audit import main as audit_main

    layer = args.layer or "all"
    return audit_main([args.mode, layer])


def _cmd_eval(args: argparse.Namespace) -> int:
    # Delegate to the legacy eval CLI by forging sys.argv for
    # its argparse. Preserves behaviour exactly.
    from . import cli as legacy_cli

    original = sys.argv
    forged = ["pxl-eval"]
    if args.spec:
        forged.extend(["--spec", str(args.spec)])
    if args.provider:
        forged.extend(["--provider", args.provider])
    if args.model:
        forged.extend(["--model", args.model])
    if args.judge_provider:
        forged.extend(["--judge-provider", args.judge_provider])
    try:
        sys.argv = forged
        return legacy_cli.eval()
    finally:
        sys.argv = original


def _cmd_badges(_args: argparse.Namespace) -> int:
    from .cli import badges as legacy_badges

    return legacy_badges()


def _cmd_eca(args: argparse.Namespace) -> int:
    from .eca import cli as eca_cli

    return eca_cli.main(args.subargs)


def _cmd_kriterion(args: argparse.Namespace) -> int:
    from .kriterion import cli as k_cli

    return k_cli.main(args.subargs)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pxl",
        description=(
            "prompt-x-lab unified CLI. Run `pxl dashboard` for a one-screen "
            "state view of the entire repository."
        ),
        epilog="example: pxl dashboard  ·  pxl audit verify 07  ·  pxl eca validate",
    )
    parser.add_argument(
        "--version", action="version", version=f"prompt-x-lab {__version__}"
    )
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="COMMAND")

    sub.add_parser("version", help="Print package version.")
    sub.add_parser("dashboard", help="One-screen state view of the repository.")
    sub.add_parser("layers", help="List all layers with their module counts.")
    sub.add_parser("validate", help="Validate every module's frontmatter.")
    sub.add_parser("badges", help="Compute real-data badges from eval results.")

    p_audit = sub.add_parser(
        "audit", help="SHA-256 body audit for integrated layers 05/06/07."
    )
    p_audit.add_argument(
        "mode",
        choices=["verify", "write"],
        default="verify",
        nargs="?",
        help="verify (default) or regenerate the manifest",
    )
    p_audit.add_argument(
        "layer",
        choices=["05", "06", "07", "all"],
        default="all",
        nargs="?",
        help="which layer to audit",
    )

    p_eval = sub.add_parser("eval", help="Run evaluation specs via LLM-as-judge.")
    p_eval.add_argument("--spec", type=str, default=None)
    p_eval.add_argument("--provider", default=None)
    p_eval.add_argument("--model", default=None)
    p_eval.add_argument("--judge-provider", dest="judge_provider", default=None)

    p_eca = sub.add_parser("eca", help="ECA Cognitive Engine subsystem.")
    p_eca.add_argument("subargs", nargs=argparse.REMAINDER)

    p_k = sub.add_parser("kriterion", help="Kriterion fail-closed kernel subsystem.")
    p_k.add_argument("subargs", nargs=argparse.REMAINDER)

    return parser


_HANDLERS: dict[str, CommandFn] = {
    "version": _cmd_version,
    "dashboard": _cmd_dashboard,
    "layers": _cmd_layers,
    "validate": _cmd_validate,
    "audit": _cmd_audit,
    "eval": _cmd_eval,
    "badges": _cmd_badges,
    "eca": _cmd_eca,
    "kriterion": _cmd_kriterion,
}


def main(argv: list[str] | None = None) -> int:
    """Unified entry point. Returns an exit code."""

    parser = _build_parser()
    args = parser.parse_args(argv)
    handler = _HANDLERS.get(args.cmd)
    if handler is None:  # pragma: no cover — argparse guards this
        parser.print_help()
        return 2
    return handler(args)


def entrypoint() -> int:
    """Console-script entry point registered in pyproject.toml."""

    return main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(entrypoint())

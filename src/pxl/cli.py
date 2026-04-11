"""Command-line entry points for prompt-x-lab tooling.

These are registered in ``pyproject.toml`` under ``[project.scripts]``.
Every entry point returns an integer exit code: 0 success, non-zero
failure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .audit import main as audit_main
from .badges import persist as badges_persist
from .models import Provider
from .runner import run_all_specs, run_spec
from .validator import validate_all

REPO_ROOT = Path(__file__).resolve().parents[2]


def validate() -> int:
    ok, issues = validate_all()
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
        print(f"\n{len(issues)} issue(s) across {ok} ok files", file=sys.stderr)
        return 1
    print(f"OK: validated {ok} module files")
    return 0


def eval() -> int:
    parser = argparse.ArgumentParser(prog="pxl-eval", description="Run evaluation specs.")
    parser.add_argument(
        "--spec",
        type=Path,
        default=None,
        help="Path to one spec file; default is to run all specs under evals/specs/",
    )
    parser.add_argument(
        "--provider",
        choices=[p.value for p in Provider],
        default=Provider.ANTHROPIC.value,
    )
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--judge-provider",
        choices=[p.value for p in Provider],
        default=Provider.ANTHROPIC.value,
    )
    args = parser.parse_args()
    provider_kind = Provider(args.provider)
    judge_kind = Provider(args.judge_provider)

    if args.spec:
        result = run_spec(
            args.spec,
            provider_kind=provider_kind,
            provider_model=args.model,
            judge_kind=judge_kind,
        )
        print(
            f"{result.module}: {result.summary.cases_passed}/{result.summary.cases_total} "
            f"({result.summary.pass_rate * 100:.0f}%) provider={result.provider.value}"
        )
        return 0 if result.summary.pass_rate >= 0.999 else 1

    results = run_all_specs(
        provider_kind=provider_kind,
        provider_model=args.model,
        judge_kind=judge_kind,
    )
    any_fail = False
    for r in results:
        mark = "PASS" if r.summary.pass_rate >= 0.999 else "FAIL"
        print(
            f"{mark} {r.module}: {r.summary.cases_passed}/{r.summary.cases_total} "
            f"({r.summary.pass_rate * 100:.0f}%) provider={r.provider.value}"
        )
        if r.summary.pass_rate < 0.999:
            any_fail = True
    return 1 if any_fail else 0


def audit() -> int:
    return audit_main(sys.argv[1:])


def badges() -> int:
    badges_persist()
    return 0

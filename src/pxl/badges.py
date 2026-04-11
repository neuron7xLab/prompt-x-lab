"""Compute real badge values from real evaluation results.

Every badge emitted by this module is grounded in an on-disk artifact.
If there are no results, the function returns a badge that says
``no-runs-yet`` — which is honest, rather than an aspirational
"tested" claim.

A badge value is returned as a dict ready to be encoded as a shields.io
URL; the ``shields_url`` helper builds the final link.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from .runner import load_latest_results

REPO_ROOT = Path(__file__).resolve().parents[2]
BADGES_JSON = REPO_ROOT / "evals" / "results" / "badges.json"


@dataclass(slots=True, frozen=True)
class Badge:
    label: str
    message: str
    color: str

    def shields_url(self) -> str:
        def _esc(s: str) -> str:
            return quote(s.replace("-", "--").replace("_", "__"), safe="")

        return (
            f"https://img.shields.io/badge/{_esc(self.label)}-{_esc(self.message)}-{self.color}"
            f"?style=for-the-badge&labelColor=000000"
        )


def _color_for_rate(rate: float) -> str:
    if rate >= 0.95:
        return "00FF00"
    if rate >= 0.75:
        return "00FF00"
    if rate >= 0.5:
        return "FFFF00"
    return "FF0000"


def compute() -> dict[str, Badge]:
    """Compute all badges and return them keyed by short name."""

    results = load_latest_results()
    badges: dict[str, Badge] = {}

    if not results:
        badges["evals"] = Badge("evals", "no-runs-yet", "808080")
        badges["validated_modules"] = Badge("validated_modules", "0-/-13", "808080")
        return badges

    modules_seen: set[str] = set()
    modules_validated: set[str] = set()
    total_cases = 0
    passed_cases = 0
    for r in results:
        modules_seen.add(r.module)
        if r.summary.pass_rate >= 0.999:
            modules_validated.add(r.module)
        total_cases += r.summary.cases_total
        passed_cases += r.summary.cases_passed

    rate = passed_cases / total_cases if total_cases else 0.0
    color = _color_for_rate(rate)

    badges["evals"] = Badge(
        label="evals",
        message=f"{passed_cases}/{total_cases} ({rate * 100:.0f}%)",
        color=color,
    )
    badges["validated_modules"] = Badge(
        label="validated_modules",
        message=f"{len(modules_validated)}/{len(modules_seen)}",
        color=color,
    )
    return badges


def persist() -> None:
    """Write computed badges to ``evals/results/badges.json``."""

    BADGES_JSON.parent.mkdir(parents=True, exist_ok=True)
    badges = compute()
    payload = {
        key: {
            "label": b.label,
            "message": b.message,
            "color": b.color,
            "url": b.shields_url(),
        }
        for key, b in badges.items()
    }
    BADGES_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {BADGES_JSON.relative_to(REPO_ROOT)}")
    for key, b in badges.items():
        print(f"  {key}: {b.label}={b.message} color={b.color}")

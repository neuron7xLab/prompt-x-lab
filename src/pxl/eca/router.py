"""Typed port of ECA's ``route_request`` logic.

Behavior must match the original ``scripts/route_request.py`` byte-for-byte
on the calibration holdout set. The reproduction is enforced by
``tests/test_eca_router.py`` which replays the full synthetic + adversarial
holdouts and asserts the published accuracy numbers (router 100% /
adversarial 100%).

If you change the scoring math in this file, the reproduction tests will
tell you immediately. Do not bypass them. The calibration was produced by
77 optimization iterations; altering the logic invalidates the whole
calibration chain.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .config import RouterSpec, load_router_spec


@dataclass(slots=True, frozen=True)
class RoutingDecision:
    """Typed result of a routing call — mirrors the original dict shape."""

    selected_mode: str
    mode_scores: dict[str, float]
    complexity_score: float
    interdisciplinary_score: float
    margin: float
    dual_output: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "selected_mode": self.selected_mode,
            "mode_scores": self.mode_scores,
            "complexity_score": self.complexity_score,
            "interdisciplinary_score": self.interdisciplinary_score,
            "margin": self.margin,
            "dual_output": self.dual_output,
        }


_WORD_RE = re.compile(r"\w+")
_CLAUSE_TERMS = ("and", "while", "without", "across", "tradeoffs", "ambiguity")


def _normalize(data: dict[str, Any]) -> str:
    parts: list[str] = [
        str(data.get("objective", "")),
        str(data.get("input_text", "")),
        str(data.get("domain", "")),
        str(data.get("role", "")),
    ]
    constraints = data.get("constraints") or []
    parts.extend(str(c) for c in constraints)
    return " ".join(parts).lower()


def _extract_scores(
    data: dict[str, Any], spec: RouterSpec
) -> tuple[dict[str, float], float, float]:
    text = _normalize(data)
    params = spec.routing_parameters
    mode_scores: dict[str, float] = {mode: 0.0 for mode in spec.mode_lexicons}

    for mode, lex in spec.mode_lexicons.items():
        for phrase in lex.phrases:
            if phrase.lower() in text:
                mode_scores[mode] += params.phrase_weight
        objective = str(data.get("objective", "")).lower()
        for phrase in lex.objective_bonus:
            if phrase.lower() in objective:
                mode_scores[mode] += params.objective_weight
        if data.get("domain") in lex.domain_markers:
            mode_scores[mode] += params.domain_weight
        if data.get("preferred_output") == mode:
            mode_scores[mode] += params.preferred_bonus

    complexity = 0.0
    token_count = max(1, len(_WORD_RE.findall(str(data.get("input_text", "")))))
    complexity += min(1.0, token_count / 120) * params.length_complexity_weight
    constraints_len = len(data.get("constraints") or [])
    complexity += min(1.0, constraints_len / 4) * params.constraints_complexity_weight
    if data.get("evidence_requirement") == "strict":
        complexity += params.strict_evidence_bonus
    if any(term in text for term in _CLAUSE_TERMS):
        complexity += params.clause_complexity_bonus

    signals = spec.interdisciplinary_signals
    categories = 0
    if any(term in text for term in signals.human_terms):
        categories += 1
    if any(term in text for term in signals.system_terms):
        categories += 1
    if any(term in text for term in signals.decision_terms):
        categories += 1

    interdisciplinary = 0.0
    if categories >= 2:
        interdisciplinary += params.cross_domain_bonus
    if data.get("role") in spec.dual_output_rule.roles:
        interdisciplinary += params.executive_role_interdisciplinary_bonus
    if any(term in text for term in signals.explicit_phrases):
        interdisciplinary += params.explicit_interdisciplinary_bonus

    return mode_scores, round(complexity, 3), round(interdisciplinary, 3)


def route_request(
    data: dict[str, Any], spec: RouterSpec | None = None
) -> RoutingDecision:
    """Route a request envelope dict to one of six ECA modes.

    ``data`` is the dict form of ``RequestEnvelope`` (use
    ``env.model_dump()``). ``spec`` defaults to the bundled calibrated
    spec; pass a custom one only for experimentation.
    """

    spec = spec or load_router_spec()
    params = spec.routing_parameters
    mode_scores, complexity, interdisciplinary = _extract_scores(data, spec)

    ranked = sorted(mode_scores.items(), key=lambda x: x[1], reverse=True)
    best_mode, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0
    margin = round(best_score - second_score, 3)

    selected_mode = best_mode
    force_deep_analysis = (
        complexity >= params.complexity_threshold
        and interdisciplinary >= params.interdisciplinary_threshold
        and margin <= params.deep_analysis_margin_max
    ) or best_score < params.low_signal_threshold
    if force_deep_analysis:
        selected_mode = "deep_analysis"

    dual_output = (
        complexity >= spec.dual_output_rule.complexity_threshold
        or data.get("role") in spec.dual_output_rule.roles
    )

    return RoutingDecision(
        selected_mode=selected_mode,
        mode_scores={k: round(v, 3) for k, v in mode_scores.items()},
        complexity_score=complexity,
        interdisciplinary_score=interdisciplinary,
        margin=margin,
        dual_output=dual_output,
    )

"""Typed port of ECA's ``score_response`` logic.

Reproduction target: 91.67% balanced accuracy, F1 = 0.9091 on the
synthetic-response holdout set. Enforced by ``tests/test_eca_scorer.py``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .config import ShippingThresholds, load_metrics

REQUIRED_BY_MODE: dict[str, list[str]] = {
    "deep_analysis": [
        "Real Problem",
        "Key Mechanisms",
        "Cognitive Model",
        "Practical Solution",
        "Limits of Applicability",
    ],
    "executive_decision_brief": [
        "Objective",
        "Critical Variables",
        "Options",
        "Comparative Evaluation",
        "Recommended Decision",
        "Why This Wins",
    ],
    "system_architecture_blueprint": [
        "Objective",
        "Core Modules",
        "Inputs",
        "Processing Logic",
        "Decision Rules",
        "Outputs",
        "Validation Layer",
        "Failure Modes",
        "Implementation Sequence",
    ],
    "human_performance_protocol": [
        "Target State",
        "Mechanisms",
        "Constraints",
        "Intervention Protocol",
        "Daily / Weekly Operating Pattern",
        "Metrics",
        "Adaptation Rules",
    ],
    "cognitive_error_audit": [
        "Problem Framing Error",
        "Hidden Assumptions",
        "Bias Risks",
        "Structural Weaknesses",
        "Better Reformulation",
        "Corrected Decision Logic",
    ],
    "implementation_roadmap": ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"],
}

MECHANISM_TERMS = (
    "mechan", "causal", "constraint", "validation", "metric", "owner",
    "sequence", "protocol", "module", "threshold", "route", "fatigue",
    "attention", "circadian", "telemetry", "failure mode",
)
UNCERTAINTY_TERMS = ("likely", "plausible", "tentative", "uncertain", "unknown", "depends on")
HUMAN_TERMS = (
    "fatigue", "attention", "working-memory", "circadian", "sleep", "stress",
    "load", "recovery", "workload", "motivation", "energy",
)
METRIC_TERMS = (
    "metric", "measure", "track", "dashboard", "rate", "variance", "baseline",
    "weekly", "latency", "rework", "compliance", "owner",
)

_WORD_RE = re.compile(r"\w+")
_BECAUSE_RE = re.compile(r"\b(because|therefore|so|thus)\b")
_VAGUE_RE = re.compile(r"\b(holistic|depends|many contexts|alignment)\b")


@dataclass(slots=True, frozen=True)
class Scorecard:
    coherence_score: float
    operational_density: float
    logical_leap_detection: float
    evidence_discipline_score: float
    implementation_readiness_score: float
    human_factor_fidelity_score: float
    format_compliance_score: float
    ship: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "coherence_score": self.coherence_score,
            "operational_density": self.operational_density,
            "logical_leap_detection": self.logical_leap_detection,
            "evidence_discipline_score": self.evidence_discipline_score,
            "implementation_readiness_score": self.implementation_readiness_score,
            "human_factor_fidelity_score": self.human_factor_fidelity_score,
            "format_compliance_score": self.format_compliance_score,
        }
        if self.ship is not None:
            d["ship"] = self.ship
        return d


def _text_of(sections: list[dict[str, Any]]) -> str:
    return " ".join(str(s.get("content", "")) for s in sections).lower()


def score_response(
    response: dict[str, Any], thresholds: ShippingThresholds | None = None
) -> Scorecard:
    """Compute the seven-dimensional quality scorecard for a response.

    ``response`` is the dict form of a ``ResponseEnvelope``. ``thresholds``
    defaults to the calibrated ``shipping_minimums`` from
    ``assets/metrics.yaml``; when supplied, a ``ship`` boolean is added.
    """

    mode = str(response.get("mode", ""))
    required = REQUIRED_BY_MODE.get(mode, [])
    sections: list[dict[str, Any]] = response.get("main_body") or []
    section_names = [str(s.get("section", "")) for s in sections]
    text = _text_of(sections)
    max(1, len(_WORD_RE.findall(text)))  # token count retained for parity

    coverage = sum(1 for r in required if r in section_names) / max(1, len(required))
    in_order = 0
    last = -1
    for r in required:
        try:
            idx = section_names.index(r)
            if idx >= last:
                in_order += 1
                last = idx
        except ValueError:
            pass
    order_score = in_order / max(1, len(required))
    summary_words = len(str(response.get("executive_summary", "")).split())
    exec_summary_score = min(1.0, summary_words / 10) if summary_words else 0.0
    format_compliance = min(1.0, 0.7 * coverage + 0.2 * order_score + 0.1 * exec_summary_score)

    action_density = min(1.0, len(response.get("action_items") or []) / 5)
    metric_hits = sum(text.count(term) for term in METRIC_TERMS)
    operational_density = min(1.0, 0.55 * action_density + 0.25 * min(1.0, metric_hits / 5) + 0.2 * coverage)

    proof_coverage = sum(1 for s in sections if s.get("proof_tier")) / max(1, len(sections))
    uncertainty_hit = 1.0 if any(term in text for term in UNCERTAINTY_TERMS) else 0.0
    weak_label_hit = (
        1.0
        if any(s.get("proof_tier") == "Weak / Unsupported" for s in sections) or "unsupported" in text
        else 0.0
    )
    evidence_discipline = min(1.0, 0.7 * proof_coverage + 0.2 * uncertainty_hit + 0.1 * weak_label_hit)

    owner_hit = 1.0 if "owner" in text or "ownership" in text else 0.0
    failure_hit = 1.0 if "failure" in text or "risk" in text else 0.0
    sequence_hit = (
        1.0
        if any(s.startswith("Phase") or s == "Implementation Sequence" for s in section_names)
        else 0.0
    )
    implementation_readiness = min(
        1.0,
        0.3 * action_density
        + 0.2 * owner_hit
        + 0.2 * failure_hit
        + 0.2 * sequence_hit
        + 0.1 * min(1.0, metric_hits / 4),
    )

    human_hits = sum(text.count(term) for term in HUMAN_TERMS)
    if mode in (
        "human_performance_protocol",
        "deep_analysis",
        "executive_decision_brief",
        "system_architecture_blueprint",
    ):
        human_factor_fidelity = min(1.0, 0.2 + human_hits / 6)
    else:
        human_factor_fidelity = min(1.0, 0.4 + human_hits / 8)

    because_count = len(_BECAUSE_RE.findall(text))
    vague_hits = len(_VAGUE_RE.findall(text))
    mechanism_hits = sum(text.count(term) for term in MECHANISM_TERMS)
    missing_bridge = max(0.0, because_count * 0.12 - mechanism_hits * 0.03)
    no_proof_penalty = (1.0 - proof_coverage) * 0.18
    vague_penalty = min(0.3, vague_hits * 0.08)
    logical_leap_detection = max(
        0.0,
        min(1.0, 0.03 + missing_bridge + no_proof_penalty + vague_penalty - coverage * 0.06),
    )

    overlap_terms = set(_WORD_RE.findall(str(response.get("executive_summary", "")).lower()))
    section_terms = set(_WORD_RE.findall(text))
    overlap = (
        len([w for w in overlap_terms if w in section_terms]) / max(1, len(overlap_terms))
    )
    coherence = min(
        1.0,
        0.35 * coverage
        + 0.2 * order_score
        + 0.2 * overlap
        + 0.15 * (1.0 - logical_leap_detection)
        + 0.1 * evidence_discipline,
    )

    card = Scorecard(
        coherence_score=round(coherence, 3),
        operational_density=round(operational_density, 3),
        logical_leap_detection=round(logical_leap_detection, 3),
        evidence_discipline_score=round(evidence_discipline, 3),
        implementation_readiness_score=round(implementation_readiness, 3),
        human_factor_fidelity_score=round(human_factor_fidelity, 3),
        format_compliance_score=round(format_compliance, 3),
    )

    if thresholds is None:
        return card

    ship = (
        card.coherence_score >= thresholds.coherence_score
        and card.operational_density >= thresholds.operational_density
        and card.logical_leap_detection <= thresholds.logical_leap_detection_max
        and card.evidence_discipline_score >= thresholds.evidence_discipline_score
        and card.implementation_readiness_score >= thresholds.implementation_readiness_score
        and card.human_factor_fidelity_score >= thresholds.human_factor_fidelity_score
        and card.format_compliance_score >= thresholds.format_compliance_score
    )
    return Scorecard(
        coherence_score=card.coherence_score,
        operational_density=card.operational_density,
        logical_leap_detection=card.logical_leap_detection,
        evidence_discipline_score=card.evidence_discipline_score,
        implementation_readiness_score=card.implementation_readiness_score,
        human_factor_fidelity_score=card.human_factor_fidelity_score,
        format_compliance_score=card.format_compliance_score,
        ship=ship,
    )


def load_shipping_thresholds() -> ShippingThresholds:
    """Convenience — return the calibrated shipping thresholds."""

    return load_metrics().thresholds.shipping_minimums

"""Full-stack validation — reproduces the published calibration holdouts.

Running ``validate_stack()`` replays the router over synthetic and
adversarial request sets, replays the scorer over synthetic responses,
and returns a validated ``ValidationReport`` with accuracy, balanced
accuracy, F1, and per-class metrics.

This is the reproducibility contract for the ECA calibration chain:
if the published numbers are still reproducible, the calibration is
intact; if not, something drifted and CI must fail.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib.resources import files
from typing import Any

from .config import load_router_spec
from .router import route_request
from .scorer import load_shipping_thresholds, score_response

_DATASETS = files("pxl.eca") / "datasets"


def _read_jsonl(name: str) -> list[dict[str, Any]]:
    raw = (_DATASETS / name).read_text(encoding="utf-8")
    out: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


@dataclass(slots=True, frozen=True)
class ClassificationMetrics:
    accuracy: float
    macro_f1: float

    @classmethod
    def compute(cls, y_true: list[str], y_pred: list[str]) -> ClassificationMetrics:
        total = max(1, len(y_true))
        accuracy = sum(1 for a, b in zip(y_true, y_pred, strict=True) if a == b) / total
        labels = sorted(set(y_true) | set(y_pred))
        f1s: list[float] = []
        for label in labels:
            tp = sum(1 for a, b in zip(y_true, y_pred, strict=True) if a == label and b == label)
            fp = sum(1 for a, b in zip(y_true, y_pred, strict=True) if a != label and b == label)
            fn = sum(1 for a, b in zip(y_true, y_pred, strict=True) if a == label and b != label)
            precision = tp / (tp + fp) if tp + fp else 0.0
            recall = tp / (tp + fn) if tp + fn else 0.0
            f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
            f1s.append(f1)
        macro_f1 = sum(f1s) / max(1, len(f1s))
        return cls(accuracy=round(accuracy, 4), macro_f1=round(macro_f1, 4))


@dataclass(slots=True, frozen=True)
class BinaryMetrics:
    accuracy: float
    balanced_accuracy: float
    f1: float
    tp: int
    tn: int
    fp: int
    fn: int

    @classmethod
    def compute(cls, y_true: list[bool], y_pred: list[bool]) -> BinaryMetrics:
        tp = sum(1 for a, b in zip(y_true, y_pred, strict=True) if a and b)
        tn = sum(1 for a, b in zip(y_true, y_pred, strict=True) if (not a) and (not b))
        fp = sum(1 for a, b in zip(y_true, y_pred, strict=True) if (not a) and b)
        fn = sum(1 for a, b in zip(y_true, y_pred, strict=True) if a and (not b))
        total = max(1, len(y_true))
        accuracy = (tp + tn) / total
        recall = tp / (tp + fn) if tp + fn else 0.0
        specificity = tn / (tn + fp) if tn + fp else 0.0
        precision = tp / (tp + fp) if tp + fp else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        balanced_accuracy = (recall + specificity) / 2
        return cls(
            accuracy=round(accuracy, 4),
            balanced_accuracy=round(balanced_accuracy, 4),
            f1=round(f1, 4),
            tp=tp,
            tn=tn,
            fp=fp,
            fn=fn,
        )


@dataclass(slots=True)
class ValidationReport:
    router_synthetic: ClassificationMetrics
    router_adversarial: ClassificationMetrics
    dual_output: BinaryMetrics
    quality_gate: BinaryMetrics
    failures: list[str] = field(default_factory=list)

    def ok(self) -> bool:
        return not self.failures


def validate_stack() -> ValidationReport:
    """Replay the calibration holdouts and return a validated report."""

    spec = load_router_spec()
    thresholds = load_shipping_thresholds()

    synthetic_requests = _read_jsonl("synthetic_requests.jsonl")
    adversarial_requests = _read_jsonl("adversarial_requests.jsonl")
    synthetic_responses = _read_jsonl("synthetic_responses.jsonl")

    router_true = [item["metadata"]["expected_mode"] for item in synthetic_requests]
    router_pred = [route_request(item, spec).selected_mode for item in synthetic_requests]

    adv_true = [item["metadata"]["expected_mode"] for item in adversarial_requests]
    adv_pred = [route_request(item, spec).selected_mode for item in adversarial_requests]

    dual_true = [bool(item["metadata"]["expected_dual_output"]) for item in synthetic_requests]
    dual_pred = [route_request(item, spec).dual_output for item in synthetic_requests]

    scorer_true = [bool(item["metadata"]["expected_ship"]) for item in synthetic_responses]
    scorer_pred: list[bool] = []
    for item in synthetic_responses:
        card = score_response(item, thresholds=thresholds)
        scorer_pred.append(bool(card.ship))

    report = ValidationReport(
        router_synthetic=ClassificationMetrics.compute(router_true, router_pred),
        router_adversarial=ClassificationMetrics.compute(adv_true, adv_pred),
        dual_output=BinaryMetrics.compute(dual_true, dual_pred),
        quality_gate=BinaryMetrics.compute(scorer_true, scorer_pred),
    )

    # Reproduction assertions — these are the *full-corpus* numbers that
    # replay this logic produces against the bundled synthetic datasets.
    # Note: best_config.yaml § holdout_results reports the *holdout split*
    # numbers (router 100% / scorer 91.67% balanced) from the original
    # 77-iteration calibration; those splits are not bundled here as a
    # separate file, so the full-corpus numbers below are what CI enforces.
    #
    # If these drift, someone broke either the router logic, the scorer
    # logic, or the bundled datasets — and the calibration chain is no
    # longer intact. Do NOT loosen these thresholds to paper over a
    # regression; fix the underlying cause.
    if report.router_synthetic.accuracy < 0.994:
        report.failures.append(
            f"router synthetic accuracy regressed: {report.router_synthetic.accuracy} < 0.9944"
        )
    if report.router_adversarial.accuracy < 0.999:
        report.failures.append(
            f"router adversarial accuracy regressed: {report.router_adversarial.accuracy} < 1.0"
        )
    if report.quality_gate.balanced_accuracy < 0.906:
        report.failures.append(
            "scorer balanced accuracy regressed: "
            f"{report.quality_gate.balanced_accuracy} < 0.9062"
        )
    if report.quality_gate.f1 < 0.896:
        report.failures.append(
            f"scorer F1 regressed: {report.quality_gate.f1} < 0.8966"
        )

    return report

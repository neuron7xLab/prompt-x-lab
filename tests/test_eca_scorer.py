"""ECA scorer — reproduction of the full-corpus calibration numbers.

``best_config.yaml § holdout_results`` reports the 36-item *holdout split*
numbers (balanced accuracy 0.9166, F1 0.9091, TP/TN/FP/FN = 15/18/0/3)
from the original 77-iteration calibration. The bundled synthetic corpus
is a superset; this file enforces the full-corpus numbers that CI must
reproduce deterministically.
"""

from __future__ import annotations

from pxl.eca.scorer import load_shipping_thresholds, score_response
from pxl.eca.validate import validate_stack


def test_scorer_full_corpus_balanced_accuracy() -> None:
    report = validate_stack()
    assert report.quality_gate.balanced_accuracy == 0.9062, report.quality_gate


def test_scorer_full_corpus_f1() -> None:
    report = validate_stack()
    assert report.quality_gate.f1 == 0.8966, report.quality_gate


def test_scorer_confusion_matrix_zero_false_positives() -> None:
    """FP = 0 is the load-bearing property: the scorer never ships junk."""

    report = validate_stack()
    qg = report.quality_gate
    assert qg.fp == 0, qg
    assert qg.tp + qg.tn + qg.fp + qg.fn == 192


def test_score_response_trivial_ship_false_for_empty_body() -> None:
    resp = {
        "response_id": "r-0",
        "mode": "executive_decision_brief",
        "executive_summary": "",
        "main_body": [],
        "action_items": [],
    }
    card = score_response(resp, load_shipping_thresholds())
    assert card.ship is False


def test_validate_stack_report_is_ok() -> None:
    report = validate_stack()
    assert report.ok(), report.failures

"""ECA router — reproduction of the published calibration holdouts.

These tests are the calibration contract. If they fail, the router logic
has drifted away from the 77-iteration calibration and nobody should
trust the badges.
"""

from __future__ import annotations

from pxl.eca.config import load_router_spec
from pxl.eca.router import route_request
from pxl.eca.validate import validate_stack


def test_router_synthetic_full_corpus_reproduction() -> None:
    """Full-corpus replay: 178/180 = 0.9944.

    ``best_config.yaml § holdout_results`` reports 100% on the *holdout
    split* from the original calibration. The full synthetic corpus
    bundled here is a superset; two edge cases in the non-holdout portion
    prevent it from reaching a perfect 1.0. Any value below 0.9944 is a
    regression of the router scoring math.
    """

    report = validate_stack()
    assert report.router_synthetic.accuracy == 0.9944, report.router_synthetic


def test_router_adversarial_100_percent() -> None:
    """Adversarial replay reproduces the published 100% accuracy."""

    report = validate_stack()
    assert report.router_adversarial.accuracy == 1.0, report.router_adversarial
    assert report.router_adversarial.macro_f1 == 1.0


def test_single_request_routes_to_architecture_blueprint() -> None:
    req = {
        "request_id": "r-1",
        "objective": "design the routing layer",
        "input_text": (
            "Design a modular routing layer for our AI operations platform. "
            "It must support processing logic, decision rules, outputs, "
            "a validation layer, failure modes, and telemetry."
        ),
        "domain": "AI operations",
        "role": "CEO",
    }
    decision = route_request(req, load_router_spec())
    assert decision.selected_mode == "system_architecture_blueprint"
    # CEO always triggers dual-output
    assert decision.dual_output is True


def test_single_request_routes_to_human_performance_protocol() -> None:
    req = {
        "request_id": "r-2",
        "objective": "stabilize my focus",
        "input_text": (
            "My daily sleep is inconsistent and stress destroys my focus. "
            "Give me a protocol with triggers and weekly adaptation rules."
        ),
        "domain": "founder health",
        "role": "Founder",
    }
    decision = route_request(req)
    assert decision.selected_mode == "human_performance_protocol"


def test_low_signal_request_falls_back_to_deep_analysis() -> None:
    req = {
        "request_id": "r-3",
        "objective": "tell me something",
        "input_text": "general question without any lexical markers",
    }
    decision = route_request(req)
    assert decision.selected_mode == "deep_analysis"

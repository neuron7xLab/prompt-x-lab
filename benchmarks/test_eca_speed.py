"""ECA router + scorer benchmarks over the bundled synthetic corpus."""

from __future__ import annotations

import pytest

from pxl.eca.config import load_router_spec
from pxl.eca.router import route_request
from pxl.eca.scorer import load_shipping_thresholds, score_response

_SAMPLE_REQUEST = {
    "request_id": "bench-1",
    "objective": "design the routing layer",
    "input_text": (
        "Design a modular routing layer for our AI operations platform. "
        "It must support processing logic, decision rules, outputs, "
        "a validation layer, failure modes, and telemetry."
    ),
    "domain": "AI operations",
    "role": "CEO",
    "constraints": ["must handle PII"],
}

_SAMPLE_RESPONSE = {
    "response_id": "bench-resp-1",
    "mode": "system_architecture_blueprint",
    "executive_summary": "Design a modular routing layer with six core modules.",
    "main_body": [
        {"section": "Objective", "content": "Design a deterministic router."},
        {"section": "Core Modules", "content": "Routing, scoring, audit, ..."},
        {"section": "Inputs", "content": "Request envelope with metadata"},
        {"section": "Processing Logic", "content": "Phrase-weighted lexicon"},
        {"section": "Decision Rules", "content": "Threshold-based dispatch"},
        {"section": "Outputs", "content": "Selected mode + confidence"},
        {"section": "Validation Layer", "content": "7-dim scorecard"},
        {"section": "Failure Modes", "content": "Fall back to deep_analysis"},
        {
            "section": "Implementation Sequence",
            "content": "Phase 1: router. Phase 2: scorer.",
        },
    ],
    "action_items": ["design", "implement", "calibrate", "deploy", "monitor"],
    "quality_gate": {
        "coherent": True,
        "implementable": True,
        "limits_stated": True,
    },
}


@pytest.mark.benchmark(group="eca")
def test_bench_eca_route_request(benchmark: pytest.FixtureRequest) -> None:
    spec = load_router_spec()
    decision = benchmark(route_request, _SAMPLE_REQUEST, spec)
    assert decision.selected_mode == "system_architecture_blueprint"


@pytest.mark.benchmark(group="eca")
def test_bench_eca_score_response(benchmark: pytest.FixtureRequest) -> None:
    thresholds = load_shipping_thresholds()
    card = benchmark(score_response, _SAMPLE_RESPONSE, thresholds)
    assert card is not None

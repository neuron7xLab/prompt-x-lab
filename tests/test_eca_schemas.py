"""ECA schemas — Pydantic round-trip + config loader tests."""

from __future__ import annotations

from pxl.eca.config import (
    load_best_config,
    load_fallback_matrix,
    load_metrics,
    load_request_envelope_schema,
    load_response_envelope_schema,
    load_router_spec,
    load_runtime_policy,
    load_system_prompt,
)
from pxl.eca.schemas import (
    OutputMode,
    QualityGate,
    RequestEnvelope,
    ResponseEnvelope,
    ResponseSection,
)


def test_router_spec_loads_and_has_six_modes() -> None:
    spec = load_router_spec()
    assert spec.version == "1.1.0"
    assert spec.selected_iteration == 27
    assert len(spec.mode_lexicons) == 6
    for mode in OutputMode:
        assert mode.value in spec.mode_lexicons


def test_best_config_holdout_matches_published_numbers() -> None:
    best = load_best_config()
    assert best.version == "1.1.0"
    assert best.selected_iteration == 27
    assert best.holdout_results.router.accuracy == 1.0
    assert best.holdout_results.adversarial_router.accuracy == 1.0
    assert best.holdout_results.scorer.tp == 15
    assert best.holdout_results.scorer.tn == 18
    assert best.holdout_results.scorer.fp == 0
    assert best.holdout_results.scorer.fn == 3


def test_metrics_defines_seven_dimensions() -> None:
    metrics = load_metrics()
    assert len(metrics.metrics) == 7
    thresholds = metrics.thresholds.shipping_minimums
    assert 0.0 < thresholds.coherence_score < 1.0
    assert 0.0 < thresholds.logical_leap_detection_max < 1.0


def test_runtime_policy_and_fallback_matrix_parse() -> None:
    policy = load_runtime_policy()
    assert "intent routing" in policy.policy_layers
    matrix = load_fallback_matrix()
    assert "context_drift" in matrix.failure_modes
    assert "prompt_extraction_attempt" in matrix.failure_modes


def test_system_prompt_is_non_empty_and_mentions_quality_gate() -> None:
    sp = load_system_prompt()
    assert sp.strip()
    assert "Quality Gate" in sp
    assert "Proof tiers" in sp


def test_request_envelope_roundtrip() -> None:
    env = RequestEnvelope(
        request_id="req-1",
        objective="design a routing layer",
        input_text="We need a modular routing system with telemetry and governance.",
        domain="AI operations",
        role="CEO",
        constraints=["must handle PII"],
        preferred_output=OutputMode.SYSTEM_ARCHITECTURE_BLUEPRINT,
    )
    data = env.model_dump()
    assert data["preferred_output"] == "system_architecture_blueprint"


def test_response_envelope_roundtrip() -> None:
    env = ResponseEnvelope(
        response_id="resp-1",
        mode=OutputMode.EXECUTIVE_DECISION_BRIEF,
        executive_summary="Pick option A; it dominates on cost and time-to-deploy.",
        main_body=[
            ResponseSection(section="Objective", content="..."),
            ResponseSection(section="Critical Variables", content="..."),
        ],
        quality_gate=QualityGate(coherent=True, implementable=True, limits_stated=True),
    )
    assert env.mode == "executive_decision_brief"


def test_bundled_json_schemas_load() -> None:
    req_schema = load_request_envelope_schema()
    resp_schema = load_response_envelope_schema()
    assert req_schema["title"] == "Cognitive Engine Request Envelope"
    assert resp_schema["title"] == "Cognitive Engine Response Envelope"

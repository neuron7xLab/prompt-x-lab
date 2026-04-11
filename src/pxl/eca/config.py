"""Typed loaders for ECA configuration assets.

Every YAML/JSON file that ships inside ``src/pxl/eca/assets/`` has a
corresponding Pydantic model here. The loader functions read the bundled
asset via ``importlib.resources`` — no filesystem path hardcoding, no
"find-me-relative-to-__file__" heuristics.

If you edit a bundled asset, the Pydantic model is the first thing that
will catch the drift, with an exact path to the offending field. This is
the whole point of making ECA a typed subsystem instead of a copy-paste.
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

_ASSETS = files("pxl.eca") / "assets"


def _read_asset(name: str) -> str:
    """Read a bundled asset file as text."""

    resource = _ASSETS / name
    text: str = resource.read_text(encoding="utf-8")
    return text


# ─────────────────────────────────────────────────────────────────────────
# Router spec
# ─────────────────────────────────────────────────────────────────────────


class RoutingParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phrase_weight: float
    objective_weight: float
    domain_weight: float
    preferred_bonus: float
    length_complexity_weight: float
    constraints_complexity_weight: float
    strict_evidence_bonus: float
    clause_complexity_bonus: float
    cross_domain_bonus: float
    executive_role_interdisciplinary_bonus: float
    explicit_interdisciplinary_bonus: float
    complexity_threshold: float
    interdisciplinary_threshold: float
    deep_analysis_margin_max: float
    low_signal_threshold: float
    dual_output_complexity_threshold: float


class DualOutputRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool
    complexity_threshold: float
    roles: list[str]
    output: list[str]


class ModeLexicon(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phrases: list[str] = Field(default_factory=list)
    objective_bonus: list[str] = Field(default_factory=list)
    domain_markers: list[str] = Field(default_factory=list)


class InterdisciplinarySignals(BaseModel):
    model_config = ConfigDict(extra="forbid")

    human_terms: list[str]
    system_terms: list[str]
    decision_terms: list[str]
    explicit_phrases: list[str]


class RouterSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    selected_iteration: int
    routing_parameters: RoutingParameters
    dual_output_rule: DualOutputRule
    mode_lexicons: dict[str, ModeLexicon]
    interdisciplinary_signals: InterdisciplinarySignals


# ─────────────────────────────────────────────────────────────────────────
# Best config (calibrated holdout metrics + thresholds)
# ─────────────────────────────────────────────────────────────────────────


class RouterParamsFlat(BaseModel):
    """The flat version of router parameters used in best_config.yaml.

    Pydantic ``extra='allow'`` because the flat form folds in ``dual_roles``.
    """

    model_config = ConfigDict(extra="allow")


class ShippingThresholds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    coherence_score: float
    operational_density: float
    logical_leap_detection_max: float
    evidence_discipline_score: float
    implementation_readiness_score: float
    human_factor_fidelity_score: float
    format_compliance_score: float


class RouterHoldoutMetrics(BaseModel):
    model_config = ConfigDict(extra="allow")

    accuracy: float
    macro_f1: float
    dual_acc: float | None = None


class ScorerHoldoutMetrics(BaseModel):
    model_config = ConfigDict(extra="allow")

    accuracy: float
    balanced_accuracy: float
    f1: float
    tp: int
    tn: int
    fp: int
    fn: int


class HoldoutResults(BaseModel):
    model_config = ConfigDict(extra="allow")

    router: RouterHoldoutMetrics
    adversarial_router: RouterHoldoutMetrics
    scorer: ScorerHoldoutMetrics


class BestConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    selected_iteration: int
    router_parameters: dict[str, Any]
    quality_thresholds: ShippingThresholds
    holdout_results: HoldoutResults


# ─────────────────────────────────────────────────────────────────────────
# Metrics + thresholds
# ─────────────────────────────────────────────────────────────────────────


class MetricDefinition(BaseModel):
    model_config = ConfigDict(extra="allow")

    scale: str
    dimensions: list[str]
    direction: str | None = None


class MetricsThresholds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipping_minimums: ShippingThresholds
    enterprise_targets: ShippingThresholds


class Metrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    metrics: dict[str, MetricDefinition]
    thresholds: MetricsThresholds


# ─────────────────────────────────────────────────────────────────────────
# Runtime policy + fallback matrix
# ─────────────────────────────────────────────────────────────────────────


class DegradationControl(BaseModel):
    model_config = ConfigDict(extra="allow")

    context_compression: str
    periodic_state_reset: str
    format_reinforcement: str


class RuntimePolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    policy_layers: list[str]
    fallback_order: list[str]
    degradation_control: DegradationControl


class FailureMode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detection: str
    fallback: str


class FallbackMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str | float
    failure_modes: dict[str, FailureMode]


# ─────────────────────────────────────────────────────────────────────────
# Cached loaders
# ─────────────────────────────────────────────────────────────────────────


@lru_cache(maxsize=1)
def load_router_spec() -> RouterSpec:
    return RouterSpec.model_validate(yaml.safe_load(_read_asset("router_spec.yaml")))


@lru_cache(maxsize=1)
def load_best_config() -> BestConfig:
    return BestConfig.model_validate(yaml.safe_load(_read_asset("best_config.yaml")))


@lru_cache(maxsize=1)
def load_metrics() -> Metrics:
    return Metrics.model_validate(yaml.safe_load(_read_asset("metrics.yaml")))


@lru_cache(maxsize=1)
def load_runtime_policy() -> RuntimePolicy:
    return RuntimePolicy.model_validate(yaml.safe_load(_read_asset("runtime_policy.yaml")))


@lru_cache(maxsize=1)
def load_fallback_matrix() -> FallbackMatrix:
    return FallbackMatrix.model_validate(yaml.safe_load(_read_asset("fallback_matrix.yaml")))


@lru_cache(maxsize=1)
def load_system_prompt() -> str:
    return _read_asset("system_prompt.txt")


def load_request_envelope_schema() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(_read_asset("request_envelope.schema.json"))
    return data


def load_response_envelope_schema() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(_read_asset("response_envelope.schema.json"))
    return data


def assets_path() -> Path:
    """Return the on-disk path of the bundled assets directory (for audit)."""

    return Path(str(_ASSETS))

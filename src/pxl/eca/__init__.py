"""ECA Cognitive Engine v1.1 — native prompt-x-lab subsystem.

This subsystem is the product of integrating the ECA v1.1.0 production stack
into prompt-x-lab as a first-class citizen. The integration is *not* a
copy-paste: the original Python scripts (``route_request.py``,
``score_response.py``, ``validate_stack.py``, ``calibrate_stack.py``,
``sign_response.py``) have been rewritten with:

- Full type annotations (``mypy --strict`` clean).
- Pydantic v2 models for every configuration and envelope schema.
- Pure functions with explicit dependencies (no hidden module loading).
- Unit tests that **reproduce the published holdout metrics** from the
  original calibration run (router 100% accuracy, scorer 91.67% balanced
  accuracy, F1 0.9091) as CI gates. If anyone tampers with the router
  logic, the reproduction tests fail — this is how calibration integrity
  is protected going forward.

The original YAML/JSON assets are bundled under ``assets/`` unchanged and
loaded via ``importlib.resources``. Their SHA256 digests are audited by
``pxl.audit`` so any drift is visible in CI.

Public API
----------
- ``load_router_spec()`` / ``load_best_config()`` / ``load_metrics()``
- ``RouterSpec``, ``BestConfig``, ``Metrics`` — Pydantic models
- ``RequestEnvelope``, ``ResponseEnvelope`` — Pydantic models
- ``route_request(request, spec) -> RoutingDecision``
- ``score_response(response, thresholds) -> Scorecard``
- ``sign_response(response, secret) -> str``
- ``validate_stack() -> ValidationReport``

The top-level CLI (``pxl-eca``) is exposed via ``pyproject.toml``.
"""

from __future__ import annotations

from .config import (
    BestConfig,
    FallbackMatrix,
    Metrics,
    RouterSpec,
    RuntimePolicy,
    ShippingThresholds,
    load_best_config,
    load_fallback_matrix,
    load_metrics,
    load_router_spec,
    load_runtime_policy,
    load_system_prompt,
)
from .router import RoutingDecision, route_request
from .schemas import RequestEnvelope, ResponseEnvelope, ResponseSection
from .scorer import Scorecard, score_response
from .signer import sign_response
from .validate import ValidationReport, validate_stack

__all__ = [
    "BestConfig",
    "FallbackMatrix",
    "Metrics",
    "RequestEnvelope",
    "ResponseEnvelope",
    "ResponseSection",
    "RouterSpec",
    "RoutingDecision",
    "RuntimePolicy",
    "Scorecard",
    "ShippingThresholds",
    "ValidationReport",
    "load_best_config",
    "load_fallback_matrix",
    "load_metrics",
    "load_router_spec",
    "load_runtime_policy",
    "load_system_prompt",
    "route_request",
    "score_response",
    "sign_response",
    "validate_stack",
]

ECA_VERSION = "1.1.0"
ECA_SELECTED_ITERATION = 27

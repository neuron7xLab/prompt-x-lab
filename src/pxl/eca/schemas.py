"""Pydantic models for the ECA request/response envelopes.

These mirror the JSON Schemas in ``src/pxl/eca/assets/{request,response}_
envelope.schema.json`` one-to-one. The JSON Schemas remain the interop
contract for any external tool; the Pydantic models are the in-process
contract used by the router, scorer, and signer.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RiskTolerance(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EvidenceRequirement(StrEnum):
    BASIC = "basic"
    STRONG = "strong"
    STRICT = "strict"


class OutputMode(StrEnum):
    """Exactly the six routing destinations from the ECA system prompt."""

    DEEP_ANALYSIS = "deep_analysis"
    EXECUTIVE_DECISION_BRIEF = "executive_decision_brief"
    SYSTEM_ARCHITECTURE_BLUEPRINT = "system_architecture_blueprint"
    HUMAN_PERFORMANCE_PROTOCOL = "human_performance_protocol"
    COGNITIVE_ERROR_AUDIT = "cognitive_error_audit"
    IMPLEMENTATION_ROADMAP = "implementation_roadmap"


class ProofTier(StrEnum):
    ESTABLISHED = "Established"
    STRONGLY_PLAUSIBLE = "Strongly Plausible"
    TENTATIVE = "Tentative"
    WEAK = "Weak / Unsupported"


class RequestEnvelope(BaseModel):
    """Structured request entering the ECA stack.

    Matches ``assets/request_envelope.schema.json``. ``metadata`` is
    permissive because callers may attach run-id, user-id, or vendor-
    specific telemetry fields.
    """

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    request_id: str
    objective: str
    input_text: str
    domain: str | None = None
    role: str | None = None
    constraints: list[str] | None = None
    risk_tolerance: RiskTolerance | None = None
    evidence_requirement: EvidenceRequirement | None = None
    preferred_output: OutputMode | None = None
    time_horizon: str | None = None
    attachments: list[str] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ResponseSection(BaseModel):
    section: str
    content: str
    proof_tier: ProofTier | None = None


class QualityGate(BaseModel):
    coherent: bool
    implementable: bool
    limits_stated: bool
    logical_leap_score: float | None = None
    format_compliance_score: float | None = None


class ResponseEnvelope(BaseModel):
    """Structured response leaving the ECA stack.

    Matches ``assets/response_envelope.schema.json``. A fully populated
    envelope is what the scorer consumes and what the signer
    cryptographically commits to.
    """

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    response_id: str
    mode: OutputMode
    executive_summary: str
    main_body: list[ResponseSection]
    action_items: list[str] | None = None
    quality_gate: QualityGate
    provenance_signature: str | None = None
    timestamp: str | None = None
    deployment_id: str | None = None

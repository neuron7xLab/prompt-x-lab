"""Pydantic models mirroring the JSON schemas under ``schemas/``.

Every model here is the single source of truth for the shape of an
artifact in the eval pipeline. The JSON Schemas in ``schemas/`` exist so
that external tools (GitHub Actions, editors, reviewers) can validate
the same artifacts without importing Python. The two sources are kept
in sync deliberately: if you edit one, edit the other.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Category(StrEnum):
    """Layer / category a module belongs to."""

    FOUNDATION = "foundation"
    COGNITION = "cognition"
    ENGINEERING = "engineering"
    PERSONAS = "personas"
    VALIDATION = "validation"
    ORCHESTRATION = "orchestration"
    PROTOCOLS = "protocols"
    AGENTS = "agents"
    FRAMEWORKS = "frameworks"
    CRYPTO = "crypto"
    RESEARCH = "research"


class Vector(StrEnum):
    COGNITIVE = "cognitive"
    ENGINEERING = "engineering"
    STRATEGIC = "strategic"
    CREATIVE = "creative"
    VALIDATION = "validation"


class Status(StrEnum):
    DRAFT = "draft"
    STABLE = "stable"
    DEPRECATED = "deprecated"


class Latency(StrEnum):
    THINKING = "thinking"
    REALTIME = "realtime"
    BATCH = "batch"


class CaseKind(StrEnum):
    POSITIVE = "positive"
    ADVERSARIAL = "adversarial"
    EDGE = "edge"


class Provider(StrEnum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    MOCK = "mock"


SemVerStr = Annotated[
    str,
    Field(pattern=r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$"),
]

SlugStr = Annotated[
    str,
    Field(pattern=r"^[a-z0-9-]+$"),
]


class ModuleFrontmatter(BaseModel):
    """YAML frontmatter of every module under test.

    Matches ``schemas/module.schema.json``. Unknown fields are allowed so
    that long-form Layer-05 modules can carry their own provenance
    metadata without triggering validation failures.
    """

    model_config = ConfigDict(extra="allow")

    title: str = Field(min_length=2, max_length=80)
    category: Category
    vector: Vector
    version: SemVerStr
    status: Status
    subtitle: str | None = None
    model_opt: str | list[str] | None = None
    latency: Latency | None = None
    slug: SlugStr | None = None
    validated: bool | None = None
    validated_on: list[str] | None = None
    origin: str | None = None
    source_file: str | None = None


class EvalCase(BaseModel):
    """A single test case inside an eval spec."""

    name: SlugStr
    kind: CaseKind = CaseKind.POSITIVE
    input: str = Field(min_length=1)
    expectations: list[str] = Field(min_length=1)
    must_refuse: bool = False


class SystemPromptAssembly(BaseModel):
    file: str
    sections: list[str] = Field(min_length=1)

    @field_validator("sections")
    @classmethod
    def _non_empty(cls, v: list[str]) -> list[str]:
        allowed = {"Identity", "Core logic", "Constraints", "Output format"}
        bad = [s for s in v if s not in allowed]
        if bad:
            msg = f"sections must be subset of {allowed}; got {bad}"
            raise ValueError(msg)
        return v


class JudgeSpec(BaseModel):
    model: str
    rubric: str

    @field_validator("rubric")
    @classmethod
    def _known_rubric(cls, v: str) -> str:
        allowed = {"expectations-only", "expectations-with-counterfactual"}
        if v not in allowed:
            msg = f"rubric must be one of {allowed}"
            raise ValueError(msg)
        return v


class EvalSpec(BaseModel):
    """A full evaluation specification for one module."""

    model_config = ConfigDict(extra="forbid")

    module: str
    system_prompt_from: SystemPromptAssembly
    cases: list[EvalCase] = Field(min_length=1)
    judge: JudgeSpec


class RubricItem(BaseModel):
    expectation: str
    satisfied: bool
    evidence: str | None = None


class CaseResult(BaseModel):
    name: str
    kind: CaseKind
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    output: str | None = None
    rubric_items: list[RubricItem] | None = None
    notes: str = ""
    latency_ms: int | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None


class ResultSummary(BaseModel):
    cases_total: int = Field(ge=0)
    cases_passed: int = Field(ge=0)
    pass_rate: float = Field(ge=0.0, le=1.0)
    aggregate_score: float | None = Field(default=None, ge=0.0, le=1.0)


class EvalResult(BaseModel):
    """One eval run of one module against one provider."""

    model_config = ConfigDict(extra="forbid")

    module: str
    provider: Provider
    model: str
    timestamp: datetime
    harness_version: str
    cases: list[CaseResult]
    summary: ResultSummary

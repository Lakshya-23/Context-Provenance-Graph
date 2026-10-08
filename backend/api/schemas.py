"""Pydantic models for API request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


# --- Core domain models ---


class Evidence(BaseModel):
    """A piece of evidence linking a term back to its source."""

    source_id: str
    page: int
    text: str


class Claim(BaseModel):
    """A statement extracted from the source document."""

    id: str
    text: str
    claim_type: str  # "definition", "business_rule", "relationship", "semantic_statement"
    source_page: int
    related_terms: list[str] = []


class GlossaryTerm(BaseModel):
    """A structured business term extracted from the document."""

    id: str
    name: str
    definition: str
    aliases: list[str] = []
    business_rules: list[str] = []
    evidence: list[Evidence] = []
    confidence: float = Field(ge=0.0, le=1.0)


class SourceInfo(BaseModel):
    """Metadata about the source document."""

    source_id: str
    name: str
    version: str
    page_count: int
    filename: str


# --- Workflow tracing ---


class TraceStep(BaseModel):
    """A single step in the extraction workflow trace."""

    name: str
    status: str  # "success" | "error"
    duration_ms: float
    input_summary: str = ""
    output_summary: str = ""
    error: str | None = None


class WorkflowTrace(BaseModel):
    """Trace of the entire extraction workflow."""

    steps: list[TraceStep] = []
    total_duration_ms: float = 0.0
    llm_calls: int = 0
    tokens_used: dict = {}


# --- Analysis result ---


class AnalysisResult(BaseModel):
    """Complete result returned from the /api/analyze endpoint."""

    source: SourceInfo
    claims: list[Claim]
    glossary: list[GlossaryTerm]
    graph: dict  # serialized ProvenanceGraph
    summary: dict
    trace: WorkflowTrace


# --- Request models ---


class AnalyzeRequest(BaseModel):
    version: str = "1.2"


class ImpactRequest(BaseModel):
    base_version: str = "1.2"
    new_version: str = "1.3"
    graph: dict  # the full provenance graph from frontend state


class EvaluateRequest(BaseModel):
    glossary: list[GlossaryTerm]
    source_text: str


# --- Impact result ---


class ChangeDetail(BaseModel):
    """A single detected change between document versions."""

    change_type: str  # "modified", "added", "removed"
    old_text: str = ""
    new_text: str = ""
    affected_terms: list[str] = []
    semantic_explanation: str = ""


class ImpactResult(BaseModel):
    """Result of change impact analysis."""

    changes: list[ChangeDetail]
    affected_terms: list[str]
    impact: dict  # grouped downstream impact by type


# --- Evaluation result ---


class EvaluationDetail(BaseModel):
    name: str
    score: float
    expected: int = 0
    found: int = 0
    missing: list[str] = []
    details: list[dict] = []


class EvaluationResult(BaseModel):
    term_coverage: EvaluationDetail
    definition_groundedness: EvaluationDetail
    evidence_accuracy: EvaluationDetail
    business_rule_completeness: EvaluationDetail
    overall: float

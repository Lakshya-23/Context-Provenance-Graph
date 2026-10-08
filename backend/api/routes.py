"""FastAPI route definitions for Context Provenance Graph."""

from __future__ import annotations

import os
import sys
from fastapi import APIRouter, HTTPException

from api.schemas import (
    AnalyzeRequest,
    AnalysisResult,
    SourceInfo,
    Claim,
    GlossaryTerm,
    WorkflowTrace,
    TraceStep,
    ImpactRequest,
    ImpactResult,
    ChangeDetail,
    EvaluateRequest,
    EvaluationResult,
)
from workflow.graph import run_extraction
from provenance.graph_engine import build_provenance_graph
from provenance.models import ProvenanceGraph
from provenance.changes import compare_versions
from provenance.impact import calculate_impact
from evaluation.evaluators import run_all_evaluations
from extraction.pdf_parser import parse_pdf, get_full_text

router = APIRouter(prefix="/api")


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "context-provenance-graph-backend",
        "llm_model": os.getenv("LLM_MODEL", "not_configured"),
    }


@router.get("/verify-llm")
def verify_llm_endpoint():
    """Perform a pre-flight test call to verify that the LLM model and API key are responding."""
    from workflow.llm import verify_llm_connection
    try:
        return verify_llm_connection()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/analyze", response_model=AnalysisResult)
def analyze_document(request: AnalyzeRequest):
    """Run extraction pipeline on the specified Revenue Policy version."""
    v_clean = request.version.strip()
    v_label = v_clean.replace(".", "_")
    source_id = f"doc_revenue_policy_v{v_label}"

    # Verify PDF exists
    pdf_filename = f"revenue_policy_v{v_label}.pdf"
    demo_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "demo"))
    pdf_path = os.path.join(demo_dir, pdf_filename)

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail=f"Document version '{request.version}' not found ({pdf_filename})",
        )

    # Pre-flight check: verify API key and model connectivity before running pipeline
    try:
        from workflow.llm import verify_llm_connection
        verify_llm_connection()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Pre-flight LLM API check failed: {str(e)}",
        )

    try:
        # Run LangGraph extraction pipeline
        state = run_extraction(source_id=source_id, source_version=v_clean)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Extraction workflow error: {str(e)}",
        )

    # Build source info
    pages = state.get("pages", [])
    source_info_data = {
        "source_id": source_id,
        "name": f"Revenue Recognition Policy v{v_clean}",
        "version": v_clean,
        "page_count": len(pages),
        "filename": pdf_filename,
    }

    # Build provenance graph
    try:
        graph = build_provenance_graph(
            source_info=source_info_data,
            claims=state.get("claims", []),
            glossary_terms=state.get("validated_terms", []),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Graph construction error: {str(e)}",
        )

    # Compute graph node counts by type
    counts_by_type: dict[str, int] = {}
    for node in graph.nodes.values():
        t = node.type.value if hasattr(node.type, "value") else str(node.type)
        counts_by_type[t] = counts_by_type.get(t, 0) + 1

    summary = {
        "total_nodes": len(graph.nodes),
        "total_edges": len(graph.edges),
        "claims_count": len(state.get("claims", [])),
        "glossary_count": len(state.get("validated_terms", [])),
        "counts_by_type": counts_by_type,
        "errors": state.get("errors", []),
    }

    # Build workflow trace
    trace_steps = [TraceStep(**s) for s in state.get("trace_steps", [])]
    total_duration = sum(s.duration_ms for s in trace_steps)

    trace = WorkflowTrace(
        steps=trace_steps,
        total_duration_ms=round(total_duration, 2),
        llm_calls=state.get("llm_calls", 0),
        tokens_used=state.get("tokens_used", {}),
    )

    return AnalysisResult(
        source=SourceInfo(**source_info_data),
        claims=[Claim(**c) for c in state.get("claims", [])],
        glossary=[GlossaryTerm(**t) for t in state.get("validated_terms", [])],
        graph=graph.model_dump(),
        summary=summary,
        trace=trace,
    )


@router.post("/impact", response_model=ImpactResult)
def analyze_impact(request: ImpactRequest):
    """Detect changes between base and new versions, and trace downstream impact."""
    # Reconstruct provenance graph
    try:
        graph = ProvenanceGraph.model_validate(request.graph)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid provenance graph payload: {str(e)}",
        )

    try:
        # Detect semantic changes between versions
        diff_result = compare_versions(
            base_version=request.base_version,
            new_version=request.new_version,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Version comparison failed: {str(e)}",
        )

    changes_raw = diff_result.get("changes", [])
    affected_terms = diff_result.get("affected_terms", [])

    # Map raw changes into ChangeDetail models
    change_details: list[ChangeDetail] = []
    for c in changes_raw:
        # Standardize affected terms format
        change_details.append(
            ChangeDetail(
                change_type=c.get("change_type", "modified"),
                old_text=c.get("old_text", ""),
                new_text=c.get("new_text", ""),
                affected_terms=c.get("affected_terms", []),
                semantic_explanation=c.get("semantic_explanation", ""),
            )
        )

    # Calculate downstream impact across the graph
    impact_data = calculate_impact(graph, affected_terms)

    return ImpactResult(
        changes=change_details,
        affected_terms=affected_terms,
        impact=impact_data,
    )


@router.post("/evaluate", response_model=EvaluationResult)
def evaluate_extraction(request: EvaluateRequest):
    """Run in-process deterministic evaluators on the extracted glossary."""
    glossary_dicts = [t.model_dump() for t in request.glossary]
    eval_results = run_all_evaluations(glossary_dicts, request.source_text)
    return EvaluationResult(**eval_results)


@router.get("/document/{version}")
def get_document_content(version: str):
    """Get parsed text and metadata for a document version."""
    v_clean = version.strip()
    v_label = v_clean.replace(".", "_")
    pdf_filename = f"revenue_policy_v{v_label}.pdf"
    demo_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "demo"))
    pdf_path = os.path.join(demo_dir, pdf_filename)

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail=f"Document version '{version}' not found ({pdf_filename})",
        )

    pages = parse_pdf(pdf_path)
    full_text = get_full_text(pages)

    return {
        "version": v_clean,
        "filename": pdf_filename,
        "page_count": len(pages),
        "pages": pages,
        "raw_text": full_text,
    }

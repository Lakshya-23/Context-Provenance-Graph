"""LangGraph workflow node functions.

Each function takes and returns ExtractionState.
Timing is tracked for the WorkflowTrace.
"""

from __future__ import annotations

import json
import time

from workflow.state import ExtractionState
from extraction.pdf_parser import parse_pdf, get_full_text
from extraction.extractor import extract_claims, extract_glossary
from extraction.evidence import map_evidence_to_pages
from extraction.validator import validate_terms


def _add_trace(
    state: ExtractionState,
    name: str,
    status: str,
    duration_ms: float,
    input_summary: str = "",
    output_summary: str = "",
    error: str | None = None,
) -> None:
    """Add a trace step to the state."""
    state["trace_steps"].append(
        {
            "name": name,
            "status": status,
            "duration_ms": round(duration_ms, 2),
            "input_summary": input_summary,
            "output_summary": output_summary,
            "error": error,
        }
    )


def parse_document(state: ExtractionState) -> ExtractionState:
    """Node 1: Extract page-aware text from the PDF."""
    start = time.time()
    try:
        import os

        version = state["source_version"]
        v_label = version.replace(".", "_")
        pdf_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "demo",
            f"revenue_policy_v{v_label}.pdf",
        )
        pdf_path = os.path.normpath(pdf_path)

        pages = parse_pdf(pdf_path)
        raw_text = get_full_text(pages)

        state["pages"] = pages
        state["raw_text"] = raw_text

        duration = (time.time() - start) * 1000
        _add_trace(
            state,
            "parse_document",
            "success",
            duration,
            input_summary=f"PDF: revenue_policy_v{v_label}.pdf",
            output_summary=f"Extracted {len(pages)} pages, {len(raw_text)} chars",
        )
    except Exception as e:
        duration = (time.time() - start) * 1000
        state["errors"].append(f"parse_document: {str(e)}")
        _add_trace(state, "parse_document", "error", duration, error=str(e))

    return state


def extract_claims_node(state: ExtractionState) -> ExtractionState:
    """Node 2: Use LLM to extract claims from the document."""
    start = time.time()
    try:
        claims, tokens = extract_claims(state["raw_text"])
        state["claims"] = claims
        state["llm_calls"] += 1
        state["tokens_used"]["extract_claims"] = tokens

        duration = (time.time() - start) * 1000
        _add_trace(
            state,
            "extract_claims",
            "success",
            duration,
            input_summary=f"Document text ({len(state['raw_text'])} chars)",
            output_summary=f"Extracted {len(claims)} claims",
        )
    except Exception as e:
        duration = (time.time() - start) * 1000
        state["errors"].append(f"extract_claims: {str(e)}")
        _add_trace(state, "extract_claims", "error", duration, error=str(e))

    return state


def extract_glossary_node(state: ExtractionState) -> ExtractionState:
    """Node 3: Use LLM to create structured glossary from claims."""
    start = time.time()
    try:
        claims_json = json.dumps(state["claims"], indent=2)
        terms, tokens = extract_glossary(
            state["raw_text"], claims_json, state["source_id"]
        )
        state["glossary_candidates"] = terms
        state["llm_calls"] += 1
        state["tokens_used"]["extract_glossary"] = tokens

        duration = (time.time() - start) * 1000
        _add_trace(
            state,
            "extract_glossary",
            "success",
            duration,
            input_summary=f"{len(state['claims'])} claims + document text",
            output_summary=f"Extracted {len(terms)} glossary candidates",
        )
    except Exception as e:
        duration = (time.time() - start) * 1000
        state["errors"].append(f"extract_glossary: {str(e)}")
        _add_trace(
            state, "extract_glossary", "error", duration, error=str(e)
        )

    return state


def map_evidence_node(state: ExtractionState) -> ExtractionState:
    """Node 4: Verify and correct evidence page numbers."""
    start = time.time()
    try:
        verified = map_evidence_to_pages(
            state["glossary_candidates"], state["pages"]
        )
        state["glossary_candidates"] = verified

        # Count verification results
        total_ev = 0
        valid_ev = 0
        for t in verified:
            for ev in t.get("evidence", []):
                total_ev += 1
                if ev.get("_valid", True) and ev.get("_match_type") != "not_found":
                    valid_ev += 1

        duration = (time.time() - start) * 1000
        _add_trace(
            state,
            "map_evidence",
            "success",
            duration,
            input_summary=f"{len(verified)} terms with evidence",
            output_summary=f"{valid_ev}/{total_ev} evidence pieces verified",
        )
    except Exception as e:
        duration = (time.time() - start) * 1000
        state["errors"].append(f"map_evidence: {str(e)}")
        _add_trace(state, "map_evidence", "error", duration, error=str(e))

    return state


def validate_output_node(state: ExtractionState) -> ExtractionState:
    """Node 5: Run Pydantic and business-rule validation."""
    start = time.time()
    try:
        validated, validation_errors = validate_terms(
            state["glossary_candidates"], state["source_id"]
        )
        state["validated_terms"] = validated
        state["errors"].extend(validation_errors)

        # Remove invalid evidence from final terms
        for term in state["validated_terms"]:
            term["evidence"] = [
                {k: v for k, v in ev.items() if not k.startswith("_")}
                for ev in term.get("evidence", [])
                if ev.get("_valid", True) and ev.get("_match_type") != "not_found"
            ]

        duration = (time.time() - start) * 1000
        _add_trace(
            state,
            "validate_output",
            "success",
            duration,
            input_summary=f"{len(state['glossary_candidates'])} candidates",
            output_summary=f"{len(validated)} terms validated, {len(validation_errors)} errors",
        )
    except Exception as e:
        duration = (time.time() - start) * 1000
        state["errors"].append(f"validate_output: {str(e)}")
        _add_trace(
            state, "validate_output", "error", duration, error=str(e)
        )

    return state


def finalize_node(state: ExtractionState) -> ExtractionState:
    """Node 6: Final cleanup and return."""
    start = time.time()

    # Clean up internal fields from evidence
    for term in state["validated_terms"]:
        term["evidence"] = [
            {k: v for k, v in ev.items() if not k.startswith("_")}
            for ev in term.get("evidence", [])
        ]

    duration = (time.time() - start) * 1000
    _add_trace(
        state,
        "finalize",
        "success",
        duration,
        input_summary=f"{len(state['validated_terms'])} validated terms",
        output_summary="Extraction complete",
    )

    return state

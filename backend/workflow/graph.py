"""LangGraph workflow definition.

Compiles the extraction pipeline into a runnable graph.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, END

from workflow.state import ExtractionState
from workflow.nodes import (
    parse_document,
    extract_claims_node,
    extract_glossary_node,
    map_evidence_node,
    validate_output_node,
    finalize_node,
)


def build_extraction_graph() -> StateGraph:
    """Build and compile the LangGraph extraction workflow.

    Flow:
        parse_document
             ↓
        extract_claims (LLM)
             ↓
        extract_glossary (LLM)
             ↓
        map_evidence
             ↓
        validate_output
             ↓
        finalize
             ↓
           END
    """
    workflow = StateGraph(ExtractionState)

    # Add nodes
    workflow.add_node("parse_document", parse_document)
    workflow.add_node("extract_claims", extract_claims_node)
    workflow.add_node("extract_glossary", extract_glossary_node)
    workflow.add_node("map_evidence", map_evidence_node)
    workflow.add_node("validate_output", validate_output_node)
    workflow.add_node("finalize", finalize_node)

    # Define edges (linear pipeline)
    workflow.set_entry_point("parse_document")
    workflow.add_edge("parse_document", "extract_claims")
    workflow.add_edge("extract_claims", "extract_glossary")
    workflow.add_edge("extract_glossary", "map_evidence")
    workflow.add_edge("map_evidence", "validate_output")
    workflow.add_edge("validate_output", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile()


# Pre-compiled graph instance
extraction_graph = build_extraction_graph()


def run_extraction(source_id: str, source_version: str) -> ExtractionState:
    """Run the full extraction workflow.

    Args:
        source_id: Identifier for the source document
        source_version: Version string (e.g. "1.2")

    Returns:
        Final ExtractionState with all results
    """
    initial_state: ExtractionState = {
        "source_id": source_id,
        "source_version": source_version,
        "pages": [],
        "raw_text": "",
        "claims": [],
        "glossary_candidates": [],
        "validated_terms": [],
        "errors": [],
        "trace_steps": [],
        "llm_calls": 0,
        "tokens_used": {},
    }

    result = extraction_graph.invoke(initial_state)
    return result

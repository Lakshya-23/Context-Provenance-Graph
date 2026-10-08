"""LangGraph extraction workflow state definition."""

from __future__ import annotations

from typing import TypedDict


class ExtractionState(TypedDict):
    """Typed state passed through the LangGraph extraction workflow."""

    source_id: str
    source_version: str
    pages: list[dict]          # [{"page": 1, "text": "..."}, ...]
    raw_text: str              # full combined text with page markers
    claims: list[dict]         # extracted claims
    glossary_candidates: list[dict]  # LLM-produced glossary candidates
    validated_terms: list[dict]      # post-validation glossary terms
    errors: list[str]          # any errors encountered
    trace_steps: list[dict]    # timing/status for each step
    llm_calls: int             # count of LLM invocations
    tokens_used: dict          # {"prompt": ..., "completion": ...}

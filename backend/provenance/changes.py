"""Version comparison and change detection.

Compares two document versions, identifies semantic changes,
and maps them to affected glossary terms.
"""

from __future__ import annotations

import json
import os

from extraction.pdf_parser import parse_pdf, get_full_text
from workflow.llm import call_llm
from workflow.prompts import SYSTEM_EXTRACTOR, SEMANTIC_DIFF_PROMPT
from provenance.linker import normalize_term

import re


def _parse_json_response(text: str) -> dict:
    """Parse JSON from LLM response."""
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = cleaned.strip().rstrip("`")
    return json.loads(cleaned)


def _get_pdf_path(version: str) -> str:
    """Get the PDF path for a given version."""
    v_label = version.replace(".", "_")
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "demo",
            f"revenue_policy_v{v_label}.pdf",
        )
    )


from pydantic import BaseModel
from api.schemas import ChangeDetail

class ChangesExtractionResponse(BaseModel):
    changes: list[ChangeDetail]

def compare_versions(
    base_version: str, new_version: str
) -> dict:
    """Compare two document versions and identify changes.

    Steps:
    1. Parse both PDFs
    2. Use LLM for semantic diff explanation
    3. Map changes to affected terms

    Returns:
        dict with changes, affected_terms, texts
    """
    base_path = _get_pdf_path(base_version)
    new_path = _get_pdf_path(new_version)

    base_pages = parse_pdf(base_path)
    new_pages = parse_pdf(new_path)

    base_text = get_full_text(base_pages)
    new_text = get_full_text(new_pages)

    # Use LLM for semantic change analysis
    prompt = SEMANTIC_DIFF_PROMPT.format(
        old_version=f"v{base_version}",
        new_version=f"v{new_version}",
        old_text=base_text,
        new_text=new_text,
    )

    result = call_llm(
        prompt=prompt,
        system=SYSTEM_EXTRACTOR,
        temperature=0.1,
        response_format=ChangesExtractionResponse,
    )

    content = result["content"]
    cleaned = re.sub(r"```(?:json)?\s*", "", content).strip().rstrip("`")
    parsed = ChangesExtractionResponse.model_validate_json(cleaned)
    changes = [c.model_dump() for c in parsed.changes]

    # Collect all affected terms
    all_affected_terms: list[str] = []
    for change in changes:
        for term_name in change.get("affected_terms", []):
            normalized = normalize_term(term_name)
            term_id = f"term_{normalized.replace(' ', '_')}"
            if term_id not in all_affected_terms:
                all_affected_terms.append(term_id)

    return {
        "changes": changes,
        "affected_terms": all_affected_terms,
        "base_text": base_text,
        "new_text": new_text,
    }

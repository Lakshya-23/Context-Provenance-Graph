"""Extraction logic for claims and glossary terms.

Calls the LLM through the llm.py wrapper and parses structured responses.
"""

from __future__ import annotations

import json
import re
from pydantic import BaseModel

from workflow.llm import call_llm
from workflow.prompts import (
    SYSTEM_EXTRACTOR,
    EXTRACT_CLAIMS_PROMPT,
    EXTRACT_GLOSSARY_PROMPT,
)
from api.schemas import Claim, GlossaryTerm

class ClaimsExtractionResponse(BaseModel):
    claims: list[Claim]

class GlossaryExtractionResponse(BaseModel):
    terms: list[GlossaryTerm]

def extract_claims(document_text: str) -> tuple[list[dict], dict]:
    """Extract claims from document text using the LLM.

    Returns:
        (claims_list, token_usage)
    """
    prompt = EXTRACT_CLAIMS_PROMPT.format(document_text=document_text)

    result = call_llm(
        prompt=prompt,
        system=SYSTEM_EXTRACTOR,
        temperature=0.1,
        response_format=ClaimsExtractionResponse,
    )

    content = result["content"]
    # litellm returns a json string if response_format is a pydantic model
    # clean it up just in case the provider wrapped it in markdown
    cleaned = re.sub(r"```(?:json)?\s*", "", content).strip().rstrip("`")
    parsed = ClaimsExtractionResponse.model_validate_json(cleaned)
    claims = [c.model_dump() for c in parsed.claims]

    tokens = {
        "prompt_tokens": result["prompt_tokens"],
        "completion_tokens": result["completion_tokens"],
    }

    return claims, tokens


def extract_glossary(
    document_text: str, claims_json: str, source_id: str
) -> tuple[list[dict], dict]:
    """Extract structured glossary terms from document and claims.

    Returns:
        (terms_list, token_usage)
    """
    prompt = EXTRACT_GLOSSARY_PROMPT.format(
        document_text=document_text,
        claims_json=claims_json,
        source_id=source_id,
    )

    result = call_llm(
        prompt=prompt,
        system=SYSTEM_EXTRACTOR,
        temperature=0.1,
        response_format=GlossaryExtractionResponse,
    )

    content = result["content"]
    cleaned = re.sub(r"```(?:json)?\s*", "", content).strip().rstrip("`")
    parsed = GlossaryExtractionResponse.model_validate_json(cleaned)
    terms = [t.model_dump() for t in parsed.terms]

    tokens = {
        "prompt_tokens": result["prompt_tokens"],
        "completion_tokens": result["completion_tokens"],
    }

    return terms, tokens

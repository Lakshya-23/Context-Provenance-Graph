"""Deterministic extraction — no LLM calls.

Returns hardcoded claims and glossary terms from demo/hardcoded_data.py.
The function signatures are identical to the original so workflow/nodes.py
requires no changes.
"""

from __future__ import annotations

import copy


def _get_version_label(source_id: str) -> str:
    """Extract version string from source_id like 'doc_revenue_policy_v1_2'."""
    if "v1_3" in source_id:
        return "1.3"
    return "1.2"


def extract_claims(document_text: str, source_id: str = "") -> tuple[list[dict], dict]:
    """Return hardcoded claims for the appropriate policy version.

    Args:
        document_text: Ignored — kept for API compatibility with nodes.py.
        source_id: Used to select v1.2 or v1.3 dataset.

    Returns:
        (claims_list, token_usage)
    """
    from demo.hardcoded_data import HARDCODED_CLAIMS_V1_2, HARDCODED_CLAIMS_V1_3

    version = _get_version_label(source_id)
    claims = copy.deepcopy(HARDCODED_CLAIMS_V1_3 if version == "1.3" else HARDCODED_CLAIMS_V1_2)

    tokens = {"prompt_tokens": 0, "completion_tokens": 0}
    return claims, tokens


def extract_glossary(
    document_text: str, claims_json: str, source_id: str
) -> tuple[list[dict], dict]:
    """Return hardcoded glossary terms for the appropriate policy version.

    Args:
        document_text: Ignored — kept for API compatibility with nodes.py.
        claims_json: Ignored — kept for API compatibility with nodes.py.
        source_id: Used to select v1.2 or v1.3 dataset.

    Returns:
        (terms_list, token_usage)
    """
    from demo.hardcoded_data import HARDCODED_GLOSSARY_V1_2, HARDCODED_GLOSSARY_V1_3

    version = _get_version_label(source_id)
    terms = copy.deepcopy(HARDCODED_GLOSSARY_V1_3 if version == "1.3" else HARDCODED_GLOSSARY_V1_2)

    tokens = {"prompt_tokens": 0, "completion_tokens": 0}
    return terms, tokens

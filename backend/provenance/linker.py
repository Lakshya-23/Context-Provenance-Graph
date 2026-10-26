"""Term normalization and alias matching.

Deterministic linking — no LLM calls.
Connects LLM-extracted glossary terms to the static downstream registry.
"""

from __future__ import annotations

import re


def normalize_term(name: str) -> str:
    """Normalize a term name for matching.

    - lowercase
    - trim whitespace
    - remove unnecessary punctuation
    - normalize common plurals
    """
    name = name.lower().strip()
    # Remove trailing punctuation
    name = re.sub(r"[.:;,!?]+$", "", name)
    # Normalize whitespace
    name = " ".join(name.split())
    # Simple plural normalization
    if name.endswith("s") and not name.endswith("ss"):
        singular = name[:-1]
        # Only de-pluralize if it looks like a simple plural
        if len(singular) > 3:
            return singular
    return name


def build_term_lookup(terms: list[dict]) -> dict[str, str]:
    """Build a lookup from normalized name/alias → term id.

    Returns:
        dict mapping normalized names to term IDs
    """
    lookup: dict[str, str] = {}
    for term in terms:
        term_id = term["id"]
        # Primary name
        lookup[normalize_term(term["name"])] = term_id
        # Aliases
        for alias in term.get("aliases", []):
            lookup[normalize_term(alias)] = term_id
    return lookup


# Known canonical term IDs for the demo registry
CANONICAL_TERMS = {
    "revenue": "term_revenue",
    "refund": "term_refund",
    "chargeback": "term_chargeback",
    "settlement": "term_settlement",
    "gross revenue": "term_gross_revenue",
    "net revenue": "term_net_revenue",
    "realized revenue": "term_realized_revenue",
    "fulfilled order": "term_fulfilled_order",
    "recognition event": "term_recognition_event",
}


def link_extracted_to_registry(
    extracted_terms: list[dict],
) -> dict[str, str]:
    """Match extracted glossary terms to canonical registry IDs.

    Returns:
        dict mapping extracted term id → canonical term id
    """
    mapping: dict[str, str] = {}
    lookup = build_term_lookup(extracted_terms)

    for canonical_name, canonical_id in CANONICAL_TERMS.items():
        normalized = normalize_term(canonical_name)
        # Check if any extracted term matches this canonical name
        if normalized in lookup:
            extracted_id = lookup[normalized]
            mapping[extracted_id] = canonical_id
        else:
            # Try fuzzy: check if canonical name appears in any term name
            for term in extracted_terms:
                term_norm = normalize_term(term["name"])
                if canonical_name in term_norm or term_norm in canonical_name:
                    mapping[term["id"]] = canonical_id
                    break

    return mapping

"""Validation for extracted glossary terms.

Applies Pydantic validation and additional business checks.
"""

from __future__ import annotations

from api.schemas import GlossaryTerm, Evidence


def validate_terms(
    raw_terms: list[dict], source_id: str
) -> tuple[list[dict], list[str]]:
    """Validate and clean extracted terms.

    Checks:
    - Term has a name
    - Term has a definition
    - Confidence is between 0 and 1
    - Evidence text is present
    - Duplicate term names are merged
    - Empty definitions are rejected

    Returns:
        (validated_terms, errors)
    """
    errors: list[str] = []
    seen_names: dict[str, int] = {}  # normalized name -> index
    validated: list[dict] = []

    for i, raw in enumerate(raw_terms):
        term_errors = []

        # Check required fields
        name = raw.get("name", "").strip()
        if not name:
            term_errors.append(f"Term at index {i} has no name")
            continue

        definition = raw.get("definition", "").strip()
        if not definition:
            term_errors.append(f"Term '{name}' has an empty definition")
            continue

        # Normalize confidence
        confidence = raw.get("confidence", 0.5)
        if not isinstance(confidence, (int, float)):
            confidence = 0.5
        confidence = max(0.0, min(1.0, float(confidence)))

        # Ensure id exists
        term_id = raw.get("id", "")
        if not term_id:
            term_id = f"term_{name.lower().replace(' ', '_')}"

        # Ensure evidence has source_id
        evidence = []
        for ev in raw.get("evidence", []):
            if not ev.get("text", "").strip():
                continue
            ev_clean = {
                "source_id": ev.get("source_id", source_id),
                "page": ev.get("page", 1),
                "text": ev["text"].strip(),
            }
            evidence.append(ev_clean)

        # Handle aliases
        aliases = [a.strip() for a in raw.get("aliases", []) if a.strip()]

        # Handle business rules
        business_rules = [
            r.strip() for r in raw.get("business_rules", []) if r.strip()
        ]

        # Check for duplicate names (merge)
        normalized_name = name.lower().strip()
        if normalized_name in seen_names:
            idx = seen_names[normalized_name]
            existing = validated[idx]
            # Merge evidence and rules
            existing["evidence"].extend(evidence)
            existing["business_rules"].extend(business_rules)
            existing["aliases"] = list(
                set(existing["aliases"] + aliases)
            )
            existing["confidence"] = max(existing["confidence"], confidence)
            continue

        clean_term = {
            "id": term_id,
            "name": name,
            "definition": definition,
            "aliases": aliases,
            "business_rules": business_rules,
            "evidence": evidence,
            "confidence": confidence,
        }

        # Validate with Pydantic
        try:
            GlossaryTerm(**clean_term)
        except Exception as e:
            term_errors.append(f"Validation error for '{name}': {str(e)}")
            continue

        seen_names[normalized_name] = len(validated)
        validated.append(clean_term)
        errors.extend(term_errors)

    return validated, errors

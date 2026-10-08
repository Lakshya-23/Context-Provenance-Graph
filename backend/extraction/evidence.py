"""Evidence mapping and verification.

Ensures every piece of evidence actually exists in the source document.
"""

from __future__ import annotations


def verify_evidence(
    evidence_text: str, pages: list[dict], claimed_page: int
) -> dict:
    """Verify that evidence text exists in the source document.

    Returns:
        dict with:
            - valid: bool
            - matched_page: int or None
            - match_type: "exact" | "partial" | "not_found"
    """
    # Normalize whitespace for comparison
    normalized_evidence = " ".join(evidence_text.split()).lower()

    # First check the claimed page
    if claimed_page > 0:
        for p in pages:
            if p["page"] == claimed_page:
                normalized_page = " ".join(p["text"].split()).lower()
                if normalized_evidence in normalized_page:
                    return {
                        "valid": True,
                        "matched_page": claimed_page,
                        "match_type": "exact",
                    }

    # If not found on claimed page, search all pages
    for p in pages:
        normalized_page = " ".join(p["text"].split()).lower()
        if normalized_evidence in normalized_page:
            return {
                "valid": True,
                "matched_page": p["page"],
                "match_type": "exact",
            }

    # Try partial matching (first 60 chars)
    partial = normalized_evidence[:60]
    for p in pages:
        normalized_page = " ".join(p["text"].split()).lower()
        if partial in normalized_page:
            return {
                "valid": True,
                "matched_page": p["page"],
                "match_type": "partial",
            }

    return {
        "valid": False,
        "matched_page": None,
        "match_type": "not_found",
    }


def map_evidence_to_pages(
    terms: list[dict], pages: list[dict]
) -> list[dict]:
    """Verify and correct evidence page numbers for all terms.

    Modifies terms in-place and returns them.
    Invalid evidence is marked but not removed.
    """
    for term in terms:
        verified_evidence = []
        for ev in term.get("evidence", []):
            result = verify_evidence(ev["text"], pages, ev.get("page", 0))
            if result["valid"]:
                ev["page"] = result["matched_page"]
                ev["_match_type"] = result["match_type"]
                verified_evidence.append(ev)
            else:
                # Mark invalid evidence — don't silently drop it
                ev["_match_type"] = "not_found"
                ev["_valid"] = False
                verified_evidence.append(ev)
        term["evidence"] = verified_evidence
    return terms

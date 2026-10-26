"""In-process deterministic evaluators for extraction quality.

No external service required — pure code checks.
"""

from __future__ import annotations


# Expected terms for the Revenue Policy document (all 9 governed terms)
EXPECTED_TERMS = [
    "Revenue",
    "Refund",
    "Chargeback",
    "Settlement",
    "Gross Revenue",
    "Net Revenue",
    "Realized Revenue",
    "Fulfilled Order",
    "Recognition Event",
]

# Key business rules that should be captured
EXPECTED_BUSINESS_RULES = [
    "revenue is recognized when an order has been fulfilled",
    "refunds processed before settlement are excluded from recognized revenue",
    "chargeback",  # partial match for chargeback rules
    "fulfilled order",  # recognition event
    "gross revenue represents the value of fulfilled orders before refund adjustments",
    "net revenue represents gross revenue less applicable refunds",
]


def evaluate_term_coverage(glossary: list[dict]) -> dict:
    """Check whether important expected concepts are extracted."""
    extracted_names = [t["name"].lower().strip() for t in glossary]
    # Also check aliases
    for t in glossary:
        for alias in t.get("aliases", []):
            extracted_names.append(alias.lower().strip())

    found = []
    missing = []
    for expected in EXPECTED_TERMS:
        normalized = expected.lower().strip()
        if any(normalized in name or name in normalized for name in extracted_names):
            found.append(expected)
        else:
            missing.append(expected)

    score = len(found) / len(EXPECTED_TERMS) if EXPECTED_TERMS else 1.0

    return {
        "name": "Term Coverage",
        "score": round(score, 2),
        "expected": len(EXPECTED_TERMS),
        "found": len(found),
        "missing": missing,
        "details": [
            {"term": t, "status": "found" if t in found else "missing"}
            for t in EXPECTED_TERMS
        ],
    }


def evaluate_definition_groundedness(
    glossary: list[dict], source_text: str
) -> dict:
    """Check whether definitions are grounded in the source."""
    source_lower = source_text.lower()
    results = []

    for term in glossary:
        definition = term.get("definition", "").lower()
        # Check if key phrases from the definition appear in source
        words = definition.split()
        # Check overlapping 4-grams
        if len(words) >= 4:
            ngrams = [
                " ".join(words[i : i + 4]) for i in range(len(words) - 3)
            ]
            matched = sum(1 for ng in ngrams if ng in source_lower)
            ratio = matched / len(ngrams) if ngrams else 0
        else:
            # Short definition — check if it appears verbatim
            ratio = 1.0 if definition in source_lower else 0.5

        results.append(
            {
                "term": term["name"],
                "grounded": ratio > 0.3,
                "score": round(min(ratio * 2, 1.0), 2),  # Scale up
            }
        )

    grounded = [r for r in results if r["grounded"]]
    score = len(grounded) / len(results) if results else 1.0

    return {
        "name": "Definition Groundedness",
        "score": round(score, 2),
        "expected": len(results),
        "found": len(grounded),
        "missing": [r["term"] for r in results if not r["grounded"]],
        "details": results,
    }


def evaluate_evidence_accuracy(
    glossary: list[dict], source_text: str
) -> dict:
    """Check whether evidence snippets exist in the source."""
    source_lower = " ".join(source_text.lower().split())
    results = []

    for term in glossary:
        for ev in term.get("evidence", []):
            ev_text = " ".join(ev.get("text", "").lower().split())
            found = ev_text in source_lower
            # Try partial (first 50 chars)
            partial = ev_text[:50] in source_lower if len(ev_text) > 50 else found
            results.append(
                {
                    "term": term["name"],
                    "evidence": ev.get("text", "")[:80],
                    "page": ev.get("page", 0),
                    "found": found or partial,
                }
            )

    accurate = [r for r in results if r["found"]]
    score = len(accurate) / len(results) if results else 1.0

    return {
        "name": "Evidence Accuracy",
        "score": round(score, 2),
        "expected": len(results),
        "found": len(accurate),
        "missing": [
            f"{r['term']}: {r['evidence']}" for r in results if not r["found"]
        ],
        "details": results,
    }


def evaluate_business_rule_completeness(glossary: list[dict]) -> dict:
    """Check whether key business rules are captured."""
    all_rules = []
    for term in glossary:
        for rule in term.get("business_rules", []):
            all_rules.append(rule.lower())

    # Also check definitions for rule content
    all_text = " ".join(all_rules)
    for term in glossary:
        all_text += " " + term.get("definition", "").lower()

    found_rules = []
    missing_rules = []
    for expected in EXPECTED_BUSINESS_RULES:
        if expected.lower() in all_text:
            found_rules.append(expected)
        else:
            missing_rules.append(expected)

    score = (
        len(found_rules) / len(EXPECTED_BUSINESS_RULES)
        if EXPECTED_BUSINESS_RULES
        else 1.0
    )

    return {
        "name": "Business Rule Completeness",
        "score": round(score, 2),
        "expected": len(EXPECTED_BUSINESS_RULES),
        "found": len(found_rules),
        "missing": missing_rules,
        "details": [
            {"rule": r, "status": "found" if r in found_rules else "missing"}
            for r in EXPECTED_BUSINESS_RULES
        ],
    }


def run_all_evaluations(
    glossary: list[dict], source_text: str
) -> dict:
    """Run all evaluators and return combined results."""
    term_cov = evaluate_term_coverage(glossary)
    def_ground = evaluate_definition_groundedness(glossary, source_text)
    ev_acc = evaluate_evidence_accuracy(glossary, source_text)
    br_comp = evaluate_business_rule_completeness(glossary)

    # Weighted average for overall score
    overall = (
        term_cov["score"] * 0.3
        + def_ground["score"] * 0.25
        + ev_acc["score"] * 0.25
        + br_comp["score"] * 0.2
    )

    return {
        "term_coverage": term_cov,
        "definition_groundedness": def_ground,
        "evidence_accuracy": ev_acc,
        "business_rule_completeness": br_comp,
        "overall": round(overall, 2),
    }

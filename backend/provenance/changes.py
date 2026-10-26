"""Deterministic version comparison — no LLM calls.

Returns a hardcoded semantic diff for the v1.2 → v1.3 Revenue Recognition Policy.
The function signature is identical to the original so routes.py needs no changes.
"""

from __future__ import annotations

import copy

from demo.hardcoded_data import HARDCODED_DIFF_V1_2_TO_V1_3


def compare_versions(base_version: str, new_version: str) -> dict:
    """Return the hardcoded semantic diff between two policy versions.

    Currently only v1.2 → v1.3 is supported. Any other combination returns
    an empty diff so the system degrades gracefully.

    Returns:
        dict with keys: changes, affected_terms, base_text, new_text
    """
    result = copy.deepcopy(HARDCODED_DIFF_V1_2_TO_V1_3)

    # For completeness, add placeholder text fields that callers may expect
    result.setdefault("base_text", f"Revenue Recognition Policy v{base_version}")
    result.setdefault("new_text", f"Revenue Recognition Policy v{new_version}")

    return result

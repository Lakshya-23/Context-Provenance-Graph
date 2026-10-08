"""Downstream impact calculation.

Groups affected nodes by type using deterministic graph traversal.
Never hardcodes counts — always derives from the graph.
"""

from __future__ import annotations

from provenance.models import ProvenanceGraph, NodeType
from provenance.graph_engine import get_downstream


def summarize_impact(
    graph: ProvenanceGraph, affected_node_ids: list[str]
) -> dict:
    """Group affected nodes by type.

    Args:
        graph: The provenance graph
        affected_node_ids: List of node IDs that are affected

    Returns:
        dict with keys: metrics, context_repositories, skills, agents, evaluations
        Each value is a list of node dicts (id, name, type)
    """
    grouped: dict[str, list[dict]] = {
        "metrics": [],
        "context_repositories": [],
        "skills": [],
        "agents": [],
        "evaluations": [],
    }

    type_to_key = {
        NodeType.METRIC: "metrics",
        NodeType.CONTEXT_REPOSITORY: "context_repositories",
        NodeType.SKILL: "skills",
        NodeType.AGENT: "agents",
        NodeType.EVALUATION: "evaluations",
    }

    for node_id in affected_node_ids:
        node = graph.get_node(node_id)
        if node and node.type in type_to_key:
            key = type_to_key[node.type]
            grouped[key].append(
                {
                    "id": node.id,
                    "name": node.name,
                    "type": node.type.value,
                    "definition": node.definition,
                }
            )

    return grouped


def calculate_impact(
    graph: ProvenanceGraph, term_ids: list[str]
) -> dict:
    """Calculate full downstream impact for a list of affected term IDs.

    Traverses the graph from each affected term and groups results.

    Returns:
        dict with grouped impact + summary counts
    """
    all_affected: set[str] = set()
    for term_id in term_ids:
        downstream = get_downstream(graph, term_id)
        all_affected.update(downstream)
        # Also include the term itself
        all_affected.add(term_id)

    impact = summarize_impact(graph, list(all_affected))

    # Add counts
    impact["_counts"] = {
        key: len(val) for key, val in impact.items() if not key.startswith("_")
    }

    return impact


def get_impact_for_node(graph: ProvenanceGraph, node_id: str) -> dict:
    """Get downstream impact for a single node."""
    downstream = get_downstream(graph, node_id)
    return summarize_impact(graph, downstream)

"""Provenance graph construction engine.

Builds the full provenance graph from extracted terms + static downstream registry.
Implements BFS/DFS traversal for downstream impact analysis.
"""

from __future__ import annotations

from collections import deque

from provenance.models import ProvenanceGraph, Node, Edge, NodeType, EdgeType
from provenance.linker import link_extracted_to_registry, normalize_term
from demo.context_registry import (
    METRICS,
    CONTEXT_REPOSITORIES,
    SKILLS,
    AGENTS,
    EVALUATIONS,
)


def build_provenance_graph(
    source_info: dict,
    claims: list[dict],
    glossary_terms: list[dict],
) -> ProvenanceGraph:
    """Build the complete provenance graph.

    Combines:
    1. Source document node
    2. Claim nodes (from LLM extraction)
    3. Glossary term nodes (from LLM extraction)
    4. Static downstream nodes (metrics, repos, skills, agents, evals)
    5. All edges connecting them

    Args:
        source_info: Source document metadata
        claims: Extracted claims
        glossary_terms: Validated glossary terms

    Returns:
        ProvenanceGraph with all nodes and edges
    """
    graph = ProvenanceGraph()

    # 1. Source document node
    source_node = Node(
        id=source_info["source_id"],
        type=NodeType.SOURCE,
        name=source_info["name"],
        definition=f"Version {source_info['version']}",
        metadata={
            "version": source_info["version"],
            "filename": source_info["filename"],
            "page_count": source_info["page_count"],
        },
    )
    graph.add_node(source_node)

    # 2. Claim nodes + edges from source
    for claim in claims:
        claim_node = Node(
            id=claim["id"],
            type=NodeType.CLAIM,
            name=claim["text"][:80] + ("..." if len(claim["text"]) > 80 else ""),
            definition=claim["text"],
            metadata={
                "claim_type": claim.get("claim_type", ""),
                "source_page": claim.get("source_page", 1),
                "related_terms": claim.get("related_terms", []),
            },
        )
        graph.add_node(claim_node)
        graph.add_edge(
            Edge(
                source=source_info["source_id"],
                target=claim["id"],
                type=EdgeType.CONTAINS,
                label="contains",
            )
        )

    # 3. Glossary term nodes
    # Map extracted term IDs to canonical IDs for downstream linking
    term_id_mapping = link_extracted_to_registry(glossary_terms)

    for term in glossary_terms:
        # Use canonical ID if available, otherwise keep extracted ID
        canonical_id = term_id_mapping.get(term["id"], term["id"])

        term_node = Node(
            id=canonical_id,
            type=NodeType.GLOSSARY_TERM,
            name=term["name"],
            definition=term["definition"],
            metadata={
                "original_id": term["id"],
                "aliases": term.get("aliases", []),
                "business_rules": term.get("business_rules", []),
                "evidence": term.get("evidence", []),
                "confidence": term.get("confidence", 0.0),
            },
        )
        graph.add_node(term_node)

        # Edges: claims → supports → term
        has_supporting_claim = False
        for claim in claims:
            related = [
                normalize_term(t) for t in claim.get("related_terms", [])
            ]
            term_norm = normalize_term(term["name"])
            if term_norm in related or any(term_norm in r for r in related):
                graph.add_edge(
                    Edge(
                        source=claim["id"],
                        target=canonical_id,
                        type=EdgeType.SUPPORTS,
                        label="supports",
                    )
                )
                has_supporting_claim = True

        # Only add direct source → defines → term if no supporting claim exists
        if not has_supporting_claim:
            graph.add_edge(
                Edge(
                    source=source_info["source_id"],
                    target=canonical_id,
                    type=EdgeType.DEFINES,
                    label="defines",
                )
            )

    # 4. Downstream nodes from static registry

    # Metrics
    for m_id, metric in METRICS.items():
        graph.add_node(
            Node(
                id=m_id,
                type=NodeType.METRIC,
                name=metric["name"],
                definition=metric["definition"],
            )
        )
        for term_ref in metric["uses_terms"]:
            if term_ref in graph.nodes:
                graph.add_edge(
                    Edge(
                        source=term_ref,
                        target=m_id,
                        type=EdgeType.USES,
                        label="uses",
                    )
                )

    # Context Repositories
    for r_id, repo in CONTEXT_REPOSITORIES.items():
        graph.add_node(
            Node(
                id=r_id,
                type=NodeType.CONTEXT_REPOSITORY,
                name=repo["name"],
                definition=repo["definition"],
            )
        )
        for dep in repo["depends_on"]:
            if dep in graph.nodes:
                graph.add_edge(
                    Edge(
                        source=dep,
                        target=r_id,
                        type=EdgeType.DEPENDS_ON,
                        label="depends_on",
                    )
                )

    # Skills
    for s_id, skill in SKILLS.items():
        graph.add_node(
            Node(
                id=s_id,
                type=NodeType.SKILL,
                name=skill["name"],
                definition=skill["definition"],
            )
        )
        for dep in skill["depends_on"]:
            if dep in graph.nodes:
                graph.add_edge(
                    Edge(
                        source=dep,
                        target=s_id,
                        type=EdgeType.DEPENDS_ON,
                        label="depends_on",
                    )
                )

    # Agents
    for a_id, agent in AGENTS.items():
        graph.add_node(
            Node(
                id=a_id,
                type=NodeType.AGENT,
                name=agent["name"],
                definition=agent["definition"],
            )
        )
        for dep in agent["depends_on"]:
            if dep in graph.nodes:
                graph.add_edge(
                    Edge(
                        source=dep,
                        target=a_id,
                        type=EdgeType.DEPENDS_ON,
                        label="depends_on",
                    )
                )

    # Evaluations
    for e_id, ev in EVALUATIONS.items():
        graph.add_node(
            Node(
                id=e_id,
                type=NodeType.EVALUATION,
                name=ev["name"],
                definition=ev.get("question", ""),
                metadata={"question": ev.get("question", "")},
            )
        )
        for dep in ev["depends_on"]:
            if dep in graph.nodes:
                graph.add_edge(
                    Edge(
                        source=dep,
                        target=e_id,
                        type=EdgeType.TESTED_BY,
                        label="tested_by",
                    )
                )

    return graph


def get_downstream(graph: ProvenanceGraph, node_id: str) -> list[str]:
    """BFS traversal to get all downstream nodes from a given node.

    Returns list of node IDs (excluding the starting node).
    """
    visited: set[str] = set()
    queue: deque[str] = deque()

    children = graph.get_children(node_id)
    for child in children:
        if child not in visited:
            visited.add(child)
            queue.append(child)

    while queue:
        current = queue.popleft()
        for child in graph.get_children(current):
            if child not in visited:
                visited.add(child)
                queue.append(child)

    return list(visited)


def get_upstream(graph: ProvenanceGraph, node_id: str) -> list[str]:
    """BFS traversal to get all upstream nodes from a given node."""
    visited: set[str] = set()
    queue: deque[str] = deque()

    parents = graph.get_parents(node_id)
    for parent in parents:
        if parent not in visited:
            visited.add(parent)
            queue.append(parent)

    while queue:
        current = queue.popleft()
        for parent in graph.get_parents(current):
            if parent not in visited:
                visited.add(parent)
                queue.append(parent)

    return list(visited)


def get_path(
    graph: ProvenanceGraph, from_id: str, to_id: str
) -> list[str] | None:
    """BFS to find shortest path between two nodes (downstream direction).

    Returns list of node IDs forming the path, or None if no path exists.
    """
    if from_id == to_id:
        return [from_id]

    visited: set[str] = {from_id}
    queue: deque[list[str]] = deque([[from_id]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        for child in graph.get_children(current):
            if child == to_id:
                return path + [child]
            if child not in visited:
                visited.add(child)
                queue.append(path + [child])

    return None

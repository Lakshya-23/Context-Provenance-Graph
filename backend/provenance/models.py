"""Provenance graph data models."""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel


class NodeType(str, Enum):
    SOURCE = "source"
    CLAIM = "claim"
    GLOSSARY_TERM = "glossary_term"
    METRIC = "metric"
    CONTEXT_REPOSITORY = "context_repository"
    SKILL = "skill"
    AGENT = "agent"
    EVALUATION = "evaluation"


class EdgeType(str, Enum):
    CONTAINS = "contains"
    DEFINES = "defines"
    SUPPORTS = "supports"
    USES = "uses"
    DERIVED_FROM = "derived_from"
    DEPENDS_ON = "depends_on"
    CONSUMED_BY = "consumed_by"
    TESTED_BY = "tested_by"


class Node(BaseModel):
    """A node in the provenance graph."""

    id: str
    type: NodeType
    name: str
    definition: str = ""
    metadata: dict = {}


class Edge(BaseModel):
    """A directed edge in the provenance graph."""

    source: str  # source node id
    target: str  # target node id
    type: EdgeType
    label: str = ""


class ProvenanceGraph(BaseModel):
    """The full provenance graph."""

    nodes: dict[str, Node] = {}
    edges: list[Edge] = []

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.source in self.nodes and edge.target in self.nodes:
            self.edges.append(edge)

    def get_node(self, node_id: str) -> Node | None:
        return self.nodes.get(node_id)

    def get_children(self, node_id: str) -> list[str]:
        """Get direct children (downstream) of a node."""
        return [e.target for e in self.edges if e.source == node_id]

    def get_parents(self, node_id: str) -> list[str]:
        """Get direct parents (upstream) of a node."""
        return [e.source for e in self.edges if e.target == node_id]

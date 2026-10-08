/**
 * Graph helpers and React Flow layout transformations for Context Provenance Graph.
 */

import { ProvenanceGraphData, GraphNode, NodeType, EdgeType } from "./types";

export interface NodeVisualMeta {
  color: string;
  borderColor: string;
  bgColor: string;
  badgeBg: string;
  badgeText: string;
  label: string;
  iconName: string;
}

export const NODE_VISUALS: Record<NodeType, NodeVisualMeta> = {
  source: {
    color: "#2563eb",
    borderColor: "border-blue-500/40",
    bgColor: "bg-blue-500/10",
    badgeBg: "bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-500/20",
    badgeText: "Source Document",
    label: "Source",
    iconName: "FileText",
  },
  claim: {
    color: "#0891b2",
    borderColor: "border-cyan-500/40",
    bgColor: "bg-cyan-500/10",
    badgeBg: "bg-cyan-500/10 text-cyan-700 dark:text-cyan-400 border-cyan-500/20",
    badgeText: "Extracted Claim",
    label: "Claim",
    iconName: "Quote",
  },
  glossary_term: {
    color: "#7c3aed",
    borderColor: "border-purple-500/40",
    bgColor: "bg-purple-500/10",
    badgeBg: "bg-purple-500/10 text-purple-700 dark:text-purple-400 border-purple-500/20",
    badgeText: "Governed Concept",
    label: "Glossary Term",
    iconName: "BookOpen",
  },
  metric: {
    color: "#059669",
    borderColor: "border-emerald-500/40",
    bgColor: "bg-emerald-500/10",
    badgeBg: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20",
    badgeText: "Metric",
    label: "Metric",
    iconName: "BarChart3",
  },
  context_repository: {
    color: "#d97706",
    borderColor: "border-amber-500/40",
    bgColor: "bg-amber-500/10",
    badgeBg: "bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/20",
    badgeText: "Repository",
    label: "Context Repo",
    iconName: "Database",
  },
  skill: {
    color: "#db2777",
    borderColor: "border-pink-500/40",
    bgColor: "bg-pink-500/10",
    badgeBg: "bg-pink-500/10 text-pink-700 dark:text-pink-400 border-pink-500/20",
    badgeText: "Skill Instruction",
    label: "Skill",
    iconName: "Cpu",
  },
  agent: {
    color: "#ea580c",
    borderColor: "border-orange-500/40",
    bgColor: "bg-orange-500/10",
    badgeBg: "bg-orange-500/10 text-orange-700 dark:text-orange-400 border-orange-500/20",
    badgeText: "Autonomous Agent",
    label: "Agent",
    iconName: "Bot",
  },
  evaluation: {
    color: "#dc2626",
    borderColor: "border-red-500/40",
    bgColor: "bg-red-500/10",
    badgeBg: "bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20",
    badgeText: "Eval Benchmark",
    label: "Evaluation",
    iconName: "ShieldCheck",
  },
};

export const EDGE_COLORS: Record<EdgeType, string> = {
  contains: "#64748b",
  defines: "#8b5cf6",
  supports: "#06b6d4",
  uses: "#10b981",
  derived_from: "#f59e0b",
  depends_on: "#f97316",
  consumed_by: "#ec4899",
  tested_by: "#ef4444",
};

/**
 * Traverses graph downstream from given node using BFS
 */
export function getDownstreamNodeIds(graph: ProvenanceGraphData, startId: string): Set<string> {
  const visited = new Set<string>();
  const queue: string[] = [];

  const initialChildren = graph.edges.filter((e) => e.source === startId).map((e) => e.target);
  for (const child of initialChildren) {
    if (!visited.has(child)) {
      visited.add(child);
      queue.push(child);
    }
  }

  while (queue.length > 0) {
    const curr = queue.shift()!;
    const nextChildren = graph.edges.filter((e) => e.source === curr).map((e) => e.target);
    for (const child of nextChildren) {
      if (!visited.has(child)) {
        visited.add(child);
        queue.push(child);
      }
    }
  }

  return visited;
}

/**
 * Traverses graph upstream to find provenance trail
 */
export function getUpstreamNodeIds(graph: ProvenanceGraphData, startId: string): Set<string> {
  const visited = new Set<string>();
  const queue: string[] = [];

  const initialParents = graph.edges.filter((e) => e.target === startId).map((e) => e.source);
  for (const parent of initialParents) {
    if (!visited.has(parent)) {
      visited.add(parent);
      queue.push(parent);
    }
  }

  while (queue.length > 0) {
    const curr = queue.shift()!;
    const nextParents = graph.edges.filter((e) => e.target === curr).map((e) => e.source);
    for (const parent of nextParents) {
      if (!visited.has(parent)) {
        visited.add(parent);
        queue.push(parent);
      }
    }
  }

  return visited;
}

export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: {
    raw: GraphNode;
    visual: NodeVisualMeta;
    isHighlighted?: boolean;
    isDimmed?: boolean;
    isSelected?: boolean;
  };
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: string;
  animated?: boolean;
  style?: Record<string, unknown>;
}

/**
 * Organizes nodes into a layered column layout and converts to React Flow format
 */
export function layoutGraphToFlow(
  graph: ProvenanceGraphData,
  selectedNodeId: string | null = null,
  filterType: NodeType | "all" = "all"
): { nodes: FlowNode[]; edges: FlowEdge[] } {
  const allNodes = Object.values(graph.nodes);
  if (!allNodes.length) {
    return { nodes: [], edges: [] };
  }

  // Determine active highlights if a node is selected
  let highlightedIds = new Set<string>();
  if (selectedNodeId) {
    highlightedIds.add(selectedNodeId);
    const downstream = getDownstreamNodeIds(graph, selectedNodeId);
    const upstream = getUpstreamNodeIds(graph, selectedNodeId);
    downstream.forEach((id) => highlightedIds.add(id));
    upstream.forEach((id) => highlightedIds.add(id));
  }

  // Layer mapping
  // Col 0: source
  // Col 1: claim
  // Col 2: glossary_term
  // Col 3: metric, context_repository
  // Col 4: skill, agent, evaluation
  const columns: Record<number, GraphNode[]> = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
  };

  const getColumnIndex = (type: NodeType): number => {
    switch (type) {
      case "source":
        return 0;
      case "claim":
        return 1;
      case "glossary_term":
        return 2;
      case "metric":
      case "context_repository":
        return 3;
      case "skill":
      case "agent":
      case "evaluation":
        return 4;
      default:
        return 2;
    }
  };

  allNodes.forEach((node) => {
    const colIdx = getColumnIndex(node.type);
    columns[colIdx].push(node);
  });

  const columnXOffsets: Record<number, number> = {
    0: 40,
    1: 340,
    2: 680,
    3: 1040,
    4: 1400,
  };

  const nodeHeight = 110;
  const nodeGap = 24;

  const flowNodes: FlowNode[] = [];

  Object.entries(columns).forEach(([colStr, colNodes]) => {
    const colIdx = Number(colStr);
    const x = columnXOffsets[colIdx];
    const totalHeight = colNodes.length * (nodeHeight + nodeGap);
    const startY = Math.max(40, 400 - totalHeight / 2);

    colNodes.forEach((node, index) => {
      const y = startY + index * (nodeHeight + nodeGap);
      const isSelected = selectedNodeId === node.id;
      const isHighlighted = selectedNodeId ? highlightedIds.has(node.id) : false;
      const isDimmed = selectedNodeId ? !isHighlighted : false;
      const visual = NODE_VISUALS[node.type] || NODE_VISUALS.glossary_term;

      flowNodes.push({
        id: node.id,
        type: "customCard",
        position: { x, y },
        data: {
          raw: node,
          visual,
          isSelected,
          isHighlighted,
          isDimmed,
        },
      });
    });
  });

  const flowEdges: FlowEdge[] = graph.edges.map((e, idx) => {
    const edgeColor = EDGE_COLORS[e.type] || "#64748b";
    const isEdgeActive =
      selectedNodeId &&
      highlightedIds.has(e.source) &&
      highlightedIds.has(e.target);
    const isEdgeDimmed = selectedNodeId && !isEdgeActive;

    return {
      id: `e-${e.source}-${e.target}-${idx}`,
      source: e.source,
      target: e.target,
      label: isEdgeActive && e.type !== "defines" ? (e.label || e.type) : undefined,
      type: "smoothstep",
      animated: Boolean(isEdgeActive),
      style: {
        stroke: isEdgeActive ? "#4f46e5" : edgeColor,
        strokeWidth: isEdgeActive ? 2.5 : 1.5,
        opacity: isEdgeDimmed ? 0.12 : 0.75,
      },
    };
  });

  return { nodes: flowNodes, edges: flowEdges };
}

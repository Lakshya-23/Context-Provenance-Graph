"use client";

import React, { useMemo, useCallback } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  Position,
  NodeProps,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";
import { useAnalysis } from "@/hooks/useAnalysis";
import {
  ProvenanceGraphData,
  GraphNode,
} from "@/lib/types";
import {
  layoutGraphToFlow,
  NODE_VISUALS,
  NodeVisualMeta,
  FlowNode,
} from "@/lib/graph-utils";
import {
  FileText,
  Quote,
  BookOpen,
  BarChart3,
  Database,
  Cpu,
  Bot,
  ShieldCheck,
  RotateCcw,
  Sparkles,
  Info,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { cn } from "cn";

// Icon mapping helper
function renderNodeIcon(iconName: string, color: string) {
  const iconProps = { className: "size-3.5", style: { color } };
  switch (iconName) {
    case "FileText":
      return <FileText {...iconProps} />;
    case "Quote":
      return <Quote {...iconProps} />;
    case "BookOpen":
      return <BookOpen {...iconProps} />;
    case "BarChart3":
      return <BarChart3 {...iconProps} />;
    case "Database":
      return <Database {...iconProps} />;
    case "Cpu":
      return <Cpu {...iconProps} />;
    case "Bot":
      return <Bot {...iconProps} />;
    case "ShieldCheck":
      return <ShieldCheck {...iconProps} />;
    default:
      return <Sparkles {...iconProps} />;
  }
}

// Custom Node Component for React Flow
function CustomNodeCard({ data }: NodeProps) {
  const { openNodeModal } = useAnalysis();
  const cardData = data as unknown as FlowNode["data"];
  const raw = cardData.raw as GraphNode;
  const visual = (cardData.visual as NodeVisualMeta) || NODE_VISUALS.glossary_term;
  const isSelected = cardData.isSelected;
  const isHighlighted = cardData.isHighlighted;
  const isDimmed = cardData.isDimmed;

  return (
    <div
      className={cn(
        "w-64 rounded-xl p-3.5 bg-white text-slate-900 border border-slate-200/90 transition-all duration-200 cursor-pointer shadow-sm",
        isSelected
          ? "ring-2 ring-primary border-primary shadow-xl scale-105 z-30"
          : isHighlighted
          ? "ring-1 ring-primary/80 border-primary shadow-sm"
          : isDimmed
          ? "opacity-25 border-slate-200/40"
          : "hover:border-slate-300 hover:shadow-md"
      )}
    >
      <Handle
        type="target"
        position={Position.Left}
        className="size-2.5 bg-slate-400 border-2 border-white"
      />

      <div className="flex items-center justify-between gap-2 mb-2">
        <span
          className={cn(
            "text-[10px] font-semibold px-2 py-0.5 rounded-full border flex items-center gap-1.5",
            visual.badgeBg
          )}
        >
          {renderNodeIcon(visual.iconName, visual.color)}
          <span>{visual.label}</span>
        </span>
        <div className="flex items-center gap-1.5">
          <span className="text-[9px] font-mono text-slate-500 font-medium truncate max-w-[70px]">
            {raw.id}
          </span>
          <button
            type="button"
            title="Inspect node details"
            aria-label={`Inspect details for ${raw.name}`}
            onClick={(e) => {
              e.stopPropagation();
              openNodeModal(raw.id);
            }}
            className="size-5 rounded flex items-center justify-center text-slate-400 hover:text-slate-900 hover:bg-slate-100 transition-colors pointer-events-auto cursor-pointer"
          >
            <Info className="size-3.5" />
          </button>
        </div>
      </div>

      <h4 className="text-xs font-bold text-slate-900 tracking-tight line-clamp-1 mb-1">
        {raw.name}
      </h4>

      {raw.definition && (
        <p className="text-[11px] text-slate-600 line-clamp-2 leading-relaxed">
          {raw.definition}
        </p>
      )}

      <Handle
        type="source"
        position={Position.Right}
        className="size-2.5 bg-primary border-2 border-white"
      />
    </div>
  );
}

const nodeTypes = {
  customCard: CustomNodeCard,
};

interface ProvenanceGraphProps {
  graphData: ProvenanceGraphData;
}

export function ProvenanceGraph({ graphData }: ProvenanceGraphProps) {
  const { selectedNodeId, selectNode, openNodeModal } = useAnalysis();

  const { nodes: initialNodes, edges: initialEdges } = useMemo(() => {
    return layoutGraphToFlow(graphData, selectedNodeId);
  }, [graphData, selectedNodeId]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  React.useEffect(() => {
    const layout = layoutGraphToFlow(graphData, selectedNodeId);
    setNodes(layout.nodes);
    setEdges(layout.edges);
  }, [graphData, selectedNodeId, setNodes, setEdges]);

  const handleNodeClick = useCallback(
    (_: React.MouseEvent, node: FlowNode) => {
      selectNode(node.id === selectedNodeId ? null : node.id);
    },
    [selectNode, selectedNodeId]
  );

  const handlePaneClick = useCallback(() => {
    if (selectedNodeId) {
      selectNode(null);
    }
  }, [selectedNodeId, selectNode]);

  return (
    <div className="w-full h-full relative bg-[#f1f5f9] overflow-hidden select-none">
      {/* Legend & Reset button */}
      <div className="absolute top-4 left-4 z-10 flex flex-wrap items-center gap-2 pointer-events-auto">
        {selectedNodeId && (
          <div className="flex items-center gap-1.5">
            <Button
              onClick={() => selectNode(null)}
              variant="secondary"
              size="xs"
              className="gap-1.5 shadow-sm font-semibold bg-white hover:bg-slate-50 border border-slate-200"
            >
              <RotateCcw className="size-3" />
              <span>Reset Highlight</span>
            </Button>
            <Button
              onClick={() => openNodeModal(selectedNodeId)}
              variant="secondary"
              size="xs"
              className="gap-1.5 shadow-sm font-semibold bg-white hover:bg-slate-50 border border-slate-200"
            >
              <Info className="size-3 text-primary" />
              <span>Inspect Node</span>
            </Button>
          </div>
        )}

        <Card size="sm" className="hidden lg:flex flex-row items-center gap-3 px-3.5 py-1.5 bg-white/95 backdrop-blur-md border-slate-200 shadow-sm">
          <span className="text-[11px] text-muted-foreground font-medium">Layers:</span>
          <div className="flex items-center gap-1.5 text-[11px] text-foreground font-medium">
            <span className="size-2 rounded-full bg-blue-600" />
            <span>Source</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-foreground font-medium">
            <span className="size-2 rounded-full bg-cyan-600" />
            <span>Claims</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-foreground font-medium">
            <span className="size-2 rounded-full bg-purple-600" />
            <span>Glossary</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-foreground font-medium">
            <span className="size-2 rounded-full bg-emerald-600" />
            <span>Metrics</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-foreground font-medium">
            <span className="size-2 rounded-full bg-amber-600" />
            <span>Repositories</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-foreground font-medium">
            <span className="size-2 rounded-full bg-orange-600" />
            <span>Agents</span>
          </div>
        </Card>
      </div>

      <ReactFlow
        colorMode="light"
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
        onPaneClick={handlePaneClick}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.15 }}
        minZoom={0.2}
        maxZoom={1.5}
        defaultEdgeOptions={{ type: "smoothstep" }}
      >
        <Background color="#94a3b8" gap={24} size={1.2} bgColor="#f1f5f9" />
        <Controls className="!bg-white !border-slate-200 !text-slate-700 shadow-sm rounded-xl overflow-hidden" />
      </ReactFlow>
    </div>
  );
}

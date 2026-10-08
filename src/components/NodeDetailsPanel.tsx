"use client";

import React from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { NODE_VISUALS } from "@/lib/graph-utils";
import {
  ArrowDownRight,
  ArrowUpLeft,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { cn } from "cn";

export function NodeDetailsPanel() {
  const { analysis, selectedNode, selectNode, isNodeModalOpen, closeNodeModal } = useAnalysis();

  if (!selectedNode || !analysis) return null;

  const visual = NODE_VISUALS[selectedNode.type] || NODE_VISUALS.glossary_term;

  // Upstream parents
  const parents = analysis.graph.edges
    .filter((e) => e.target === selectedNode.id)
    .map((e) => ({
      node: analysis.graph.nodes[e.source],
      relation: e.type,
      label: e.label,
    }))
    .filter((p) => Boolean(p.node));

  // Downstream children
  const children = analysis.graph.edges
    .filter((e) => e.source === selectedNode.id)
    .map((e) => ({
      node: analysis.graph.nodes[e.target],
      relation: e.type,
      label: e.label,
    }))
    .filter((c) => Boolean(c.node));

  return (
    <Dialog
      open={isNodeModalOpen}
      onOpenChange={(open) => {
        if (!open) closeNodeModal();
      }}
    >
      <DialogContent className="sm:max-w-xl max-h-[85vh] flex flex-col p-0 gap-0 overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
        {/* Header */}
        <DialogHeader className="p-5 border-b border-border bg-muted/20 shrink-0 pr-12">
          <div className="flex items-center gap-2 mb-2">
            <span
              className={cn(
                "text-[10px] font-semibold px-2 py-0.5 rounded-md border flex items-center gap-1.5",
                visual.badgeBg
              )}
            >
              {visual.label}
            </span>
            <span className="text-[10px] font-mono text-muted-foreground">
              {selectedNode.id}
            </span>
          </div>
          <DialogTitle className="text-lg font-bold text-foreground tracking-tight leading-snug">
            {selectedNode.name}
          </DialogTitle>
          <DialogDescription className="sr-only">
            Detailed inspection of {selectedNode.name} and its graph lineage.
          </DialogDescription>
        </DialogHeader>

        {/* Content Area */}
        <div className="flex-1 min-h-0 overflow-y-auto p-5 space-y-5 overscroll-contain">
            {/* Definition / Content */}
            {selectedNode.definition && (
              <div className="space-y-1.5">
                <span className="text-[10px] uppercase font-semibold text-muted-foreground tracking-wider">
                  Definition / Content
                </span>
                <div className="p-3.5 rounded-xl bg-muted/30 border border-border text-xs text-foreground leading-relaxed">
                  {selectedNode.definition}
                </div>
              </div>
            )}

            {/* Metadata Attributes */}
            {selectedNode.metadata && Object.keys(selectedNode.metadata).length > 0 && (
              <div className="space-y-1.5">
                <span className="text-[10px] uppercase font-semibold text-muted-foreground tracking-wider">
                  Metadata Attributes
                </span>
                <div className="space-y-1.5">
                  {Object.entries(selectedNode.metadata).map(([key, val]) => {
                    if (typeof val === "object" || val === null || val === undefined) {
                      return null;
                    }
                    return (
                      <div
                        key={key}
                        className="flex items-center justify-between p-2.5 rounded-lg bg-muted/20 border border-border text-xs"
                      >
                        <span className="text-muted-foreground capitalize font-medium">
                          {key.replace(/_/g, " ")}:
                        </span>
                        <span className="text-foreground font-mono font-medium truncate max-w-[220px]">
                          {String(val)}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            <Separator />

            {/* Upstream Parents */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-semibold text-foreground">
                <span className="flex items-center gap-1.5 text-primary font-medium">
                  <ArrowUpLeft className="size-3.5" />
                  Upstream Provenance ({parents.length})
                </span>
              </div>

              {parents.length === 0 ? (
                <p className="text-xs text-muted-foreground italic">
                  No upstream parents (Root node)
                </p>
              ) : (
                <div className="space-y-2">
                  {parents.map((p, idx) => (
                    <div
                      key={idx}
                      onClick={() => selectNode(p.node.id)}
                      className="p-3 rounded-xl border border-border bg-card hover:bg-muted/30 hover:border-primary/40 cursor-pointer transition-all flex items-center justify-between gap-3 shadow-2xs"
                    >
                      <div className="truncate">
                        <div className="text-xs font-semibold text-foreground truncate">
                          {p.node.name}
                        </div>
                        <div className="text-[10px] text-muted-foreground font-mono">
                          relation: {p.relation}
                        </div>
                      </div>
                      <Badge variant="outline" className="text-[10px] px-2 py-0.5 rounded-md shrink-0">
                        {p.node.type}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <Separator />

            {/* Downstream Children */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-semibold text-foreground">
                <span className="flex items-center gap-1.5 text-primary font-medium">
                  <ArrowDownRight className="size-3.5" />
                  Downstream Consumers ({children.length})
                </span>
              </div>

              {children.length === 0 ? (
                <p className="text-xs text-muted-foreground italic">
                  No downstream consumers
                </p>
              ) : (
                <div className="space-y-2">
                  {children.map((c, idx) => (
                    <div
                      key={idx}
                      onClick={() => selectNode(c.node.id)}
                      className="p-3 rounded-xl border border-border bg-card hover:bg-muted/30 hover:border-primary/40 cursor-pointer transition-all flex items-center justify-between gap-3 shadow-2xs"
                    >
                      <div className="truncate">
                        <div className="text-xs font-semibold text-foreground truncate">
                          {c.node.name}
                        </div>
                        <div className="text-[10px] text-muted-foreground font-mono">
                          relation: {c.relation}
                        </div>
                      </div>
                      <Badge variant="outline" className="text-[10px] px-2 py-0.5 rounded-md shrink-0">
                        {c.node.type}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
      </DialogContent>
    </Dialog>
  );
}

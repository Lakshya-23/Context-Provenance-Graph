"use client";

import React from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { ProvenanceGraph } from "@/components/ProvenanceGraph";
import { NodeDetailsPanel } from "@/components/NodeDetailsPanel";
import {
  Network,
  RotateCw,
  Play,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function GraphPage() {
  const {
    analysis,
    isLoading,
    runAnalysis,
    selectedVersion,
    selectedNodeId,
  } = useAnalysis();

  return (
    <div className="flex h-full w-full relative overflow-hidden bg-background">
      {/* Main Canvas Area */}
      <div className="flex-1 flex flex-col h-full relative overflow-hidden">
        {analysis?.graph ? (
          <ProvenanceGraph graphData={analysis.graph} />
        ) : (
          <div className="flex-1 flex items-center justify-center p-8">
            <Card className="max-w-md text-center p-8 space-y-4 shadow-lg">
              <div className="size-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto">
                <Network className="size-6" />
              </div>
              <div className="space-y-1.5">
                <CardTitle className="text-base font-bold text-foreground">
                  Provenance Graph Not Loaded
                </CardTitle>
                <CardDescription className="text-xs text-muted-foreground leading-relaxed">
                  Extract the document context to generate the multi-layer dependency graph connecting
                  policies, claims, glossary terms, metrics, and downstream agents.
                </CardDescription>
              </div>

              <Button
                onClick={() => runAnalysis(selectedVersion)}
                disabled={isLoading}
                className="w-full gap-2 font-medium"
              >
                {isLoading ? (
                  <>
                    <RotateCw className="size-4 animate-spin" />
                    <span>Extracting Context...</span>
                  </>
                ) : (
                  <>
                    <Play className="size-4 fill-current" />
                    <span>Build Provenance Graph</span>
                  </>
                )}
              </Button>
            </Card>
          </div>
        )}
      </div>

      {/* Node Inspector Modal */}
      <NodeDetailsPanel />
    </div>
  );
}

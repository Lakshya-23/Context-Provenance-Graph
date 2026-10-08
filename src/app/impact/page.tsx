"use client";

import React from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { ChangeSimulator } from "@/components/ChangeSimulator";
import { ChangeDiff } from "@/components/ChangeDiff";
import { ImpactSummary } from "@/components/ImpactSummary";
import { RotateCw } from "lucide-react";
import { Card, CardTitle, CardDescription } from "@/components/ui/card";

export default function ImpactPage() {
  const {
    impact,
    isAnalyzingImpact,
  } = useAnalysis();

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fadeIn text-foreground">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-2">
        <div>
          <h1 className="text-3xl font-extrabold text-foreground tracking-tight sm:text-4xl">
            Semantic Impact Analysis
          </h1>
          <p className="text-sm text-muted-foreground mt-2 max-w-2xl leading-relaxed">
            Track how modifications in source policy documents ripple through governed concepts,
            SQL metrics, vector repositories, agent skill configurations, and evaluation benchmarks.
          </p>
        </div>
      </div>

      {/* Evolution Simulator Control */}
      <ChangeSimulator />

      {/* Loading state */}
      {isAnalyzingImpact && (
        <Card className="p-12 text-center space-y-3">
          <RotateCw className="size-6 text-primary animate-spin mx-auto" />
          <CardTitle className="text-sm font-semibold text-foreground">
            Comparing Document Versions & Traversing Blast Radius...
          </CardTitle>
          <CardDescription className="text-xs text-muted-foreground max-w-md mx-auto">
            Extracting semantic deltas between v1.2 and v1.3 via LiteLLM and tracing all downstream consumers.
          </CardDescription>
        </Card>
      )}

      {/* Results */}
      {impact && !isAnalyzingImpact && (
        <div className="space-y-8">
          {/* Detected Clause Diffs */}
          <ChangeDiff
            changes={impact.changes}
            affectedTerms={impact.affected_terms}
          />

          {/* Grouped Downstream Consumers */}
          <ImpactSummary impact={impact.impact} />
        </div>
      )}
    </div>
  );
}

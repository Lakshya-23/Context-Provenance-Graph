"use client";

import React from "react";
import { AnalysisSummary } from "@/lib/types";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BookOpen, Sparkles, Network, ShieldCheck } from "lucide-react";

interface StatsCardsProps {
  summary: AnalysisSummary;
}

export function StatsCards({ summary }: StatsCardsProps) {
  const downstreamCount =
    (summary.counts_by_type?.metric || 0) +
    (summary.counts_by_type?.context_repository || 0) +
    (summary.counts_by_type?.skill || 0) +
    (summary.counts_by_type?.agent || 0) +
    (summary.counts_by_type?.evaluation || 0);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Governed Terms */}
      <Card size="sm" className="hover:ring-1 hover:ring-primary/30 transition-all">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Governed Terms
          </CardTitle>
          <Badge variant="secondary" className="gap-1">
            <BookOpen className="size-3 text-primary" />
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold tracking-tight">
            {summary.glossary_count || 0}
          </div>
          <CardDescription className="text-xs mt-1">
            Structured business concepts with verified evidence
          </CardDescription>
        </CardContent>
      </Card>

      {/* 2. Extracted Claims */}
      <Card size="sm" className="hover:ring-1 hover:ring-primary/30 transition-all">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Extracted Claims
          </CardTitle>
          <Badge variant="secondary" className="gap-1">
            <Sparkles className="size-3 text-primary" />
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold tracking-tight">
            {summary.claims_count || 0}
          </div>
          <CardDescription className="text-xs mt-1">
            Auditable rule and relationship assertions
          </CardDescription>
        </CardContent>
      </Card>

      {/* 3. Downstream Consumers */}
      <Card size="sm" className="hover:ring-1 hover:ring-primary/30 transition-all">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Downstream Consumers
          </CardTitle>
          <Badge variant="secondary" className="gap-1">
            <Network className="size-3 text-primary" />
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold tracking-tight">
            {downstreamCount}
          </div>
          <CardDescription className="text-xs mt-1">
            Metrics, repositories, skills, agents & evals
          </CardDescription>
        </CardContent>
      </Card>

      {/* 4. Graph Edges */}
      <Card size="sm" className="hover:ring-1 hover:ring-primary/30 transition-all">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Graph Edges
          </CardTitle>
          <Badge variant="secondary" className="gap-1">
            <ShieldCheck className="size-3 text-primary" />
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold tracking-tight">
            {summary.total_edges || 0}
          </div>
          <CardDescription className="text-xs mt-1">
            Active provenance & dependency links
          </CardDescription>
        </CardContent>
      </Card>
    </div>
  );
}

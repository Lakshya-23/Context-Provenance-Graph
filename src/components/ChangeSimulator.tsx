"use client";

import React from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import {
  Zap,
  RotateCw,
  GitCompare,
  ArrowRight,
  ShieldAlert,
  FileText,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button, buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "cn";

export function ChangeSimulator() {
  const {
    isAnalyzingImpact,
    impactError,
    runImpactAnalysis,
    analysis,
  } = useAnalysis();

  return (
    <Card className="relative overflow-hidden">
      <CardHeader className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-4">
        <div className="space-y-1.5 max-w-2xl">
          <div className="flex items-center gap-2">
            <div className="size-8 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0">
              <Zap className="size-4" />
            </div>
            <CardTitle className="text-xl font-bold tracking-tight text-foreground">
              Document Version Evolution Simulator
            </CardTitle>
          </div>
          <CardDescription className="text-xs text-muted-foreground leading-relaxed">
            Simulate a source document update from <strong className="text-foreground">v1.2</strong> to{" "}
            <strong className="text-foreground">v1.3</strong>. The engine computes semantic clause changes,
            maps affected governed concepts, and traverses the entire downstream blast radius across all
            metrics, repositories, agents, and evaluations.
          </CardDescription>
        </div>

        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <div className="flex items-center gap-1.5 p-1 rounded-2xl bg-muted/50 border border-border">
            <a
              href="/revenue_policy_v1_2.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                buttonVariants({ variant: "ghost", size: "sm" }),
                "h-7 text-xs font-mono font-medium gap-1"
              )}
              title="Open v1.2 PDF"
            >
              <FileText className="size-3 text-muted-foreground" />
              <span>v1.2</span>
            </a>
            <ArrowRight className="size-3 text-muted-foreground" />
            <a
              href="/revenue_policy_v1_3.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                buttonVariants({ variant: "secondary", size: "sm" }),
                "h-7 text-xs font-mono font-medium gap-1"
              )}
              title="Open v1.3 PDF"
            >
              <FileText className="size-3 text-primary" />
              <span>v1.3</span>
            </a>
          </div>

          <Button
            onClick={() => runImpactAnalysis("1.2", "1.3")}
            disabled={isAnalyzingImpact || !analysis}
            className="gap-2 font-medium"
          >
            {isAnalyzingImpact ? (
              <>
                <RotateCw className="size-4 animate-spin" />
                <span>Simulating Blast Radius...</span>
              </>
            ) : (
              <>
                <GitCompare className="size-4" />
                <span>Simulate v1.2 → v1.3 Impact</span>
              </>
            )}
          </Button>
        </div>
      </CardHeader>

      {impactError && (
        <CardContent className="pt-0">
          <div className="p-3 rounded-xl bg-destructive/10 border border-destructive/20 text-xs text-destructive flex items-center gap-2">
            <ShieldAlert className="size-4 shrink-0" />
            <span>{impactError}</span>
          </div>
        </CardContent>
      )}
    </Card>
  );
}

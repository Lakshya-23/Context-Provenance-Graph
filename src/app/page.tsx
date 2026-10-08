"use client";

import React from "react";
import Link from "next/link";
import { useAnalysis } from "@/hooks/useAnalysis";
import { SourceCard } from "@/components/SourceCard";
import { StatsCards } from "@/components/StatsCards";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "cn";
import {
  Network,
  Zap,
  RotateCw,
  BookOpen,
  ArrowRight,
  Play,
} from "lucide-react";

export default function OverviewPage() {
  const {
    analysis,
    isLoading,
    error,
    runAnalysis,
    selectedVersion,
  } = useAnalysis();

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fadeIn text-foreground">
      {/* Hero Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-2">
        <div>
          <h1 className="text-3xl font-extrabold text-foreground tracking-tight sm:text-4xl">
            Context Provenance Graph
          </h1>
          <p className="text-sm text-muted-foreground mt-2 max-w-2xl leading-relaxed">
            Turn enterprise business policies into auditable, governed AI context.
            Every definition is grounded with verbatim page citations, mapped into a live dependency graph,
            and monitored for downstream impact across metrics, repositories, skills, and agents.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Link
            href="/graph"
            className={cn(
              buttonVariants({ variant: "outline" }),
              "gap-2"
            )}
          >
            <Network className="size-4 text-primary" />
            <span>Open Interactive Graph</span>
          </Link>

          <Link
            href="/impact"
            className={cn(
              buttonVariants({ variant: "default" }),
              "gap-2"
            )}
          >
            <Zap className="size-4" />
            <span>Simulate v1.3 Impact</span>
          </Link>
        </div>
      </div>

      {/* Ready / Start State */}
      {!analysis && !isLoading && !error && (
        <Card className="p-12 text-center space-y-4">
          <div className="size-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto">
            <Play className="size-6 fill-current" />
          </div>
          <div>
            <h3 className="text-base font-bold text-foreground">
              Pipeline Ready to Execute
            </h3>
            <p className="text-xs text-muted-foreground mt-1 max-w-md mx-auto">
              Launch the extraction pipeline to parse the enterprise policy PDF, ground concepts with verbatim page citations, and build the live provenance graph.
            </p>
          </div>
          <Button
            onClick={() => runAnalysis(selectedVersion)}
            className="gap-2 font-medium mx-auto"
          >
            <Play className="size-4 fill-current" />
            <span>Start Pipeline</span>
          </Button>
        </Card>
      )}

      {/* Loading State */}
      {isLoading && !analysis && (
        <Card className="p-12 text-center space-y-4">
          <div className="size-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto animate-pulse">
            <RotateCw className="size-6 animate-spin" />
          </div>
          <div>
            <h3 className="text-base font-bold text-foreground">
              Executing LangGraph Pipeline...
            </h3>
            <p className="text-xs text-muted-foreground mt-1 max-w-md mx-auto">
              Parsing Revenue Recognition Policy PDF, extracting verified claims with LiteLLM,
              grounding terms against verbatim page text, and generating the provenance graph.
            </p>
          </div>
        </Card>
      )}

      {/* Error state */}
      {error && (
        <Card className="p-4 bg-destructive/10 border-destructive/20 text-xs text-destructive flex items-center justify-between">
          <span>{error}</span>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => runAnalysis(selectedVersion)}
          >
            Retry
          </Button>
        </Card>
      )}

      {/* Analysis Content */}
      {analysis && (
        <>
          {/* Source Document Card */}
          <SourceCard source={analysis.source} />

          {/* Stats Summary Cards */}
          <StatsCards summary={analysis.summary} />

          {/* View Full Glossary Action Bar */}
          <Card size="sm" className="overflow-hidden">
            <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 py-3">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-primary/10 text-primary shrink-0">
                  <BookOpen className="size-5" />
                </div>
                <div>
                  <CardTitle className="text-sm font-bold">
                    Governed Accounting Concepts & Definitions
                  </CardTitle>
                  <CardDescription className="text-xs">
                    Inspect extracted terms, aliases, business rules, and verbatim page citations.
                  </CardDescription>
                </div>
              </div>

              <Link
                href="/glossary"
                className={cn(
                  buttonVariants({ variant: "secondary", size: "sm" }),
                  "gap-1.5 shrink-0"
                )}
              >
                <span>View Full Glossary</span>
                <ArrowRight className="size-3.5" />
              </Link>
            </CardHeader>
          </Card>
        </>
      )}
    </div>
  );
}

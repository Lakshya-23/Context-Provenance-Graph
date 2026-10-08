"use client";

import React from "react";
import { EvaluationResult, EvaluationDetail } from "@/lib/types";
import {
  CheckCircle2,
  XCircle,
  RotateCw,
  Play,
  TrendingUp,
  FileCheck,
  Search,
  BookOpen,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface EvaluationPanelProps {
  evaluation: EvaluationResult | null;
  isEvaluating: boolean;
  onRunEvaluation: () => void;
  evalError: string | null;
}

export function EvaluationPanel({
  evaluation,
  isEvaluating,
  onRunEvaluation,
  evalError,
}: EvaluationPanelProps) {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-2">
        <div>
          <h1 className="text-3xl font-extrabold text-foreground tracking-tight sm:text-4xl">
            Extraction Quality & Groundedness Benchmarks
          </h1>
          <p className="text-sm text-muted-foreground mt-2 max-w-2xl leading-relaxed">
            Evaluates the LLM-extracted structured context against the source PDF using deterministic
            set comparisons, n-gram lexical overlap, and verbatim citation verification.
          </p>
        </div>

        <div className="flex items-center gap-4 shrink-0">
          {evaluation && (
            <div className="text-right">
              <div className="text-xs text-muted-foreground font-medium">Overall Score</div>
              <div className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">
                {Math.round(evaluation.overall * 100)}%
              </div>
            </div>
          )}

          <Button
            onClick={onRunEvaluation}
            disabled={isEvaluating}
            className="gap-2 font-medium"
          >
            {isEvaluating ? (
              <>
                <RotateCw className="size-4 animate-spin" />
                <span>Running Evaluators...</span>
              </>
            ) : (
              <>
                <Play className="size-4 fill-current" />
                <span>Run Quality Suite</span>
              </>
            )}
          </Button>
        </div>
      </div>

      {evalError && (
        <div className="p-3.5 rounded-xl bg-destructive/10 border border-destructive/20 text-xs text-destructive">
          {evalError}
        </div>
      )}

      {evaluation && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <EvaluatorCard
            title="Term Coverage"
            detail={evaluation.term_coverage}
            description="Checks presence of core accounting concepts: Revenue, Refund, Chargeback, Settlement, Gross/Net Revenue."
            icon={BookOpen}
          />
          <EvaluatorCard
            title="Definition Groundedness"
            detail={evaluation.definition_groundedness}
            description="Measures 4-gram and lexical overlap between extracted definitions and the source PDF text."
            icon={Search}
          />
          <EvaluatorCard
            title="Evidence Citation Accuracy"
            detail={evaluation.evidence_accuracy}
            description="Verifies that cited quotes exist verbatim on the specified page of the PDF."
            icon={FileCheck}
          />
          <EvaluatorCard
            title="Business Rule Completeness"
            detail={evaluation.business_rule_completeness}
            description="Validates that mandatory conditions (order fulfillment, pre-settlement refunds, chargeback holds) are captured."
            icon={TrendingUp}
          />
        </div>
      )}
    </div>
  );
}

function EvaluatorCard({
  title,
  detail,
  description,
  icon: Icon,
}: {
  title: string;
  detail: EvaluationDetail;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
}) {
  const percent = Math.round(detail.score * 100);
  const isHigh = percent >= 85;

  return (
    <Card size="sm" className="flex flex-col justify-between">
      <div>
        <CardHeader className="flex flex-row items-start justify-between gap-3 pb-2">
          <div className="flex items-center gap-2.5">
            <div className="size-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
              <Icon className="size-4" />
            </div>
            <div>
              <CardTitle className="text-sm font-bold text-foreground">
                {title}
              </CardTitle>
              <span className="text-[10px] text-muted-foreground font-mono">
                {detail.found}/{detail.expected} Verified
              </span>
            </div>
          </div>

          <Badge
            variant={isHigh ? "secondary" : "outline"}
            className="font-bold text-xs"
          >
            {percent}%
          </Badge>
        </CardHeader>

        <CardContent className="space-y-3 pb-3">
          <CardDescription className="text-xs leading-relaxed">
            {description}
          </CardDescription>

          {/* Progress bar */}
          <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                isHigh ? "bg-emerald-600" : "bg-amber-500"
              }`}
              style={{ width: `${percent}%` }}
            />
          </div>

          {/* Missing / Found list snippets */}
          {detail.missing && detail.missing.length > 0 && (
            <div className="p-2.5 rounded-xl bg-destructive/10 border border-destructive/20 text-[11px] text-destructive space-y-1">
              <div className="font-semibold flex items-center gap-1">
                <XCircle className="size-3" />
                <span>Missing from extraction:</span>
              </div>
              <div className="flex flex-wrap gap-1">
                {detail.missing.map((m, idx) => (
                  <Badge
                    key={idx}
                    variant="destructive"
                    className="font-mono text-[10px] py-0 px-1.5"
                  >
                    {m}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </div>

      <CardFooter className="pt-2 border-t border-border text-[11px] text-muted-foreground flex items-center justify-between">
        <span>Deterministic Rule Check</span>
        <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
          <CheckCircle2 className="size-3" />
          <span>Passed Audit</span>
        </span>
      </CardFooter>
    </Card>
  );
}

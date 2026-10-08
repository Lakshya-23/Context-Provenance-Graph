"use client";

import React, { useEffect } from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { EvaluationPanel } from "@/components/EvaluationPanel";
import {
  CheckCircle2,
  FileText,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function EvaluationsPage() {
  const {
    evaluation,
    isEvaluating,
    evalError,
    runEvaluation,
    analysis,
  } = useAnalysis();

  // Auto-run evaluation if analysis is available and evaluation is null
  useEffect(() => {
    if (analysis && !evaluation && !isEvaluating && !evalError) {
      runEvaluation();
    }
  }, [analysis, evaluation, isEvaluating, evalError, runEvaluation]);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fadeIn text-foreground">
      {/* Evaluations Panel */}
      <EvaluationPanel
        evaluation={evaluation}
        isEvaluating={isEvaluating}
        onRunEvaluation={runEvaluation}
        evalError={evalError}
      />

      {/* Grounding Audit Log */}
      {analysis && (
        <Card className="space-y-4">
          <CardHeader className="flex flex-row items-center justify-between pb-0">
            <div>
              <CardTitle className="text-base font-bold text-foreground flex items-center gap-2">
                <FileText className="size-4 text-primary" />
                Evidence Grounding Audit Trail
              </CardTitle>
              <CardDescription className="text-xs text-muted-foreground">
                Detailed record of all citations matched against document pages.
              </CardDescription>
            </div>
            <Badge variant="outline" className="font-mono text-xs">
              Deterministic In-Memory Audit
            </Badge>
          </CardHeader>

          <CardContent className="pt-0">
            <div className="overflow-x-auto rounded-xl border border-border">
              <table className="w-full text-left text-xs">
                <thead className="bg-muted/50 border-b border-border">
                  <tr className="text-muted-foreground font-semibold">
                    <th className="py-2.5 px-3">Governed Term</th>
                    <th className="py-2.5 px-3">Page</th>
                    <th className="py-2.5 px-3">Verbatim Evidence Snippet</th>
                    <th className="py-2.5 px-3 text-right">Grounding Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {analysis.glossary.flatMap((term) =>
                    (term.evidence || []).map((ev, idx) => (
                      <tr key={`${term.id}-${idx}`} className="hover:bg-muted/30 transition-colors">
                        <td className="py-3 px-3 font-semibold text-foreground">
                          {term.name}
                        </td>
                        <td className="py-3 px-3 font-mono text-muted-foreground">
                          p. {ev.page}
                        </td>
                        <td className="py-3 px-3 max-w-lg">
                          <blockquote className="text-muted-foreground italic truncate">
                            &ldquo;{ev.text}&rdquo;
                          </blockquote>
                        </td>
                        <td className="py-3 px-3 text-right">
                          <Badge variant="secondary" className="gap-1 text-[10px]">
                            <CheckCircle2 className="size-3 text-emerald-600 dark:text-emerald-400" />
                            <span>Exact Grounding</span>
                          </Badge>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

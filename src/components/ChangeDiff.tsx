"use client";

import React from "react";
import { ChangeDetail } from "@/lib/types";
import {
  GitCommit,
  Sparkles,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ChangeDiffProps {
  changes: ChangeDetail[];
  affectedTerms: string[];
}

export function ChangeDiff({ changes, affectedTerms }: ChangeDiffProps) {
  if (!changes || changes.length === 0) {
    return (
      <Card className="p-8 text-center">
        <GitCommit className="size-8 text-muted-foreground mx-auto mb-2" />
        <CardTitle className="text-sm font-semibold text-foreground">
          No Semantic Changes Detected
        </CardTitle>
        <CardDescription className="text-xs text-muted-foreground mt-1 max-w-sm mx-auto">
          Click &ldquo;Simulate v1.2 → v1.3 Impact&rdquo; above to run the LLM semantic diff between document revisions.
        </CardDescription>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <Sparkles className="size-4 text-amber-500" />
          <h3 className="text-base font-bold text-foreground tracking-tight">
            Detected Policy Clause Revisions ({changes.length})
          </h3>
        </div>

        {affectedTerms.length > 0 && (
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs text-muted-foreground font-medium mr-1">
              Directly Affected:
            </span>
            {affectedTerms.map((t, idx) => (
              <Badge
                key={idx}
                variant="outline"
                className="font-mono text-[10px]"
              >
                {t.replace(/^term_/, "").replace(/_/g, " ")}
              </Badge>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-4">
        {changes.map((change, idx) => (
          <Card key={idx} className="space-y-3">
            {/* Header */}
            <CardHeader className="flex flex-row items-center justify-between pb-0">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="font-mono font-bold">
                  #{idx + 1}
                </Badge>
                <Badge variant="secondary" className="uppercase text-[10px] tracking-wider font-semibold">
                  {change.change_type} Clause
                </Badge>
              </div>

              {change.affected_terms?.length > 0 && (
                <div className="flex items-center gap-1.5 flex-wrap">
                  {change.affected_terms.map((term, tIdx) => (
                    <Badge
                      key={tIdx}
                      variant="outline"
                      className="text-[10px] font-mono"
                    >
                      {term}
                    </Badge>
                  ))}
                </div>
              )}
            </CardHeader>

            <CardContent className="space-y-3 pt-0">
              {/* Semantic Explanation */}
              {change.semantic_explanation && (
                <div className="p-3.5 rounded-2xl bg-muted/40 border border-border text-xs text-foreground leading-relaxed">
                  <div className="flex items-center gap-1.5 text-primary font-semibold mb-1 text-xs">
                    <Sparkles className="size-3.5" />
                    <span>Semantic Impact Rationale:</span>
                  </div>
                  {change.semantic_explanation}
                </div>
              )}

              {/* Diff Comparison */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
                {/* Old v1.2 */}
                <div className="p-3.5 rounded-2xl bg-destructive/10 border border-destructive/20 space-y-1.5">
                  <div className="text-[10px] font-mono font-bold text-destructive uppercase tracking-wider">
                    - v1.2 Previous Text
                  </div>
                  <p className="text-xs text-destructive/90 leading-relaxed font-sans">
                    {change.old_text || "(Clause not present in v1.2)"}
                  </p>
                </div>

                {/* New v1.3 */}
                <div className="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 space-y-1.5">
                  <div className="text-[10px] font-mono font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">
                    + v1.3 Revised Text
                  </div>
                  <p className="text-xs text-emerald-900 dark:text-emerald-200 leading-relaxed font-sans">
                    {change.new_text || "(Clause removed in v1.3)"}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

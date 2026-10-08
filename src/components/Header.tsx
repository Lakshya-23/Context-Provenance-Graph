"use client";

import React from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import {
  Play,
  RotateCw,
  Clock,
  FileText,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function Header() {
  const {
    analysis,
    selectedVersion,
    setSelectedVersion,
    isLoading,
    runAnalysis,
  } = useAnalysis();

  return (
    <header className="h-16 border-b border-border bg-card/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-10 text-foreground">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-xs uppercase tracking-wider font-semibold text-muted-foreground flex items-center gap-1.5">
            <FileText className="size-3.5 text-primary" />
            Document
          </span>
          <Select
            value={selectedVersion}
            onValueChange={(v) => {
              if (v) setSelectedVersion(v);
            }}
          >
            <SelectTrigger className="w-[320px] h-8 text-xs font-semibold bg-background border-border">
              <span className="flex flex-1 text-left line-clamp-1 overflow-hidden truncate">
                {selectedVersion === "1.2"
                  ? "Revenue Recognition Policy v1.2 (Base)"
                  : "Revenue Recognition Policy v1.3 (Revised)"}
              </span>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1.2">
                Revenue Recognition Policy v1.2 (Base)
              </SelectItem>
              <SelectItem value="1.3">
                Revenue Recognition Policy v1.3 (Revised)
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        {analysis && (
          <Badge variant="outline" className="hidden md:flex items-center gap-2 px-2.5 py-1 text-xs text-muted-foreground font-normal">
            <Clock className="w-3 h-3 text-primary" />
            <span>
              {analysis.trace.total_duration_ms > 0
                ? `${(analysis.trace.total_duration_ms / 1000).toFixed(2)}s`
                : "Cached"}
            </span>
            <span className="text-muted-foreground/40">•</span>
            <span className="font-mono text-foreground">
              {analysis.trace.llm_calls} LLM calls
            </span>
          </Badge>
        )}
      </div>

      <div className="flex items-center gap-3">
        <Button
          onClick={() => runAnalysis(selectedVersion)}
          disabled={isLoading}
          size="sm"
          className="gap-2 font-medium"
        >
          {isLoading ? (
            <>
              <RotateCw className="w-3.5 h-3.5 animate-spin" />
              <span>{analysis ? "Re-Running Pipeline..." : "Starting Pipeline..."}</span>
            </>
          ) : (
            <>
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{analysis ? "Re-Run Pipeline" : "Start Pipeline"}</span>
            </>
          )}
        </Button>
      </div>
    </header>
  );
}

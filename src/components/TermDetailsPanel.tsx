"use client";

import React from "react";
import { GlossaryTerm } from "@/lib/types";
import { useRouter } from "next/navigation";
import { useAnalysis } from "@/hooks/useAnalysis";
import {
  BookOpen,
  CheckCircle,
  FileText,
  Tag,
  Scale,
  Network,
  ShieldCheck,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface TermDetailsPanelProps {
  term: GlossaryTerm | null;
  isOpen: boolean;
  onClose: () => void;
}

export function TermDetailsPanel({
  term,
  isOpen,
  onClose,
}: TermDetailsPanelProps) {
  const router = useRouter();
  const { selectNode, closeNodeModal } = useAnalysis();

  if (!term) return null;

  const handleViewInGraph = () => {
    selectNode(term.id);
    closeNodeModal();
    onClose();
    router.push("/graph");
  };

  const confidencePercent = Math.round((term.confidence || 0.9) * 100);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl max-h-[85vh] flex flex-col p-0 gap-0 overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
        {/* Header */}
        <DialogHeader className="p-6 border-b border-border bg-muted/20 shrink-0 pr-12">
          <div className="flex items-start gap-4">
            <div className="size-11 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
              <BookOpen className="size-5" />
            </div>
            <div className="space-y-1">
              <DialogTitle className="text-xl font-bold tracking-tight text-foreground">
                {term.name}
              </DialogTitle>
              <div className="flex items-center gap-2 flex-wrap pt-0.5">
                <Badge variant="outline" className="font-mono text-[10px]">
                  {term.id}
                </Badge>
                <Badge variant="secondary" className="gap-1 text-[10px]">
                  <CheckCircle className="size-3 text-emerald-600 dark:text-emerald-400" />
                  <span>{confidencePercent}% Confidence</span>
                </Badge>
              </div>
            </div>
          </div>
          <DialogDescription className="sr-only">
            Detailed breakdown of {term.name} definition, business rules, and citations.
          </DialogDescription>
        </DialogHeader>

        {/* Scrollable Body */}
        <div className="flex-1 min-h-0 overflow-y-auto p-6 space-y-6 overscroll-contain">
          {/* Action button */}
          <Button
            onClick={handleViewInGraph}
            className="w-full gap-2 font-medium"
          >
            <Network className="size-4" />
            <span>Trace Dependencies in Provenance Graph</span>
          </Button>

            {/* Governed Definition */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Governed Definition
              </div>
              <div className="p-4 rounded-xl bg-muted/40 border border-border text-sm text-foreground leading-relaxed">
                {term.definition}
              </div>
            </div>

            {/* Recognized Aliases */}
            {term.aliases && term.aliases.length > 0 && (
              <div className="space-y-2">
                <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Recognized Aliases & Synonyms
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {term.aliases.map((alias, idx) => (
                    <Badge
                      key={idx}
                      variant="outline"
                      className="font-mono text-xs gap-1.5 py-1 px-2.5 rounded-lg"
                    >
                      <Tag className="size-3 text-muted-foreground" />
                      <span>{alias}</span>
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            <Separator />

            {/* Business Rules */}
            {term.business_rules && term.business_rules.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  <Scale className="size-4 text-primary" />
                  <span>Associated Business Rules ({term.business_rules.length})</span>
                </div>
                <div className="space-y-2">
                  {term.business_rules.map((rule, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 rounded-xl border border-border bg-muted/20 flex items-start gap-3"
                    >
                      <span className="size-5 rounded-full bg-primary/10 text-primary font-mono text-[11px] flex items-center justify-center shrink-0 mt-0.5">
                        {idx + 1}
                      </span>
                      <p className="text-xs text-foreground leading-relaxed">
                        {rule}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Verified Citations */}
            {term.evidence && term.evidence.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  <ShieldCheck className="size-4 text-emerald-600 dark:text-emerald-400" />
                  <span>Verified Grounding Citations ({term.evidence.length})</span>
                </div>
                <div className="space-y-3">
                  {term.evidence.map((ev, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl border border-border bg-card space-y-2.5 shadow-2xs"
                    >
                      <div className="flex items-center justify-between">
                        <Badge variant="outline" className="font-mono text-[10px] gap-1">
                          <FileText className="size-3 text-primary" />
                          <span>Page {ev.page}</span>
                        </Badge>
                        <Badge variant="secondary" className="text-[10px] gap-1">
                          <CheckCircle className="size-3 text-emerald-600 dark:text-emerald-400" />
                          <span>Verbatim in PDF</span>
                        </Badge>
                      </div>
                      <blockquote className="text-xs text-muted-foreground italic border-l-2 border-primary/50 pl-3 py-1 leading-relaxed bg-muted/40 rounded-r">
                        &ldquo;{ev.text}&rdquo;
                      </blockquote>
                    </div>
                  ))}
                </div>
              </div>
            )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

"use client";

import React from "react";
import { GlossaryTerm } from "@/lib/types";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  BookOpen,
  CheckCircle,
  FileText,
  Tag,
  Scale,
  ArrowRight,
} from "lucide-react";

interface GlossaryTermCardProps {
  term: GlossaryTerm;
  onSelect: (term: GlossaryTerm) => void;
  onViewInGraph?: (termId: string) => void;
}

export function GlossaryTermCard({
  term,
  onSelect,
}: GlossaryTermCardProps) {
  const confidencePercent = Math.round((term.confidence || 0.9) * 100);

  return (
    <Card
      onClick={() => onSelect(term)}
      size="sm"
      className="cursor-pointer hover:ring-2 hover:ring-primary/40 transition-all flex flex-col justify-between"
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-primary/10 text-primary shrink-0">
              <BookOpen className="size-4" />
            </div>
            <CardTitle className="text-base font-bold">
              {term.name}
            </CardTitle>
          </div>
          <Badge variant="secondary" className="gap-1 text-[11px]">
            <CheckCircle className="size-3 text-emerald-600 dark:text-emerald-400" />
            <span>{confidencePercent}%</span>
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-3 pb-3">
        <CardDescription className="text-xs line-clamp-3 leading-relaxed">
          {term.definition}
        </CardDescription>

        {term.aliases && term.aliases.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {term.aliases.slice(0, 3).map((alias, idx) => (
              <Badge key={idx} variant="outline" className="font-mono text-[10px] gap-1 px-1.5 py-0">
                <Tag className="size-2.5 opacity-60" />
                <span>{alias}</span>
              </Badge>
            ))}
            {term.aliases.length > 3 && (
              <span className="text-[10px] text-muted-foreground self-center">
                +{term.aliases.length - 3}
              </span>
            )}
          </div>
        )}
      </CardContent>

      <CardFooter className="pt-2 border-t border-border flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-3 text-[11px]">
          {term.business_rules?.length > 0 && (
            <span className="flex items-center gap-1 font-medium">
              <Scale className="size-3 text-primary" />
              <span>{term.business_rules.length} rules</span>
            </span>
          )}
          {term.evidence?.length > 0 && (
            <span className="flex items-center gap-1 font-medium">
              <FileText className="size-3 text-cyan-600 dark:text-cyan-400" />
              <span>{term.evidence.length} citations</span>
            </span>
          )}
        </div>

        <span className="flex items-center gap-1 text-primary font-medium text-xs">
          <span>Inspect</span>
          <ArrowRight className="size-3.5" />
        </span>
      </CardFooter>
    </Card>
  );
}

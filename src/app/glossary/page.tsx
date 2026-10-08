"use client";

import React, { useState, useMemo } from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { GlossaryTermCard } from "@/components/GlossaryTermCard";
import { TermDetailsPanel } from "@/components/TermDetailsPanel";
import { GlossaryTerm } from "@/lib/types";
import {
  BookOpen,
  Search,
  RotateCw,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "cn";

export default function GlossaryPage() {
  const { analysis, isLoading } = useAnalysis();
  const [search, setSearch] = useState("");
  const [selectedTerm, setSelectedTerm] = useState<GlossaryTerm | null>(null);
  const [filterType, setFilterType] = useState<"all" | "rules" | "citations">("all");

  const terms = analysis?.glossary || [];

  const filteredTerms = useMemo(() => {
    return terms.filter((term) => {
      const matchesSearch =
        term.name.toLowerCase().includes(search.toLowerCase()) ||
        term.definition.toLowerCase().includes(search.toLowerCase()) ||
        term.aliases?.some((a) => a.toLowerCase().includes(search.toLowerCase()));

      if (!matchesSearch) return false;

      if (filterType === "rules") {
        return term.business_rules && term.business_rules.length > 0;
      }
      if (filterType === "citations") {
        return term.evidence && term.evidence.length > 0;
      }
      return true;
    });
  }, [terms, search, filterType]);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fadeIn text-foreground">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-2">
        <div>
          <h1 className="text-3xl font-extrabold text-foreground tracking-tight sm:text-4xl">
            Governed Context Glossary
          </h1>
          <p className="text-sm text-muted-foreground mt-2 max-w-2xl leading-relaxed">
            All enterprise concepts extracted ,complete with business rules,
            recognized aliases, confidence ratings, and verbatim PDF citations.
          </p>
        </div>

        <Link
          href="/graph"
          className={cn(
            buttonVariants({ variant: "outline" }),
            "gap-2 shrink-0 font-medium"
          )}
        >
          <span>View Provenance Lineage</span>
          <ArrowRight className="size-4" />
        </Link>
      </div>

      {/* Search and Filters Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-96">
          <Search className="size-4 text-muted-foreground absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <Input
            type="text"
            placeholder="Search concepts, definitions, aliases..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 h-10 text-xs bg-background border-border shadow-xs"
          />
        </div>

        <div className="flex items-center gap-1.5 w-full sm:w-auto">
          <Button
            variant={filterType === "all" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilterType("all")}
            className="text-xs"
          >
            All Terms ({terms.length})
          </Button>
          <Button
            variant={filterType === "rules" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilterType("rules")}
            className="text-xs"
          >
            Has Business Rules
          </Button>
          <Button
            variant={filterType === "citations" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilterType("citations")}
            className="text-xs"
          >
            With Citations
          </Button>
        </div>
      </div>

      {/* Empty / Loading State */}
      {isLoading && (
        <Card className="p-12 text-center space-y-3">
          <RotateCw className="size-6 text-primary animate-spin mx-auto" />
          <h3 className="text-sm font-semibold text-foreground">
            Extracting glossary terms...
          </h3>
        </Card>
      )}

      {!isLoading && filteredTerms.length === 0 && (
        <Card className="p-12 text-center space-y-2">
          <BookOpen className="size-8 text-muted-foreground mx-auto" />
          <h3 className="text-sm font-semibold text-foreground">
            {terms.length === 0 ? "No Glossary Extracted Yet" : "No Matching Terms Found"}
          </h3>
          <p className="text-xs text-muted-foreground max-w-sm mx-auto">
            {terms.length === 0
              ? "Run the extraction pipeline from the header to populate the governed vocabulary."
              : "Try adjusting your search criteria or filter tags."}
          </p>
        </Card>
      )}

      {/* Terms Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTerms.map((term) => (
          <GlossaryTermCard
            key={term.id}
            term={term}
            onSelect={(t) => setSelectedTerm(t)}
          />
        ))}
      </div>

      {/* Details Slide-out Sheet */}
      <TermDetailsPanel
        term={selectedTerm}
        isOpen={Boolean(selectedTerm)}
        onClose={() => setSelectedTerm(null)}
      />
    </div>
  );
}

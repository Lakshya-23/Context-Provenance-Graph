"use client";

import React from "react";
import { ImpactSummaryData } from "@/lib/types";
import {
  BarChart3,
  Database,
  Cpu,
  Bot,
  ShieldCheck,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ImpactSummaryProps {
  impact: ImpactSummaryData;
}

export function ImpactSummary({ impact }: ImpactSummaryProps) {
  const categories = [
    {
      title: "Impacted Metrics",
      items: impact.metrics || [],
      icon: BarChart3,
      color: "text-emerald-600 dark:text-emerald-400",
      actionText: "Requires formula recalculation",
    },
    {
      title: "Impacted Repositories",
      items: impact.context_repositories || [],
      icon: Database,
      color: "text-amber-600 dark:text-amber-400",
      actionText: "Requires SQL mart migration",
    },
    {
      title: "Impacted Agent Skills",
      items: impact.skills || [],
      icon: Cpu,
      color: "text-pink-600 dark:text-pink-400",
      actionText: "Requires instruction update",
    },
    {
      title: "Impacted AI Agents",
      items: impact.agents || [],
      icon: Bot,
      color: "text-orange-600 dark:text-orange-400",
      actionText: "Requires system prompt sync",
    },
    {
      title: "Impacted Evaluations",
      items: impact.evaluations || [],
      icon: ShieldCheck,
      color: "text-red-600 dark:text-red-400",
      actionText: "Test cases may fail / need update",
    },
  ];

  const totalImpacted = categories.reduce((sum, c) => sum + c.items.length, 0);

  return (
    <div className="space-y-6">
      {/* Overview banner */}
      <Card className="bg-amber-500/10 border-amber-500/20">
        <CardContent className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="size-10 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-amber-400 flex items-center justify-center shrink-0">
              <AlertTriangle className="size-5" />
            </div>
            <div>
              <CardTitle className="text-sm font-bold text-foreground">
                Downstream Blast Radius: {totalImpacted} Entities Affected
              </CardTitle>
              <CardDescription className="text-xs text-muted-foreground">
                Graph traversal traced all downstream consumers dependent on modified clauses.
              </CardDescription>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Grid of categories */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {categories.map((cat, idx) => {
          const Icon = cat.icon;
          return (
            <Card key={idx} size="sm" className="flex flex-col justify-between">
              <div>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <div className="flex items-center gap-2">
                    <Icon className={`size-4 ${cat.color}`} />
                    <CardTitle className="text-xs font-bold uppercase tracking-wider">
                      {cat.title}
                    </CardTitle>
                  </div>
                  <Badge variant="secondary" className="font-mono text-[10px]">
                    {cat.items.length} affected
                  </Badge>
                </CardHeader>

                <CardContent className="space-y-2">
                  {cat.items.length === 0 ? (
                    <p className="text-xs text-muted-foreground italic py-3 text-center">
                      No downstream entities affected.
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {cat.items.map((item, iIdx) => (
                        <div
                          key={iIdx}
                          className="p-2.5 rounded-xl bg-muted/40 border border-border space-y-1"
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-semibold text-foreground">
                              {item.name}
                            </span>
                            <span className="text-[9px] font-mono text-muted-foreground">
                              {item.id}
                            </span>
                          </div>
                          {item.definition && (
                            <p className="text-[11px] text-muted-foreground line-clamp-2">
                              {item.definition}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </div>

              {cat.items.length > 0 && (
                <CardFooter className="pt-2 border-t border-border flex items-center justify-between text-[11px] text-amber-600 dark:text-amber-400 font-medium">
                  <span>{cat.actionText}</span>
                  <ArrowRight className="size-3" />
                </CardFooter>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
}

"use client";

import React from "react";
import { SourceInfo } from "@/lib/types";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "cn";
import { FileText, CheckCircle, ExternalLink } from "lucide-react";

interface SourceCardProps {
  source: SourceInfo;
}

export function SourceCard({ source }: SourceCardProps) {
  const isV12 = source.version === "1.2";

  return (
    <Card className="overflow-hidden">
      <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-2xl bg-primary/10 text-primary shrink-0 flex items-center justify-center">
            <FileText className="size-6" />
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <CardTitle className="text-xl font-bold tracking-tight">
                {source.name}
              </CardTitle>
              <Badge variant="outline" className="font-mono text-xs">
                v{source.version}
              </Badge>
            </div>
            <CardDescription className="text-xs max-w-2xl leading-relaxed">
              Canonical financial policy defining criteria for revenue recognition, refund handling,
              and chargeback exclusions across all enterprise reporting systems.
            </CardDescription>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-center shrink-0">
          <a
            href="/revenue_policy_v1_2.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className={cn(
              buttonVariants({ variant: isV12 ? "default" : "outline", size: "sm" }),
              "gap-1.5"
            )}
          >
            <FileText className="size-3.5" />
            <span>v1.2 PDF</span>
            <ExternalLink className="size-3 opacity-60" />
          </a>

          <a
            href="/revenue_policy_v1_3.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className={cn(
              buttonVariants({ variant: !isV12 ? "default" : "outline", size: "sm" }),
              "gap-1.5"
            )}
          >
            <FileText className="size-3.5" />
            <span>v1.3 PDF</span>
            <ExternalLink className="size-3 opacity-60" />
          </a>
        </div>
      </CardHeader>
      <CardContent className="pt-0 text-xs text-muted-foreground flex items-center justify-between border-t border-border pt-3">
        <div>Document filename: <span className="font-mono font-medium text-foreground">{source.filename}</span></div>
        <div>Page count: <span className="font-semibold text-foreground">{source.page_count} pages</span></div>
      </CardContent>
    </Card>
  );
}

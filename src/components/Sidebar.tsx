"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  Network,
  Zap,
  CheckCircle2,
  Layers,
} from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { cn } from "cn";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const navItems: NavItem[] = [
  {
    name: "Overview",
    href: "/",
    icon: Layers,
  },
  {
    name: "Governed Glossary",
    href: "/glossary",
    icon: BookOpen,
  },
  {
    name: "Provenance Graph",
    href: "/graph",
    icon: Network,
  },
  {
    name: "Impact Analysis",
    href: "/impact",
    icon: Zap,
  },
  {
    name: "Evaluations",
    href: "/evaluations",
    icon: CheckCircle2,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-sidebar-border bg-sidebar text-sidebar-foreground flex flex-col justify-between shrink-0 select-none z-20">
      <div>
        {/* Brand header */}
        <div className="p-6">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="size-10 rounded-2xl bg-primary text-primary-foreground flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform duration-200">
              <Network className="size-5" />
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-sidebar-foreground block">
                Context Graph
              </span>
              <span className="text-[11px] font-medium text-muted-foreground block tracking-wider uppercase">
                AI Governance Engine
              </span>
            </div>
          </Link>
        </div>

        <Separator />

        {/* Navigation list */}
        <nav className="p-4 space-y-1.5">
          <div className="px-3 py-1.5 text-xs font-semibold tracking-wider text-muted-foreground uppercase">
            Workspaces
          </div>
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  buttonVariants({
                    variant: isActive ? "secondary" : "ghost",
                    size: "default",
                  }),
                  "w-full justify-between h-10 px-3 font-medium",
                  isActive
                    ? "bg-sidebar-accent text-sidebar-accent-foreground font-semibold"
                    : "text-muted-foreground hover:text-sidebar-foreground"
                )}
              >
                <div className="flex items-center gap-3">
                  <Icon className="size-4 shrink-0" />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <Badge
                    variant={isActive ? "default" : "outline"}
                    className="text-[10px] px-1.5 py-0 h-4"
                  >
                    {item.badge}
                  </Badge>
                )}
              </Link>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}

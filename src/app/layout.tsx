import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { Sidebar } from "@/components/Sidebar";
import { Header } from "@/components/Header";
import { AnalysisProvider } from "@/hooks/useAnalysis";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "Context Provenance Graph — Enterprise AI Governance",
  description:
    "Trace business documents to governed context, downstream metrics, repositories, skills, and agents with semantic impact analysis.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={cn(
        "h-full antialiased",
        inter.variable,
        "font-sans"
      )}
    >
      <body className="min-h-full flex flex-row bg-background text-foreground antialiased overflow-hidden font-sans">
        <AnalysisProvider>
          <Sidebar />
          <div className="flex-1 flex flex-col h-screen overflow-hidden">
            <Header />
            <main className="flex-1 overflow-y-auto">
              {children}
            </main>
          </div>
        </AnalysisProvider>
      </body>
    </html>
  );
}

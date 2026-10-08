"use client";

import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from "react";
import {
  AnalysisResult,
  ImpactResult,
  EvaluationResult,
  ProvenanceGraphData,
  GraphNode,
} from "@/lib/types";
import {
  analyzeDocument,
  analyzeImpact,
  evaluateExtraction,
  getDocument,
} from "@/lib/api";

interface AnalysisContextType {
  analysis: AnalysisResult | null;
  selectedVersion: string;
  setSelectedVersion: (v: string) => void;
  isLoading: boolean;
  error: string | null;
  selectedNodeId: string | null;
  selectedNode: GraphNode | null;
  selectNode: (id: string | null) => void;
  isNodeModalOpen: boolean;
  openNodeModal: (id?: string) => void;
  closeNodeModal: () => void;
  runAnalysis: (version?: string) => Promise<void>;
  
  // Impact State
  impact: ImpactResult | null;
  isAnalyzingImpact: boolean;
  impactError: string | null;
  runImpactAnalysis: (baseVersion?: string, targetVersion?: string) => Promise<void>;
  
  // Evaluation State
  evaluation: EvaluationResult | null;
  isEvaluating: boolean;
  evalError: string | null;
  runEvaluation: () => Promise<void>;
  
  // Document raw text
  documentText: string;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const [selectedVersion, setSelectedVersion] = useState<string>("1.2");
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [isNodeModalOpen, setIsNodeModalOpen] = useState<boolean>(false);

  const [impact, setImpact] = useState<ImpactResult | null>(null);
  const [isAnalyzingImpact, setIsAnalyzingImpact] = useState<boolean>(false);
  const [impactError, setImpactError] = useState<string | null>(null);

  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [evalError, setEvalError] = useState<string | null>(null);

  const [documentText, setDocumentText] = useState<string>("");

  const selectNode = useCallback((id: string | null) => {
    setSelectedNodeId(id);
  }, []);

  const openNodeModal = useCallback((id?: string) => {
    if (id) {
      setSelectedNodeId(id);
    }
    setIsNodeModalOpen(true);
  }, []);

  const closeNodeModal = useCallback(() => {
    setIsNodeModalOpen(false);
  }, []);

  const runAnalysis = useCallback(async (versionToRun = selectedVersion) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await analyzeDocument(versionToRun);
      setAnalysis(result);
      setSelectedVersion(versionToRun);

      // Also fetch document raw text for preview/evals
      try {
        const doc = await getDocument(versionToRun);
        setDocumentText(doc.raw_text);
      } catch {
        // Document fetch fallback
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to run extraction workflow";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [selectedVersion]);

  const runImpactAnalysis = useCallback(
    async (base = "1.2", target = "1.3") => {
      if (!analysis?.graph) {
        setImpactError("Base provenance graph not available. Run extraction first.");
        return;
      }
      setIsAnalyzingImpact(true);
      setImpactError(null);
      try {
        const res = await analyzeImpact(base, target, analysis.graph);
        setImpact(res);
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : "Failed to run impact analysis";
        setImpactError(msg);
      } finally {
        setIsAnalyzingImpact(false);
      }
    },
    [analysis]
  );

  const runEvaluation = useCallback(async () => {
    if (!analysis?.glossary) {
      setEvalError("No extracted glossary available. Run extraction first.");
      return;
    }
    setIsEvaluating(true);
    setEvalError(null);
    try {
      const text = documentText || analysis.claims.map((c) => c.text).join("\n");
      const res = await evaluateExtraction(analysis.glossary, text);
      setEvaluation(res);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to run evaluators";
      setEvalError(msg);
    } finally {
      setIsEvaluating(false);
    }
  }, [analysis, documentText]);

  // Selected node derived object
  const selectedNode: GraphNode | null =
    analysis && selectedNodeId && analysis.graph.nodes[selectedNodeId]
      ? analysis.graph.nodes[selectedNodeId]
      : null;

  return (
    <AnalysisContext.Provider
      value={{
        analysis,
        selectedVersion,
        setSelectedVersion,
        isLoading,
        error,
        selectedNodeId,
        selectedNode,
        selectNode,
        isNodeModalOpen,
        openNodeModal,
        closeNodeModal,
        runAnalysis,
        impact,
        isAnalyzingImpact,
        impactError,
        runImpactAnalysis,
        evaluation,
        isEvaluating,
        evalError,
        runEvaluation,
        documentText,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error("useAnalysis must be used within an AnalysisProvider");
  }
  return context;
}

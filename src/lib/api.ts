/**
 * API client for interacting with the Context Provenance Graph FastAPI backend.
 */

import {
  AnalysisResult,
  ImpactResult,
  EvaluationResult,
  ProvenanceGraphData,
  GlossaryTerm,
} from "./types";

const getApiBaseUrl = (): string => {
  if (typeof window !== "undefined" && process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "");
  }
  return (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");
};

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Request failed with status ${res.status}`;
    try {
      const errorJson = await res.json();
      if (errorJson.detail) {
        errorDetail = typeof errorJson.detail === "string" 
          ? errorJson.detail 
          : JSON.stringify(errorJson.detail);
      }
    } catch {
      // response wasn't JSON
    }
    throw new Error(errorDetail);
  }
  return res.json() as Promise<T>;
}

export async function checkHealth(): Promise<{ status: string; service: string; llm_model: string }> {
  const url = `${getApiBaseUrl()}/api/health`;
  const res = await fetch(url, { cache: "no-store" });
  return handleResponse(res);
}

export async function verifyLlm(): Promise<{ status: string; model: string; response: string }> {
  const url = `${getApiBaseUrl()}/api/verify-llm`;
  const res = await fetch(url, { cache: "no-store" });
  return handleResponse(res);
}

export async function analyzeDocument(version = "1.2"): Promise<AnalysisResult> {
  const url = `${getApiBaseUrl()}/api/analyze`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ version }),
  });
  return handleResponse<AnalysisResult>(res);
}

export async function analyzeImpact(
  baseVersion = "1.2",
  newVersion = "1.3",
  graph: ProvenanceGraphData
): Promise<ImpactResult> {
  const url = `${getApiBaseUrl()}/api/impact`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      base_version: baseVersion,
      new_version: newVersion,
      graph,
    }),
  });
  return handleResponse<ImpactResult>(res);
}

export async function evaluateExtraction(
  glossary: GlossaryTerm[],
  sourceText: string
): Promise<EvaluationResult> {
  const url = `${getApiBaseUrl()}/api/evaluate`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      glossary,
      source_text: sourceText,
    }),
  });
  return handleResponse<EvaluationResult>(res);
}

export async function getDocument(version: string): Promise<{
  version: string;
  filename: string;
  page_count: number;
  pages: Array<{ page: number; text: string }>;
  raw_text: string;
}> {
  const url = `${getApiBaseUrl()}/api/document/${encodeURIComponent(version)}`;
  const res = await fetch(url, { cache: "no-store" });
  return handleResponse(res);
}

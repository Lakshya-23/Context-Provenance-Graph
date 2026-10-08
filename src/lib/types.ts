/**
 * TypeScript types for Context Provenance Graph
 */

export interface Evidence {
  source_id: string;
  page: number;
  text: string;
  _match_type?: string;
  _valid?: boolean;
}

export interface Claim {
  id: string;
  text: string;
  claim_type: "definition" | "business_rule" | "relationship" | "semantic_statement" | string;
  source_page: number;
  related_terms: string[];
}

export interface GlossaryTerm {
  id: string;
  name: string;
  definition: string;
  aliases: string[];
  business_rules: string[];
  evidence: Evidence[];
  confidence: number;
}

export interface SourceInfo {
  source_id: string;
  name: string;
  version: string;
  page_count: number;
  filename: string;
}

export interface TraceStep {
  name: string;
  status: "success" | "error";
  duration_ms: number;
  input_summary: string;
  output_summary: string;
  error?: string | null;
}

export interface WorkflowTrace {
  steps: TraceStep[];
  total_duration_ms: number;
  llm_calls: number;
  tokens_used: Record<string, { prompt_tokens: number; completion_tokens: number }>;
}

export type NodeType =
  | "source"
  | "claim"
  | "glossary_term"
  | "metric"
  | "context_repository"
  | "skill"
  | "agent"
  | "evaluation";

export type EdgeType =
  | "contains"
  | "defines"
  | "supports"
  | "uses"
  | "derived_from"
  | "depends_on"
  | "consumed_by"
  | "tested_by";

export interface GraphNode {
  id: string;
  type: NodeType;
  name: string;
  definition: string;
  metadata?: Record<string, unknown>;
}

export interface GraphEdge {
  source: string;
  target: string;
  type: EdgeType;
  label?: string;
}

export interface ProvenanceGraphData {
  nodes: Record<string, GraphNode>;
  edges: GraphEdge[];
}

export interface AnalysisSummary {
  total_nodes: number;
  total_edges: number;
  claims_count: number;
  glossary_count: number;
  counts_by_type: Record<string, number>;
  errors: string[];
}

export interface AnalysisResult {
  source: SourceInfo;
  claims: Claim[];
  glossary: GlossaryTerm[];
  graph: ProvenanceGraphData;
  summary: AnalysisSummary;
  trace: WorkflowTrace;
}

export interface ChangeDetail {
  change_type: "modified" | "added" | "removed";
  old_text: string;
  new_text: string;
  affected_terms: string[];
  semantic_explanation: string;
}

export interface ImpactedItem {
  id: string;
  name: string;
  type: string;
  definition: string;
}

export interface ImpactSummaryData {
  metrics: ImpactedItem[];
  context_repositories: ImpactedItem[];
  skills: ImpactedItem[];
  agents: ImpactedItem[];
  evaluations: ImpactedItem[];
  _counts?: {
    metrics: number;
    context_repositories: number;
    skills: number;
    agents: number;
    evaluations: number;
  };
}

export interface ImpactResult {
  changes: ChangeDetail[];
  affected_terms: string[];
  impact: ImpactSummaryData;
}

export interface EvaluationItemDetail {
  term?: string;
  status?: "found" | "missing";
  score?: number;
  grounded?: boolean;
  evidence?: string;
  page?: number;
  found?: boolean;
  rule?: string;
}

export interface EvaluationDetail {
  name: string;
  score: number;
  expected: number;
  found: number;
  missing: string[];
  details: EvaluationItemDetail[];
}

export interface EvaluationResult {
  term_coverage: EvaluationDetail;
  definition_groundedness: EvaluationDetail;
  evidence_accuracy: EvaluationDetail;
  business_rule_completeness: EvaluationDetail;
  overall: number;
}

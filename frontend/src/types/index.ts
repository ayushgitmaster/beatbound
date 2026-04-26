// Shared TypeScript types for the Cardiac DSS frontend

export interface HistoryMessage {
  role: "user" | "assistant";
  content: string;
}

export interface Source {
  content: string;
  source: string;
  relevance_score: number;
  page?: number;
  doc_type?: string;
}

export interface ReasoningStep {
  step: number;
  description: string;
  confidence: number;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  relevance_scores: number[];
  reasoning_steps: ReasoningStep[];
  is_fallback: boolean;
  fallback_warning?: string;
}

// Lab Parser
export interface LabValues {
  troponin?: number;
  troponin_unit?: string;
  ldl?: number;
  ldl_unit?: string;
  hdl?: number;
  hdl_unit?: string;
  cholesterol?: number;
  cholesterol_unit?: string;
  triglycerides?: number;
  triglycerides_unit?: string;
  glucose?: number;
  glucose_unit?: string;
  systolic_bp?: number;
  diastolic_bp?: number;
  creatinine?: number;
  creatinine_unit?: string;
  egfr?: number;
  bnp?: number;
  hba1c?: number;
}

export interface SummaryRow {
  test: string;
  value: string;
  normal_range: string;
}

export interface LabUploadResponse {
  values: LabValues;
  categories: Record<string, unknown>;
  summary_table: SummaryRow[];
  rag_prompt: string;
  source_file: string;
}

// Risk Scores
export interface RiskScoreRequest {
  age?: number;
  sex?: string;
  race?: string;
  total_cholesterol?: number;
  hdl_cholesterol?: number;
  ldl_cholesterol?: number;
  systolic_bp?: number;
  diastolic_bp?: number;
  is_smoker?: boolean;
  has_diabetes?: boolean;
  on_bp_treatment?: boolean;
  has_af?: boolean;
  has_heart_failure?: boolean;
  has_hypertension?: boolean;
  has_vascular_disease?: boolean;
  stroke_tia_history?: boolean;
  labile_inr?: boolean;
  on_antiplatelet_or_nsaid?: boolean;
  alcohol_use?: boolean;
  renal_disease?: boolean;
  liver_disease?: boolean;
  bleeding_history?: boolean;
  heart_rate?: number;
  creatinine?: number;
  killip_class?: number;
  cardiac_arrest?: boolean;
  st_deviation?: boolean;
  elevated_enzymes?: boolean;
}

export interface ScoreBreakdownItem {
  label: string;
  value: string | number | boolean;
  points?: number;
}

export interface RiskScore {
  name: string;
  score?: number;
  risk_percent?: number;
  risk_category: string;
  interpretation: string;
  breakdown?: ScoreBreakdownItem[];
  recommendations?: string[];
}

export interface RiskScoreResponse {
  scores: RiskScore[];
  risk_level: "LOW" | "MODERATE" | "HIGH" | "CRITICAL" | "UNKNOWN";
  explanation: string;
  overall_recommendation: string;
}

// Explainability
export interface ExplainResponse {
  sources: Array<Record<string, unknown>>;
  reasoning_steps: Array<Record<string, unknown>>;
  overall_confidence: number;
  risk_breakdown?: Record<string, unknown>;
  query?: string;
}

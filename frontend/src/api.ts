import axios from "axios";
import type {
  ChatResponse,
  HistoryMessage,
  LabUploadResponse,
  RiskScoreRequest,
  RiskScoreResponse,
  ExplainResponse,
} from "./types";

const http = axios.create({ baseURL: "/api" });

// ── Chat ─────────────────────────────────────────────────────────────────────
export const chat = async (
  message: string,
  history: HistoryMessage[] = []
): Promise<ChatResponse> => {
  const { data } = await http.post<ChatResponse>("/chat", { message, history });
  return data;
};

// ── Lab Parser ────────────────────────────────────────────────────────────────
export const uploadReport = async (file: File): Promise<LabUploadResponse> => {
  const form = new FormData();
  form.append("file", file);
  const { data } = await http.post<LabUploadResponse>("/upload-report", form);
  return data;
};

/** Legacy endpoint kept for backward compat */
export const analyzeLabPdf = uploadReport;

export const labAiAnalysis = async (ragPrompt: string): Promise<{ analysis: string }> => {
  const { data } = await http.post("/lab/ai-analysis", { rag_prompt: ragPrompt });
  return data;
};

// ── Risk Score ────────────────────────────────────────────────────────────────
export const riskScore = async (
  req: RiskScoreRequest
): Promise<RiskScoreResponse> => {
  const { data } = await http.post<RiskScoreResponse>("/risk-score", req);
  return data;
};

// ── Explainability ────────────────────────────────────────────────────────────
export const getExplain = async (): Promise<ExplainResponse> => {
  const { data } = await http.get<ExplainResponse>("/explain");
  return data;
};

// ── Resources ─────────────────────────────────────────────────────────────────
export const getConditions = async () => {
  const { data } = await http.get("/resources/conditions");
  return data;
};

export const getSymptoms = async () => {
  const { data } = await http.get("/resources/symptoms");
  return data;
};

// ── Symptom assessment ────────────────────────────────────────────────────────
export const symptomAssess = async (message: string) => {
  const { data } = await http.post(`/symptom/assess?message=${encodeURIComponent(message)}`);
  return data;
};

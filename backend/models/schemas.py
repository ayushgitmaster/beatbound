"""
Pydantic schemas for all API request/response models.
"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


# ── Chat ──────────────────────────────────────────────────────────────────────

class HistoryMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[HistoryMessage]] = []


class Source(BaseModel):
    content: str
    source: str
    relevance_score: float
    page: Optional[int] = None
    doc_type: Optional[str] = "general"


class ReasoningStep(BaseModel):
    step: int
    description: str
    confidence: float


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    relevance_scores: List[float] = []
    reasoning_steps: List[ReasoningStep] = []
    is_fallback: bool = False
    fallback_warning: Optional[str] = None


# ── Lab Parser ─────────────────────────────────────────────────────────────────

class LabValues(BaseModel):
    troponin: Optional[float] = None
    troponin_unit: Optional[str] = None
    ldl: Optional[float] = None
    ldl_unit: Optional[str] = None
    hdl: Optional[float] = None
    hdl_unit: Optional[str] = None
    cholesterol: Optional[float] = None
    cholesterol_unit: Optional[str] = None
    triglycerides: Optional[float] = None
    triglycerides_unit: Optional[str] = None
    glucose: Optional[float] = None
    glucose_unit: Optional[str] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    creatinine: Optional[float] = None
    creatinine_unit: Optional[str] = None
    egfr: Optional[float] = None
    bnp: Optional[float] = None
    hba1c: Optional[float] = None


class LabUploadResponse(BaseModel):
    values: LabValues
    categories: Dict[str, Any] = {}
    summary_table: List[Dict[str, Any]] = []
    rag_prompt: str = ""
    source_file: str = ""


class LabAIRequest(BaseModel):
    rag_prompt: str


class LabAIResponse(BaseModel):
    analysis: str


# ── Risk Score ─────────────────────────────────────────────────────────────────

class RiskScoreRequest(BaseModel):
    # Demographics
    age: Optional[int] = Field(None, ge=18, le=120)
    sex: Optional[str] = None           # "male" | "female"
    race: Optional[str] = "white"       # "white" | "african_american" | "other"

    # Lipids / vitals (from lab or manual)
    total_cholesterol: Optional[float] = None
    hdl_cholesterol: Optional[float] = None
    ldl_cholesterol: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None

    # Conditions
    is_smoker: Optional[bool] = False
    has_diabetes: Optional[bool] = False
    on_bp_treatment: Optional[bool] = False

    # CHA2DS2-VASc
    has_af: Optional[bool] = False
    has_heart_failure: Optional[bool] = False
    has_hypertension: Optional[bool] = False
    has_vascular_disease: Optional[bool] = False
    stroke_tia_history: Optional[bool] = False

    # HAS-BLED
    labile_inr: Optional[bool] = False
    on_antiplatelet_or_nsaid: Optional[bool] = False
    alcohol_use: Optional[bool] = False
    renal_disease: Optional[bool] = False
    liver_disease: Optional[bool] = False
    bleeding_history: Optional[bool] = False

    # GRACE (ACS)
    heart_rate: Optional[int] = None
    creatinine: Optional[float] = None  # mg/dL
    killip_class: Optional[int] = 1
    cardiac_arrest: Optional[bool] = False
    st_deviation: Optional[bool] = False
    elevated_enzymes: Optional[bool] = False


class ScoreBreakdownItem(BaseModel):
    label: str
    value: Any
    points: Optional[float] = None


class RiskScore(BaseModel):
    name: str
    score: Optional[float] = None
    risk_percent: Optional[float] = None
    risk_category: str
    interpretation: str
    breakdown: Optional[List[ScoreBreakdownItem]] = None
    recommendations: Optional[List[str]] = None


class RiskScoreResponse(BaseModel):
    scores: List[RiskScore]
    risk_level: str          # "LOW" | "MODERATE" | "HIGH" | "CRITICAL"
    explanation: str
    overall_recommendation: str


# ── Explainability ─────────────────────────────────────────────────────────────

class ExplainResponse(BaseModel):
    sources: List[Dict[str, Any]] = []
    reasoning_steps: List[Dict[str, Any]] = []
    overall_confidence: float = 0.0
    risk_breakdown: Optional[Dict[str, Any]] = None
    query: Optional[str] = None

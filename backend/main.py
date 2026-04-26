"""
Cardiac DSS API - Multimodal Cardiac Decision Support System.
Run from project root: uvicorn backend.main:app --reload --port 8000
"""
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Cardiac DSS API starting up...")
    yield
    logger.info("Cardiac DSS API shutting down.")


app = FastAPI(
    title="Cardiac DSS API",
    description="Multimodal Cardiac Decision Support System",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from beatbound.backend.routes.chat import router as chat_router
from beatbound.backend.routes.parser import router as parser_router
from beatbound.backend.routes.risk import router as risk_router
from beatbound.backend.routes.explain import router as explain_router
from beatbound.backend.core import heart_knowledge as hk
from beatbound.backend.core.heart_chain import SymptomAssessmentChain

app.include_router(chat_router, prefix="/api")
app.include_router(parser_router, prefix="/api")
app.include_router(risk_router, prefix="/api")
app.include_router(explain_router, prefix="/api")


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Cardiac DSS API", "version": "3.0.0"}


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/api/resources/conditions", tags=["Resources"])
def get_conditions():
    return hk.HEART_CONDITIONS


@app.get("/api/resources/symptoms", tags=["Resources"])
def get_symptoms():
    return hk.HEART_SYMPTOMS


_symptom_chain = None


def _get_symptom_chain():
    global _symptom_chain
    if _symptom_chain is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model="google/gemini-2.0-flash-001",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={"Authorization": f"Bearer {api_key}"},
            temperature=0.3,
        )
        _symptom_chain = SymptomAssessmentChain(llm)
    return _symptom_chain


@app.post("/api/symptom/assess", tags=["Symptom"])
def symptom_assess(message: str):
    chain = _get_symptom_chain()
    return chain.run(message)

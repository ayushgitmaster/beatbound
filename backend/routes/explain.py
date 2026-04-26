"""
GET /api/explain  — Return the most recent reasoning chain + evidence.
"""
import logging
from fastapi import APIRouter, HTTPException
from beatbound.backend.models.schemas import ExplainResponse
from beatbound.backend.services.explainability import get_last_payload

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Explainability"])


@router.get("/explain", response_model=ExplainResponse)
async def explain():
    """
    Return the reasoning chain from the most recent chat or risk-score request.
    Includes: retrieved documents, relevance scores, reasoning steps, risk breakdown.
    """
    payload = get_last_payload()
    if not payload:
        return ExplainResponse(
            sources=[],
            reasoning_steps=[
                {
                    "step": 1,
                    "description": "No query has been processed yet. Send a /chat request first.",
                    "confidence": 1.0,
                }
            ],
            overall_confidence=0.95,
        )

    return ExplainResponse(
        sources=payload.get("sources", []),
        reasoning_steps=payload.get("reasoning_steps", []),
        overall_confidence=payload.get("overall_confidence", 0.95),
        risk_breakdown=payload.get("risk_breakdown"),
        query=payload.get("query"),
    )

"""
POST /api/risk-score    — Compute all applicable risk scores (ASCVD, CHA2DS2-VASc, HAS-BLED, GRACE).
POST /api/risk/ascvd    — Individual ASCVD (backward-compat).
POST /api/risk/chads2vasc  — Individual CHA2DS2-VASc (backward-compat).
POST /api/risk/hasbled  — Individual HAS-BLED (backward-compat).
POST /api/risk/framingham — Framingham (backward-compat, wraps ASCVD).
"""
import logging
from fastapi import APIRouter, HTTPException
from beatbound.backend.models.schemas import RiskScoreRequest, RiskScoreResponse
from beatbound.backend.services.risk_calculator import compute_risk_scores

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Risk"])


@router.post("/risk-score", response_model=RiskScoreResponse)
async def risk_score(req: RiskScoreRequest):
    """
    Compute all applicable cardiovascular risk scores in one call.
    Returns ASCVD, CHA₂DS₂-VASc, HAS-BLED, and GRACE (when inputs are available).
    """
    try:
        return compute_risk_scores(req)
    except Exception as exc:
        logger.error(f"Risk score error: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


# ── Individual calculator endpoints (backward-compatible) ─────────────────────

@router.post("/risk/ascvd")
async def risk_ascvd(req: RiskScoreRequest):
    try:
        result = compute_risk_scores(req)
        scores = {s.name: s for s in result.scores}
        ascvd = scores.get("ASCVD (10-year)")
        if not ascvd:
            raise HTTPException(status_code=422, detail="Insufficient data for ASCVD (need age, sex, lipids).")
        return ascvd
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/risk/chads2vasc")
async def risk_chads2vasc(req: RiskScoreRequest):
    try:
        result = compute_risk_scores(req)
        scores = {s.name: s for s in result.scores}
        chads = scores.get("CHA₂DS₂-VASc")
        if not chads:
            raise HTTPException(status_code=422, detail="Insufficient data for CHA₂DS₂-VASc (need age and sex).")
        return chads
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/risk/hasbled")
async def risk_hasbled(req: RiskScoreRequest):
    try:
        result = compute_risk_scores(req)
        scores = {s.name: s for s in result.scores}
        hasbled = scores.get("HAS-BLED")
        if not hasbled:
            raise HTTPException(status_code=422, detail="Could not compute HAS-BLED.")
        return hasbled
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/risk/framingham")
async def risk_framingham(req: RiskScoreRequest):
    """Alias → ASCVD calculation (Pooled Cohort Equations are the modern replacement)."""
    return await risk_ascvd(req)

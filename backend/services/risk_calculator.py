"""
Risk calculator service — wraps core OOP calculator classes and adds GRACE score.
Returns unified RiskScoreResponse with color-coded risk levels for all calculators.
"""
import logging
import math
from typing import List, Optional, Dict, Any

from beatbound.backend.models.schemas import (
    RiskScoreRequest, RiskScoreResponse, RiskScore, ScoreBreakdownItem
)

logger = logging.getLogger(__name__)


# ── ASCVD (Pooled Cohort Equations) ───────────────────────────────────────────

def _ascvd(req: RiskScoreRequest) -> Optional[RiskScore]:
    if req.age is None or req.sex is None:
        return None
    age = req.age
    sex = req.sex.lower()
    race = (req.race or "white").lower()
    tc = req.total_cholesterol or 180.0
    hdl = req.hdl_cholesterol or 50.0
    sbp = req.systolic_bp or 120.0
    on_tx = req.on_bp_treatment or False
    diabetes = req.has_diabetes or False
    smoker = req.is_smoker or False

    if not (40 <= age <= 79):
        return RiskScore(
            name="ASCVD (10-year)",
            risk_category="Unavailable",
            interpretation="Age must be 40–79 for ASCVD calculation.",
        )

    try:
        ln_age = math.log(age)
        ln_tc = math.log(tc)
        ln_hdl = math.log(hdl)
        ln_sbp = math.log(sbp)

        if sex == "female" and race == "african_american":
            s10 = 0.9533
            mean_coef = 86.608
            coef = (
                17.1141 * ln_age
                + 0.9396 * ln_tc
                - 18.9196 * ln_hdl
                + 29.2907 * ln_age * ln_hdl
                + 27.8197 * ln_sbp if not on_tx else 0
                + 29.2907 * ln_age * ln_sbp if not on_tx else 0
                + (0.8738 * 1 if smoker else 0)
                + (0.8738 * ln_age if smoker else 0)
                + (0.8645 * 1 if diabetes else 0)
            )
        elif sex == "female":
            s10 = 0.9665
            mean_coef = -29.799
            coef = (
                -7.574 * ln_age
                + 4.884 * ln_age ** 2
                + 13.540 * ln_tc
                - 3.114 * ln_age * ln_tc
                - 13.578 * ln_hdl
                + 3.149 * ln_age * ln_hdl
                + 2.019 * ln_sbp if on_tx else 0
                + (1.957 * ln_sbp if not on_tx else 0)
                + (7.574 * 1 if smoker else 0)
                - (1.665 * ln_age if smoker else 0)
                + (0.661 * 1 if diabetes else 0)
            )
        elif sex == "male" and race == "african_american":
            s10 = 0.8942
            mean_coef = 19.540
            coef = (
                2.469 * ln_age
                + 0.302 * ln_tc
                - 0.307 * ln_hdl
                + 1.916 * ln_sbp if on_tx else 0
                + (1.809 * ln_sbp if not on_tx else 0)
                + (0.549 * 1 if smoker else 0)
                + (0.645 * 1 if diabetes else 0)
            )
        else:  # white male default
            s10 = 0.9144
            mean_coef = 61.180
            coef = (
                12.344 * ln_age
                + 11.853 * ln_tc
                - 2.664 * ln_age * ln_tc
                - 7.990 * ln_hdl
                + 1.769 * ln_age * ln_hdl
                + 1.797 * ln_sbp if on_tx else 0
                + (1.764 * ln_sbp if not on_tx else 0)
                + (7.837 * 1 if smoker else 0)
                - (1.795 * ln_age if smoker else 0)
                + (0.658 * 1 if diabetes else 0)
            )

        risk = (1 - s10 ** math.exp(coef - mean_coef)) * 100
        risk = round(max(0.0, min(100.0, risk)), 1)
    except Exception:
        risk = 10.0  # safe fallback

    if risk < 5:
        category = "Low"
        interp = "Low 10-year ASCVD risk. Focus on healthy lifestyle habits."
    elif risk < 7.5:
        category = "Borderline"
        interp = "Borderline risk. Discuss statin therapy with risk-enhancing factors."
    elif risk < 20:
        category = "Intermediate"
        interp = "Intermediate risk. Statin therapy and lifestyle modification recommended."
    else:
        category = "High"
        interp = "High risk. High-intensity statin therapy strongly recommended."

    breakdown = [
        ScoreBreakdownItem(label="Age", value=age),
        ScoreBreakdownItem(label="Total Cholesterol", value=f"{tc} mg/dL"),
        ScoreBreakdownItem(label="HDL Cholesterol", value=f"{hdl} mg/dL"),
        ScoreBreakdownItem(label="Systolic BP", value=f"{sbp} mmHg"),
        ScoreBreakdownItem(label="On BP Treatment", value=str(on_tx)),
        ScoreBreakdownItem(label="Diabetes", value=str(diabetes)),
        ScoreBreakdownItem(label="Smoker", value=str(smoker)),
    ]
    recs = [
        "Statin therapy" if risk >= 7.5 else "Lifestyle counselling",
        "Blood pressure control < 130/80 mmHg",
        "Smoking cessation" if smoker else "Maintain non-smoking status",
        "HbA1c < 7% if diabetic" if diabetes else "Screen for diabetes annually",
    ]

    return RiskScore(
        name="ASCVD (10-year)",
        risk_percent=risk,
        risk_category=category,
        interpretation=interp,
        breakdown=breakdown,
        recommendations=recs,
    )


# ── CHA2DS2-VASc ──────────────────────────────────────────────────────────────

def _chads2vasc(req: RiskScoreRequest) -> Optional[RiskScore]:
    if req.age is None or req.sex is None:
        return None

    score = 0
    breakdown = []
    age = req.age
    sex = req.sex.lower()

    # C — Congestive heart failure
    if req.has_heart_failure:
        score += 1
        breakdown.append(ScoreBreakdownItem(label="Congestive Heart Failure", value="Yes", points=1))
    else:
        breakdown.append(ScoreBreakdownItem(label="Congestive Heart Failure", value="No", points=0))

    # H — Hypertension
    if req.has_hypertension:
        score += 1
        breakdown.append(ScoreBreakdownItem(label="Hypertension", value="Yes", points=1))
    else:
        breakdown.append(ScoreBreakdownItem(label="Hypertension", value="No", points=0))

    # A2 — Age ≥75
    if age >= 75:
        score += 2
        breakdown.append(ScoreBreakdownItem(label="Age ≥75", value=str(age), points=2))
    else:
        breakdown.append(ScoreBreakdownItem(label="Age ≥75", value=str(age), points=0))

    # D — Diabetes
    if req.has_diabetes:
        score += 1
        breakdown.append(ScoreBreakdownItem(label="Diabetes", value="Yes", points=1))
    else:
        breakdown.append(ScoreBreakdownItem(label="Diabetes", value="No", points=0))

    # S2 — Stroke/TIA history
    if req.stroke_tia_history:
        score += 2
        breakdown.append(ScoreBreakdownItem(label="Stroke/TIA History", value="Yes", points=2))
    else:
        breakdown.append(ScoreBreakdownItem(label="Stroke/TIA History", value="No", points=0))

    # V — Vascular disease
    if req.has_vascular_disease:
        score += 1
        breakdown.append(ScoreBreakdownItem(label="Vascular Disease", value="Yes", points=1))
    else:
        breakdown.append(ScoreBreakdownItem(label="Vascular Disease", value="No", points=0))

    # A — Age 65–74
    if 65 <= age <= 74:
        score += 1
        breakdown.append(ScoreBreakdownItem(label="Age 65–74", value=str(age), points=1))
    else:
        breakdown.append(ScoreBreakdownItem(label="Age 65–74", value=str(age), points=0))

    # Sc — Sex category (female)
    if sex == "female":
        score += 1
        breakdown.append(ScoreBreakdownItem(label="Sex (Female)", value="Yes", points=1))
    else:
        breakdown.append(ScoreBreakdownItem(label="Sex (Female)", value="No", points=0))

    # Annual stroke risk lookup
    stroke_risk_map = {
        0: 0.0, 1: 1.3, 2: 2.2, 3: 3.2, 4: 4.0,
        5: 6.7, 6: 9.8, 7: 9.6, 8: 12.5, 9: 15.2,
    }
    annual_risk = stroke_risk_map.get(min(score, 9), 15.2)

    if score == 0 or (score == 1 and sex == "female"):
        category = "Low"
        rec = "No anticoagulation required."
    elif score == 1 and sex == "male":
        category = "Low-Moderate"
        rec = "Consider anticoagulation after risk-benefit discussion."
    elif score == 2:
        category = "Moderate"
        rec = "Oral anticoagulation (DOAC preferred) is recommended."
    else:
        category = "High"
        rec = "Oral anticoagulation strongly recommended. DOAC preferred over warfarin."

    return RiskScore(
        name="CHA₂DS₂-VASc",
        score=float(score),
        risk_percent=annual_risk,
        risk_category=category,
        interpretation=(
            f"Score {score}/9 — estimated annual stroke risk {annual_risk}%. {rec}"
        ),
        breakdown=breakdown,
        recommendations=[rec, "Evaluate HAS-BLED bleeding risk before anticoagulation."],
    )


# ── HAS-BLED ──────────────────────────────────────────────────────────────────

def _hasbled(req: RiskScoreRequest) -> Optional[RiskScore]:
    score = 0
    breakdown = []

    checks: List[tuple] = [
        ("Hypertension (uncontrolled, SBP>160)", bool(req.has_hypertension and (req.systolic_bp or 0) > 160)),
        ("Renal Disease", bool(req.renal_disease)),
        ("Liver Disease", bool(req.liver_disease)),
        ("Prior Stroke", bool(req.stroke_tia_history)),
        ("Bleeding History or Predisposition", bool(req.bleeding_history)),
        ("Labile INR", bool(req.labile_inr)),
        ("Elderly (Age >65)", bool((req.age or 0) > 65)),
        ("Antiplatelet/NSAID Use", bool(req.on_antiplatelet_or_nsaid)),
        ("Alcohol Use", bool(req.alcohol_use)),
    ]

    for label, present in checks:
        pts = 1 if present else 0
        score += pts
        breakdown.append(ScoreBreakdownItem(label=label, value="Yes" if present else "No", points=pts))

    bleeding_risk_map = {0: 1.13, 1: 1.02, 2: 1.88, 3: 3.74, 4: 8.70, 5: 12.50}
    annual_bleed = bleeding_risk_map.get(min(score, 5), 12.50)

    if score <= 1:
        category = "Low"
        interp = f"Low bleeding risk (score {score}). Anticoagulation likely safe."
    elif score == 2:
        category = "Moderate"
        interp = f"Moderate bleeding risk (score {score}). Caution with anticoagulation; correct modifiable risk factors."
    else:
        category = "High"
        interp = (
            f"High bleeding risk (score {score}). Does NOT preclude anticoagulation but "
            "mandates close monitoring and correction of modifiable factors."
        )

    return RiskScore(
        name="HAS-BLED",
        score=float(score),
        risk_percent=annual_bleed,
        risk_category=category,
        interpretation=interp,
        breakdown=breakdown,
        recommendations=[
            "Control blood pressure tightly (target <130/80 mmHg).",
            "Review antiplatelet/NSAID use — stop if not essential.",
            "Reduce alcohol consumption.",
            "Monitor INR closely if on warfarin.",
        ],
    )


# ── GRACE ─────────────────────────────────────────────────────────────────────

def _grace(req: RiskScoreRequest) -> Optional[RiskScore]:
    if req.age is None or req.heart_rate is None or req.systolic_bp is None:
        return None

    age = req.age
    hr = req.heart_rate
    sbp = req.systolic_bp or 120
    creat = req.creatinine or 1.0
    killip = req.killip_class or 1

    def _age_pts(a):
        if a < 30: return 0
        if a < 40: return 8
        if a < 50: return 25
        if a < 60: return 41
        if a < 70: return 58
        if a < 80: return 75
        if a < 90: return 91
        return 100

    def _hr_pts(h):
        if h < 50: return 0
        if h < 70: return 3
        if h < 90: return 9
        if h < 110: return 15
        if h < 150: return 24
        if h < 200: return 38
        return 46

    def _sbp_pts(s):
        if s < 80: return 58
        if s < 100: return 53
        if s < 120: return 43
        if s < 140: return 34
        if s < 160: return 24
        if s < 200: return 10
        return 0

    def _creat_pts(c):
        if c < 0.4: return 1
        if c < 0.8: return 4
        if c < 1.2: return 7
        if c < 1.6: return 10
        if c < 2.0: return 13
        if c < 4.0: return 21
        return 28

    def _killip_pts(k):
        return {1: 0, 2: 20, 3: 39, 4: 59}.get(k, 0)

    score = (
        _age_pts(age)
        + _hr_pts(hr)
        + _sbp_pts(sbp)
        + _creat_pts(creat)
        + _killip_pts(killip)
        + (43 if req.cardiac_arrest else 0)
        + (28 if req.st_deviation else 0)
        + (14 if req.elevated_enzymes else 0)
    )

    if score < 109:
        category = "Low"
        in_hosp = "<1%"
        six_mo = "<3%"
        interp = f"Low GRACE risk (score {score}). Early discharge and outpatient follow-up may be appropriate."
    elif score <= 140:
        category = "Intermediate"
        in_hosp = "1–3%"
        six_mo = "3–8%"
        interp = f"Intermediate GRACE risk (score {score}). In-hospital monitoring and early invasive strategy recommended."
    else:
        category = "High"
        in_hosp = ">3%"
        six_mo = ">8%"
        interp = f"High GRACE risk (score {score}). Urgent invasive strategy (within 24h) strongly recommended."

    breakdown = [
        ScoreBreakdownItem(label="Age", value=age, points=_age_pts(age)),
        ScoreBreakdownItem(label="Heart Rate", value=f"{hr} bpm", points=_hr_pts(hr)),
        ScoreBreakdownItem(label="Systolic BP", value=f"{sbp} mmHg", points=_sbp_pts(sbp)),
        ScoreBreakdownItem(label="Creatinine", value=f"{creat} mg/dL", points=_creat_pts(creat)),
        ScoreBreakdownItem(label="Killip Class", value=killip, points=_killip_pts(killip)),
        ScoreBreakdownItem(label="Cardiac Arrest", value=str(req.cardiac_arrest), points=43 if req.cardiac_arrest else 0),
        ScoreBreakdownItem(label="ST Deviation", value=str(req.st_deviation), points=28 if req.st_deviation else 0),
        ScoreBreakdownItem(label="Elevated Enzymes", value=str(req.elevated_enzymes), points=14 if req.elevated_enzymes else 0),
    ]

    return RiskScore(
        name="GRACE (ACS)",
        score=float(score),
        risk_category=category,
        interpretation=f"{interp} Estimated in-hospital mortality: {in_hosp}; 6-month mortality: {six_mo}.",
        breakdown=breakdown,
        recommendations=[
            "Urgent cardiology referral" if score > 140 else "Cardiology review within 72 hours",
            "Dual antiplatelet therapy (aspirin + P2Y12 inhibitor)",
            "Anticoagulation therapy",
            "Serial ECG and troponin monitoring",
        ],
    )


# ── Overall risk level aggregation ────────────────────────────────────────────

def _aggregate_risk_level(scores: list) -> str:
    categories = [s.risk_category.upper() for s in scores if s]
    if any(c in ("HIGH", "CRITICAL") for c in categories):
        return "HIGH"
    if any(c in ("INTERMEDIATE", "MODERATE") for c in categories):
        return "MODERATE"
    return "LOW"


# ── Public entry point ────────────────────────────────────────────────────────

def compute_risk_scores(req: RiskScoreRequest) -> RiskScoreResponse:
    """Compute all applicable risk scores and return a unified response."""
    scores = []

    ascvd = _ascvd(req)
    if ascvd:
        scores.append(ascvd)

    chads = _chads2vasc(req)
    if chads:
        scores.append(chads)

    hasbled = _hasbled(req)
    if hasbled:
        scores.append(hasbled)

    grace = _grace(req)
    if grace:
        scores.append(grace)

    if not scores:
        return RiskScoreResponse(
            scores=[],
            risk_level="UNKNOWN",
            explanation="Insufficient input data to compute any risk scores. Please provide age, sex, and relevant biomarker values.",
            overall_recommendation="Please consult your physician for a complete cardiovascular risk assessment.",
        )

    risk_level = _aggregate_risk_level(scores)

    high_risk_scores = [s for s in scores if "High" in s.risk_category or "Intermediate" in s.risk_category]
    explanation_parts = [f"{s.name}: {s.risk_category}" for s in scores]
    explanation = "Risk summary — " + "; ".join(explanation_parts) + "."

    if risk_level == "HIGH":
        overall_rec = (
            "Urgent medical evaluation recommended. Consider specialist referral and initiation "
            "of evidence-based pharmacotherapy."
        )
    elif risk_level == "MODERATE":
        overall_rec = (
            "Schedule a physician review within 1–2 weeks. Lifestyle modification and risk factor "
            "optimisation are priorities."
        )
    else:
        overall_rec = (
            "Continue preventive health measures. Annual cardiovascular risk screening is advised."
        )

    return RiskScoreResponse(
        scores=scores,
        risk_level=risk_level,
        explanation=explanation,
        overall_recommendation=overall_rec,
    )

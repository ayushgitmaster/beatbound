"""
POST /api/upload-report   — Lab report upload (PDF / image).
POST /api/lab/ai-analysis — AI analysis of extracted lab values.
"""
import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from beatbound.backend.models.schemas import LabUploadResponse, LabAIRequest, LabAIResponse, LabValues

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Lab Parser"])

ALLOWED_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/tiff",
    "image/bmp",
}


@router.post("/upload-report", response_model=LabUploadResponse)
async def upload_report(file: UploadFile = File(...)):
    """
    Accept a PDF or image lab report, run OCR/parsing, and return
    structured biomarker values in JSON.
    """
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{content_type}'. Upload a PDF or image.",
        )

    raw = await file.read()
    if len(raw) > 20 * 1024 * 1024:  # 20 MB cap
        raise HTTPException(status_code=413, detail="File exceeds 20 MB limit.")

    try:
        if "pdf" in content_type:
            result = _parse_pdf_bytes(raw, file.filename or "report.pdf")
        else:
            result = _parse_image_bytes(raw, file.filename or "report.png")
    except Exception as exc:
        logger.error(f"Lab parsing error: {exc}", exc_info=True)
        raise HTTPException(status_code=422, detail=f"Could not parse lab report: {exc}")

    return result


def _parse_pdf_bytes(raw: bytes, filename: str) -> LabUploadResponse:
    from beatbound.backend.core.multimodal_parser import PDFLabReportParser
    import pandas as pd

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name

    try:
        parser = PDFLabReportParser()
        parsed = parser.parse_pdf(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    values_raw = parsed.get("values", {})
    lab_values = _map_to_lab_values(values_raw)
    rag_prompt = _build_rag_prompt(values_raw, filename)
    summary = _build_summary(values_raw)

    return LabUploadResponse(
        values=lab_values,
        categories=parsed.get("categories", {}),
        summary_table=summary,
        rag_prompt=rag_prompt,
        source_file=filename,
    )


def _parse_image_bytes(raw: bytes, filename: str) -> LabUploadResponse:
    """OCR-based parsing for image lab reports."""
    try:
        import pytesseract
        from PIL import Image
        import io

        img = Image.open(io.BytesIO(raw))
        text = pytesseract.image_to_string(img)
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="OCR dependencies (pytesseract / Pillow) not installed. Only PDF upload is supported.",
        )

    from beatbound.backend.core.multimodal_parser import PDFLabReportParser
    parser = PDFLabReportParser()

    # Reuse regex extraction on OCR text
    values_raw = {}
    for key, patterns in parser.patterns.items():
        val = parser.extract_value(text.lower(), patterns)
        if val[0] is not None:
            values_raw[key] = {"value": val[0], "unit": val[1]}

    lab_values = _map_to_lab_values(values_raw)
    rag_prompt = _build_rag_prompt(values_raw, filename)
    summary = _build_summary(values_raw)

    return LabUploadResponse(
        values=lab_values,
        categories={},
        summary_table=summary,
        rag_prompt=rag_prompt,
        source_file=filename,
    )


def _map_to_lab_values(values_raw: dict) -> LabValues:
    def v(key):
        item = values_raw.get(key, {})
        if isinstance(item, dict):
            return item.get("value")
        return None

    def u(key):
        item = values_raw.get(key, {})
        if isinstance(item, dict):
            return item.get("unit")
        return None

    return LabValues(
        troponin=v("troponin"),
        troponin_unit=u("troponin"),
        ldl=v("ldl_cholesterol"),
        ldl_unit=u("ldl_cholesterol"),
        hdl=v("hdl_cholesterol"),
        hdl_unit=u("hdl_cholesterol"),
        cholesterol=v("total_cholesterol"),
        cholesterol_unit=u("total_cholesterol"),
        triglycerides=v("triglycerides"),
        triglycerides_unit=u("triglycerides"),
        glucose=v("glucose"),
        glucose_unit=u("glucose"),
        creatinine=v("creatinine"),
        creatinine_unit=u("creatinine"),
        egfr=v("egfr"),
        bnp=v("bnp"),
        hba1c=v("hba1c"),
    )


_NORMAL_RANGES = {
    "total_cholesterol": "< 200 mg/dL",
    "ldl_cholesterol": "< 100 mg/dL",
    "hdl_cholesterol": "> 60 mg/dL",
    "triglycerides": "< 150 mg/dL",
    "glucose": "70–99 mg/dL (fasting)",
    "troponin": "< 0.04 ng/mL",
    "creatinine": "0.6–1.2 mg/dL",
    "egfr": "> 60 mL/min/1.73m²",
    "bnp": "< 100 pg/mL",
    "hba1c": "< 5.7%",
}

_DISPLAY_NAMES = {
    "total_cholesterol": "Total Cholesterol",
    "ldl_cholesterol": "LDL Cholesterol",
    "hdl_cholesterol": "HDL Cholesterol",
    "triglycerides": "Triglycerides",
    "glucose": "Glucose",
    "troponin": "Troponin",
    "creatinine": "Creatinine",
    "egfr": "eGFR",
    "bnp": "BNP",
    "hba1c": "HbA1c",
}


def _build_summary(values_raw: dict) -> list:
    rows = []
    for key, display in _DISPLAY_NAMES.items():
        item = values_raw.get(key)
        if item and isinstance(item, dict) and item.get("value") is not None:
            rows.append({
                "test": display,
                "value": f"{item['value']} {item.get('unit', '')}".strip(),
                "normal_range": _NORMAL_RANGES.get(key, "—"),
            })
    return rows


def _build_rag_prompt(values_raw: dict, filename: str) -> str:
    lines = [f"Lab report: {filename}\n"]
    for key, display in _DISPLAY_NAMES.items():
        item = values_raw.get(key)
        if item and isinstance(item, dict) and item.get("value") is not None:
            lines.append(f"- {display}: {item['value']} {item.get('unit', '')}".strip())
    if len(lines) == 1:
        return ""
    lines.append(
        "\nBased on these results, provide a clinical interpretation, flag abnormal values, "
        "and suggest follow-up actions."
    )
    return "\n".join(lines)


@router.post("/lab/ai-analysis", response_model=LabAIResponse)
async def lab_ai_analysis(req: LabAIRequest):
    """
    Generate an AI clinical analysis from extracted lab values (RAG prompt string).
    """
    if not req.rag_prompt.strip():
        raise HTTPException(status_code=422, detail="rag_prompt cannot be empty.")
    try:
        import os
        api_key = os.getenv("OPENROUTER_API_KEY")
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model="google/gemini-2.0-flash-001",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={"Authorization": f"Bearer {api_key}"},
            temperature=0.2,
        )
        system = (
            "You are BeatBound, a cardiac clinical assistant. "
            "Analyse the provided lab results in plain language. "
            "Highlight abnormal values, explain clinical significance, and suggest follow-up. "
            "Add a disclaimer that findings should be reviewed by a qualified physician."
        )
        response = llm.invoke(f"{system}\n\n{req.rag_prompt}")
        return LabAIResponse(analysis=response.content)
    except Exception as exc:
        logger.error(f"Lab AI analysis error: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))

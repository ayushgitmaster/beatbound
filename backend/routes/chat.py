"""
POST /api/chat  — Gemini-based conversational endpoint.
"""
import logging
from fastapi import APIRouter, HTTPException
from beatbound.backend.models.schemas import ChatRequest, ChatResponse
from beatbound.backend.services.rag_pipeline import run_rag_chat

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Cardiac chat powered directly by Gemini.

    - Sends the user message and conversation history to Gemini.
    - Returns the model answer without document retrieval.
    """
    if not req.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    try:
        return await run_rag_chat(req)
    except EnvironmentError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during chat processing.")

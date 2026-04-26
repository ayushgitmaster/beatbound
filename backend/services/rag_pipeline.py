"""
Direct Gemini chat — no retrieval, no ChromaDB.
"""
import logging
import os

from beatbound.backend.models.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are BeatBound, a cardiac health assistant.
Provide helpful, evidence-based answers about heart health and cardiac conditions.
Keep answers concise, clear, and patient-friendly.
Always remind users to consult a qualified healthcare professional for personalised medical advice."""


def _get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY not set in environment.")
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model="google/gemini-2.0-flash-001",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={"Authorization": f"Bearer {api_key}"},
        temperature=0.2,
        max_tokens=1024,
    )


def _build_history_context(history: list) -> str:
    if not history:
        return ""
    lines = []
    for msg in history[-8:]:
        role = "User" if msg.role == "user" else "Assistant"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines) + "\n"


async def run_rag_chat(request: ChatRequest) -> ChatResponse:
    """Call Gemini directly with conversation history — no document retrieval."""
    llm = _get_llm()
    query = request.message.strip()
    history_ctx = _build_history_context(request.history or [])

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"{history_ctx}"
        f"User: {query}\nAssistant:"
    )

    response = llm.invoke(prompt)

    return ChatResponse(
        answer=response.content,
        sources=[],
        relevance_scores=[],
        reasoning_steps=[],
        is_fallback=False,
    )

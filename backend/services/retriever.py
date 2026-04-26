"""
ChromaDB-backed semantic retriever using sentence-transformers embeddings.
Provides similarity search with relevance scores and automatic knowledge bootstrapping.
"""
import logging
import os
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

PERSIST_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "cardiac_knowledge"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RELEVANCE_THRESHOLD = 0.35  # below this → fallback to generic LLM response

_vector_store = None  # module-level singleton


def _get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store():
    """Return the singleton ChromaDB vector store, bootstrapping if empty."""
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    from langchain_community.vectorstores import Chroma

    PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = _get_embeddings()

    _vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(PERSIST_DIR),
    )

    # Bootstrap with clinical knowledge if the store is empty
    if _vector_store._collection.count() == 0:
        logger.info("ChromaDB empty — bootstrapping with cardiac knowledge documents…")
        _bootstrap_knowledge()

    count = _vector_store._collection.count()
    logger.info(f"ChromaDB ready: {count} chunks in '{COLLECTION_NAME}'")
    return _vector_store


def _bootstrap_knowledge():
    """Seed the vector store with embedded cardiac clinical knowledge."""
    from beatbound.backend.services.knowledge_docs import get_cardiac_documents
    documents = get_cardiac_documents()
    build_vector_store(documents)


def build_vector_store(documents):
    """(Re)build the vector store from a list of LangChain Documents."""
    global _vector_store
    from langchain_community.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = splitter.split_documents(documents)

    PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = _get_embeddings()

    _vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(PERSIST_DIR),
    )
    logger.info(f"Vector store built with {len(chunks)} chunks from {len(documents)} documents")


def retrieve_with_scores(query: str, k: int = 4) -> List[Dict]:
    """
    Retrieve top-k relevant chunks with relevance scores.

    Returns a list of dicts:
        {content, source, relevance_score, page, doc_type}

    Scores are in [0, 1] where 1 = perfect match.
    """
    vs = get_vector_store()
    try:
        results = vs.similarity_search_with_relevance_scores(query, k=k)
        chunks = [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Clinical Guidelines"),
                "relevance_score": round(float(score), 4),
                "page": doc.metadata.get("page"),
                "doc_type": doc.metadata.get("doc_type", "clinical"),
            }
            for doc, score in results
        ]
        # Sort by relevance descending
        chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        return chunks
    except Exception as exc:
        logger.error(f"Retrieval error: {exc}", exc_info=True)
        return []


def is_fallback(chunks: List[Dict]) -> bool:
    """Return True if the best chunk is below the relevance threshold."""
    if not chunks:
        return True
    return chunks[0]["relevance_score"] < RELEVANCE_THRESHOLD

# BeatBound — Multimodal Cardiac Decision Support System

A production-ready full-stack application for cardiac clinical decision support,
combining Retrieval-Augmented Generation (RAG), multimodal lab parsing, and
evidence-based risk calculators.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + TypeScript + Tailwind CSS + Vite |
| Backend | FastAPI (Python 3.11+) |
| AI / RAG | LangChain + ChromaDB + sentence-transformers |
| LLM | Google Gemini 2.5 Flash |

## Project Structure

`
beatbound/
  backend/
    main.py              # FastAPI app entry point
    models/
      schemas.py         # Pydantic request/response models
    routes/
      chat.py            # POST /api/chat (RAG chat)
      parser.py          # POST /api/upload-report (lab parsing)
      risk.py            # POST /api/risk-score (all calculators)
      explain.py         # GET /api/explain (reasoning chain)
    services/
      rag_pipeline.py    # RAG retrieval + LLM pipeline
      retriever.py       # ChromaDB vector store
      risk_calculator.py # ASCVD, CHA2DS2-VASc, HAS-BLED, GRACE
      explainability.py  # Reasoning chain builder
      knowledge_docs.py  # Seed clinical documents for ChromaDB
    core/
      cardiac_risk_calculators.py
      heart_chain.py
      heart_knowledge.py
      multimodal_parser.py
    utils/
    chroma_db/           # Auto-created, persisted vector store
    requirements.txt
    run.bat
  frontend/
    src/
      api.ts             # Axios API client
      types/index.ts     # TypeScript types
      lib/utils.ts       # cn(), risk colour helpers
      components/
        Sidebar.tsx
        ui/              # Button, Card, Badge, Progress, Spinner
      pages/
        Chat.tsx         # RAG chat with collapsible source panel
        Lab.tsx          # PDF upload + AI analysis
        Risk.tsx         # Combined risk dashboard
        Explain.tsx      # Explainability panel
        Symptom.tsx      # Symptom checker
        Resources.tsx    # Clinical reference
        About.tsx
    package.json
    tailwind.config.js
    postcss.config.js
    vite.config.ts
  .env.example
`

## Quick Start

### 1. Environment setup

`ash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
`

### 2. Backend

`ash
cd d:/beatbound
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
`

Or use ackend/run.bat on Windows.

### 3. Frontend

`ash
cd frontend
npm install
npm run dev
# App: http://localhost:5173
`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | RAG chat with clinical evidence |
| POST | /api/upload-report | PDF/image lab report parsing |
| POST | /api/risk-score | All risk scores (ASCVD + CHA2DS2-VASc + HAS-BLED + GRACE) |
| GET | /api/explain | Last reasoning chain + evidence |
| GET | /api/resources/conditions | Heart condition reference |
| GET | /api/resources/symptoms | Symptom guide |
| POST | /api/symptom/assess | LangChain symptom assessment |

## Features

- **RAG Chat**: Grounded answers from clinical guidelines. Falls back to general LLM with warning banner when relevance < threshold.
- **Lab Parser**: Regex + OCR extraction of troponin, LDL, HDL, glucose, creatinine, eGFR, BNP, HbA1c.
- **Risk Dashboard**: ASCVD, CHA₂DS₂-VASc, HAS-BLED, GRACE with colour-coded progress bars and breakdown.
- **Explainability**: Retrieved documents, relevance scores, reasoning steps — all visible in the UI.
- **Voice Mode**: Toggle placeholder for ElevenLabs TTS integration.

## Disclaimer

BeatBound is for educational and research purposes only. It does not constitute
medical advice. Always consult a qualified healthcare professional.
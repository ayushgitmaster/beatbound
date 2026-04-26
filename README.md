<div align="center">

# 🫀 BeatBound

### AI-Powered Cardiac Clinical Decision Support System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A production-ready full-stack application combining **Retrieval-Augmented Generation**, **multimodal lab report parsing**, and **evidence-based cardiac risk calculators** — all inside a real-time React UI.

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Reference](#-api-reference) • [Project Structure](#-project-structure) • [Disclaimer](#%EF%B8%8F-disclaimer)

</div>

---

## ✨ Features

<details>
<summary><b>🤖 AI Chat (RAG)</b></summary>

Grounded conversational Q&A backed by clinical guidelines stored in a ChromaDB vector store. Automatically falls back to a general LLM response with a warning banner when document relevance drops below threshold.

</details>

<details>
<summary><b>🧪 Lab Report Parser</b></summary>

Upload a PDF or image lab report. BeatBound extracts key biomarkers via regex + OCR — troponin, LDL, HDL, glucose, creatinine, eGFR, BNP, HbA1c — and runs an AI clinical analysis.

</details>

<details>
<summary><b>📊 Cardiac Risk Dashboard</b></summary>

Computes four validated risk scores from a single form submission:

| Score | Use Case |
|---|---|
| **ASCVD** (Pooled Cohort Equations) | 10-year atherosclerotic cardiovascular disease risk |
| **CHA2DS2-VASc** | Stroke risk in atrial fibrillation |
| **HAS-BLED** | Bleeding risk on anticoagulation |
| **GRACE** | In-hospital / 6-month mortality in ACS |

Each score is colour-coded (low / moderate / high) with a full breakdown panel.

</details>

<details>
<summary><b>🔍 Explainability Dashboard</b></summary>

Every AI response exposes its reasoning chain: retrieved source documents, per-step confidence scores, and an overall confidence meter — giving full transparency into how answers are generated.

</details>

<details>
<summary><b>🩺 Symptom Checker</b></summary>

LangChain-powered cardiac symptom triage that classifies urgency and suggests next steps.

</details>

<details>
<summary><b>🔊 Voice Mode</b></summary>

ElevenLabs TTS integration toggle for audio playback of AI responses.

</details>

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19 · TypeScript · Tailwind CSS · Vite |
| **Backend** | FastAPI · Python 3.11+ · Pydantic v2 |
| **AI / RAG** | LangChain · ChromaDB · sentence-transformers |
| **LLM** | Gemini 2.0 Flash via OpenRouter |
| **Lab Parsing** | pdfplumber · Pillow · regex OCR |
| **Data** | NumPy · pandas |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai/keys) API key

### 1 — Clone & configure

```bash
git clone https://github.com/your-username/beatbound.git
cd beatbound
cp .env.example .env
# Open .env and add your OPENROUTER_API_KEY
```

### 2 — Backend

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

> Windows shortcut: run `backend/run.bat`

Interactive API docs available at **http://localhost:8000/docs**

### 3 — Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at **http://localhost:5173**

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | RAG chat with clinical evidence |
| `POST` | `/api/upload-report` | PDF / image lab report parsing |
| `POST` | `/api/risk-score` | ASCVD + CHA2DS2-VASc + HAS-BLED + GRACE |
| `GET` | `/api/explain` | Last reasoning chain + retrieved evidence |
| `GET` | `/api/resources/conditions` | Heart condition reference library |
| `GET` | `/api/resources/symptoms` | Symptom guide |
| `POST` | `/api/symptom/assess` | LangChain symptom triage |

---

## 📁 Project Structure

<details>
<summary>Expand full tree</summary>

```
beatbound/
├── backend/
│   ├── main.py                     # FastAPI app entry point
│   ├── models/
│   │   └── schemas.py              # Pydantic request/response models
│   ├── routes/
│   │   ├── chat.py                 # POST /api/chat
│   │   ├── parser.py               # POST /api/upload-report
│   │   ├── risk.py                 # POST /api/risk-score
│   │   └── explain.py              # GET  /api/explain
│   ├── services/
│   │   ├── rag_pipeline.py         # RAG retrieval + LLM pipeline
│   │   ├── retriever.py            # ChromaDB vector store
│   │   ├── risk_calculator.py      # ASCVD, CHA2DS2-VASc, HAS-BLED, GRACE
│   │   ├── explainability.py       # Reasoning chain builder
│   │   └── knowledge_docs.py       # Clinical document seeder
│   ├── core/
│   │   ├── cardiac_risk_calculators.py
│   │   ├── heart_chain.py
│   │   ├── heart_knowledge.py
│   │   └── multimodal_parser.py
│   ├── chroma_db/                  # Auto-created on first run
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api.ts                  # Axios API client
│       ├── types/index.ts          # TypeScript types
│       ├── lib/utils.ts            # cn(), risk colour helpers
│       ├── components/
│       │   ├── Sidebar.tsx
│       │   └── ui/                 # Button, Card, Badge, Progress, Spinner
│       └── pages/
│           ├── Chat.tsx            # RAG chat
│           ├── Lab.tsx             # PDF upload + AI analysis
│           ├── Risk.tsx            # Risk score dashboard
│           ├── Explain.tsx         # Explainability panel
│           ├── Symptom.tsx         # Symptom checker
│           ├── Resources.tsx       # Clinical reference
│           └── About.tsx
├── .env.example
└── README.md
```

</details>

---

## ⚠️ Disclaimer

BeatBound is intended for **educational and research purposes only**. It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions.

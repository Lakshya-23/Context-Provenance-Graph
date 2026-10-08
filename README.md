# Context Provenance Graph

An interactive enterprise governance platform that transforms unstructured business documents into governed, auditable AI context, connects that context to downstream consumers (metrics, repositories, skills, agents, and evaluations), and traces the blast radius of policy revisions.

---

## Architecture Overview

```
Revenue_Policy.pdf
       │
       ▼
  PyMuPDF Parser (Page-Aware)
       │
       ▼
  LangGraph Extraction Pipeline (LiteLLM)
       │
       ├── Extract Claims (Rules & assertions)
       ├── Extract Governed Concepts (Definitions & aliases)
       ├── Evidence Verification (Verbatim page matching)
       └── Pydantic Schema Validation
       │
       ▼
  Provenance Graph Engine (NetworkX-style BFS/DFS)
       │
       ├── Layer 0: Source Document
       ├── Layer 1: Extracted Claims
       ├── Layer 2: Governed Glossary
       └── Layer 3: Downstream Ecosystem
             ├── Metrics (Gross/Net/Realized Revenue)
             ├── Context Repositories (Data Warehouse SQL models)
             ├── Agent Skills (Revenue calculation instructions)
             ├── Autonomous Agents (Finance Analyst bots)
             └── Evaluations (Rule test benchmarks)
       │
       ▼
  Downstream Blast-Radius & Change Analysis
       ├── v1.2 vs v1.3 Semantic Policy Diff
       ├── Affected Term Mapping
       └── Automated BFS Blast Radius Traversal
```

---

## Tech Stack

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, `@xyflow/react` (React Flow), Tailwind CSS v4, Lucide Icons.
- **Backend**: Python 3.12, FastAPI, LangGraph, LiteLLM, PyMuPDF (`pymupdf`), Pydantic v2.
- **Supported LLM Providers**: Groq, Google Gemini, OpenAI, Anthropic, or any LiteLLM-compatible model.
- **Security & Hosting**: Designed for Vercel (Frontend) and Render (Backend).

---

## Configuration & Environment Variables

Copy `.env.example` to `.env` in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:

```env
# --- Model Selection ---
# Option 1: Groq 
LLM_MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY=gsk_your_groq_api_key_here

# Option 2: Google Gemini
# LLM_MODEL=gemini/gemini-2.0-flash
# GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here

# --- Rate Limiting Options ---
# Maximum requests per minute to stay within free/standard tier limits
LLM_RPM_LIMIT=30
# Minimum sleep delay (seconds) between consecutive LLM calls
LLM_MIN_DELAY_SECONDS=1.0

# --- Networking ---
PORT=8000
NEXT_PUBLIC_API_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## Running Locally

### Terminal 1: Backend Service (FastAPI)

```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

- API Base: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### Terminal 2: Frontend Service (Next.js)

```bash
# From repository root
npm run dev
```

- Access the web interface at `http://localhost:3000`

---

## Application Features & Navigation

1. **Overview (`/`)**:
   - Source document card with PDF viewer and metadata.
   - High-level KPIs: Governed Terms, Extracted Claims, Downstream Consumers, Graph Edges.
   - Preview of governed concepts and workflow trace inspector.

2. **Governed Context Glossary (`/glossary`)**:
   - Filterable & searchable glossary of enterprise accounting terms.
   - Inspection drawer displaying definitions, business rules, and verbatim page citations.

3. **Interactive Provenance Graph (`/graph`)**:
   - Multi-layer React Flow diagram with custom node cards.
   - Layered visual layout: Source → Claims → Terms → Metrics/Repos → Skills/Agents/Evals.
   - Click any node to highlight upstream lineage and downstream blast radius.

4. **Semantic Impact Analysis (`/impact`)**:
   - Version evolution simulator (v1.2 base vs v1.3 revision).
   - LLM semantic diff explaining the rationale behind policy changes (e.g. pre-settlement refund deductions).
   - Deterministic grouping all impacted downstream metrics, pipelines, agents, and test cases.

5. **Deterministic Evaluators (`/evaluations`)**:
   - In-process evaluation benchmarks:
     - **Term Coverage**: Validates expected concepts are present.
     - **Definition Groundedness**: N-gram lexical overlap against source text.
     - **Evidence Accuracy**: Verbatim quote and page verification.
     - **Business Rule Completeness**: Audits condition coverage.
   - Grounding audit table showing citations and verification status.

---

## Production Deployment

### Backend on Render (Web Service)
- **Root Directory**: `backend`
- **Environment**: Python
- **Build Command**: `pip install uv && uv sync`
- **Start Command**: `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `LLM_MODEL`: e.g. `groq/llama-3.3-70b-versatile`
  - `GROQ_API_KEY`: your API key
  - `ALLOWED_ORIGINS`: `https://your-app.vercel.app`

### Frontend on Vercel
- **Root Directory**: `./` (root)
- **Framework Preset**: Next.js
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: `https://your-backend.onrender.com`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Service health status and configured model |
| `POST` | `/api/analyze` | Run LangGraph extraction pipeline on specified document version |
| `POST` | `/api/impact` | Compare document versions and calculate downstream blast radius |
| `POST` | `/api/evaluate` | Run in-process deterministic evaluation benchmarks |
| `GET` | `/api/document/{version}` | Retrieve parsed pages and raw text for a policy version |

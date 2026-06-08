# Wuthering Waves Agent

An agentic AI advisor for Wuthering Waves that delivers real-time character builds, team compositions, and farming recommendations.

## Live Demo

[gameplay-agent-for-wuthering-waves.vercel.app](https://gameplay-agent-for-wuthering-waves.vercel.app)

## Architecture

```
┌──────────────────┐      ┌──────────────────┐      ┌─────────────────────┐
│  React Frontend  │ ───▶ │  FastAPI Backend │ ───▶ │  LangGraph ReAct    │
│  (Vercel)        │      │  (Railway)       │      │  Agent (GPT-4o)     │
└──────────────────┘      └──────────────────┘      └──────────┬──────────┘
                                                                │
                          ┌─────────────────────────────────────┴──────────┐
                          │                                                │
                          ▼                                                ▼
                  ┌────────────────┐                            ┌────────────────┐
                  │     Tools      │                            │  ChromaDB RAG  │
                  │                │                            │                │
                  │ • Game8 Scrape │                            │ Vector store + │
                  │ • Reddit Meta  │                            │ sentence-      │
                  │ • Farming Adv. │                            │ transformers   │
                  │ • Build Scrape │                            │                │
                  └────────────────┘                            └────────────────┘
```


## How It Works

Every user message is first passed through a ChromaDB retrieval step, which pulls the most relevant chunks from a seeded Wuthering Waves knowledge base and prepends them as context. That  prompt is handed to a LangGraph ReAct agent powered by GPT-4o, which decides if it has enough information to answer or needs to call a tool. Tools cover real-time scraping (Game8 tier lists, character pages, wuthering.gg builds), community signal (Reddit search), and deterministic logic (farming priority by Union Level). The loop continues until the model produces a final answer, which is returned to the frontend along with the full conversation history so context is preserved across turns.

## Local Setup

Clone the repo:

```bash
git clone https://github.com/your-handle/wuwa-agent.git
cd wuwa-agent
```

**Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=fc-...
```

Seed the vector DB and start the API:

```bash
python populate_db.py
python api.py
```

The API runs at `http://localhost:8000`.

**Frontend**

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

Start the dev server:

```bash
npm run dev
```

Open `http://localhost:5173`.

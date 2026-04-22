# RedM Command Center V3

*AI-Powered Anti-Trafficking Campaign Generator*

Auto-generated setup doc for the distribution ZIP produced by
`scripts/build_distribution.py`. This is the document a colleague receives
when they unpack `RedM_MVP_V3_Distribution.zip`.

---

## Quick start

### 1. Setup environment

```bash
cd backend
cp .env.template .env
# Edit .env and add your API keys
pip install -r requirements.txt
```

### 2. Start the server

```bash
cd backend
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Open the dashboard

- Open `design_v3.html` in your browser
- Or navigate to `http://localhost:8000`

---

## Required API keys

- **OpenAI** (GPT-4o + GPT-4o-mini) — campaign planning, writing, quality, compliance
- **Google Gemini** (gemini-3.1-flash) — image generation
- **Exa** — neural news search (optional, Google News RSS is primary)
- **LangSmith** — observability / tracing (optional)

## Documentation shipped in the ZIP

- `RedM_V3_Walkthrough.html` — full system walkthrough with architecture diagrams
- `RedM_V3_System_Walkthrough.pdf` — PDF version of the walkthrough
- `RedM_Presentation_Guide.pdf` — 5-minute presentation script
  (see [`redm-presentation-guide.md`](./redm-presentation-guide.md))

## Tech stack

- **Backend**: FastAPI + LangGraph + SQLite
- **Frontend**: Single-page HTML / CSS / JS (`design_v3.html`)
- **AI models**: GPT-4o, GPT-4o-mini, Gemini 3.1 Flash

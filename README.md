# RedM Command Center V3
## AI-Powered Anti-Trafficking Campaign Generator

### Quick Start

1. **Setup environment:**
   ```bash
   cd backend
   cp .env.template .env
   # Edit .env and add your API keys
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   cd backend
   python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Open the dashboard:**
   - Open `design_v3.html` in your browser
   - Or navigate to `http://localhost:8000`

### Required API Keys
- **OpenAI** (GPT-4o + GPT-4o-mini) — campaign planning, writing, quality, compliance
- **Google Gemini** (gemini-3.1-flash) — image generation
- **Exa** — neural news search (optional, Google News RSS is primary)
- **LangSmith** — observability/tracing (optional)

### Documentation
- `RedM_V3_Walkthrough.html` — Full system walkthrough with architecture diagrams
- `RedM_V3_System_Walkthrough.pdf` — PDF version of the walkthrough
- `RedM_Presentation_Guide.pdf` — 5-minute presentation script

### Tech Stack
- **Backend:** FastAPI + LangGraph + SQLite
- **Frontend:** Single-page HTML/CSS/JS (design_v3.html)
- **AI Models:** GPT-4o, GPT-4o-mini, Gemini 3.1 Flash

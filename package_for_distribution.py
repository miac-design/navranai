"""Package RedM MVP V3 for distribution — strips API keys and runtime artifacts."""
import zipfile
import os

PROJECT_ROOT = r"E:\Internship\Fully_functional_MVP_V3"
OUTPUT_ZIP = r"E:\Internship\RedM_MVP_V3_Distribution.zip"

# Directories/files to EXCLUDE
EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules", "outputs", ".venv", "venv"}
EXCLUDE_FILES = {".env", "redm_v3.db", "redm.db"}
EXCLUDE_EXTENSIONS = {".pyc", ".pyo", ".db-journal"}

# Utility scripts not needed by colleague
EXCLUDE_UTILITY = {
    "generate_walkthrough_pdf.py",
    "html_to_pdf.py",
    "architecture_diagram.html",
    "design_complete.html",
}

# .env template with placeholder values
ENV_TEMPLATE = """# RedM Command Center V3 — Environment Variables
# Copy this file to .env and fill in your API keys

TAVILY_API_KEY=your_tavily_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
EXA_API_KEY=your_exa_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=Agent-8-Observability
"""

def should_include(filepath, relpath):
    """Check if a file should be included in the zip."""
    basename = os.path.basename(filepath)
    _, ext = os.path.splitext(basename)

    # Check excluded files
    if basename in EXCLUDE_FILES:
        return False
    if basename in EXCLUDE_UTILITY:
        return False
    if ext in EXCLUDE_EXTENSIONS:
        return False

    # Check excluded directories
    parts = relpath.split(os.sep)
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False

    return True


def main():
    included = []
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Skip excluded directories entirely
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                filepath = os.path.join(root, f)
                relpath = os.path.relpath(filepath, PROJECT_ROOT)

                if should_include(filepath, relpath):
                    arcname = os.path.join("RedM_MVP_V3", relpath)
                    zf.write(filepath, arcname)
                    included.append(relpath)

        # Add .env.template instead of .env
        zf.writestr("RedM_MVP_V3/backend/.env.template", ENV_TEMPLATE)
        included.append("backend/.env.template (safe placeholder)")

        # Add a README for setup
        readme = """# RedM Command Center V3
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
"""
        zf.writestr("RedM_MVP_V3/README.md", readme)
        included.append("README.md (generated)")

    # Print summary
    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"ZIP created: {OUTPUT_ZIP}")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Files included: {len(included)}")
    print(f"{'='*50}")
    print(f"\nSENSITIVE FILES EXCLUDED:")
    print(f"  ✗ .env (API keys)")
    print(f"  ✗ redm_v3.db (17 MB database)")
    print(f"  ✗ outputs/ (generated images)")
    print(f"  ✗ __pycache__/")
    print(f"\nSAFE FILES ADDED:")
    print(f"  ✓ .env.template (placeholder keys)")
    print(f"  ✓ README.md (setup instructions)")
    print(f"\nAll {len(included)} files:")
    for f in sorted(included):
        print(f"  {f}")


if __name__ == "__main__":
    main()

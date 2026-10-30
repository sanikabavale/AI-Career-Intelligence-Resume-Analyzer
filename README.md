# AI Career Intelligence & Resume Analyzer

A Python-first Streamlit application for resume parsing, explainable job matching, skills-gap analysis, an interactive knowledge graph, retrieval-grounded career chat, and learning roadmaps.

## Features
- Username/password accounts stored in SQLite with PBKDF2 password hashing.
- PDF and DOCX resume parsing; image uploads and scanned PDF pages can use OCR when Tesseract is installed.
- Extensible built-in software/IT job library (job catalog is editable in `core/job_catalog.py`).
- Explainable weighted match score with category breakdown, matched/missing skills, and evidence snippets.
- Knowledge graph built from extracted resume entities and job/skill relationships.
- RAG-style retrieval over a small built-in career knowledge base and the active resume/job text.
- Optional LangChain + OpenAI chat if `OPENAI_API_KEY` is configured; offline grounded retrieval answer otherwise.
- Personalized roadmap and CSV export of job match results.
- Tests for scoring and parser utilities.

## Run on Windows PowerShell
1. Extract this ZIP.
2. Open PowerShell in the extracted `AI_Career_Intelligence_Resume_Analyzer` folder.
3. Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Optional: copy `.env.example` to `.env` and add an API key. The application also runs in offline mode without a key. Never commit `.env`.
5. Start the application:

```powershell
streamlit run app.py
```

## Optional OCR setup
Install Tesseract OCR separately and make sure `tesseract.exe` is on PATH. If it is installed elsewhere, set `TESSERACT_CMD` in `.env`. Without Tesseract, normal text PDFs and DOCX still work; scanned documents show an actionable warning.

## AI mode
- Without `OPENAI_API_KEY`: deterministic local scoring and retrieval-based responses are used. This is useful for demos and testing.
- With `OPENAI_API_KEY`: the career assistant can use LangChain's ChatOpenAI integration. API charges and provider availability depend on your account.
- The numeric match score is a heuristic compatibility indicator, not a probability of getting hired. Check the displayed evidence and requirements.

## Project layout
- `app.py`: login and navigation shell
- `pages/`: Streamlit pages
- `core/resume_parser.py`: PDF/DOCX/image text extraction
- `core/scoring.py`: explainable matching algorithm
- `core/job_catalog.py`: extensible job-role library
- `core/graph_engine.py`: knowledge graph construction and rendering
- `core/rag_engine.py`: grounded retrieval and optional LangChain chat
- `core/roadmap.py`: skill-gap roadmap generation
- `database/db.py`: user accounts and analysis history
- `tests/`: basic automated tests

## Important limitations
This is a college-project starter with real working core features, not a production hiring decision system. Validate scores against real job descriptions before using them for consequential decisions. Avoid uploading sensitive documents you do not have permission to process. For production deployment, add rate limiting, stronger session management, encrypted storage, audit logging, file retention controls, and a proper production database.

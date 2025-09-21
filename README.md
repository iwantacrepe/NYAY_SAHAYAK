Nyay Sahayak — Demystifying Complex Court Documents (README)
====================================================================

Live Demo
---------
https://nyaysahayak.streamlit.app/

Overview
--------
Nyay Sahayak (न्याय सहायक) is an agentic AI system that converts complex, jargon-filled
court documents (PDF or scanned images) into clear, plain-language explanations with
citations and actionable insights. The app is built with Streamlit (Python) and uses
Google Vertex AI in the cloud. Agents work under a Python orchestrator and communicate
using a standardized pattern (MCP-style interfaces for tool/connector access).

Key Features
------------
• Upload PDFs or scanned images of legal documents
• OCR & preprocessing for scanned files<br>
• Agentic processing (as one unit under an orchestrator)<br>
• Plain-language summaries of clauses/sections<br>
• References to statutes, acts, and relevant precedents<br>
• Unified dashboard for overview, explanations, citations, and actions<br>
• Export full analysis as PDF and JSON<br>
• Configurable via environment variables (no keys in code)<br>

High-Level Architecture
-----------------------
• Frontend: Streamlit app (file upload, language selection, interactive dashboard)
• Orchestrator (Python): Routes tasks, shares context, coordinates agents<br>
• Agents (single logical block): triage, demystify, research, strategy (internals hidden)<br>
• Google Vertex AI: LLMs and embeddings for generation and retrieval<br>
• Optional Vector Index: for improved retrieval (local/managed)<br>
• Storage: Cloud or local storage for files/chunks and generated artifacts<br>
• MCP Protocol: standard pattern for tool/connector boundaries<br>
• Output: Unified dashboard + export pack (PDF + JSON)<br>

Tech Stack
----------
• Python 3.11
• Streamlit
• Google Vertex AI (LLMs, embeddings)
• PyPDF2, python-docx, Pillow (PIL)
• OCR: pytesseract (local) or Vertex OCR (cloud)
• dotenv for environment variables
• (Optional) Vector DB/Index (FAISS, Chroma, or managed)

## ⚡ Quick Start (Local)

### 1) Prerequisites  
- Python 3.11  
- (Optional) Tesseract installed if using local OCR (pytesseract)  
- Google Cloud project with Vertex AI enabled (if calling Vertex)  

### 2) Clone  
```bash
git clone https://github.com/iwantacrepe/NYAY_SAHAYAK.git
cd nyay-sahayak
```

3) Create virtual environment
```bash
   # Using venv
   python -m venv .venv
   . .venv/bin/activate        # macOS/Linux
   .venv\Scripts\activate    # Windows
```

5) Install dependencies
```bash
    pip install -r requirements.txt
```
7) Configure environment (local .env file)
   Create a file named .env in the project root with:
```bash
    GOOGLE_PROJECT_ID=your-project-id
     GOOGLE_REGION=your-region
     GOOGLE_VERTEX_MODEL=text-bison (or other model name)
     GOOGLE_API_KEY=your-vertex-or-genai-key
     # If using service account json:
     GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service_account.json
```
9) Run
```bash
   streamlit run main.py
   (Then open http://localhost:8501 in your browser.)
```
Sample requirements.txt
-----------------------
streamlit
python-dotenv
PyPDF2
python-docx
Pillow
pytesseract
pdf2image
google-generativeai
google-cloud-aiplatform
# If you use a vector index:
faiss-cpu
# or
chromadb

Environment & Secrets
---------------------
• Local development:
  - Use a .env file (loaded via python-dotenv)
  - Or set env vars in your shell/IDE

• Streamlit Cloud deployment:
  - Place requirements.txt at the project root
  - Set secrets via Streamlit Cloud -> App -> Settings -> Secrets
    Example keys:
      GOOGLE_PROJECT_ID
      GOOGLE_REGION
      GOOGLE_VERTEX_MODEL
      GOOGLE_API_KEY
      GOOGLE_APPLICATION_CREDENTIALS (if using a service account via secrets)
  - Avoid hardcoding credentials in code or committing secrets to git

Deploying on Streamlit Cloud
----------------------------
1) Push your code to GitHub
2) Create a new Streamlit Cloud app from the repo
3) Ensure requirements.txt is present at the repo root
4) Add your secrets in the Streamlit Cloud settings
5) Deploy; if you change dependencies or secrets, reboot the app

Usage Flow
----------
1) Open the app (local or deployed)
2) Upload a PDF or scanned image
3) App runs OCR (if needed) and extracts text
4) Orchestrator routes tasks to agents (as a single logical unit)
5) Vertex AI powers summarization, explanation, and retrieval
6) Review the unified dashboard
7) Export as PDF and JSON if needed

Privacy & Security
------------------
• API keys and service accounts are stored in environment variables or Streamlit secrets
• Uploaded files are processed to generate outputs; do not retain beyond session unless explicitly saved
• Review your cloud storage and logging policies to meet compliance requirements

Roadmap
-------
• Real-time Q&A over the uploaded case
• More Indian languages (Marathi, Tamil, etc.)
• Direct integration with Supreme Court/High Court endpoints
• RAG improvements with a curated legal corpus
• Optional deployment to Cloud Run or Kubernetes for scale

License
-------
MIT License (see LICENSE file if included).

Notes
-----
• If Streamlit shows 'No module named streamlit', ensure requirements.txt is present at the
  repo root and that 'streamlit' is listed, then redeploy.
• If OCR fails on Streamlit Cloud due to missing system packages, prefer Vertex OCR or
  use a hosted OCR microservice. For local dev, install Tesseract.

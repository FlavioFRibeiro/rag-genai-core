# AI Agent for Your Files (RAG PDF Chat)

A compact, well-structured Retrieval-Augmented Generation (RAG) app to chat with multiple PDFs. It is intentionally simple, but organized like a production codebase: core logic in `src/`, app UI in `apps/`, and clear separation between ingestion, retrieval, and orchestration.

## Highlights
- Multi-PDF chat with retrieval-augmented answers
- Per-page metadata and visual page preview under each response
- Clean, minimal structure that is easy to extend or hand off to a team

## How It Works (Short)
1. PDFs are parsed page-by-page and chunked.
2. Embeddings are generated and stored in a FAISS vector store.
3. A retriever + LLM chain answers questions with source context.
4. The matching page is rendered for quick visual verification.

## Tech Stack
- `streamlit` - UI
- `python-dotenv` - environment variables
- `PyPDF2` - PDF text extraction
- `langchain` - chains and memory
- `langchain-openai` - OpenAI LLM + embeddings
- `langchain-community` - FAISS integration
- `faiss-cpu` - vector search backend
- `PyMuPDF` - PDF page rendering

## Setup
1. Create a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_key_here
```

## Run
```bash
streamlit run apps/streamlit_app.py
```

## Project Structure
- `apps/streamlit_app.py` - Streamlit UI + session state
- `apps/html_files.py` - HTML/CSS chat templates
- `src/rag_genai_core/config.py` - shared settings
- `src/rag_genai_core/ingestion.py` - PDF loading and chunking
- `src/rag_genai_core/retrieval.py` - embeddings, vector store, retriever chain
- `src/rag_genai_core/rag_pipeline.py` - pipeline orchestrator

## Design Notes
- The codebase is small by design, but modular for clean maintenance.
- Each layer has a single responsibility, which keeps changes isolated.
- New components (chunkers, vector stores, or LLMs) can be added without touching the UI.

# AI Agent for Your Files (RAG PDF Chat)

This project is a lightweight Retrieval-Augmented Generation (RAG) app that lets you chat with multiple PDFs through a Streamlit UI. The core logic lives in `src/`, and the UI lives in `apps/` for a clean, team-friendly structure.

## Features
- Upload multiple PDFs and ask questions about their content.
- Page-aware retrieval (the answer can reference the source file and page).
- Visual preview of the source PDF page under each bot response.
- Simple UI with a guided flow (upload -> process -> ask).

## Tech Stack / Libraries
- `streamlit` - web UI
- `python-dotenv` - environment variables
- `PyPDF2` - PDF text extraction
- `langchain` - conversational chain and memory
- `langchain-openai` - OpenAI LLM + embeddings
- `langchain-community` - FAISS vector store integration
- `faiss-cpu` - vector similarity search backend (required by FAISS)
- `PyMuPDF` - render PDF pages as images

## Setup
1. Create a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI key:

```env
OPENAI_API_KEY=your_key_here
```

## Run
```bash
streamlit run apps/streamlit_app.py
```

## Structure
- `apps/streamlit_app.py` - Streamlit UI and session state
- `apps/html_files.py` - HTML/CSS chat templates
- `src/rag_genai_core/config.py` - shared settings
- `src/rag_genai_core/ingestion.py` - PDF loading and chunking
- `src/rag_genai_core/retrieval.py` - embeddings, vector store, and retriever chain
- `src/rag_genai_core/rag_pipeline.py` - orchestrates the pipeline

## Notes
- `apps/streamlit_app.py` is the entry point for the Streamlit app.
- The app extracts per-page text and stores page metadata so you can identify where answers come from.
- Source pages are rendered from the original PDFs to provide visual context.

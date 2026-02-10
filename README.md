# RAG_PDFs_AI_Agent

Simple, well-organized RAG app to chat with multiple PDFs. The project is small by design, with a clear split between the UI in `apps/` and core logic in `src/`.

## Highlights
- Multi-PDF chat with retrieval-augmented answers
- Per-page metadata and visual page preview of the source
- Clean structure that is easy to extend

## How it works (short)
1. PDFs are read page-by-page and chunked.
2. Embeddings are generated and stored in FAISS.
3. A retriever + LLM answer with source context.
4. The most relevant page can be rendered for visual validation.

## Stack
- `streamlit` - UI
- `python-dotenv` - environment variables
- `PyPDF2` - text extraction
- `langchain` / `langchain-openai` - LLM and chains
- `langchain-community` - FAISS
- `faiss-cpu` - vector search
- `PyMuPDF` - page rendering

## Setup
1. (Optional) Create a virtual environment.
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

## Project structure
```text
RAG_PDFs_AI_Agent/
|-- apps/                 # Streamlit UI and HTML templates
|-- src/
|   |-- rag_genai_core/   # Core RAG logic
|   |   |-- config.py
|   |   |-- ingestion.py
|   |   |-- retrieval.py
|   |   `-- rag_pipeline.py
|-- requirements.txt
`-- README.md
```

## Quick configuration
Key parameters are in `src/rag_genai_core/config.py`:
- `LLM_MODEL` (default: `gpt-4o-mini`)
- `CHUNK_SIZE` and `CHUNK_OVERLAP`
- `PAGE_DPI` (page preview quality)

## Design notes
- Each module has a clear responsibility.
- New chunkers, vector stores, or LLMs can be swapped without touching the UI.

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_OVERLAP, CHUNK_SIZE


def get_pdf_documents(pdf_docs):
    """Extract text per page and attach source + page metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    documents = []
    empty_files = []

    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
        except Exception:
            empty_files.append(pdf.name)
            continue

        has_text = False
        for page_index, page in enumerate(pdf_reader.pages, start=1):
            page_text = page.extract_text() or ""
            if not page_text.strip():
                continue

            has_text = True
            page_docs = text_splitter.create_documents(
                [page_text],
                metadatas=[{"source": pdf.name, "page": page_index}],
            )
            documents.extend(page_docs)

        if not has_text:
            empty_files.append(pdf.name)

    return documents, empty_files

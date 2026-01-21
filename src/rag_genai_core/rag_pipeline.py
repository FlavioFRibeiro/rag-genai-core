from .ingestion import get_pdf_documents
from .retrieval import get_conversation_chain, get_vectorstore


def build_rag_pipeline(pdf_docs):
    documents, empty_files = get_pdf_documents(pdf_docs)
    if not documents:
        return None, None, empty_files

    vectorstore = get_vectorstore(documents)
    conversation_chain = get_conversation_chain(vectorstore)
    return conversation_chain, vectorstore, empty_files

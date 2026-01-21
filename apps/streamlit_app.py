import warnings
import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
import fitz

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rag_genai_core.config import PAGE_DPI
from rag_genai_core.rag_pipeline import build_rag_pipeline
from apps.html_files import css, bot_template, user_template

# Suppress noisy warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Load environment variables at startup
load_dotenv(ROOT / ".env")


def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload and process PDFs first!")
        return

    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]
    st.session_state.chat_sources.append(response.get("source_documents", []))


def render_source_preview(doc):
    source_name = doc.metadata.get("source", "Unknown")
    page_number = doc.metadata.get("page")
    if page_number:
        st.info(f"**Arquivo:** {source_name} (page {page_number})")
    else:
        st.info(f"**Arquivo:** {source_name}")

    if page_number and source_name in st.session_state.pdf_bytes:
        cache_key = (source_name, page_number)
        image_bytes = st.session_state.page_images.get(cache_key)
        if image_bytes is None:
            try:
                pdf_stream = st.session_state.pdf_bytes[source_name]
                pdf_doc = fitz.open(stream=pdf_stream, filetype="pdf")
                page = pdf_doc.load_page(page_number - 1)
                pix = page.get_pixmap(dpi=PAGE_DPI)
                image_bytes = pix.tobytes("png")
                st.session_state.page_images[cache_key] = image_bytes
            except Exception:
                image_bytes = None
            finally:
                try:
                    pdf_doc.close()
                except Exception:
                    pass
        if image_bytes:
            st.image(image_bytes, caption=f"{source_name} - page {page_number}")


def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "last_question" not in st.session_state:
        st.session_state.last_question = ""
    if "chat_sources" not in st.session_state:
        st.session_state.chat_sources = []
    if "pdf_bytes" not in st.session_state:
        st.session_state.pdf_bytes = {}
    if "page_images" not in st.session_state:
        st.session_state.page_images = {}
    if "process_status" not in st.session_state:
        st.session_state.process_status = None
    if "process_message" not in st.session_state:
        st.session_state.process_message = None
    if "process_warnings" not in st.session_state:
        st.session_state.process_warnings = []

    def handle_question():
        if st.session_state.question_input:
            handle_userinput(st.session_state.question_input)
            st.session_state.last_question = st.session_state.question_input
            st.session_state.question_input = ""

    st.header("Chat with multiple PDFs :books:")

    st.text_input(
        "Ask a question about your documents:",
        key="question_input",
        on_change=handle_question,
    )
    if st.session_state.conversation is None:
        st.info("Upload and process your PDFs to start asking questions.")

    st.markdown("---")

    if st.session_state.conversation is not None and st.session_state.chat_history:
        sources_rev = list(reversed(st.session_state.chat_sources))
        source_idx = 0
        for i, message in enumerate(reversed(st.session_state.chat_history)):
            if i % 2 == 0:
                st.write(
                    bot_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )
                if source_idx < len(sources_rev) and sources_rev[source_idx]:
                    render_source_preview(sources_rev[source_idx][0])
                source_idx += 1
            else:
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'",
            accept_multiple_files=True,
        )
        if st.button("Process"):
            if not pdf_docs:
                st.session_state.process_status = "error"
                st.session_state.process_message = "Please upload at least one PDF file!"
            elif not os.getenv("OPENAI_API_KEY"):
                st.session_state.process_status = "error"
                st.session_state.process_message = (
                    "OPENAI_API_KEY is not set. Add it to a .env file in the project root."
                )
            else:
                with st.spinner("Processing"):
                    st.session_state.pdf_bytes = {pdf.name: pdf.getvalue() for pdf in pdf_docs}
                    st.session_state.page_images = {}
                    st.session_state.chat_sources = []
                    st.session_state.chat_history = None
                    st.session_state.last_question = ""
                    st.session_state.process_warnings = []

                    conversation_chain, vectorstore, empty_files = build_rag_pipeline(pdf_docs)
                    if empty_files:
                        st.session_state.process_warnings = empty_files
                    if not conversation_chain:
                        st.session_state.process_status = "error"
                        st.session_state.process_message = (
                            "No text could be extracted from the uploaded PDFs."
                        )
                    else:
                        st.session_state.conversation = conversation_chain
                        st.session_state.vectorstore = vectorstore
                        st.session_state.process_status = "success"
                        st.session_state.process_message = (
                            "Processing complete! You can now ask questions about your documents."
                        )

        if st.session_state.process_warnings:
            st.warning("No extractable text found in: " + ", ".join(st.session_state.process_warnings))
        if st.session_state.process_status == "error" and st.session_state.process_message:
            st.error(st.session_state.process_message)
        if st.session_state.process_status == "success" and st.session_state.process_message:
            st.success(st.session_state.process_message)


if __name__ == "__main__":
    main()

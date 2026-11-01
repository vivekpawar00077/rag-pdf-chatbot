import io
import os
import streamlit as st
from load_pdf import load_pdf
from chunker import chunk_pages
from retriever import build_index, search
from generator import answer
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv(Path(__file__).parent / ".env")
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="Chat with your PDF", page_icon="📄")
st.title("📄 Chat with your PDF")
st.caption("RAG pipeline: PDF → chunks → embeddings → FAISS search → Gemini answer")

uploaded = st.file_uploader("Upload a text-based PDF", type="pdf")


@st.cache_resource(show_spinner="Reading and indexing your PDF...")
def prepare(file_bytes):
    pages = load_pdf(io.BytesIO(file_bytes))
    chunks = chunk_pages(pages)
    index = build_index(chunks)
    return chunks, index


if uploaded:
    chunks, index = prepare(uploaded.getvalue())
    st.success(f"Indexed {len(chunks)} chunks. Ask away!")

    question = st.text_input("Your question")
    if question:
        with st.spinner("Thinking..."):
            results = search(question, index, chunks, top_k=5)
            reply = answer(question, results)
        st.subheader("Answer")
        st.write(reply)
        with st.expander("Sources used"):
            for r in results:
                st.markdown(f"**Page {r['page']}** (score {r['score']:.2f})")
                st.text(r["text"])
else:
    st.info("Upload a PDF to get started.")
\# Chat with your PDF (RAG Chatbot)



Upload a text-based PDF and ask questions about it. Answers come only from the document, with the source chunks shown.



\## How it works

1\. \*\*Load\*\*: extract text from each page (pypdf)

2\. \*\*Chunk\*\*: split into 500-character pieces with 100 overlap

3\. \*\*Embed\*\*: convert chunks to vectors (sentence-transformers, all-MiniLM-L6-v2)

4\. \*\*Retrieve\*\*: find the top 5 closest chunks (FAISS)

5\. \*\*Generate\*\*: Gemini answers using only those chunks, with page numbers



\## Tech stack

Python, Streamlit, sentence-transformers, FAISS, Google Gemini API



\## Run locally

```

git clone https://github.com/vivekpawar00077/rag-pdf-chatbot.git

cd rag-pdf-chatbot

pip install -r requirements.txt

```

Create a `.env` file containing `GEMINI\_API\_KEY=your-key`, then run:

```

streamlit run app.py

```



\## Limitations and next steps

\- Does not work on scanned PDFs (needs OCR)

\- Fixed-size chunking can cut sentences; sentence-based splitting would be better

\- Semantic search is weak on exact details like emails; hybrid search (keyword + embeddings) would help

\- API calls retry with exponential backoff when the service is overloaded


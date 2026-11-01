import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index(chunks):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype="float32")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index


def search(query, index, chunks, top_k=3):
    q = model.encode([query], normalize_embeddings=True)
    q = np.array(q, dtype="float32")
    scores, ids = index.search(q, top_k)
    results = []
    for score, i in zip(scores[0], ids[0]):
        results.append(
            {"score": float(score), "page": chunks[i]["page"], "text": chunks[i]["text"]}
        )
    return results


if __name__ == "__main__":
    from load_pdf import load_pdf
    from chunker import chunk_pages

    pages = load_pdf("sample.pdf")
    chunks = chunk_pages(pages)
    index = build_index(chunks)
    print("Index ready. Type a question (or 'exit' to quit).")

    while True:
        question = input("\nQuestion: ")
        if question.strip().lower() == "exit":
            break
        for r in search(question, index, chunks):
            print(f"\n[score {r['score']:.2f} | page {r['page']}]")
            print(r["text"])
def chunk_pages(pages, chunk_size=500, overlap=100):
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            piece = text[start:end].strip()
            if piece:
                chunks.append({"page": page["page"], "text": piece})
            start += chunk_size - overlap
    return chunks


if __name__ == "__main__":
    from load_pdf import load_pdf

    pages = load_pdf("sample.pdf")
    chunks = chunk_pages(pages)
    print(f"Total chunks: {len(chunks)}")
    print("---- Chunk 1 ----")
    print(chunks[0]["text"])
    print("---- Chunk 2 ----")
    print(chunks[1]["text"])
from pypdf import PdfReader


def load_pdf(path):
    reader = PdfReader(path)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"page": page_number, "text": text})
    return pages


if __name__ == "__main__":
    pages = load_pdf("sample.pdf")
    print(f"Total pages: {len(pages)}")
    print("---- First 500 characters of page 1 ----")
    print(pages[0]["text"][:500])
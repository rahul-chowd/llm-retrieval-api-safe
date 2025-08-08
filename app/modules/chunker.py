import re
from typing import List

def chunk_text(text: str, max_words: int = 300, overlap: int = 50) -> List[str]:
    # Split full text into words
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + max_words
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += (max_words - overlap)  # overlap helps preserve context

    return chunks

# --- TESTING ---

if __name__ == "__main__":
    from extractor import extract_text_from_pdf
    sample_path = "temp_docs/39146a06505b48a4928ab7a447f7020c.pdf"
    text = extract_text_from_pdf(sample_path)
    chunks = chunk_text(text, max_words=300, overlap=50)

    print(f"✅ Total chunks: {len(chunks)}")
    print(f"\n🧩 Preview of first chunk:\n\n{chunks[0]}")

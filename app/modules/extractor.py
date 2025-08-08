import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        full_text = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")  # plain text
            full_text.append(text.strip())

        return "\n\n".join(full_text)

    except Exception as e:
        print(f"❌ Error extracting PDF text: {e}")
        raise

# --- TESTING ---

if __name__ == "__main__":
    sample_path = "temp_docs/39146a06505b48a4928ab7a447f7020c.pdf"  # Replace with your file if different
    text = extract_text_from_pdf(sample_path)
    print("✅ Extracted text (first 500 characters):\n")
    print(text[:500])  # Just preview first few lines

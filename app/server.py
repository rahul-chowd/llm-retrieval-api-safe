from flask import Flask, request, jsonify
from app.modules.extractor import extract_text_from_pdf
from app.modules.chunker import chunk_text
from app.modules.embeddings import embed_and_store, query_similar_chunks
from app.modules.answer_generator import generate_answer
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/api/v1/hackrx/run", methods=["POST"])
def run_submission():
    try:
        data = request.get_json()

        pdf_url = data.get("documents")
        questions = data.get("questions", [])

        if not pdf_url or not questions:
            return jsonify({"error": "Missing 'documents' or 'questions' field"}), 400

        # Step 1: Download the PDF to temp_docs
        os.makedirs("temp_docs", exist_ok=True)
        local_pdf_path = "temp_docs/temp.pdf"
        response = requests.get(pdf_url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to download PDF"}), 400

        with open(local_pdf_path, "wb") as f:
            f.write(response.content)

        # Step 2: Extract and chunk text
        text = extract_text_from_pdf(local_pdf_path)
        chunks = chunk_text(text)

        # Step 3: Embed and store chunks
        embed_and_store(chunks)

        # Step 4: Generate answers
        answers = []
        for question in questions:
            hits = query_similar_chunks(question)
            chunk_ids = [hit[0] for hit in hits]
            retrieved_chunks = [chunk for i, chunk in enumerate(chunks) if f"chunk-{i}" in chunk_ids]
            answer = generate_answer(retrieved_chunks, question)
            answers.append(answer)

        return jsonify({"answers": answers}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000)

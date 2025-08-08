from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from app.modules.answer_generator import generate_answer
load_dotenv()

from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import os

import requests  # <-- add this near the top

def send_to_webhook(answer: str, question: str, webhook_url: str):
    payload = {
        "question": question,
        "answer": answer
    }
    try:
        response = requests.post(webhook_url, json=payload)
        print("✅ Webhook sent. Status code:", response.status_code)
    except Exception as e:
        print("❌ Error sending to webhook:", e)


# 1. Load the embedding model
model = SentenceTransformer("all-mpnet-base-v2")


# 2. Initialize Pinecone client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

index_name = "insurance-index"

# 3. Create index if it doesn’t exist, in GCP us-central1 (free tier)
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"      # ← changed from us-west1 to us-central1
        )
    )

index = pc.Index(index_name)

# 4. Embed & upload chunks
def embed_and_store(chunks: List[str]) -> List[str]:
    vectors = model.encode(chunks).tolist()
    ids     = [f"chunk-{i}" for i in range(len(chunks))]
    index.upsert(vectors=zip(ids, vectors))
    return ids
print("Total vectors in index:", index.describe_index_stats()["total_vector_count"])


# 5. Query similar chunks
def query_similar_chunks(question: str, top_k: int = 5) -> List[Tuple[str, float]]:
    qv = model.encode([question])[0].tolist()
    res = index.query(vector=qv, top_k=top_k, include_metadata=False)
    return [(m["id"], m["score"]) for m in res["matches"]]

if __name__ == "__main__":
    from chunker import chunk_text
    from extractor import extract_text_from_pdf

    pdf_path = "temp_docs/39146a06505b48a4928ab7a447f7020c.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    print(f"Uploading {len(chunks)} chunks…")
    ids = embed_and_store(chunks)

    hits = query_similar_chunks("What is the grace period for premium payment?")
    print("Top hits:", hits)

    chunk_ids = [hit[0] for hit in hits]
    retrieved_chunks = [chunk for id_, chunk in zip(ids, chunks) if id_ in chunk_ids]

    answer = generate_answer(retrieved_chunks, "What is the grace period for premium payment?")
    print("Final Answer:\n", answer)
    
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
       send_to_webhook(answer, "What is the grace period for premium payment?", webhook_url)
    else:
       print("⚠️ WEBHOOK_URL not set in .env file, skipping webhook.")








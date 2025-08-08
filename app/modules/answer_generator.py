import os
import openai
from dotenv import load_dotenv

load_dotenv()

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o")  # fallback to gpt-4o if not set

def generate_answer(chunks, question):
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.
    
    Context:
    {context}

    Question:
    {question}

    Answer:"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response["choices"][0]["message"]["content"]

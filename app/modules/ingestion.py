import os
import requests
from uuid import uuid4
from pathlib import Path

# Create temp folder if it doesn't exist
TEMP_DIR = Path("temp_docs")
TEMP_DIR.mkdir(exist_ok=True)

def fetch_document(url: str) -> str:
    try:
        # Get file extension from URL (basic method)
        ext = url.split(".")[-1].split("?")[0]
        filename = f"{uuid4().hex}.{ext}"
        filepath = TEMP_DIR / filename

        # Download file
        response = requests.get(url)
        response.raise_for_status()  # raises error if not 200

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✅ Downloaded to: {filepath}")
        return str(filepath)

    except Exception as e:
        print(f"❌ Failed to fetch document: {e}")
        raise

# --- TESTING ---

if __name__ == "__main__":
    test_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    path = fetch_document(test_url)
    print(f"Document saved at: {path}")

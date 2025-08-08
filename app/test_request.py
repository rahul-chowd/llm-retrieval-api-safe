import requests

url = "http://localhost:8000/api/v1/hackrx/run"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 52270cf7813e09f935c6ec5fb06e9607b4f3aace553501f05ffc4acfa840a654"
}

data = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
}

response = requests.post(url, headers=headers, json=data)

print("Status code:", response.status_code)
print("Response JSON:", response.json())

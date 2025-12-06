import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    json={
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Hello from Groq!"}],
    },
    headers={"Authorization": f"Bearer {api_key}"},
)
print(response.json())

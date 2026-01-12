import os
import time
import requests

ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]

def chunk_text(text, max_chars):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + max_chars
        chunks.append(text[start:end])
        start = end

    return chunks

def summarize_chunk(text):
    url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a professional summarization engine."
            },
            {
                "role": "user",
                "content": f"Summarize the given text: \n\n{text}"
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
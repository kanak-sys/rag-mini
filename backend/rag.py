import os
import requests
from dotenv import load_dotenv
from db import insert_doc, search_docs

load_dotenv()

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
VOYAGE_URL = "https://api.voyageai.com/v1/embeddings"

def chunk_text(text, size=800, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def embed_text(text):
    headers = {
        "Authorization": f"Bearer {VOYAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "voyage-2",
        "input": text
    }
    res = requests.post(VOYAGE_URL, headers=headers, json=payload)
    res.raise_for_status()
    return res.json()["data"][0]["embedding"]

def ingest_text(text):
    chunks = chunk_text(text)
    for c in chunks:
        emb = embed_text(c)
        insert_doc(c, emb)

def query_rag(question):
    q_emb = embed_text(question)
    docs = search_docs(q_emb, k=3)

    if not docs:
        return {
            "answer": "I couldn't find relevant information in the provided documents.",
            "sources": []
        }

    context = ""
    for i, d in enumerate(docs):
        context += f"[{i+1}] {d['content']}\n\n"
    # print("CONTEXT SENT TO LLM:\n", context)


    return {
        "context": context,
        "sources": docs
    }


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def answer_with_llm(question, context):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer only using the provided context. Cite sources like [1], [2]. If the answer is not in the context, say you don't know."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    }

    res = requests.post(GROQ_URL, headers=headers, json=payload)
    # print("GROQ STATUS:", res.status_code, res.text)  # debug
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

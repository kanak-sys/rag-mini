from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag import ingest_text, query_rag, answer_with_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "backend running"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    ingest_text(req.text)
    return {"status": "ingested"}

@app.post("/query")
def query(req: QueryRequest):
    res = query_rag(req.question)
    if not res["sources"]:
        return res
    answer = answer_with_llm(req.question, res["context"])
    return {
        "answer": answer,
        "sources": res["sources"]
    }

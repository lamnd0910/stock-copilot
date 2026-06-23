from fastapi import FastAPI
from pydantic import BaseModel
from app.retriever import Retriever
from app.generate import answer

app = FastAPI()
retriever = Retriever()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Query):
    hits = retriever.search(q.question)
    return {"answer": answer(q.question, hits),
            "sources": [d["id"] for d, _ in hits]}
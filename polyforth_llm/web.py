from __future__ import annotations

import os
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from polyforth_llm.config import load_settings
from polyforth_llm.llm import LLMClient
from polyforth_llm.retriever import RetrievedChunk, Retriever


class TeachRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class TeachResponse(BaseModel):
    answer: str
    citations: list[str]


app = FastAPI(title="polyforth-llm API", version="0.1.0")
settings = load_settings()
retriever = Retriever(settings)
llm = LLMClient(settings)
api_key = os.getenv("APP_API_KEY", "").strip()


def _auth(x_api_key: str | None = Header(default=None)) -> None:
    if not api_key:
        return
    if x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")


def _build_prompt(question: str, contexts: list[RetrievedChunk]) -> str:
    block = "\n\n".join([f"[{c.source}] ({c.heading}) {c.text}" for c in contexts])
    return (
        "Answer the question using the context below.\n"
        "Rules:\n"
        "1) Prefer context facts over prior knowledge.\n"
        "2) If context is insufficient, explicitly say what is missing.\n"
        "3) Cite supporting statements with [source] tags exactly as shown.\n\n"
        f"Context:\n{block}\n\n"
        f"Question:\n{question}\n"
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/teach", response_model=TeachResponse, dependencies=[Depends(_auth)])
def teach(payload: TeachRequest) -> TeachResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")
    chunks = retriever.search(question, top_k=payload.top_k)
    prompt = _build_prompt(question, chunks)
    answer = llm.complete(prompt)
    citations = sorted({c.source for c in chunks})
    return TeachResponse(answer=answer, citations=citations)

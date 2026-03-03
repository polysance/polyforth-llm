from __future__ import annotations

import json
from dataclasses import dataclass

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from polyforth_llm.config import Settings


@dataclass
class RetrievedChunk:
    page: int
    text: str
    score: float


class Retriever:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.index = faiss.read_index(str(settings.index_dir / "knowledge.faiss"))
        with open(settings.index_dir / "chunks.json", "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        self.embed_model = SentenceTransformer(settings.embedding_model)

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        k = top_k or self.settings.top_k
        q = self.embed_model.encode([query], convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, k)

        out: list[RetrievedChunk] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = self.chunks[idx]
            out.append(
                RetrievedChunk(page=int(chunk["page"]), text=str(chunk["text"]), score=float(score))
            )
        return out

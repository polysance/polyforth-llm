from __future__ import annotations

import json
from pathlib import Path
from typing import List

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from polyforth_llm.config import load_settings


def _extract_pdf_text(pdf_path: Path) -> List[dict]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append({"page": idx, "text": text})
    return pages


def _chunk_text(pages: List[dict], chunk_size: int, overlap: int) -> List[dict]:
    chunks = []
    for page_item in pages:
        page = page_item["page"]
        text = page_item["text"]
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append({"page": page, "text": chunk})
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
    return chunks


def build_index() -> None:
    settings = load_settings()
    if not settings.pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at {settings.pdf_path}")

    settings.index_dir.mkdir(parents=True, exist_ok=True)

    pages = _extract_pdf_text(settings.pdf_path)
    if not pages:
        raise ValueError("No extractable text found in PDF.")

    chunks = _chunk_text(pages, settings.chunk_size, settings.chunk_overlap)
    texts = [c["text"] for c in chunks]

    model = SentenceTransformer(settings.embedding_model)
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    embeddings = embeddings.astype(np.float32)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    faiss.write_index(index, str(settings.index_dir / "knowledge.faiss"))
    with open(settings.index_dir / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=True, indent=2)

    print(f"Indexed {len(chunks)} chunks from {len(pages)} pages.")
    print(f"Saved index to: {settings.index_dir}")

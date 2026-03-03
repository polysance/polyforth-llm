from __future__ import annotations

import json
from pathlib import Path
from typing import List

import faiss
import numpy as np
from docx import Document
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from polyforth_llm.config import load_settings


def _chunk_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def _extract_pdf_sections(pdf_path: Path) -> List[dict]:
    reader = PdfReader(str(pdf_path))
    sections: List[dict] = []
    for idx, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            sections.append({"source": f"p{idx}", "heading": f"Page {idx}", "text": text})
    return sections


def _extract_docx_sections(docx_path: Path) -> List[dict]:
    doc = Document(str(docx_path))
    sections: List[dict] = []
    current_heading = "Document"
    current_lines: list[str] = []

    def flush() -> None:
        if current_lines:
            text = "\n".join(current_lines).strip()
            if text:
                sections.append(
                    {
                        "source": f"section:{current_heading}",
                        "heading": current_heading,
                        "text": text,
                    }
                )

    for p in doc.paragraphs:
        text = (p.text or "").strip()
        if not text:
            continue

        style_name = (p.style.name if p.style is not None else "") or ""
        if style_name.startswith("Heading"):
            flush()
            current_heading = text
            current_lines = []
            continue

        current_lines.append(text)

    flush()
    return sections


def _extract_sections(source_path: Path) -> List[dict]:
    suffix = source_path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf_sections(source_path)
    if suffix == ".docx":
        return _extract_docx_sections(source_path)
    raise ValueError(f"Unsupported source type: {suffix}. Use .pdf or .docx")


def _chunk_sections(sections: List[dict], chunk_size: int, overlap: int) -> List[dict]:
    chunks: List[dict] = []
    for section in sections:
        for chunk_text in _chunk_with_overlap(section["text"], chunk_size, overlap):
            chunks.append(
                {
                    "source": section["source"],
                    "heading": section["heading"],
                    "text": chunk_text,
                }
            )
    return chunks


def build_index() -> None:
    settings = load_settings()
    if not settings.source_path.exists():
        raise FileNotFoundError(f"Source file not found at {settings.source_path}")

    settings.index_dir.mkdir(parents=True, exist_ok=True)

    sections = _extract_sections(settings.source_path)
    if not sections:
        raise ValueError("No extractable text found in source document.")

    chunks = _chunk_sections(sections, settings.chunk_size, settings.chunk_overlap)
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

    print(f"Indexed {len(chunks)} chunks from {len(sections)} sections.")
    print(f"Saved index to: {settings.index_dir}")

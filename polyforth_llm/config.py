from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    source_path: Path
    index_dir: Path
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    top_k: int
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    system_prompt: str


def load_settings() -> Settings:
    load_dotenv()

    return Settings(
        source_path=Path(os.getenv("SOURCE_PATH", os.getenv("PDF_PATH", "data/polyForth-llm.docx"))),
        index_dir=Path(os.getenv("INDEX_DIR", "index")),
        chunk_size=int(os.getenv("CHUNK_SIZE", "1200")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "150")),
        embedding_model=os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        ),
        top_k=int(os.getenv("TOP_K", "5")),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        system_prompt=os.getenv(
            "SYSTEM_PROMPT",
            (
                "You are a precise programming language tutor and coding assistant. "
                "Use retrieved context where possible and cite sources as [src]."
            ),
        ),
    )

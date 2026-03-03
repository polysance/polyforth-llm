# polyforth-llm

A minimal RAG assistant for polyForth (or any language) backed by a single `.pdf` or `.docx` knowledge source.

## What this repo now does

1. Extracts text from a PDF or DOCX.
2. Chunks and embeds the text.
3. Builds a local FAISS index.
4. Runs a chat CLI that retrieves relevant chunks and asks an LLM to answer with citations.

## Quick start

### 1) Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2) Add your source document

Default is `data/polyforth-llm.docx` (set `SOURCE_PATH` in `.env` if different).

### 3) Build the index

```bash
python scripts/build_index.py
```

### 4) Chat

```bash
python scripts/chat.py
```

Type `exit` to quit.

## Model configuration

By default the app uses an OpenAI-compatible API client. Configure in `.env`:

- `LLM_BASE_URL`: API endpoint (OpenAI or local gateway like Ollama-compatible).
- `LLM_API_KEY`: API key/token.
- `LLM_MODEL`: model ID (recommended: a code-capable instruct model).

## Notes

- Starting with one source document is fine for Q&A.
- For stronger code generation/debugging, add examples, tests, and compiler/tool feedback over time.
- DOCX with headings/TOC is preferred because section-aware chunking improves retrieval relevance.

# Retrieval-Augmented Generation system for polyForth using local FAISS retrieval + local Ollama inference

A minimal RAG assistant for polyForth (or any language) backed by a single `.pdf` or `.docx` knowledge source.

* Implementation checklist: see [implementation-agent](IMPLEMENTATION.md).
* Teaching mode docs: [teaching](TEACHING_README.md) and [implementation-teaching](TEACHING_IMPLEMENTATION.md).
* Project roadmap: [roadmap](docs/ROADMAP.md).
* Teaching benchmark: [benchmark-v1](evaluation/teaching-benchmark.md).
* Env presets: [profiles](profiles/README.md).
* RAG literature hub: [literature](literature/README.md).
* Local-first build path: [local-first](docs/LOCAL_FIRST_BUILD.md).
* Posterior build notes: [build-notes](docs/POSTERIOR_BUILD_NOTES.md).
* Current strategy and forward execution order: see top of [implementation-agent](IMPLEMENTATION.md).
* Public testing deploy guide: [cloudflare-tunnel](DEPLOYMENT_CLOUDFLARE.md).

## Why RAG Matters

Retrieval-Augmented Generation (RAG) separates knowledge access from answer generation: first retrieve evidence, then generate. This makes systems more auditable, since answers can cite source chunks rather than relying only on opaque model memory. For teaching workloads, this improves trust, exposes missing-context cases, and gives a concrete way to evaluate hallucination risk. A local-first RAG stack also turns AI from a black box into an inspectable pipeline where chunking, retrieval ranking, prompts, and model choice can each be measured and tuned. The literature hub in this repo maps these ideas from theory to operations and pedagogy:

- `literature/README.md`

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

### 1.5) Slow internet/offline prep (recommended)

Run once while online to cache embeddings model locally:

```bash
python scripts/download_embedding_model.py
```

### 2) Add your source document

Default is `data/polyForth-llm.docx` (set `SOURCE_PATH` in `.env` if different).

### 3) Build the index

```bash
python scripts/build_index.py
```

### 4) Chat

```bash
python scripts/chat.py
```

Type `exit` to quit.

### 5) API (for web testing)

```bash
python scripts/serve_api.py
```

Endpoints:

- `GET /health`
- `POST /teach` (optional `X-API-Key` if `APP_API_KEY` is set)

## Model configuration

By default the app uses an OpenAI-compatible API client. Configure in `.env`:

- `LLM_BASE_URL`: API endpoint (OpenAI or local gateway like Ollama-compatible).
- `LLM_API_KEY`: API key/token.
- `LLM_MODEL`: model ID (recommended: a code-capable instruct model).

## Notes

- Starting with one source document is fine for Q&A.
- For stronger code generation/debugging, add examples, tests, and compiler/tool feedback over time.
- DOCX with headings/TOC is preferred because section-aware chunking improves retrieval relevance.
- Default embedding model path is local: `models/all-MiniLM-L6-v2`.

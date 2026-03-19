# polyforth-llm

A minimal RAG assistant for polyForth (or any language) backed by a single `.pdf` or `.docx` knowledge source.

* Implementation checklist: see [implementation-agent](IMPLEMENTATION.md).
* Teaching mode docs: [teaching](TEACHING_README.md) and [implementation-teaching](TEACHING_IMPLEMENTATION.md).
* Project roadmap: [roadmap](docs/ROADMAP.md).
* Teaching benchmark: [benchmark-v1](evaluation/teaching-benchmark.md).
* Env presets: [profiles](profiles/README.md).
* Current strategy and forward execution order: see top of [implementation-agent](IMPLEMENTATION.md).
* Public testing deploy guide: [cloudflare-tunnel](DEPLOYMENT_CLOUDFLARE.md).

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

## Host computer specs

* AMD Ryzen 9 5950X Processor
* ASUS Prime A520M-K Motherboard Socket AM4
* Corsair Vengeance LPX 64GB (2x32GB) DDR4 3200MHz C16
* Intenso Internal M.2 SSD SATA III Top, 512 GB, 520 MB/s
* Debian Linux with KDE Plasma desktop
* XFX Speedster SWFT105 Radeon RX 6400 Gaming Graphics Card with 4GB GDDR6, AMD RDNA™ 2 (RX-64XL4SFG2)
* Corsair 4000D Airflow Tempered Glass Mid-Tower ATX Case
* be quiet! Pure Power 12 850W Power Supply, 80 Plus® Gold Efficiency, ATX 3.1 with Full Support for PCIe 5.1 GPUs
* Corsair 240mm AIO Liquid CPU Cooler (AM4 compatible)

## Local model profile

### Recommendation for current setup (RX 6400 4GB)

Use this architecture now:

1. Keep retrieval local (current FAISS + sentence-transformers setup).
2. Use hosted LLM API for generation by default.
3. If fully local, prefer very small quantized models due to 4GB VRAM.
4. Prefer moderate context windows for speed/latency.

Suggested starting model class:

- Hosted: code-capable instruct model via API.
- Local fallback: compact quantized code model where memory allows.

Not recommended on current setup:

- 30B-class local code models for interactive usage.
- Expecting the 4GB GPU to run mid/large LLMs effectively.

### Upgrade path

1. Storage first: move to 1TB to 2TB NVMe (model files and cache grow quickly).
2. Then GPU: 24GB VRAM minimum for practical local coding assistants, 48GB+ preferred for larger models and longer contexts.

### Practical deployment split

- Best quality now: local RAG + hosted LLM API.
- Best fully-local now: local RAG + quantized 7B to 16B model.

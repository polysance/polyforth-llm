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

## Host computer specs

* AMD Ryzen 9 5950X Processor
* ASUS Prime A520M-K Motherboard Socket AM4
* Corsair Vengeance LPX 64GB (2x32GB) DDR4 3200MHz C16
* Intenso Internal M.2 SSD SATA III Top, 512 GB, 520 MB/s

## Local model profile

### Recommendation for current setup (no discrete GPU listed)

Use this architecture now:

1. Keep retrieval local (current FAISS + sentence-transformers setup).
2. Use a smaller local instruct/code model (quantized 7B to 16B class) for generation.
3. Prefer moderate context windows for speed/latency.

Suggested starting model class:

- DeepSeek-Coder-V2-Lite (quantized) or a comparable 7B to 14B code-instruct model.

Not recommended on current setup:

- 30B-class code models for interactive usage, because CPU-only latency will usually be too high.

### Upgrade path

1. Storage first: move to 1TB to 2TB NVMe (model files and cache grow quickly).
2. Then GPU: 24GB VRAM minimum for practical local coding assistants, 48GB+ preferred for larger models and longer contexts.

### Practical deployment split

- Best quality now: local RAG + hosted LLM API.
- Best fully-local now: local RAG + quantized 7B to 16B model.

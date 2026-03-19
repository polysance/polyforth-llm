# Local-First Build Guide (Round 1)

This guide documents what we are starting with, what was done in the first build run, and the local-first path for the next phase.

## Goal

Build a polyForth tutor that is:

1. Source-grounded on `data/polyForth-llm.docx`.
2. Operational locally first (ingestion/retrieval always local, generation local where possible).
3. Easy to evaluate for complexity and next-step decisions.

## Starting point

Project architecture in this repo:

1. Ingest source document (`.docx` or `.pdf`).
2. Chunk text.
3. Create embeddings.
4. Build FAISS index.
5. Retrieve top-k chunks per question.
6. Send retrieval context to an OpenAI-compatible chat endpoint.

Important distinction:

1. We are not training a new base LLM here.
2. We are building a RAG tutor pipeline around an existing model interface.

## Current baseline (2026-03-19)

Completed and verified:

1. Python environment bootstrapped (`.venv`).
2. Dependencies installed (with `faiss-cpu` updated to `1.13.2` for Python 3.13).
3. Embedding model cached locally at `models/all-MiniLM-L6-v2`.
4. Index built from `data/polyForth-llm.docx`.
5. Artifacts present:
   - `index/knowledge.faiss`
   - `index/chunks.json`
6. Retrieval smoke test returns relevant hits.

Reference log:

- `evaluation/build-results-2026-03-19.md`

## What is local already

These are fully local now:

1. Document storage.
2. Chunking.
3. Embedding generation.
4. FAISS index build.
5. Retrieval at query time.

## What still depends on model backend

Answer generation currently expects an OpenAI-compatible API (`LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`).

This can be:

1. Hosted provider endpoint (requires external API key).
2. Local model server endpoint (no external key required if server is local and open).

## Local-first round 1 workflow

### A) Keep retrieval/index local (already done)

```bash
. .venv/bin/activate
python scripts/build_index.py
```

### B) Run generation locally via OpenAI-compatible local server

Set `.env` values to local endpoint, for example:

```env
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_API_KEY=local
LLM_MODEL=<your-local-model-name>
```

Notes:

1. The server must expose OpenAI-compatible `/v1/chat/completions`.
2. Keep model size modest on current hardware.

### C) Run teaching/chat loops

```bash
. .venv/bin/activate
python scripts/teaching_chat.py
```

or

```bash
. .venv/bin/activate
python scripts/chat.py
```

### D) Benchmark and record

Use:

- `evaluation/teaching-benchmark.md`

Store results as:

- `evaluation/results-YYYY-MM-DD.md`

## Complexity checkpoints (what to learn in round 1)

Measure these before scaling:

1. Local model startup and memory fit.
2. Median response latency in `explain`, `socratic`, and `quiz`.
3. Citation quality and hallucination behavior.
4. Retrieval quality for key topics (`stack`, `control flow`, `memory`, `DUP`, etc.).
5. Stability over longer sessions.

## Decision gates for round 2

After one full benchmark cycle, choose next path:

1. Tune retrieval/chunking first if citations are weak.
2. Tune prompts first if clarity is weak but citations are present.
3. Upgrade local model size only if latency and memory are acceptable.
4. Consider hosted fallback only if local quality is below your teaching target.

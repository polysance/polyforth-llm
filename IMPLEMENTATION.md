# polyforth-llm Implementation Guide

This guide defines the next steps after your host computer is ready.

## Target OS

- Debian Linux
- KDE Plasma desktop

## Debian prerequisites

Install base packages first:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential git
```

Optional but useful on KDE desktop:

```bash
sudo apt install -y libopenblas-dev
```

## Slow internet strategy (recommended)

Do one online setup pass, then operate mostly offline.

1. Install Python dependencies once.
2. Download embedding model once to local disk.
3. Build FAISS index locally.
4. Keep reusing local model and index.

One-time download command:

```bash
python scripts/download_embedding_model.py
```

This stores the embedding model in:

- `models/all-MiniLM-L6-v2`

## Goal

Build a reliable polyForth assistant that:

1. Answers language questions from your document source.
2. Generates code with citations to source sections.
3. Improves over time with real usage feedback.

## Phase 1: Base environment

1. Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Configure environment:

```bash
cp .env.example .env
```

4. Confirm `SOURCE_PATH` points to your file:

```env
SOURCE_PATH=data/polyforth-llm.docx
```

5. Confirm embedding model uses local path:

```env
EMBEDDING_MODEL=models/all-MiniLM-L6-v2
```

## Phase 2: Build and validate index

1. Build index:

```bash
python scripts/build_index.py
```

2. Verify artifacts exist:

- `index/knowledge.faiss`
- `index/chunks.json`

3. Quick quality check:

- Open `index/chunks.json`
- Confirm chunk records include:
  - `source`
  - `heading`
  - `text`

If headings look wrong, improve styles in DOCX (`Heading 1/2/3`) and rebuild.

## Phase 3: Wire model backend

Choose one mode:

1. Hosted API (recommended first)
2. Local model server

Set these in `.env`:

```env
LLM_BASE_URL=...
LLM_API_KEY=...
LLM_MODEL=...
```

Notes:

- For current CPU-only setup, prefer smaller quantized models for local deployment.
- For best quality now, use hosted code-capable instruct model.

## Phase 4: First acceptance test

Run chat:

```bash
python scripts/chat.py
```

Test with 10 representative questions:

1. Syntax rules
2. Stack behavior
3. Control flow words
4. Memory/model specifics
5. Common errors and fixes
6. Equivalent idioms
7. Code example requests
8. Debugging prompts
9. “Where is this defined?” questions
10. Ambiguous questions (should ask for clarification or say missing)

Pass criteria:

- Answers include source tags like `[section:...]` or `[pX]`.
- No fabricated facts when context is missing.
- Code examples are consistent with source terminology.

## Phase 5: Tune retrieval

Tune `.env` values iteratively:

- `CHUNK_SIZE` (start: 1200)
- `CHUNK_OVERLAP` (start: 150)
- `TOP_K` (start: 5)

Recommended loop:

1. Run the same 10-question set.
2. Track wrong/missing answers.
3. Adjust one variable at a time.
4. Rebuild index.
5. Re-test.

## Phase 6: Add debug/code reliability

After baseline Q&A works:

1. Add a “code task mode” prompt template:
   - Request step-by-step reasoning in private.
   - Output only final answer + cited references.
2. Add optional tool loop:
   - Save generated code snippet.
   - Run local checker/interpreter/compiler if available.
   - Return compile/runtime feedback to model for repair.

This is the main step that improves generation/debug quality.

## Phase 7: Operational checklist

Before regular usage:

1. Version your source file (keep original plus date/version metadata).
2. Snapshot `.env` used for each run.
3. Track failed questions in `evaluation/failures.md`.
4. Re-index whenever source content changes.

## Phase 8: Hardware upgrade trigger points

Upgrade when you see:

1. High latency on long answers.
2. Frequent context truncation.
3. Need for larger local model quality.

Priority:

1. SSD to 1TB to 2TB NVMe.
2. Add 24GB+ VRAM GPU (48GB+ preferred for larger local models).

## Immediate next commands

Run these in order:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/build_index.py
python scripts/chat.py
```

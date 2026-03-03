# polyforth-llm Implementation Guide

This guide defines the next steps after your host computer is ready.

## Hardware guidance first

Current host configuration:

- AMD Ryzen 9 5950X
- 64GB DDR4 RAM
- 512GB SSD
- Debian Linux + KDE Plasma
- Radeon RX 6400 (4GB VRAM)

Advice for current configuration:

1. This is good for local ingestion, embeddings, FAISS indexing, and retrieval.
2. Use hosted LLM API for best answer quality and speed today.
3. The RX 6400 helps desktop responsiveness but 4GB VRAM is below practical local LLM GPU targets.
4. If fully local, use compact quantized models and expect higher latency than hosted/API inference.
5. Avoid 30B-class local models for interactive use.

Recommended hardware profile:

1. CPU: modern 12+ core processor.
2. RAM: 64GB minimum (128GB preferred if running larger local models).
3. Storage: 1TB to 2TB NVMe SSD.
4. GPU: 24GB VRAM minimum for practical local coding assistants.
5. GPU preferred target: 48GB+ VRAM for larger models and longer context windows.

Current vs recommended correlation:

| Component | Current | Recommended | Status | Impact |
|---|---|---|---|---|
| CPU | Ryzen 9 5950X (16 cores) | Modern 12+ cores | Meets/Exceeds | Strong for ingestion, embeddings, retrieval, and orchestration. |
| RAM | 64GB DDR4 | 64GB min (128GB preferred) | Meets minimum | Good baseline; 128GB helps larger local models and bigger contexts. |
| Storage | 512GB SSD | 1TB to 2TB NVMe | Gap | Main bottleneck for local model files, caches, and future growth. |
| GPU | Radeon RX 6400 (4GB) | 24GB min, 48GB+ preferred | Gap | Discrete GPU present, but VRAM is far below practical local coding-model targets. |

Practical conclusion:

1. You are ready now for local RAG and hosted LLM generation.
2. For fully local coding assistant quality, prioritize storage upgrade first, then add GPU.

Incremental improvements (in priority order):

1. Increase storage to 1TB to 2TB NVMe for model files/cache/indexes.
2. Add discrete GPU with at least 24GB VRAM (48GB+ preferred for larger models).
3. After GPU upgrade, evaluate larger code models and longer context settings.

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

## Hardware bring-up checklist (before full software rollout)

1. Cooler mechanical check:
   - Heatsink firmly mounted to AM4 bracket/backplate.
   - Fan clips fully seated in both fan corner grooves and heatsink fin notches.
   - Fan cannot shift or detach with light hand pressure.
2. Thermal paste check:
   - Fresh paste, even pressure, no visible pump-out at edges.
3. BIOS check:
   - CPU fan detected.
   - PWM fan curve enabled.
4. Debian sensor/stress check:

```bash
sudo apt update
sudo apt install -y lm-sensors stress-ng
sensors
stress-ng --cpu 16 --timeout 120s
sensors
```

Pass/fail targets for Ryzen 9 5950X with air cooling:

1. Idle (after a few minutes): typically around 40C to 60C depending on room temp.
2. Short all-core stress: should ramp but remain stable without thermal shutdown.
3. No fan detachment, scraping, or abnormal vibration noise under load.

If the fan mount is unstable, stop and fix mechanics before running indexing/model workloads.

## Custom clip guidance (DIY)

Recommendation:

1. Do not rely on soldered wire loops as the primary fan retention method.
2. Prefer proper replacement wire clips for the exact cooler model from the manufacturer.

If you still prototype custom retention:

1. Use spring-steel style tension clips or a rigid printed bracket rated for heat.
2. Keep all metal clear of motherboard traces, VRM heatsinks, and fan blades.
3. Add a secondary tether so a failed clip cannot drop the fan into components.
4. Test at low RPM first, then full RPM while monitoring vibration and temperatures.
5. Do not route or solder anything that can short the fan header or motherboard.

About using two Slim Silent Fan 8 units:

1. Electrically possible only if fan header current limits are respected.
2. Use a proper PWM splitter/hub instead of hand-soldered power joins.
3. Small 80mm slim fans usually increase noise and may not improve tower-cooler pressure profile.
4. A single well-mounted 120mm tower fan is usually better for this cooler class.

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

- With RX 6400 4GB, prefer hosted inference for best results.
- If local-only, stick to compact quantized models and smaller context settings.
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

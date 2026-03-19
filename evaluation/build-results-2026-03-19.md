# Build Results - 2026-03-19

## Goal
Build the polyforth-llm agent pipeline against the canonical knowledge source document:
- `data/polyForth-llm.docx`

## Repo baseline
- Commit checked out: `941c094` (`Align source defaults and make scripts runnable from repo root`)
- Working tree before build: clean

## Build run summary
Status: **BLOCKED (host tooling/permissions)**

### What was attempted
1. Environment bootstrap:
```bash
python3 -m venv .venv && . .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt
```
Result:
- Failed: `ensurepip is not available` (python venv module missing).

2. Install venv tooling with sudo:
```bash
sudo apt update && sudo apt install -y python3-venv
```
Result:
- Failed: `sudo` requires interactive password in this execution environment.

3. User-space fallback for virtualenv:
```bash
python3 -m pip install --user virtualenv
```
Result:
- Failed: `/usr/bin/python3: No module named pip`.

4. Direct apt install without sudo (escalated execution):
```bash
apt update && apt install -y python3-venv python3-pip
```
Result:
- Failed: permission denied on apt locks (`/var/lib/apt/lists/lock`).

## Verified environment facts
- Python available: `Python 3.13.5`
- `pip`: missing
- `.venv`: missing
- `.env`: missing
- Source document exists: `data/polyForth-llm.docx`
- Index artifacts currently missing:
  - `index/knowledge.faiss`
  - `index/chunks.json`

## Unblock commands to run on host (interactive shell with sudo)
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip build-essential

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python scripts/download_embedding_model.py
python scripts/build_index.py
```

## Expected success criteria after unblock
1. `models/all-MiniLM-L6-v2/` populated.
2. `index/knowledge.faiss` exists.
3. `index/chunks.json` exists and includes `source`, `heading`, `text` fields.
4. `python scripts/teaching_chat.py` starts successfully with configured LLM API values.

## Notes
- This run did not reach model download, index build, or teaching-chat startup because system package installation is required first.

---

## Continuation Run - 2026-03-19 (after host prerequisites installed)

Status: **SUCCESS (core build completed)**

### Additional changes made during continuation
1. Updated dependency pin for Python 3.13 compatibility:
   - `faiss-cpu==1.8.0.post1` -> `faiss-cpu==1.13.2` in `requirements.txt`.

### Commands executed
```bash
python3 -m venv --clear .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/download_embedding_model.py
python scripts/build_index.py
```

### Results
1. Dependency install completed successfully in `.venv`.
2. Embedding model cached locally:
   - `models/all-MiniLM-L6-v2/`
3. Index build completed successfully:
   - `Indexed 704 chunks from 282 sections.`
   - `Saved index to: index`
4. Index artifacts verified:
   - `index/knowledge.faiss` (1,081,389 bytes)
   - `index/chunks.json` (804,467 bytes)
5. Chunk schema verified:
   - keys: `heading`, `source`, `text`

### Retrieval smoke test
Executed in virtualenv with query:
- `What does DUP do in polyForth?`

Result:
- 3 hits returned from index with non-zero similarity scores.
- Retrieval path is functioning end-to-end.

### Current readiness
- Knowledge base ingestion/index pipeline is operational against:
  - `data/polyForth-llm.docx`
- Next step for full tutor validation:
  - Configure real `LLM_API_KEY` in `.env`.
  - Run `python scripts/teaching_chat.py`.
  - Execute `evaluation/teaching-benchmark.md` and save `evaluation/results-YYYY-MM-DD.md`.

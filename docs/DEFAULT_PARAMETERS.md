# Default Parameters (Validated Set)

This document captures the currently validated default parameter set for local-first operation.

## Scope

These defaults are for:

1. Local retrieval/indexing.
2. Local inference through Ollama OpenAI-compatible API.
3. Reproducible baseline runs before deeper tuning.

## Environment profile

Use:

1. `profiles/.env.local-ollama.default`

Apply:

```bash
cp profiles/.env.local-ollama.default .env
```

## Retrieval/index defaults

1. `SOURCE_PATH=data/polyForth-llm.docx`
2. `INDEX_DIR=index`
3. `CHUNK_SIZE=1000`
4. `CHUNK_OVERLAP=120`
5. `EMBEDDING_MODEL=models/all-MiniLM-L6-v2`
6. `TOP_K=4`

## Local generation defaults

1. `LLM_BASE_URL=http://127.0.0.1:11434/v1`
2. `LLM_API_KEY=ollama`
3. `LLM_MODEL=qwen2.5-coder:7b-instruct-q4_K_M`
4. `SYSTEM_PROMPT=concise polyForth tutor with citation and missing-context behavior`

## Dependency compatibility pins

These pins were required for this validated baseline:

1. `faiss-cpu==1.13.2`
2. `httpx==0.27.2` (compatibility with `openai==1.51.2`)

## Ollama server setting

For local cloud-disable behavior:

1. File: `~/.ollama/server.json`
2. Value:

```json
{
  "disable_ollama_cloud": true
}
```

## Validation checklist

1. `python scripts/build_index.py` succeeds.
2. `index/knowledge.faiss` and `index/chunks.json` exist.
3. `GET http://127.0.0.1:11434/v1/models` returns local model list.
4. `python scripts/teaching_chat.py` starts successfully with local `.env`.

## Prewarm and keep-alive defaults

To reduce cold-start delays, prewarm the model and keep it loaded:

1. Set keep-alive in shell before `ollama serve`:

```bash
export OLLAMA_KEEP_ALIVE=24h
ollama serve
```

2. Run one-time prewarm call:

```bash
bash scripts/prewarm_ollama.sh
```

Optional model override:

```bash
bash scripts/prewarm_ollama.sh qwen2.5-coder:7b-instruct-q4_K_M
```

### Prewarm reporting fields

Each run reports and logs:

1. HTTP status
2. Request latency in seconds
3. Returned model id
4. Token usage (`prompt_tokens`, `completion_tokens`, `total_tokens`)
5. Result status (`ok` or `error`)

Default log file:

- `evaluation/prewarm.log`

## Optional systemd user service

Create `~/.config/systemd/user/ollama-prewarm.service`:

```ini
[Unit]
Description=Prewarm local Ollama model
After=default.target

[Service]
Type=oneshot
Environment=LLM_BASE_URL=http://127.0.0.1:11434/v1
Environment=LLM_API_KEY=ollama
Environment=LLM_MODEL=qwen2.5-coder:7b-instruct-q4_K_M
ExecStart=/bin/bash /home/cartheur/ame/aiventure/aiventure-github/polysance/polyforth-llm/scripts/prewarm_ollama.sh

[Install]
WantedBy=default.target
```

Enable:

```bash
systemctl --user daemon-reload
systemctl --user enable --now ollama-prewarm.service
```

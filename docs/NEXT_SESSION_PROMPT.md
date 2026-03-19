# Next Session Prompt

Use this prompt at the start of the next session:

```text
Resume this polyforth-llm project from current repo state.

Context:
- We are building a local-first RAG tutor for polyForth (FAISS retrieval + Ollama generation).
- Local model: qwen2.5-coder:7b-instruct-q4_K_M.
- Validated defaults are documented in docs/DEFAULT_PARAMETERS.md and profiles/.env.local-ollama.default.
- Prewarm script exists at scripts/prewarm_ollama.sh and now logs status/latency/token usage to evaluation/prewarm.log.
- Ollama cloud-disable setting should be true in ~/.ollama/server.json.

Immediate goal:
1) Ensure ollama serve is running with OLLAMA_KEEP_ALIVE=24h.
2) Run bash scripts/prewarm_ollama.sh and show the logged metrics.
3) Run the 10-question benchmark slice from evaluation/teaching-benchmark.md (Foundations 1-10) with concise responses and save outputs to evaluation/benchmark-slice-YYYY-MM-DD.md.
4) Score results using the rubric and write evaluation/results-YYYY-MM-DD.md.
5) Summarize the biggest issues (retrieval vs prompt vs model behavior) and propose the next tuning step.

Constraints:
- Ask before making file edits.
- Do not commit .env or profiles/pubkey.txt.
- Keep progress visible during long runs (per-question progress updates).
```

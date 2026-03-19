#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-${LLM_MODEL:-qwen2.5-coder:7b-instruct-q4_K_M}}"
BASE_URL="${LLM_BASE_URL:-http://127.0.0.1:11434/v1}"
API_KEY="${LLM_API_KEY:-ollama}"
KEEP_ALIVE="${OLLAMA_KEEP_ALIVE:-24h}"
LOG_FILE="${PREWARM_LOG_FILE:-evaluation/prewarm.log}"
TMP_BODY="$(mktemp)"
trap 'rm -f "${TMP_BODY}"' EXIT

echo "Prewarming model: ${MODEL}"
echo "Endpoint: ${BASE_URL}"
echo "Keep-alive: ${KEEP_ALIVE}"

mkdir -p "$(dirname "${LOG_FILE}")"

HTTP_CODE="$(
  curl -sS "${BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"model\": \"${MODEL}\",
    \"messages\": [{\"role\": \"user\", \"content\": \"warmup\"}],
    \"max_tokens\": 1,
    \"temperature\": 0,
    \"stream\": false,
    \"keep_alive\": \"${KEEP_ALIVE}\"
  }" \
  -o "${TMP_BODY}" \
  -w "%{http_code}|%{time_total}"
)"

HTTP_STATUS="${HTTP_CODE%%|*}"
LATENCY_S="${HTTP_CODE##*|}"
TIMESTAMP="$(date -Iseconds)"

if [[ "${HTTP_STATUS}" != "200" ]]; then
  echo "Prewarm failed: HTTP ${HTTP_STATUS}"
  echo "Response body:"
  cat "${TMP_BODY}"
  printf "%s status=%s latency_s=%s model=%s result=error\n" \
    "${TIMESTAMP}" "${HTTP_STATUS}" "${LATENCY_S}" "${MODEL}" >> "${LOG_FILE}"
  exit 1
fi

MODEL_ID="$(
  python3 - <<'PY' "${TMP_BODY}"
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)
print(data.get("model", "unknown"))
PY
)"

TOKENS="$(
  python3 - <<'PY' "${TMP_BODY}"
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)
usage = data.get("usage", {})
print(
    "prompt_tokens={0} completion_tokens={1} total_tokens={2}".format(
        usage.get("prompt_tokens", "n/a"),
        usage.get("completion_tokens", "n/a"),
        usage.get("total_tokens", "n/a"),
    )
)
PY
)"

printf "%s status=%s latency_s=%s model=%s %s result=ok\n" \
  "${TIMESTAMP}" "${HTTP_STATUS}" "${LATENCY_S}" "${MODEL_ID}" "${TOKENS}" >> "${LOG_FILE}"

echo "Prewarm complete."
echo "HTTP status: ${HTTP_STATUS}"
echo "Latency (s): ${LATENCY_S}"
echo "Model id: ${MODEL_ID}"
echo "Usage: ${TOKENS}"
echo "Logged: ${LOG_FILE}"

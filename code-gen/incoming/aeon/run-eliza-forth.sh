#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if command -v gforth >/dev/null 2>&1; then
  export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp}"
  exec gforth eliza-gforth.fs
elif command -v pforth >/dev/null 2>&1; then
  exec pforth eliza-pforth.4th
else
  echo "Neither gforth nor pforth found in PATH." >&2
  exit 1
fi

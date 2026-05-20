#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp}"
exec gforth ideal-gforth.fs

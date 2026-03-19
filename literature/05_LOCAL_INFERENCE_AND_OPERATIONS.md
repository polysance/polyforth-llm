# 05 - Local Inference and Operations

## Local-first principles

1. Keep retrieval local.
2. Keep generation local when feasible.
3. Prefer reproducible, scriptable workflows.

## Operational components

1. Python runtime + dependencies
2. Embedding model cache
3. FAISS index artifacts
4. Local model server (Ollama)
5. Environment configuration (`.env`)

## Common local risks

1. Dependency version drift
2. Model-server compatibility mismatches
3. Resource pressure (RAM/VRAM/disk)
4. Slow cold starts and latency spikes

## Controls

1. Pin dependencies.
2. Log build/validation steps.
3. Keep benchmark history.
4. Validate endpoints before teaching sessions.

## Security and governance notes

1. Keep secrets local (`.env` uncommitted).
2. Use local-only endpoints when privacy is required.
3. Track configuration changes with commit history where appropriate.

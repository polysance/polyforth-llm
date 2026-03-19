# Env Profiles

Use one of these presets as your working `.env`:

1. `profiles/.env.hosted.example`
2. `profiles/.env.local-lite.example`
3. `profiles/.env.teaching.example`
4. `profiles/.env.local-ollama.default` (validated local baseline)

## Quick use

```bash
cp profiles/.env.local-ollama.default .env
```

Then edit API/model values as needed.

For local-first round-one execution details and checkpoints, see:

- `docs/LOCAL_FIRST_BUILD.md`
- `docs/DEFAULT_PARAMETERS.md`

## Profile intent

1. hosted:
   - Best quality and latency for current hardware.
2. local-lite:
   - Local inference on constrained hardware (lower quality/throughput).
3. teaching:
   - Optimized defaults for lesson/quiz/tutor workflows.
4. local-ollama.default:
   - Validated local-first baseline using Ollama + qwen2.5-coder.

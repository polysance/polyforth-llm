# Env Profiles

Use one of these presets as your working `.env`:

1. `profiles/.env.hosted.example`
2. `profiles/.env.local-lite.example`
3. `profiles/.env.teaching.example`

## Quick use

```bash
cp profiles/.env.teaching.example .env
```

Then edit API/model values as needed.

For local-first round-one execution details and checkpoints, see:

- `docs/LOCAL_FIRST_BUILD.md`

## Profile intent

1. hosted:
   - Best quality and latency for current hardware.
2. local-lite:
   - Local inference on constrained hardware (lower quality/throughput).
3. teaching:
   - Optimized defaults for lesson/quiz/tutor workflows.

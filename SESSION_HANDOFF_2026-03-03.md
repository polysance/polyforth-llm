# Session Handoff (2026-03-03)

## Current status

Preparation is complete for this phase.

Completed:

1. Source ingestion pipeline (`.docx` / `.pdf`) and FAISS index workflow.
2. Standard chat mode and dedicated teaching mode.
3. Teaching documentation, roadmap, benchmark set, and env profiles.
4. Hardware strategy and forward execution plan documented.

## Waiting on hardware delivery

Ordered:

1. CPU cooling system (AIO path).
2. SATA-powered PWM hub.

Decision:

1. Do not attempt ad-hoc fan retention tricks while waiting.

## Next actions after parts arrive

1. Install AIO + PWM hub.
2. Run thermal validation before sustained workloads.
3. On the host machine:
   - `cp profiles/.env.teaching.example .env`
   - `python scripts/build_index.py`
   - `python scripts/teaching_chat.py`
4. Start teaching/evaluation loop with:
   - `evaluation/teaching-benchmark.md`

## Resume point

Resume from hardware validation, then proceed directly into teaching mode operations and benchmark tracking.

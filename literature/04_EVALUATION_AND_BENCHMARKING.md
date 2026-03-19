# 04 - Evaluation and Benchmarking

## Why evaluation matters

RAG quality can regress silently after prompt, model, or retrieval changes. Use fixed benchmark questions and scoring.

## Core metrics in this project

1. Correctness
2. Citation quality
3. Teaching clarity
4. Hallucination control

Reference benchmark:

- `evaluation/teaching-benchmark.md`

## Evaluation method

1. Use fixed question set.
2. Score each answer with the same rubric.
3. Save dated result files.
4. Compare against baseline before adopting changes.

## Regression gates

Do not promote changes when:

1. Average score drops materially.
2. Fabricated citations appear.
3. Missing-context handling degrades.

## Fast iteration strategy

1. Run 10-question smoke benchmark for quick signal.
2. Run full benchmark for release-level confidence.

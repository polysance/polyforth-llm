# 03 - System Design Patterns

## Pattern A: Minimal single-source RAG

Use one canonical source and enforce citations.

Strengths:

1. Simple governance.
2. Easy debugging.
3. Fast iteration.

Limitations:

1. Narrow scope.
2. Sensitive to source structure/quality.

## Pattern B: Local retrieval + hosted generation

Strengths:

1. Better generation quality quickly.
2. Lower local compute burden.

Limitations:

1. External dependency and API cost.
2. Data governance concerns.

## Pattern C: Fully local retrieval + local generation

Strengths:

1. Maximum control/privacy.
2. Offline capability.

Limitations:

1. Hardware constraints.
2. More operations work.

## Pattern D: Multi-stage retrieval

Coarse retrieval followed by reranking.

Strengths:

1. Better precision/recall balance.

Limitations:

1. Increased complexity and latency.

## Recommended current pattern for this repo

Pattern C for educational transparency, with benchmark-driven iteration before adding architectural complexity.

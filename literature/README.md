# RAG Literature Hub

This section is an educational landing site for the theory and practice behind the system in this repository.

## Purpose

Use this hub to:

1. Learn core Retrieval-Augmented Generation (RAG) concepts.
2. Understand architectural and operational tradeoffs.
3. Study evaluation methods for trustworthy teaching systems.
4. Connect academic ideas to this polyforth-llm implementation.

## Reading map

1. `01_RAG_GLOSSARY.md`
   - Core vocabulary and foundational definitions.
2. `02_THEORY_AND_ALGORITHMS.md`
   - Retrieval/generation theory, ranking behavior, and algorithmic choices.
3. `03_SYSTEM_DESIGN_PATTERNS.md`
   - Common RAG architecture patterns and their tradeoffs.
4. `04_EVALUATION_AND_BENCHMARKING.md`
   - What to measure, how to score, and regression discipline.
5. `05_LOCAL_INFERENCE_AND_OPERATIONS.md`
   - Local runtime constraints, reliability, and deployment considerations.
6. `06_TEACHING_AND_CURRICULUM.md`
   - Pedagogical design for source-grounded tutoring systems.

## How this maps to this repo

1. Ingestion and indexing code:
   - `polyforth_llm/ingest.py`
2. Retrieval and ranking:
   - `polyforth_llm/retriever.py`
3. Prompting and generation:
   - `polyforth_llm/chat.py`
   - `polyforth_llm/teaching.py`
4. Evaluation baseline:
   - `evaluation/teaching-benchmark.md`

## Suggested study order

1. Start with glossary.
2. Read theory/algorithms.
3. Review design patterns.
4. Apply evaluation and operations sections to current experiments.

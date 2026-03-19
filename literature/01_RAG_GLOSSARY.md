# 01 - RAG Glossary

## Retrieval-Augmented Generation (RAG)

A pipeline pattern that retrieves relevant source context first, then asks an LLM to answer using that context.

## Source grounding

Constraining answers to evidence drawn from known sources instead of unconstrained model memory.

## Ingestion

Converting raw source files (`.docx`, `.pdf`) into normalized text suitable for chunking and indexing.

## Chunking

Splitting source text into smaller segments for retrieval. Overlap is used to reduce context fragmentation.

## Embedding

Mapping text into a high-dimensional vector space where semantic similarity can be measured numerically.

## Vector index

A data structure for nearest-neighbor search over embeddings (FAISS in this repo).

## Similarity search

Ranking stored vectors by closeness to query vector (cosine-like behavior here via normalized vectors + inner product).

## Top-k retrieval

Returning the `k` highest-scoring chunks for a query.

## Prompt grounding

Injecting retrieved chunks into the model prompt as explicit evidence for generation.

## Citation discipline

Requiring source tags in answers so claims can be traced and audited.

## Hallucination

Generated content not supported by available evidence.

## Tuning (system tuning)

Adjusting retrieval parameters, prompts, and model/runtime settings without changing model weights.

## Fine-tuning (weight tuning)

Updating model weights on training data. Not used in this repository at present.

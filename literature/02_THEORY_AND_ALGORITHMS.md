# 02 - Theory and Algorithms

## Core decomposition

RAG decomposes QA into:

1. Retrieval problem: find relevant evidence.
2. Generation problem: synthesize response from evidence.

## Retrieval objective

Given query embedding `q` and chunk embeddings `x_i`, rank by similarity and return top-k.

In this repo:

1. Embeddings are normalized.
2. FAISS `IndexFlatIP` is used.
3. Inner product over normalized vectors approximates cosine similarity ranking.

## Chunking effects

Chunk size and overlap control bias/variance in retrieval:

1. Larger chunks:
   - Higher context coverage, lower precision.
2. Smaller chunks:
   - Higher precision, more fragmentation risk.
3. Overlap:
   - Improves continuity but increases index size and redundancy.

## Prompting as inference control

Prompt constraints shape how the model handles evidence:

1. Prefer retrieved context over priors.
2. Cite claims.
3. Declare missing context when evidence is insufficient.

## Failure modes

1. Retrieval miss: relevant chunk not in top-k.
2. Retrieval noise: top-k includes mostly weak evidence.
3. Evidence underuse: model ignores retrieved context.
4. Citation mismatch: cites chunks that do not support claim.

## Practical implication

Quality depends on retrieval fidelity plus generation discipline, not on model size alone.

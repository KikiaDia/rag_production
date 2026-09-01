# Reproducibility coordinates for RAG

RAG reproducibility is harder than ordinary API reproducibility because retrieval data
is part of model behavior.

A release must identify:
1. Git SHA/tag and immutable package/artifact digest.
2. Python version and exact dependency lock.
3. Prompt registry name + resolved immutable prompt version.
4. Model endpoint/type/inference config.
5. Embedding model.
6. Chunking algorithm/config.
7. Delta source/chunk table + exact snapshot/version.
8. Vector Search endpoint/index.
9. Retrieval parameters: top_k, filters, score threshold.
10. Evaluation dataset version + evaluation run/report.
11. Environment/DAB target and deployment config hash.

Rollback should restore the complete known-good coordinate set. A prompt-only rollback is
valid only when the incident is isolated to the prompt.

# Energy Technical Docs RAG — production-oriented Databricks project

Use case: answer questions on energy-sector technical documents with citations,
abstention when evidence is insufficient, reproducible prompt/model/retrieval/evaluation
coordinates, CI/CD, staging, monitoring and rollback.

## Architecture

Documents -> ingestion -> parsing/chunking -> Delta -> Vector Search -> Retriever
-> prompt from MLflow Prompt Registry -> Foundation Model -> FastAPI -> MLflow Tracing
-> evaluation/monitoring.

Local/CI uses deterministic in-memory retrieval + answer generation. Databricks adapters
are isolated behind interfaces and must be validated against the target workspace.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
uvicorn energy_rag.server:app --reload
```

## Reproducibility

A release is defined by code + dependency lock + prompt version + model config +
retrieval config + corpus snapshot + vector index coordinate + evaluation dataset +
evaluation run + deployment config + artifact digest. See `docs/REPRODUCIBILITY.md`.
"# rag_production" 

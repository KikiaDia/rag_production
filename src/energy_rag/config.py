from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["local", "dev", "staging", "prod"] = "local"
    backend: Literal["fake", "databricks"] = "fake"

    prompt_name: str = "main.genai.energy_rag_answer"
    prompt_ref: str = "dev"
    model_endpoint: str = "databricks-llama-4-maverick"
    model_type: str = "chat"
    model_temperature: float = Field(default=0.0, ge=0, le=2)
    model_max_tokens: int = Field(default=1000, gt=0)

    vector_search_endpoint: str = "energy-vs-endpoint"
    vector_index_name: str = "main.genai.energy_docs_index"
    source_table: str = "main.genai.energy_docs_chunks"
    corpus_snapshot: str = "local-fixture-v1"
    embedding_model: str = "databricks-gte-large-en"

    top_k: int = Field(default=4, ge=1, le=20)
    min_relevance_score: float = Field(default=0.55, ge=0, le=1)
    request_timeout_seconds: float = Field(default=30.0, gt=0)
    max_question_chars: int = Field(default=5000, gt=0)

    eval_dataset_name: str = "main.genai.energy_rag_eval"
    mlflow_experiment_name: str = "/Shared/energy-rag"

    min_context_recall: float = 0.90
    min_citation_correctness: float = 0.95
    min_answer_correctness: float = 0.90
    max_p95_latency_ms: float = 8000.0

    release_id: str = "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=5000)
    session_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[str]
    abstained: bool
    request_id: str
    latency_ms: float
    release_id: str
    prompt_version: int | None = None
    model_name: str | None = None


class HealthResponse(BaseModel):
    status: str
    environment: str
    release_id: str

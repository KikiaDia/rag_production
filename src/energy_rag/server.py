import time
import uuid
from fastapi import FastAPI, HTTPException
from energy_rag.config import get_settings
from energy_rag.contracts import HealthResponse, QueryRequest, QueryResponse
from energy_rag.factory import build_service

settings = get_settings()
service = build_service(settings)
app = FastAPI(title="Energy Technical Docs RAG", version="0.2.0")


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", environment=settings.environment, release_id=settings.release_id)


@app.get("/ready", response_model=HealthResponse)
def ready():
    return HealthResponse(status="ready", environment=settings.environment, release_id=settings.release_id)


@app.post("/query", response_model=QueryResponse)
async def query(payload: QueryRequest):
    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    try:
        result = await service.answer(payload.question)
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="RAG request timed out") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    latency_ms = (time.perf_counter() - started) * 1000
    return QueryResponse(
        answer=result.answer,
        citations=list(result.citations),
        abstained=result.abstained,
        request_id=request_id,
        latency_ms=latency_ms,
        release_id=settings.release_id,
        prompt_version=result.prompt_version,
        model_name=result.model_name,
    )

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    title: str
    text: str
    page: int | None
    score: float = 0.0

    @property
    def citation(self) -> str:
        page = f", p. {self.page}" if self.page is not None else ""
        return f"[{self.document_id}{page}]"


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: tuple[str, ...]
    abstained: bool
    retrieved_chunk_ids: tuple[str, ...]
    prompt_version: int | None = None
    model_name: str | None = None

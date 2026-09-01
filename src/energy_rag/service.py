import asyncio
from energy_rag.config import Settings
from energy_rag.domain import RagAnswer
from energy_rag.generation import Generator
from energy_rag.retrieval import Retriever


class RagService:
    def __init__(self, settings: Settings, retriever: Retriever, generator: Generator):
        self.settings = settings
        self.retriever = retriever
        self.generator = generator

    async def answer(self, question: str) -> RagAnswer:
        chunks = list(self.retriever.search(question, self.settings.top_k))
        chunks = [c for c in chunks if c.score >= self.settings.min_relevance_score]
        if not chunks:
            return RagAnswer(
                answer="Je ne dispose pas de preuves suffisantes dans la documentation fournie.",
                citations=(), abstained=True, retrieved_chunk_ids=()
            )
        return await asyncio.wait_for(
            self.generator.generate(question, chunks),
            timeout=self.settings.request_timeout_seconds,
        )

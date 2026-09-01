import re
from typing import Protocol, Sequence
from energy_rag.config import Settings
from energy_rag.domain import DocumentChunk, RagAnswer
from energy_rag.prompt_registry import load_runtime_prompt


class Generator(Protocol):
    async def generate(self, question: str, chunks: Sequence[DocumentChunk]) -> RagAnswer: ...


class DeterministicGenerator:
    async def generate(self, question: str, chunks: Sequence[DocumentChunk]) -> RagAnswer:
        useful = [c for c in chunks if c.score > 0]
        if not useful:
            return RagAnswer(
                answer="Je ne dispose pas de preuves suffisantes dans la documentation fournie.",
                citations=(), abstained=True, retrieved_chunk_ids=tuple(c.chunk_id for c in chunks)
            )
        c = useful[0]
        sentence = re.split(r"(?<=[.!?])\s+", c.text)[0]
        return RagAnswer(
            answer=f"{sentence} {c.citation}",
            citations=(c.citation,),
            abstained=False,
            retrieved_chunk_ids=tuple(x.chunk_id for x in chunks),
        )


class DatabricksGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def generate(self, question: str, chunks: Sequence[DocumentChunk]) -> RagAnswer:
        try:
            from databricks_openai import AsyncDatabricksOpenAI
            import mlflow
        except ImportError as exc:
            raise RuntimeError('Install Databricks extras: pip install -e ".[databricks]"') from exc

        prompt = load_runtime_prompt(self.settings)
        context = "\n\n".join(
            f"{c.citation} {c.title}\n{c.text}" for c in chunks
        )
        rendered = prompt.template.format(question=question, context=context)
        client = AsyncDatabricksOpenAI()
        response = await client.chat.completions.create(
            model=str(prompt.model_config["model_name"]),
            messages=[{"role": "user", "content": rendered}],
            temperature=float(prompt.model_config["temperature"]),
            max_tokens=int(prompt.model_config["max_tokens"]),
        )
        answer = response.choices[0].message.content or ""
        used = tuple(c.citation for c in chunks if c.citation in answer)
        return RagAnswer(
            answer=answer,
            citations=used,
            abstained=not bool(used),
            retrieved_chunk_ids=tuple(c.chunk_id for c in chunks),
            prompt_version=prompt.version,
            model_name=str(prompt.model_config["model_name"]),
        )

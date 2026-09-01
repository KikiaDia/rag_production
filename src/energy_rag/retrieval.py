from typing import Protocol, Sequence
from energy_rag.domain import DocumentChunk


class Retriever(Protocol):
    def search(self, query: str, top_k: int) -> Sequence[DocumentChunk]: ...


class InMemoryRetriever:
    def __init__(self, chunks: Sequence[DocumentChunk]):
        self.chunks = list(chunks)

    @staticmethod
    def _score(query: str, text: str) -> float:
        q = {w.lower().strip(".,?!:;()") for w in query.split() if len(w) > 2}
        t = {w.lower().strip(".,?!:;()") for w in text.split()}
        if not q:
            return 0.0
        return len(q & t) / len(q)

    def search(self, query: str, top_k: int) -> Sequence[DocumentChunk]:
        scored = [
            DocumentChunk(
                chunk_id=c.chunk_id, document_id=c.document_id, title=c.title,
                text=c.text, page=c.page, score=self._score(query, c.text)
            )
            for c in self.chunks
        ]
        return sorted(scored, key=lambda x: x.score, reverse=True)[:top_k]


class DatabricksVectorSearchRetriever:
    """Thin adapter. Keep vendor-specific code out of application logic."""

    def __init__(self, endpoint_name: str, index_name: str):
        self.endpoint_name = endpoint_name
        self.index_name = index_name

    def search(self, query: str, top_k: int) -> Sequence[DocumentChunk]:
        try:
            from databricks.vector_search.client import VectorSearchClient
        except ImportError as exc:
            raise RuntimeError('Install Databricks extras: pip install -e ".[databricks]"') from exc

        client = VectorSearchClient()
        index = client.get_index(
            endpoint_name=self.endpoint_name,
            index_name=self.index_name,
        )
        result = index.similarity_search(
            query_text=query,
            columns=["chunk_id", "document_id", "title", "text", "page"],
            num_results=top_k,
        )
        rows = result.get("result", {}).get("data_array", [])
        columns = [c["name"] for c in result.get("manifest", {}).get("columns", [])]
        chunks = []
        for row in rows:
            obj = dict(zip(columns, row))
            score = float(obj.get("score") or obj.get("_score") or 0.0)
            chunks.append(DocumentChunk(
                chunk_id=str(obj["chunk_id"]),
                document_id=str(obj["document_id"]),
                title=str(obj.get("title") or ""),
                text=str(obj["text"]),
                page=int(obj["page"]) if obj.get("page") is not None else None,
                score=score,
            ))
        return chunks

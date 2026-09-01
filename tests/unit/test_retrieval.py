from energy_rag.fixtures import LOCAL_CHUNKS
from energy_rag.retrieval import InMemoryRetriever

def test_transformer_query_retrieves_transformer():
    rows=InMemoryRetriever(LOCAL_CHUNKS).search("transformer oil temperature inspection", 1)
    assert rows[0].document_id == "TR-001"
    assert rows[0].score > 0

from energy_rag.domain import DocumentChunk

LOCAL_CHUNKS = [
    DocumentChunk(
        "transformer-1", "TR-001", "Transformer maintenance manual",
        "Transformer oil temperature above 95 C requires immediate inspection and load review.",
        12
    ),
    DocumentChunk(
        "breaker-1", "CB-001", "Circuit breaker maintenance guide",
        "Circuit breaker contact resistance must be checked during scheduled maintenance.",
        8
    ),
]

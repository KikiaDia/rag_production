from energy_rag.domain import DocumentChunk


def chunk_text(document_id: str, title: str, text: str, chunk_size: int = 700, overlap: int = 100):
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")
    normalized = " ".join(text.split())
    chunks = []
    start = 0
    idx = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        piece = normalized[start:end].strip()
        if piece:
            chunks.append(DocumentChunk(
                chunk_id=f"{document_id}-{idx}",
                document_id=document_id,
                title=title,
                text=piece,
                page=None,
            ))
        if end == len(normalized):
            break
        start = end - overlap
        idx += 1
    return chunks

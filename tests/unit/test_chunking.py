import pytest
from energy_rag.chunking import chunk_text

def test_chunking_is_deterministic():
    a=chunk_text("D1","t","abc def ghi " * 100, chunk_size=50, overlap=10)
    b=chunk_text("D1","t","abc def ghi " * 100, chunk_size=50, overlap=10)
    assert [x.chunk_id for x in a] == [x.chunk_id for x in b]

def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("D1","t","abc", chunk_size=10, overlap=10)

import asyncio
from energy_rag.config import Settings
from energy_rag.factory import build_service

def test_unknown_question_abstains():
    result=asyncio.run(build_service(Settings(backend="fake", min_relevance_score=0.2)).answer("cryptocurrency investment"))
    assert result.abstained is True
    assert result.citations == ()

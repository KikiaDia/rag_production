from energy_rag.config import Settings
from energy_rag.fixtures import LOCAL_CHUNKS
from energy_rag.generation import DeterministicGenerator, DatabricksGenerator
from energy_rag.retrieval import InMemoryRetriever, DatabricksVectorSearchRetriever
from energy_rag.service import RagService


def build_service(settings: Settings) -> RagService:
    if settings.backend == "databricks":
        retriever = DatabricksVectorSearchRetriever(
            settings.vector_search_endpoint, settings.vector_index_name
        )
        generator = DatabricksGenerator(settings)
    else:
        retriever = InMemoryRetriever(LOCAL_CHUNKS)
        generator = DeterministicGenerator()
    return RagService(settings, retriever, generator)

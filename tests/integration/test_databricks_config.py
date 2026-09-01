import os, pytest
from energy_rag.config import Settings

@pytest.mark.integration
def test_databricks_coordinates_present():
    if os.getenv("RUN_DATABRICKS_INTEGRATION") != "1":
        pytest.skip("Set RUN_DATABRICKS_INTEGRATION=1")
    s=Settings(backend="databricks")
    assert "." in s.vector_index_name
    assert "." in s.prompt_name

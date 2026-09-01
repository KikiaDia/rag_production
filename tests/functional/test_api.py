from fastapi.testclient import TestClient
from energy_rag.server import app

client=TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_query_contract():
    r=client.post("/query", json={"question":"transformer oil temperature inspection"})
    assert r.status_code == 200
    body=r.json()
    assert set(["answer","citations","abstained","request_id","release_id"]).issubset(body)

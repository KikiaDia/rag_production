import os, httpx
base=os.environ["RAG_BASE_URL"].rstrip("/")
assert httpx.get(base+"/health", timeout=10).status_code == 200
r=httpx.post(base+"/query", json={"question":"When should transformer oil temperature trigger inspection?"}, timeout=30)
r.raise_for_status()
assert "answer" in r.json()
print("smoke OK")

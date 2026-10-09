from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)

def test_health(): assert c.get("/api/health").json()["status"] == "ok"
def test_examples_count(): assert len(c.get("/api/examples").json()) >= 8
def test_analyze_ok():
    r = c.post("/api/analyze", json={"message": "Share your password now, account will be suspended", "message_type": "email"})
    assert r.status_code == 200 and r.json()["risk_score"] > 0
def test_empty_rejected(): assert c.post("/api/analyze", json={"message": "   "}).status_code == 422
def test_too_long(): assert c.post("/api/analyze", json={"message": "a" * 10001}).status_code == 413
def test_bad_type(): assert c.post("/api/analyze", json={"message": "hi", "message_type": "fax"}).status_code == 422

from fastapi.testclient import TestClient
from app.main import app
def test_docs_available(): assert TestClient(app).get("/docs").status_code == 200

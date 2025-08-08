# test_ping.py
from fastapi.testclient import TestClient
from app.core.app import create_app

app = create_app()
client = TestClient(app)

def test_ping():
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.text == "pong"

# space
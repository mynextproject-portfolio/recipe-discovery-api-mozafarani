# test_ping.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ping():
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.text == "pong"

# space
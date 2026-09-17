from fastapi.testclient import TestClient

from src.api.server import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_query_endpoint_with_fake_agent(monkeypatch):
    class FakeAgent:
        def run(self, question: str) -> str:
            return f"Answer for: {question}"

    monkeypatch.setattr("src.api.server.agent", FakeAgent())

    response = client.post(
        "/query",
        json={"question": "What is this project about?"},
        headers={"Origin": "http://localhost:3000"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Answer for: What is this project about?"
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

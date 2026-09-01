from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommendations_endpoint():
    response = client.get("/recommendations/U001?top_n=3")

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == "U001"
    assert body["count"] == 3
    assert len(body["recommendations"]) == 3
    assert all("reason" in item for item in body["recommendations"])


def test_top_n_validation():
    response = client.get("/recommendations/U001?top_n=0")
    assert response.status_code == 422

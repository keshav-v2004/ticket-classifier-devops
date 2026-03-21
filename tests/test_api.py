from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_predict_validation():
    # Test that empty text returns a 422 Validation Error
    response = client.post("/predict", json={"ticket_text": ""})
    assert response.status_code == 422
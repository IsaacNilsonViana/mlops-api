from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json()["n_features"] == 13

def test_predict_valido():
    features = [13.2, 1.78, 2.14, 11.2, 100.0, 2.65, 2.76, 0.26, 1.28, 4.38, 1.05, 3.4, 1050.0]
    response = client.post("/predict", json={"features": features})
    assert response.status_code == 200
    assert response.json()["classe"] in [0, 1, 2]

def test_predict_invalido():
    response = client.post("/predict", json={"features": [1, 2, 3]})
    assert response.status_code == 422

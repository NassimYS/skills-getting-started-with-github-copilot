import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    # Inscription
    response = client.post("/activities/Math Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Double inscription (doit échouer)
    response = client.post("/activities/Math Club/signup?email=tester@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Désinscription
    response = client.delete("/activities/Math Club/unregister?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Désinscription d'un non-inscrit (doit échouer)
    response = client.delete("/activities/Math Club/unregister?email=tester@mergington.edu")
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]

    # Activité inexistante
    response = client.post("/activities/Unknown/signup?email=test@mergington.edu")
    assert response.status_code == 404
    response = client.delete("/activities/Unknown/unregister?email=test@mergington.edu")
    assert response.status_code == 404

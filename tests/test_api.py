import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_restaurants():
    response = client.get("/restaurants/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_restaurant():
    payload = {"name": "TestResto", "address": "Somewhere 42"}
    
    response = client.post("/restaurants/", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["address"] == payload["address"]

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "TripXplo AI API" in response.json()["message"]

def test_query_endpoint_structure():
    """Test that the query endpoint accepts POST requests"""
    # This test doesn't require actual API keys, just tests structure
    response = client.post("/query", json={"question": "test"})
    # Should return 200 or an error, but not 404 or 405
    assert response.status_code != 404
    assert response.status_code != 405

def test_packages_endpoint():
    """Test the packages endpoint"""
    response = client.get("/packages")
    # Should return 200 or an error, but not 404
    assert response.status_code != 404
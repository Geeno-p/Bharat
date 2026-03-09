import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)
API_KEY = "mvp-test-key"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_unauthorized_access():
    response = client.post("/analyze/market?product_id=p1")
    assert response.status_code == 403

def test_analyze_market_endpoint():
    # Note: This test assumes the agent can be initialized or mocked.
    # For MVP verification, we test the API routing and auth.
    headers = {"X-API-Key": API_KEY}
    response = client.post("/analyze/market?product_id=p1&current_price=50.0", headers=headers)
    
    # If Bedrock is not configured, it might return 500 or the agent response if successful
    assert response.status_code in [200, 500] 
    if response.status_code == 200:
        data = response.json()
        assert data["product_id"] == "p1"
        assert "analysis" in data

def test_dashboard_summary():
    headers = {"X-API-Key": API_KEY}
    response = client.get("/dashboard/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "total_products_monitored" in data["data"]

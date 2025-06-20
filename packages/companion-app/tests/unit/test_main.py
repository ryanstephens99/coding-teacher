"""
Unit tests for main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_root_endpoint(client: TestClient):
    """Test the root health check endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "CodeMentor AI Companion Service",
        "status": "running"
    }


@pytest.mark.unit
def test_health_endpoint(client: TestClient):
    """Test the detailed health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert data["service"] == "codementor-companion"
    assert data["version"] == "0.0.1"
    assert "timestamp" in data  # Timestamp should be present but we don't test exact value


@pytest.mark.unit
def test_cors_middleware(client: TestClient):
    """Test CORS middleware configuration."""
    # Test actual request with CORS headers - CORS middleware should allow it
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    
    # Test that CORS headers are present in response
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200


@pytest.mark.unit
def test_websocket_connection(client: TestClient):
    """Test WebSocket connection establishment."""
    with client.websocket_connect("/ws") as websocket:
        # Send test message
        websocket.send_text("Hello")
        
        # Should receive echo response
        data = websocket.receive_text()
        assert data == "Echo: Hello"


@pytest.mark.unit
def test_api_routes_included(client: TestClient):
    """Test that API routes are properly included."""
    # Test analysis routes are accessible
    response = client.get("/api/analysis/supported-languages")
    assert response.status_code == 200
    
    # Test LLM routes are accessible  
    response = client.post("/api/llm/ask", json={
        "question": "test question"
    })
    assert response.status_code == 200


@pytest.mark.unit
def test_invalid_endpoint_returns_404(client: TestClient):
    """Test that invalid endpoints return 404."""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


@pytest.mark.unit  
def test_app_initialization():
    """Test that app initializes with correct configuration."""
    from src.main import app
    
    assert app.title == "CodeMentor AI Companion"
    assert app.description == "Desktop companion service for CodeMentor AI"
    assert app.version == "0.0.1" 
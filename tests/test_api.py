import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_query_endpoint():
    """Test query endpoint"""
    response = client.post(
        "/query",
        json={
            "query": "test query",
            "top_k": 5,
            "use_reranking": True
        }
    )
    # May return 503 if engine not loaded
    assert response.status_code in [200, 503]

def test_metrics_endpoint():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

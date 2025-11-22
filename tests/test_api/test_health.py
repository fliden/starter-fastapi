"""Tests for health check endpoints."""

from fastapi import status
from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint.

    Args:
        client: Test client fixture
    """
    response = client.get("/api/v1/health")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "starter-fastapi"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "environment" in data


def test_readiness_check(client: TestClient) -> None:
    """Test the readiness check endpoint.

    Args:
        client: Test client fixture
    """
    response = client.get("/api/v1/ready")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "ready"


def test_liveness_check(client: TestClient) -> None:
    """Test the liveness check endpoint.

    Args:
        client: Test client fixture
    """
    response = client.get("/api/v1/live")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "alive"


def test_root_endpoint(client: TestClient) -> None:
    """Test the root endpoint.

    Args:
        client: Test client fixture
    """
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert data["docs"] == "/docs"

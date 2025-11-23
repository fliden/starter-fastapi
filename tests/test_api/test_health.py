"""Tests for health check endpoints."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test the health check endpoint.

    Args:
        client: Test client fixture
    """
    response = await client.get("/api/v1/health")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "starter-fastapi"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient) -> None:
    """Test the readiness check endpoint.

    Args:
        client: Test client fixture
    """
    response = await client.get("/api/v1/ready")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.asyncio
async def test_liveness_check(client: AsyncClient) -> None:
    """Test the liveness check endpoint.

    Args:
        client: Test client fixture
    """
    response = await client.get("/api/v1/live")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient) -> None:
    """Test the root endpoint.

    Args:
        client: Test client fixture
    """
    response = await client.get("/")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert data["docs"] == "/docs"

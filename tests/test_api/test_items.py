"""Tests for item management endpoints."""

import pytest
from fastapi import status
from httpx import AsyncClient

from starter_fastapi.models.item import ItemCreate


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, sample_item_data: ItemCreate) -> None:
    """Test creating a new item.

    Args:
        client: Test client fixture
        sample_item_data: Sample item data fixture
    """
    response = await client.post(
        "/api/v1/items",
        json=sample_item_data.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["name"] == sample_item_data.name
    assert data["description"] == sample_item_data.description
    assert data["price"] == sample_item_data.price
    assert data["is_available"] == sample_item_data.is_available
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_item_minimal(
    client: AsyncClient, sample_item_data_minimal: ItemCreate
) -> None:
    """Test creating an item with minimal required fields.

    Args:
        client: Test client fixture
        sample_item_data_minimal: Minimal sample item data fixture
    """
    response = await client.post(
        "/api/v1/items",
        json=sample_item_data_minimal.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["name"] == sample_item_data_minimal.name
    assert data["price"] == sample_item_data_minimal.price
    assert data["is_available"] is True  # Default value


@pytest.mark.asyncio
async def test_create_item_invalid_price(client: AsyncClient) -> None:
    """Test creating an item with invalid price.

    Args:
        client: Test client fixture
    """
    invalid_data = {
        "name": "Invalid Item",
        "price": -10.0,  # Invalid: negative price
    }

    response = await client.post("/api/v1/items", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient, sample_item_data: ItemCreate) -> None:
    """Test retrieving a specific item by ID.

    Args:
        client: Test client fixture
        sample_item_data: Sample item data fixture
    """
    # First create an item
    create_response = await client.post(
        "/api/v1/items",
        json=sample_item_data.model_dump(),
    )
    created_item = create_response.json()
    item_id = created_item["id"]

    # Then retrieve it
    response = await client.get(f"/api/v1/items/{item_id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == sample_item_data.name
    assert data["price"] == sample_item_data.price


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient) -> None:
    """Test retrieving a non-existent item.

    Args:
        client: Test client fixture
    """
    response = await client.get("/api/v1/items/non-existent-id")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert "error" in data


@pytest.mark.asyncio
async def test_list_items_empty(client: AsyncClient) -> None:
    """Test listing items when none exist.

    Args:
        client: Test client fixture
    """
    response = await client.get("/api/v1/items")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient) -> None:
    """Test listing multiple items.

    Args:
        client: Test client fixture
    """
    # Create multiple items
    for i in range(3):
        await client.post(
            "/api/v1/items",
            json={
                "name": f"Item {i}",
                "price": float(i + 1) * 10,
            },
        )

    # List all items
    response = await client.get("/api/v1/items")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_list_items_with_pagination(client: AsyncClient) -> None:
    """Test listing items with pagination.

    Args:
        client: Test client fixture
    """
    # Create multiple items
    for i in range(10):
        await client.post(
            "/api/v1/items",
            json={
                "name": f"Item {i}",
                "price": float(i + 1) * 10,
            },
        )

    # Test pagination
    response = await client.get("/api/v1/items?skip=2&limit=3")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_list_items_available_only(client: AsyncClient) -> None:
    """Test filtering items by availability.

    Args:
        client: Test client fixture
    """
    # Create available and unavailable items
    await client.post(
        "/api/v1/items",
        json={"name": "Available Item", "price": 10.0, "is_available": True},
    )
    await client.post(
        "/api/v1/items",
        json={"name": "Unavailable Item", "price": 20.0, "is_available": False},
    )

    # List only available items
    response = await client.get("/api/v1/items?available_only=true")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert all(item["is_available"] for item in data)


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, sample_item_data: ItemCreate) -> None:
    """Test updating an item.

    Args:
        client: Test client fixture
        sample_item_data: Sample item data fixture
    """
    # Create an item
    create_response = await client.post(
        "/api/v1/items",
        json=sample_item_data.model_dump(),
    )
    created_item = create_response.json()
    item_id = created_item["id"]

    # Update the item
    update_data = {
        "name": "Updated Item",
        "price": 149.99,
    }

    response = await client.patch(f"/api/v1/items/{item_id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Updated Item"
    assert data["price"] == 149.99
    # Description should remain unchanged
    assert data["description"] == sample_item_data.description


@pytest.mark.asyncio
async def test_update_item_not_found(client: AsyncClient) -> None:
    """Test updating a non-existent item.

    Args:
        client: Test client fixture
    """
    update_data = {"name": "Updated Item"}

    response = await client.patch("/api/v1/items/non-existent-id", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, sample_item_data: ItemCreate) -> None:
    """Test deleting an item.

    Args:
        client: Test client fixture
        sample_item_data: Sample item data fixture
    """
    # Create an item
    create_response = await client.post(
        "/api/v1/items",
        json=sample_item_data.model_dump(),
    )
    created_item = create_response.json()
    item_id = created_item["id"]

    # Delete the item
    response = await client.delete(f"/api/v1/items/{item_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the item is deleted
    get_response = await client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_item_not_found(client: AsyncClient) -> None:
    """Test deleting a non-existent item.

    Args:
        client: Test client fixture
    """
    response = await client.delete("/api/v1/items/non-existent-id")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_item_count(client: AsyncClient) -> None:
    """Test getting item count.

    Args:
        client: Test client fixture
    """
    # Create some items
    for i in range(5):
        await client.post(
            "/api/v1/items",
            json={
                "name": f"Item {i}",
                "price": float(i + 1) * 10,
                "is_available": i % 2 == 0,  # Alternate availability
            },
        )

    # Get total count
    response = await client.get("/api/v1/items/stats/count")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["count"] == 5


@pytest.mark.asyncio
async def test_get_item_count_available_only(client: AsyncClient) -> None:
    """Test getting count of available items only.

    Args:
        client: Test client fixture
    """
    # Create available and unavailable items
    for i in range(5):
        await client.post(
            "/api/v1/items",
            json={
                "name": f"Item {i}",
                "price": float(i + 1) * 10,
                "is_available": i % 2 == 0,
            },
        )

    # Get available count (0, 2, 4 = 3 items)
    response = await client.get("/api/v1/items/stats/count?available_only=true")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["count"] == 3

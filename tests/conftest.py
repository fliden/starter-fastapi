"""Shared test fixtures and configuration."""

import pytest
from fastapi.testclient import TestClient

from starter_fastapi.main import app
from starter_fastapi.models.item import ItemCreate
from starter_fastapi.services.item_service import ItemService
from starter_fastapi.services.item_service import item_service as global_item_service


@pytest.fixture(autouse=True)
def reset_global_item_service() -> None:
    """Reset the global item service instance before each test.

    This ensures test isolation by clearing the in-memory storage.
    """
    global_item_service._items.clear()


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application.

    Returns:
        Test client instance
    """
    return TestClient(app)


@pytest.fixture
def item_service() -> ItemService:
    """Create a fresh item service instance for testing.

    Returns:
        ItemService instance
    """
    return ItemService()


@pytest.fixture
def sample_item_data() -> ItemCreate:
    """Create sample item data for testing.

    Returns:
        Sample ItemCreate instance
    """
    return ItemCreate(
        name="Test Item",
        description="This is a test item",
        price=99.99,
        is_available=True,
        metadata={"category": "test", "tags": ["sample"]},
    )


@pytest.fixture
def sample_item_data_minimal() -> ItemCreate:
    """Create minimal sample item data for testing.

    Returns:
        Minimal ItemCreate instance
    """
    return ItemCreate(
        name="Minimal Item",
        price=19.99,
    )


@pytest.fixture
async def created_item(item_service: ItemService, sample_item_data: ItemCreate):
    """Create and return a sample item.

    Args:
        item_service: Item service instance
        sample_item_data: Sample item data

    Returns:
        Created item instance
    """
    return await item_service.create_item(sample_item_data)


@pytest.fixture
async def multiple_items(item_service: ItemService):
    """Create multiple sample items for testing.

    Args:
        item_service: Item service instance

    Returns:
        List of created items
    """
    items_data = [
        ItemCreate(name=f"Item {i}", description=f"Description {i}", price=float(i * 10))
        for i in range(1, 6)
    ]

    items = []
    for item_data in items_data:
        item = await item_service.create_item(item_data)
        items.append(item)

    return items

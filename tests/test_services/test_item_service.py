"""Tests for item service."""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from starter_fastapi.core.exceptions import NotFoundError
from starter_fastapi.models.item import Item, ItemCreate, ItemUpdate
from starter_fastapi.services.item_service import ItemService


@pytest.mark.asyncio
async def test_create_item(
    item_service: ItemService, session: AsyncSession, sample_item_data: ItemCreate
) -> None:
    """Test creating an item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
        sample_item_data: Sample item data fixture
    """
    item = await item_service.create_item(session, sample_item_data)

    assert isinstance(item, Item)
    assert item.name == sample_item_data.name
    assert item.description == sample_item_data.description
    assert item.price == sample_item_data.price
    assert item.is_available == sample_item_data.is_available
    assert item.id is not None
    assert item.created_at is not None
    assert item.updated_at is not None


@pytest.mark.asyncio
async def test_get_item(
    item_service: ItemService, session: AsyncSession, sample_item_data: ItemCreate
) -> None:
    """Test retrieving an item by ID.

    Args:
        item_service: Item service fixture
        session: Database session fixture
        sample_item_data: Sample item data fixture
    """
    created_item = await item_service.create_item(session, sample_item_data)

    retrieved_item = await item_service.get_item(session, created_item.id)

    assert retrieved_item.id == created_item.id
    assert retrieved_item.name == created_item.name
    assert retrieved_item.price == created_item.price


@pytest.mark.asyncio
async def test_get_item_not_found(item_service: ItemService, session: AsyncSession) -> None:
    """Test retrieving a non-existent item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    with pytest.raises(NotFoundError) as exc_info:
        await item_service.get_item(session, "non-existent-id")

    assert "not found" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_list_items_empty(item_service: ItemService, session: AsyncSession) -> None:
    """Test listing items when none exist.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    items = await item_service.list_items(session)

    assert isinstance(items, list)
    assert len(items) == 0


@pytest.mark.asyncio
async def test_list_items(item_service: ItemService, session: AsyncSession) -> None:
    """Test listing multiple items.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    # Create multiple items
    items_data = [ItemCreate(name=f"Item {i}", price=float(i * 10)) for i in range(1, 4)]

    for item_data in items_data:
        await item_service.create_item(session, item_data)

    items = await item_service.list_items(session)

    assert len(items) == 3
    # Items should be sorted by created_at descending (newest first)
    assert items[0].name == "Item 3"
    assert items[1].name == "Item 2"
    assert items[2].name == "Item 1"


@pytest.mark.asyncio
async def test_list_items_with_pagination(item_service: ItemService, session: AsyncSession) -> None:
    """Test listing items with pagination.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    # Create multiple items
    for i in range(10):
        await item_service.create_item(
            session, ItemCreate(name=f"Item {i}", price=float((i + 1) * 10))
        )

    # Test pagination
    items = await item_service.list_items(session, skip=2, limit=3)

    assert len(items) == 3


@pytest.mark.asyncio
async def test_list_items_available_only(item_service: ItemService, session: AsyncSession) -> None:
    """Test filtering items by availability.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    # Create available and unavailable items
    await item_service.create_item(
        session, ItemCreate(name="Available 1", price=10.0, is_available=True)
    )
    await item_service.create_item(
        session, ItemCreate(name="Unavailable", price=20.0, is_available=False)
    )
    await item_service.create_item(
        session, ItemCreate(name="Available 2", price=30.0, is_available=True)
    )

    items = await item_service.list_items(session, available_only=True)

    assert len(items) == 2
    assert all(item.is_available for item in items)


@pytest.mark.asyncio
async def test_update_item(
    item_service: ItemService, session: AsyncSession, sample_item_data: ItemCreate
) -> None:
    """Test updating an item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
        sample_item_data: Sample item data fixture
    """
    created_item = await item_service.create_item(session, sample_item_data)
    original_updated_at = created_item.updated_at

    update_data = ItemUpdate(name="Updated Name", price=199.99)

    updated_item = await item_service.update_item(session, created_item.id, update_data)

    assert updated_item.id == created_item.id
    assert updated_item.name == "Updated Name"
    assert updated_item.price == 199.99
    # Description should remain unchanged
    assert updated_item.description == sample_item_data.description
    # updated_at should be different
    assert updated_item.updated_at >= original_updated_at


@pytest.mark.asyncio
async def test_update_item_partial(
    item_service: ItemService, session: AsyncSession, sample_item_data: ItemCreate
) -> None:
    """Test partial update of an item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
        sample_item_data: Sample item data fixture
    """
    created_item = await item_service.create_item(session, sample_item_data)

    # Update only the price
    update_data = ItemUpdate(price=299.99)

    updated_item = await item_service.update_item(session, created_item.id, update_data)

    assert updated_item.price == 299.99
    # Other fields should remain unchanged
    assert updated_item.name == created_item.name
    assert updated_item.description == created_item.description


@pytest.mark.asyncio
async def test_update_item_not_found(item_service: ItemService, session: AsyncSession) -> None:
    """Test updating a non-existent item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    update_data = ItemUpdate(name="Updated Name")

    with pytest.raises(NotFoundError):
        await item_service.update_item(session, "non-existent-id", update_data)


@pytest.mark.asyncio
async def test_delete_item(
    item_service: ItemService, session: AsyncSession, sample_item_data: ItemCreate
) -> None:
    """Test deleting an item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
        sample_item_data: Sample item data fixture
    """
    created_item = await item_service.create_item(session, sample_item_data)

    await item_service.delete_item(session, created_item.id)

    # Verify the item is deleted
    with pytest.raises(NotFoundError):
        await item_service.get_item(session, created_item.id)


@pytest.mark.asyncio
async def test_delete_item_not_found(item_service: ItemService, session: AsyncSession) -> None:
    """Test deleting a non-existent item.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    with pytest.raises(NotFoundError):
        await item_service.delete_item(session, "non-existent-id")


@pytest.mark.asyncio
async def test_get_item_count(item_service: ItemService, session: AsyncSession) -> None:
    """Test getting item count.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    # Initially should be 0
    count = await item_service.get_item_count(session)
    assert count == 0

    # Create some items
    for i in range(5):
        await item_service.create_item(
            session, ItemCreate(name=f"Item {i}", price=float((i + 1) * 10))
        )

    count = await item_service.get_item_count(session)
    assert count == 5


@pytest.mark.asyncio
async def test_get_item_count_available_only(
    item_service: ItemService, session: AsyncSession
) -> None:
    """Test getting count of available items only.

    Args:
        item_service: Item service fixture
        session: Database session fixture
    """
    # Create available and unavailable items
    for i in range(5):
        await item_service.create_item(
            session,
            ItemCreate(name=f"Item {i}", price=float((i + 1) * 10), is_available=i % 2 == 0),
        )

    # Total count
    total_count = await item_service.get_item_count(session)
    assert total_count == 5

    # Available count (0, 2, 4 = 3 items)
    available_count = await item_service.get_item_count(session, available_only=True)
    assert available_count == 3

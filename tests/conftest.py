"""Shared test fixtures and configuration."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from starter_fastapi.core.db import get_session
from starter_fastapi.main import app
from starter_fastapi.models.item import ItemCreate
from starter_fastapi.services.item_service import ItemService


@pytest.fixture(name="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture(name="client")
async def client_fixture(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for the FastAPI application."""
    app.dependency_overrides[get_session] = lambda: session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def item_service() -> ItemService:
    """Get the item service instance.

    Returns:
        ItemService instance
    """
    from starter_fastapi.services.item_service import item_service

    return item_service


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
        meta={"category": "test", "tags": ["sample"]},
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
async def created_item(session: AsyncSession, sample_item_data: ItemCreate):
    """Create and return a sample item.

    Args:
        session: Database session
        sample_item_data: Sample item data

    Returns:
        Created item instance
    """
    return await item_service.create_item(session, sample_item_data)


@pytest.fixture
async def multiple_items(session: AsyncSession):
    """Create multiple sample items for testing.

    Args:
        session: Database session

    Returns:
        List of created items
    """
    items_data = [
        ItemCreate(name=f"Item {i}", description=f"Description {i}", price=float(i * 10))
        for i in range(1, 6)
    ]

    items = []
    for item_data in items_data:
        item = await item_service.create_item(session, item_data)
        items.append(item)

    return items

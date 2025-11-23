"""Item management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from starter_fastapi.core.db import get_session
from starter_fastapi.core.logging import get_logger
from starter_fastapi.models.item import Item, ItemCreate, ItemUpdate
from starter_fastapi.services.item_service import item_service

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item with the provided details",
)
async def create_item(
    item_data: ItemCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Item:
    """Create a new item.

    Args:
        item_data: Item creation data
        session: Database session

    Returns:
        The created item
    """
    logger.info("Creating new item", item_name=item_data.name)
    item = await item_service.create_item(session, item_data)
    return item


@router.get(
    "",
    response_model=list[Item],
    summary="List all items",
    description="Retrieve a list of items with optional filtering and pagination",
)
async def list_items(
    session: Annotated[AsyncSession, Depends(get_session)],
    skip: Annotated[int, Query(ge=0, description="Number of items to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Maximum items to return")] = 100,
    available_only: Annotated[bool, Query(description="Filter for available items only")] = False,
) -> list[Item]:
    """List all items with optional filtering and pagination.

    Args:
        session: Database session
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return (max 100)
        available_only: If True, only return available items

    Returns:
        List of items
    """
    logger.info("Listing items", skip=skip, limit=limit, available_only=available_only)
    items = await item_service.list_items(
        session, skip=skip, limit=limit, available_only=available_only
    )
    return items


@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Get item by ID",
    description="Retrieve a specific item by its unique identifier",
)
async def get_item(
    item_id: Annotated[str, Path(description="Unique item identifier")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Item:
    """Get a specific item by ID.

    Args:
        item_id: The item ID
        session: Database session

    Returns:
        The requested item

    Raises:
        NotFoundError: If the item is not found
    """
    logger.info("Getting item", item_id=item_id)
    item = await item_service.get_item(session, item_id)
    return item


@router.patch(
    "/{item_id}",
    response_model=Item,
    summary="Update an item",
    description="Update specific fields of an existing item",
)
async def update_item(
    item_id: Annotated[str, Path(description="Unique item identifier")],
    item_data: ItemUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Item:
    """Update an existing item.

    Only the fields provided in the request will be updated.

    Args:
        item_id: The item ID
        item_data: Item update data
        session: Database session

    Returns:
        The updated item

    Raises:
        NotFoundError: If the item is not found
    """
    logger.info("Updating item", item_id=item_id)
    item = await item_service.update_item(session, item_id, item_data)
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Delete an item by its unique identifier",
)
async def delete_item(
    item_id: Annotated[str, Path(description="Unique item identifier")],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete an item.

    Args:
        item_id: The item ID
        session: Database session

    Raises:
        NotFoundError: If the item is not found
    """
    logger.info("Deleting item", item_id=item_id)
    await item_service.delete_item(session, item_id)


@router.get(
    "/stats/count",
    response_model=dict[str, int],
    summary="Get item count",
    description="Get the total count of items",
)
async def get_item_count(
    session: Annotated[AsyncSession, Depends(get_session)],
    available_only: Annotated[bool, Query(description="Count only available items")] = False,
) -> dict[str, int]:
    """Get the total count of items.

    Args:
        session: Database session
        available_only: If True, only count available items

    Returns:
        Dictionary containing the item count
    """
    logger.info("Getting item count", available_only=available_only)
    count = await item_service.get_item_count(session, available_only=available_only)
    return {"count": count}

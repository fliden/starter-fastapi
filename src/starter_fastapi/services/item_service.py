"""Item service containing business logic for item operations."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import func
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from starter_fastapi.core.exceptions import NotFoundError
from starter_fastapi.core.logging import get_logger
from starter_fastapi.models.item import Item, ItemCreate, ItemUpdate

logger = get_logger(__name__)


class ItemService:
    """Service for managing item operations."""

    async def create_item(self, session: AsyncSession, item_data: ItemCreate) -> Item:
        """Create a new item.

        Args:
            session: Database session
            item_data: Item creation data

        Returns:
            The created item
        """
        item_id = str(uuid.uuid4())
        now = datetime.now(UTC)

        item = Item(
            id=item_id,
            name=item_data.name,
            description=item_data.description,
            price=item_data.price,
            is_available=item_data.is_available,
            meta=item_data.meta,
            created_at=now,
            updated_at=now,
        )

        session.add(item)
        await session.commit()
        await session.refresh(item)

        logger.info("Item created", item_id=item_id, item_name=item.name)

        return item

    async def get_item(self, session: AsyncSession, item_id: str) -> Item:
        """Get an item by ID.

        Args:
            session: Database session
            item_id: The item ID

        Returns:
            The requested item

        Raises:
            NotFoundError: If the item is not found
        """
        item = await session.get(Item, item_id)

        if not item:
            logger.warning("Item not found", item_id=item_id)
            raise NotFoundError(
                message=f"Item with id '{item_id}' not found",
                details={"item_id": item_id},
            )

        logger.debug("Item retrieved", item_id=item_id)

        return item

    async def list_items(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        available_only: bool = False,
    ) -> list[Item]:
        """List all items with optional filtering and pagination.

        Args:
            session: Database session
            skip: Number of items to skip (for pagination)
            limit: Maximum number of items to return
            available_only: If True, only return available items

        Returns:
            List of items
        """
        query = select(Item)

        if available_only:
            query = query.where(Item.is_available == True)  # noqa: E712

        # Sort by created_at descending (newest first)
        query = query.order_by(col(Item.created_at).desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await session.exec(query)
        items = list(result.all())

        logger.debug(
            "Items listed",
            returned_count=len(items),
            skip=skip,
            limit=limit,
            available_only=available_only,
        )

        return items

    async def update_item(
        self, session: AsyncSession, item_id: str, item_data: ItemUpdate
    ) -> Item:
        """Update an existing item.

        Args:
            session: Database session
            item_id: The item ID
            item_data: Item update data (only provided fields will be updated)

        Returns:
            The updated item

        Raises:
            NotFoundError: If the item is not found
        """
        item = await self.get_item(session, item_id)

        # Update only the provided fields
        update_data = item_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        # Update the timestamp
        item.updated_at = datetime.now(UTC)

        session.add(item)
        await session.commit()
        await session.refresh(item)

        logger.info("Item updated", item_id=item_id, updated_fields=list(update_data.keys()))

        return item

    async def delete_item(self, session: AsyncSession, item_id: str) -> None:
        """Delete an item.

        Args:
            session: Database session
            item_id: The item ID

        Raises:
            NotFoundError: If the item is not found
        """
        item = await self.get_item(session, item_id)

        await session.delete(item)
        await session.commit()

        logger.info("Item deleted", item_id=item_id)

    async def get_item_count(self, session: AsyncSession, available_only: bool = False) -> int:
        """Get the total count of items.

        Args:
            session: Database session
            available_only: If True, only count available items

        Returns:
            Total number of items
        """
        query = select(func.count()).select_from(Item)

        if available_only:
            query = query.where(Item.is_available == True)  # noqa: E712

        result = await session.exec(query)
        count = result.one()

        logger.debug("Item count retrieved", count=count, available_only=available_only)

        return count


# Global service instance
item_service = ItemService()


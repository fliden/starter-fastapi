"""Item service containing business logic for item operations."""

import uuid
from datetime import datetime, timezone

from starter_fastapi.core.exceptions import NotFoundError
from starter_fastapi.core.logging import get_logger
from starter_fastapi.models.item import Item, ItemCreate, ItemUpdate

logger = get_logger(__name__)


class ItemService:
    """Service for managing item operations.

    This is a simple in-memory implementation for demonstration purposes.
    In a production application, this would interact with a database.
    """

    def __init__(self) -> None:
        """Initialize the service with an in-memory storage."""
        self._items: dict[str, Item] = {}

    async def create_item(self, item_data: ItemCreate) -> Item:
        """Create a new item.

        Args:
            item_data: Item creation data

        Returns:
            The created item
        """
        item_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        item = Item(
            id=item_id,
            name=item_data.name,
            description=item_data.description,
            price=item_data.price,
            is_available=item_data.is_available,
            metadata=item_data.metadata,
            created_at=now,
            updated_at=now,
        )

        self._items[item_id] = item

        logger.info("Item created", item_id=item_id, item_name=item.name)

        return item

    async def get_item(self, item_id: str) -> Item:
        """Get an item by ID.

        Args:
            item_id: The item ID

        Returns:
            The requested item

        Raises:
            NotFoundError: If the item is not found
        """
        item = self._items.get(item_id)

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
        skip: int = 0,
        limit: int = 100,
        available_only: bool = False,
    ) -> list[Item]:
        """List all items with optional filtering and pagination.

        Args:
            skip: Number of items to skip (for pagination)
            limit: Maximum number of items to return
            available_only: If True, only return available items

        Returns:
            List of items
        """
        items = list(self._items.values())

        if available_only:
            items = [item for item in items if item.is_available]

        # Sort by created_at descending (newest first)
        items.sort(key=lambda x: x.created_at, reverse=True)

        # Apply pagination
        items = items[skip : skip + limit]

        logger.debug(
            "Items listed",
            total_count=len(self._items),
            returned_count=len(items),
            skip=skip,
            limit=limit,
            available_only=available_only,
        )

        return items

    async def update_item(self, item_id: str, item_data: ItemUpdate) -> Item:
        """Update an existing item.

        Args:
            item_id: The item ID
            item_data: Item update data (only provided fields will be updated)

        Returns:
            The updated item

        Raises:
            NotFoundError: If the item is not found
        """
        item = await self.get_item(item_id)

        # Update only the provided fields
        update_data = item_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        # Update the timestamp
        item.updated_at = datetime.now(timezone.utc)

        self._items[item_id] = item

        logger.info("Item updated", item_id=item_id, updated_fields=list(update_data.keys()))

        return item

    async def delete_item(self, item_id: str) -> None:
        """Delete an item.

        Args:
            item_id: The item ID

        Raises:
            NotFoundError: If the item is not found
        """
        if item_id not in self._items:
            logger.warning("Attempt to delete non-existent item", item_id=item_id)
            raise NotFoundError(
                message=f"Item with id '{item_id}' not found",
                details={"item_id": item_id},
            )

        del self._items[item_id]

        logger.info("Item deleted", item_id=item_id)

    async def get_item_count(self, available_only: bool = False) -> int:
        """Get the total count of items.

        Args:
            available_only: If True, only count available items

        Returns:
            Total number of items
        """
        if available_only:
            count = sum(1 for item in self._items.values() if item.is_available)
        else:
            count = len(self._items)

        logger.debug("Item count retrieved", count=count, available_only=available_only)

        return count


# Global service instance
item_service = ItemService()

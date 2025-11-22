"""Item models for request/response validation."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ItemBase(BaseModel):
    """Base item model with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    is_available: bool = Field(default=True, description="Item availability status")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean the name field."""
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        """Validate and clean the description field."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class ItemCreate(ItemBase):
    """Model for creating a new item."""

    pass


class ItemUpdate(BaseModel):
    """Model for updating an existing item.

    All fields are optional to support partial updates.
    """

    name: str | None = Field(None, min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float | None = Field(None, gt=0, description="Item price (must be positive)")
    is_available: bool | None = Field(None, description="Item availability status")
    metadata: dict[str, Any] | None = Field(None, description="Additional metadata")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """Validate and clean the name field."""
        if v is not None:
            return v.strip()
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        """Validate and clean the description field."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class Item(ItemBase):
    """Complete item model with all fields including database fields."""

    id: str = Field(..., description="Unique item identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Example Item",
                    "description": "This is an example item",
                    "price": 29.99,
                    "is_available": True,
                    "metadata": {"category": "electronics", "tags": ["new", "featured"]},
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z",
                }
            ]
        }
    }

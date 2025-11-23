"""Main router for API version 1."""

from fastapi import APIRouter

from starter_fastapi.api.v1.endpoints import items

# Create the main v1 router
router = APIRouter()

# Include endpoint routers
router.include_router(items.router, prefix="/items", tags=["items"])

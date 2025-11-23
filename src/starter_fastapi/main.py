"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from starter_fastapi.api.v1 import router as v1_router
from starter_fastapi.api.v1.endpoints import health
from starter_fastapi.core.config import settings
from starter_fastapi.core.exceptions import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
)
from starter_fastapi.core.logging import get_logger, setup_logging

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager.

    This function is called when the application starts up and shuts down.
    Use it for setup and teardown tasks like database connections, etc.

    Args:
        app: The FastAPI application instance

    Yields:
        None
    """
    # Startup
    logger.info(
        "Starting application",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

    # Add startup tasks here (database connections, cache initialization, etc.)

    yield

    # Shutdown
    logger.info("Shutting down application")

    # Add shutdown tasks here (close database connections, cleanup, etc.)


# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, generic_exception_handler)


# Include API routers
app.include_router(v1_router, prefix=settings.api_v1_prefix)
app.include_router(health.router, tags=["health"])


@app.get("/", include_in_schema=False)
async def root() -> JSONResponse:
    """Root endpoint redirecting to documentation.

    Returns:
        JSON response with API information
    """
    return JSONResponse(
        content={
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "starter_fastapi.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )

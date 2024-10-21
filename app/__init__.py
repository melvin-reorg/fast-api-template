"""
This module initializes the FastAPI application with necessary configurations,
middlewares, and routes.

Modules:
    contextlib: Provides utilities for working with context managers.
    fastapi: FastAPI framework for building APIs.
    anyio: Provides asynchronous I/O capabilities.
    app.middleware.logger: Custom logging middleware.
    .utils.headers: Utility for injecting default headers.
    .core.config: Configuration settings for the application.
    .api: API routes.
    .utils.logger: Logger utility.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from anyio import to_thread
from app.middleware.logger import LogMiddleware
from .utils.headers import default_headers_injection
from .core.config import get_app_config
from .api import router
from .utils.logger import logger

# Load application configuration
app_config = get_app_config()

# API prefix
API_PREFIX = "/api"


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.

    Args:
        _: FastAPI instance (unused).

    Yields:
        None
    """
    # Startup code
    logger.info("Starting up")

    # Configure thread pool limiter
    limiter = to_thread.current_default_thread_limiter()
    limiter.total_tokens = 1000

    # Yield control back to FastAPI
    yield

    # Shutdown code
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title=app_config.APP_TITLE_,
        version=app_config.APP_VERSION_,
        docs_url=app_config.DOCS_URL_,
        openapi_url=app_config.OPEN_API_URL_,
        lifespan=lifespan,
    )

    # Include API router with prefix and dependencies
    app.include_router(
        router=router,
        prefix=f"{API_PREFIX}/{app_config.API_VERSION_}",
        dependencies=[Depends(default_headers_injection)],
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.CORS_ORIGIN_,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom logging middleware
    app.add_middleware(LogMiddleware)

    return app

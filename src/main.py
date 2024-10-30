"""Main module for the FastAPI Starter Template application.

This module sets up the FastAPI application, including middleware,
routers, and event handlers for startup and shutdown.
"""

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.auth.router import router as auth_router
from src.core.exceptions import add_exception_handlers
from src.core.logging import logger
from src.database.database import Base, engine
from src.items.router import router as items_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Application started")

    yield

    # Shutdown
    logger.info("Application shutting down")


app = FastAPI(
    title="FastAPI Starter Template",
    description=(
        "A modular monolithic starter template for FastAPI with async SQLAlchemy, "
        "JWT authentication, and more."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(items_router, prefix="/api", tags=["Items"])

# Add exception handlers
add_exception_handlers(app)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the FastAPI Starter Template"}


def custom_openapi():
    """Generate a custom OpenAPI schema for the application.

    Returns:
        dict: The custom OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Starter Template API",
        version="0.1.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

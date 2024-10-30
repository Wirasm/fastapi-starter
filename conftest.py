"""Pytest configuration and fixtures for the FastAPI Starter Template.

This module contains pytest fixtures that can be used across multiple test files.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database.database import Base, get_db
from src.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:54321/test_db"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a new database session for a test."""
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with async_session() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture
async def client(test_session) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with a test database session."""

    async def override_get_db():
        try:
            yield test_session
        finally:
            await test_session.close()

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def authenticated_client(
    client: AsyncClient,
) -> AsyncGenerator[AsyncClient, None]:
    """Create an authenticated test client."""
    # Register a test user
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )

    # Login and get token
    response = await client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "testpassword123"},
    )
    token = response.json()["access_token"]

    # Create a new client with authentication headers
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    ) as auth_client:
        yield auth_client


@pytest.fixture
async def test_item(authenticated_client: AsyncClient) -> dict:
    """Create a test item and return its data."""
    response = await authenticated_client.post(
        "/api/items",
        json={"name": "Test Item", "description": "Test Description"},
    )
    return response.json()

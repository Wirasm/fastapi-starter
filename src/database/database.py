"""
Module for database configuration and session management.

This module sets up the database connection, creates the engine,
and provides a function to get database sessions.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    """
    Dependency function to get a database session.

    This function creates a new AsyncSession for each request,
    and ensures that the session is closed after the request is completed.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

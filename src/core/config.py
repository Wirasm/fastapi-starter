"""
Core configuration module.

This module handles loading environment variables for the entire application.
It ensures consistent configuration across all parts of the application.
"""

import os
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
print(f"Project root: {PROJECT_ROOT}")

# Load environment variables from .env file
env_file = PROJECT_ROOT / ".env"
print(f"Loading environment from: {env_file} (exists: {env_file.exists()})")

# First, print current env vars before loading
print("\nBefore loading .env:")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"DEV_DATABASE_URL: {os.getenv('DEV_DATABASE_URL')}")

# Load the .env file
load_dotenv(env_file, override=True)

# Print env vars after loading to verify
print("\nAfter loading .env:")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"DEV_DATABASE_URL: {os.getenv('DEV_DATABASE_URL')}")


@lru_cache()
def get_database_url() -> str:
    """Get the database URL from environment variables.

    Returns:
        str: The database URL to use for the application.
    """
    database_url = os.getenv("DATABASE_URL") or os.getenv("DEV_DATABASE_URL")
    if not database_url:
        raise ValueError("No database URL configured. Check your .env file.")
    print(f"\nReturning database URL: {database_url}")
    return database_url


# Export commonly used configuration
DATABASE_URL = get_database_url()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

"""Module containing the User model for authentication.

This module defines the User model which represents the users table in the database.
"""

import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.database.models import BaseModel


class User(BaseModel):
    """User model representing a user in the system.

    Attributes:
        id (UUID): The unique identifier for the user.
        email (str): The user's email address (unique).
        hashed_password (str): The hashed password of the user.
        is_active (bool): Indicates whether the user account is active.
        is_superuser (bool): Indicates whether the user has superuser privileges.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

"""Module containing the Item model for the items in the application.

This module defines the Item model which represents the items table in the database.
"""

import uuid

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.database.models import BaseModel


class Item(BaseModel):
    """Item model representing an item in the system.

    Attributes:
        id (UUID): The unique identifier for the item.
        name (str): The name of the item.
        description (str): A detailed description of the item.
        is_active (bool): Indicates whether the item is active or not.
    """

    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

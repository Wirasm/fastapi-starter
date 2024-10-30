"""Module for base database model.

This module defines the BaseModel class which serves as the base
for all other database models in the application.
"""

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from .database import Base


class BaseModel(Base):
    """Base model class for all database models.

    This class provides common fields and functionality that will be
    inherited by all other database model classes in the application.

    Attributes:
        id (int): Primary key for the model.
        created_at (datetime): Timestamp for when the record was created.
        updated_at (datetime): Timestamp for when the record was last updated.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

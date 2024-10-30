"""Module containing Pydantic schemas for the items in the application.

This module defines the Pydantic models used for data validation and serialization
for item-related operations.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4


class ItemCreate(BaseModel):
    """Pydantic model for creating a new item.

    Attributes:
        name (str): The name of the item.
        description (Optional[str]): An optional description of the item.
    """

    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    """Pydantic model for updating an existing item.

    Attributes:
        name (Optional[str]): The updated name of the item.
        description (Optional[str]): The updated description of the item.
        is_active (Optional[bool]): The updated active status of the item.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ItemOut(BaseModel):
    """Pydantic model for outputting item information.

    Attributes:
        id (UUID4): The unique identifier of the item.
        name (str): The name of the item.
        description (Optional[str]): The description of the item.
        is_active (bool): The active status of the item.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str
    description: Optional[str]
    is_active: bool

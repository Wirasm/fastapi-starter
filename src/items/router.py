"""Module for handling item-related routes in the application."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_active_user
from src.auth.models import User
from src.database.database import get_db

from .models import Item
from .schemas import ItemCreate, ItemOut, ItemUpdate

router = APIRouter()


@router.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new item."""
    try:
        db_item = Item(**item.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the item: {str(e)}",
        ) from e


@router.get("/items", response_model=List[ItemOut])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve a list of items."""
    try:
        query = select(Item).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving items: {str(e)}",
        ) from e


@router.get("/items/{item_id}", response_model=ItemOut)
async def read_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve a specific item by ID."""
    try:
        query = select(Item).where(Item.id == item_id)
        result = await db.execute(query)
        db_item = result.scalar_one_or_none()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the item: {str(e)}",
        ) from e


@router.put("/items/{item_id}", response_model=ItemOut)
async def update_item(
    item_id: UUID,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an existing item."""
    try:
        query = select(Item).where(Item.id == item_id)
        result = await db.execute(query)
        db_item = result.scalar_one_or_none()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)

        await db.commit()
        await db.refresh(db_item)
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the item: {str(e)}",
        ) from e


@router.delete("/items/{item_id}", response_model=ItemOut)
async def delete_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an item."""
    try:
        query = select(Item).where(Item.id == item_id)
        result = await db.execute(query)
        db_item = result.scalar_one_or_none()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        await db.delete(db_item)
        await db.commit()
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the item: {str(e)}",
        ) from e

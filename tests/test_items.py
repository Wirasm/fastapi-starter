"""Tests for item-related endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_item(authenticated_client: AsyncClient):
    """Test creating a new item."""
    response = await authenticated_client.post(
        "/api/items",
        json={"name": "New Item", "description": "New Description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Item"
    assert data["description"] == "New Description"
    assert data["is_active"] is True
    assert "id" in data


async def test_create_item_no_auth(client: AsyncClient):
    """Test creating an item without authentication."""
    response = await client.post(
        "/api/items",
        json={"name": "New Item", "description": "New Description"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


async def test_read_items(authenticated_client: AsyncClient, test_item: dict):
    """Test retrieving a list of items."""
    response = await authenticated_client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["id"] == test_item["id"] for item in data)


async def test_read_items_pagination(authenticated_client: AsyncClient):
    """Test items list pagination."""
    # Create multiple items
    for i in range(5):
        await authenticated_client.post(
            "/api/items",
            json={"name": f"Item {i}", "description": f"Description {i}"},
        )

    # Test pagination
    response = await authenticated_client.get("/api/items?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


async def test_read_item(authenticated_client: AsyncClient, test_item: dict):
    """Test retrieving a specific item."""
    response = await authenticated_client.get(f"/api/items/{test_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item["id"]
    assert data["name"] == test_item["name"]
    assert data["description"] == test_item["description"]


async def test_read_item_not_found(authenticated_client: AsyncClient):
    """Test retrieving a non-existent item."""
    response = await authenticated_client.get(
        "/api/items/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


async def test_update_item(authenticated_client: AsyncClient, test_item: dict):
    """Test updating an item."""
    response = await authenticated_client.put(
        f"/api/items/{test_item['id']}",
        json={
            "name": "Updated Name",
            "description": "Updated Description",
            "is_active": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item["id"]
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Description"
    assert data["is_active"] is False


async def test_update_item_partial(authenticated_client: AsyncClient, test_item: dict):
    """Test partial update of an item."""
    response = await authenticated_client.put(
        f"/api/items/{test_item['id']}", json={"name": "Only Name Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item["id"]
    assert data["name"] == "Only Name Updated"
    assert data["description"] == test_item["description"]  # Unchanged


async def test_update_item_not_found(authenticated_client: AsyncClient):
    """Test updating a non-existent item."""
    response = await authenticated_client.put(
        "/api/items/00000000-0000-0000-0000-000000000000",
        json={"name": "New Name"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


async def test_delete_item(authenticated_client: AsyncClient, test_item: dict):
    """Test deleting an item."""
    # Delete the item
    response = await authenticated_client.delete(f"/api/items/{test_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item["id"]

    # Verify item is deleted
    response = await authenticated_client.get(f"/api/items/{test_item['id']}")
    assert response.status_code == 404


async def test_delete_item_not_found(authenticated_client: AsyncClient):
    """Test deleting a non-existent item."""
    response = await authenticated_client.delete(
        "/api/items/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


async def test_create_item_invalid_data(authenticated_client: AsyncClient):
    """Test creating an item with invalid data."""
    response = await authenticated_client.post("/api/items", json={})
    assert response.status_code == 422  # Validation error


async def test_update_item_invalid_data(
    authenticated_client: AsyncClient, test_item: dict
):
    """Test updating an item with invalid data."""
    response = await authenticated_client.put(
        f"/api/items/{test_item['id']}",
        json={"name": ["invalid"]},  # name should be a string
    )
    assert response.status_code == 422  # Validation error

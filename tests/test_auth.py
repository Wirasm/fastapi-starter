"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_user(client):
    """Test user registration."""
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True
    assert data["is_superuser"] is False


async def test_register_duplicate_email(client):
    """Test registration with an email that's already registered."""
    # First registration
    await client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "testpassword123"},
    )

    # Attempt duplicate registration
    response = await client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


async def test_login_success(client):
    """Test successful login."""
    # Register a user first
    await client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "testpassword123"},
    )

    # Attempt login
    response = await client.post(
        "/auth/token",
        data={"username": "login@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = await client.post(
        "/auth/token",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


async def test_get_current_user(client):
    """Test getting current user information."""
    # Register and login a user
    await client.post(
        "/auth/register",
        json={"email": "me@example.com", "password": "testpassword123"},
    )
    login_response = await client.post(
        "/auth/token",
        data={"username": "me@example.com", "password": "testpassword123"},
    )
    token = login_response.json()["access_token"]

    # Get user info
    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["is_active"] is True


async def test_get_current_user_invalid_token(client):
    """Test getting user info with invalid token."""
    response = await client.get(
        "/auth/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


async def test_get_current_user_no_token(client):
    """Test getting user info without token."""
    response = await client.get("/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

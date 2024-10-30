"""Module for JWT token handling."""

from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr

from src.core.config import JWT_ALGORITHM, JWT_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model."""

    email: Optional[EmailStr] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new access token.

    Args:
        data: The data to encode in the token.
        expires_delta: Optional expiration time delta.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token.

    Args:
        token: The token to verify.

    Returns:
        TokenData: The decoded token data.

    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(email=email)
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    return token_data

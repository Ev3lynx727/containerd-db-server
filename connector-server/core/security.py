"""
Security utilities for the database connector API.
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    """JWT Token model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model."""
    client_id: Optional[str] = None
    scopes: list[str] = []


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        client_id = payload.get("sub")
        scopes: list = payload.get("scopes", [])
        if client_id is None:
            raise credentials_exception
        token_data = TokenData(client_id=str(client_id), scopes=scopes)
    except JWTError:
        raise credentials_exception
    return token_data


def generate_api_key() -> str:
    """Generate a secure API key."""
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage."""
    import hashlib
    return hashlib.sha256(api_key.encode()).hexdigest()


def validate_api_key_format(api_key: str) -> bool:
    """Validate API key format."""
    import re
    # API keys should be alphanumeric, 32-64 characters
    return bool(re.match(r'^[a-zA-Z0-9]{32,64}$', api_key))

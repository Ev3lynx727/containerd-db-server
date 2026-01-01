"""
API key management functionality.
"""
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.api_key import ApiKey


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def create_api_key(
    db: Session,
    client_id: str,
    scopes: List[str] = None,
    expires_days: int = 365,
    rate_limit: int = 1000
) -> tuple[str, ApiKey]:
    """Create a new API key."""
    import secrets
    import string

    # Generate random API key
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for _ in range(32))

    # Hash for storage
    key_hash = hash_api_key(api_key)

    # Generate key ID (first 8 chars of hash)
    key_id = key_hash[:8]

    expires_at = datetime.utcnow() + timedelta(days=expires_days)

    db_api_key = ApiKey(
        key_id=key_id,
        key_hash=key_hash,
        client_id=client_id,
        scopes=scopes or [],
        expires_at=expires_at,
        rate_limit=rate_limit,
        is_active=True
    )

    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    return api_key, db_api_key


def verify_api_key(db: Session, api_key: str) -> Optional[ApiKey]:
    """Verify an API key."""
    key_hash = hash_api_key(api_key)
    api_key_obj = db.query(ApiKey).filter(
        ApiKey.key_hash == key_hash,
        ApiKey.is_active == True,
        ApiKey.expires_at > datetime.utcnow()
    ).first()

    if api_key_obj:
        # Update last used
        api_key_obj.last_used = datetime.utcnow()
        db.commit()

    return api_key_obj


def get_api_keys(db: Session, client_id: str = None, skip: int = 0, limit: int = 100) -> List[ApiKey]:
    """Get list of API keys."""
    query = db.query(ApiKey)
    if client_id:
        query = query.filter(ApiKey.client_id == client_id)
    return query.offset(skip).limit(limit).all()


def revoke_api_key(db: Session, key_id: str) -> bool:
    """Revoke an API key."""
    api_key = db.query(ApiKey).filter(ApiKey.key_id == key_id).first()
    if not api_key:
        return False

    api_key.is_active = False
    db.commit()
    return True


def update_api_key_rate_limit(db: Session, key_id: str, rate_limit: int) -> bool:
    """Update API key rate limit."""
    api_key = db.query(ApiKey).filter(ApiKey.key_id == key_id).first()
    if not api_key:
        return False

    api_key.rate_limit = rate_limit
    db.commit()
    return True
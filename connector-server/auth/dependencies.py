"""
FastAPI dependencies for authentication and authorization.
"""
from typing import List

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..auth.api_keys import verify_api_key
from ..models.api_key import ApiKey


security = HTTPBearer(auto_error=False)


async def get_api_key(
    request: Request,
    db: Session = Depends(get_db)
) -> ApiKey:
    """Extract and verify API key from request headers."""
    api_key_header = request.headers.get("X-API-Key")

    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    api_key_obj = verify_api_key(db, api_key_header)
    if not api_key_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return api_key_obj


def check_scopes(required_scopes: List[str]):
    """Create a dependency to check if API key has required scopes."""

    def scope_checker(api_key: ApiKey = Depends(get_api_key)) -> ApiKey:
        """Check if API key has required scopes."""
        if not all(scope in api_key.scopes for scope in required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required scopes: {required_scopes}",
            )
        return api_key

    return scope_checker


def rate_limit_check(api_key: ApiKey = Depends(get_api_key)):
    """Check rate limit for API key."""
    # This would typically integrate with Redis for rate limiting
    # For now, just return the API key
    return api_key


# Pre-configured dependencies
require_read_scope = check_scopes(["read"])
require_write_scope = check_scopes(["write"])
require_admin_scope = check_scopes(["admin"])
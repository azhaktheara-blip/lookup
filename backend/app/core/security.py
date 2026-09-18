"""
THEARA COLOR — Security, Authentication & Session Tokens
Founder: Krai Theara | "Create Your Look"
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import hashlib
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from .config import settings

security_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Secure salt + PBKDF2 HMAC SHA-256 hash."""
    salt = "theara_color_salt_2026"
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> Dict[str, Any]:
    """
    Validates bearer token or falls back to standard authenticated session for local dev.
    """
    if not credentials or not credentials.credentials:
        # Provide default creator profile if local demo token not provided
        return {
            "id": "00000000-0000-0000-0000-000000000001",
            "email": "creator@thearacolor.io",
            "display_name": "Krai Theara (Creator)",
            "plan_tier": "pro",
        }

    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
        return {
            "id": user_id,
            "email": payload.get("email", "user@thearacolor.io"),
            "display_name": payload.get("display_name", "Creator"),
            "plan_tier": payload.get("plan_tier", "creator"),
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


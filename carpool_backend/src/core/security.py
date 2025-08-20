import hashlib
import hmac
import base64
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Callable

from fastapi import HTTPException, status
from src.core.config import get_settings
from src.db.memory import db
from src.models.enums import UserRole
from src.models.user import UserPublic


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Simple salted password hashing using SHA-256 (placeholder, not for production)."""
    settings = get_settings()
    salted = (settings.secret_key + password).encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


# PUBLIC_INTERFACE
def verify_password(password: str, hashed: str) -> bool:
    """Verify plaintext password against hash."""
    calc = hash_password(password)
    return hmac.compare_digest(calc, hashed)


# PUBLIC_INTERFACE
def create_access_token(sub: str, expires_minutes: Optional[int] = None) -> str:
    """Create a signed access token (simple HS256-like placeholder)."""
    settings = get_settings()
    header = {"alg": "HS256", "typ": "JWT"}
    exp_minutes = expires_minutes or settings.access_token_expire_minutes
    payload = {
        "sub": sub,
        "exp": int((datetime.utcnow() + timedelta(minutes=exp_minutes)).timestamp()),
        "iat": int(datetime.utcnow().timestamp()),
        "iss": settings.app_name,
    }
    header_b64 = _b64encode(json.dumps(header).encode())
    payload_b64 = _b64encode(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(settings.secret_key.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


# PUBLIC_INTERFACE
def decode_access_token(token: str) -> Optional[Dict]:
    """Decode and verify a token. Returns payload dict if valid, otherwise None."""
    try:
        settings = get_settings()
        header_b64, payload_b64, signature_b64 = token.split(".")
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(settings.secret_key.encode(), signing_input, hashlib.sha256).digest()
        actual_sig = _b64decode(signature_b64)
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
        payload = json.loads(_b64decode(payload_b64).decode())
        # Expiry check
        if "exp" in payload and int(payload["exp"]) < int(datetime.utcnow().timestamp()):
            return None
        return payload
    except Exception:
        return None


# PUBLIC_INTERFACE
def get_current_user_from_token(token: Optional[str]) -> Optional[UserPublic]:
    """Decode token and return current UserPublic if valid."""
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    uid = payload.get("sub")
    user = db.get_user(uid)
    if not user:
        return None
    return UserPublic(id=user.id, email=user.email, full_name=user.full_name, role=user.role)


# PUBLIC_INTERFACE
def require_auth(token: Optional[str] = None) -> UserPublic:
    """FastAPI dependency-like helper to enforce authentication using token query for MVP."""
    user = get_current_user_from_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


# PUBLIC_INTERFACE
def require_role(required: UserRole) -> Callable[..., UserPublic]:
    """Return a callable that enforces the given role."""
    def _inner(token: Optional[str] = None) -> UserPublic:
        user = require_auth(token)
        if user.role != required:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return _inner

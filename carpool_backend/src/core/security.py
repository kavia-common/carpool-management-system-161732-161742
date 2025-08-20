import hashlib
import hmac
import base64
import json
from datetime import datetime, timedelta
from typing import Optional, Dict

from src.core.config import get_settings


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

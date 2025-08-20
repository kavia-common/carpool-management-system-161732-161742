from fastapi import APIRouter, HTTPException
from fastapi import status
from typing import Optional

from src.db.memory import db
from src.core.security import verify_password, create_access_token, get_current_user_from_token
from src.models.user import AuthToken, LoginRequest, MeResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=AuthToken, summary="Login", description="Authenticate a user and get an access token.")
def login(payload: LoginRequest) -> AuthToken:
    """
    Authenticate a user by email and password and return a bearer token.
    """
    found = db.get_user_by_email(payload.email)
    if not found:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user, password_hash = found
    if not verify_password(payload.password, password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user.id)
    return AuthToken(access_token=token)


@router.get("/me", response_model=MeResponse, summary="Get current user", description="Return the current authenticated user's profile.")
def me(token: Optional[str] = None) -> MeResponse:
    """
    Return the current authenticated user's profile based on provided token query param.
    Note: for demo: pass ?token={access_token}. In production, use Authorization header.
    """
    user = get_current_user_from_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return MeResponse(**user.model_dump())

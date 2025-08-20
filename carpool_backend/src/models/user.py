from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from src.models.enums import UserRole
from src.models.common import EntityMeta


class UserBase(BaseModel):
    """Base fields for a user."""
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., description="Full name of the user")
    role: UserRole = Field(..., description="Role of the user")


class UserCreate(UserBase):
    """Payload for creating a new user."""
    password: str = Field(..., min_length=6, description="Password for the user")


class UserUpdate(BaseModel):
    """Payload for updating user details."""
    full_name: Optional[str] = Field(None, description="Updated full name")
    role: Optional[UserRole] = Field(None, description="Updated role")
    password: Optional[str] = Field(None, min_length=6, description="Updated password")


class User(UserBase):
    """User entity returned to clients."""
    id: str = Field(..., description="User ID")
    meta: EntityMeta = Field(default_factory=EntityMeta, description="Metadata timestamps")


class UserPublic(BaseModel):
    """Public view of a user (no sensitive data)."""
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., description="Full name of the user")
    role: UserRole = Field(..., description="Role of the user")


class AuthToken(BaseModel):
    """Authentication token response."""
    access_token: str = Field(..., description="Access token (JWT or placeholder)")
    token_type: str = Field(default="bearer", description="Token type")


class LoginRequest(BaseModel):
    """Login request payload."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


class MeResponse(UserPublic):
    """Response for /me endpoint."""
    pass

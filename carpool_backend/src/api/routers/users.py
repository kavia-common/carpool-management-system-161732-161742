from typing import List
from fastapi import APIRouter, HTTPException, status
from src.services.users_service import users_service
from src.models.user import UserCreate, UserUpdate, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED, summary="Create user", description="Create a new user.")
def create_user(payload: UserCreate) -> UserPublic:
    """Create a user."""
    user = users_service.create_user(payload)
    return UserPublic(id=user.id, email=user.email, full_name=user.full_name, role=user.role)


@router.get("", response_model=List[UserPublic], summary="List users", description="List all users.")
def list_users() -> List[UserPublic]:
    """List users."""
    return [UserPublic(id=u.id, email=u.email, full_name=u.full_name, role=u.role) for u in users_service.list_users()]


@router.get("/{user_id}", response_model=UserPublic, summary="Get user", description="Get a user by ID.")
def get_user(user_id: str) -> UserPublic:
    """Get a specific user."""
    u = users_service.get_user(user_id)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserPublic(id=u.id, email=u.email, full_name=u.full_name, role=u.role)


@router.put("/{user_id}", response_model=UserPublic, summary="Update user", description="Update user details.")
def update_user(user_id: str, payload: UserUpdate) -> UserPublic:
    """Update user."""
    u = users_service.update_user(user_id, payload)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserPublic(id=u.id, email=u.email, full_name=u.full_name, role=u.role)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user", description="Delete a user.")
def delete_user(user_id: str) -> None:
    """Delete user."""
    ok = users_service.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

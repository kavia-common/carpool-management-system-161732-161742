from typing import List, Optional

from src.db.memory import db
from src.models.user import User, UserCreate, UserUpdate
from src.core.security import hash_password


class UsersService:
    """Service providing user-related operations."""

    # PUBLIC_INTERFACE
    def create_user(self, payload: UserCreate) -> User:
        """Create a user with hashed password."""
        password_hash = hash_password(payload.password)
        return db.create_user(payload, password_hash)

    # PUBLIC_INTERFACE
    def update_user(self, user_id: str, payload: UserUpdate) -> Optional[User]:
        """Update a user and optionally password."""
        new_hash = hash_password(payload.password) if payload.password else None
        return db.update_user(user_id, payload, new_hash)

    # PUBLIC_INTERFACE
    def list_users(self) -> List[User]:
        """List all users."""
        return db.list_users()

    # PUBLIC_INTERFACE
    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return db.get_user(user_id)

    # PUBLIC_INTERFACE
    def delete_user(self, user_id: str) -> bool:
        """Delete user by ID."""
        return db.delete_user(user_id)


users_service = UsersService()

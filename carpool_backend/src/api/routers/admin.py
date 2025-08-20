from typing import Optional
from fastapi import APIRouter
from src.db.memory import db
from src.models.common import APIMessage
from src.models.enums import UserRole
from src.core.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/reset", response_model=APIMessage, summary="Reset in-memory DB", description="Reset the in-memory database to an empty state.")
def reset_db(token: Optional[str] = None) -> APIMessage:
    """Reset the in-memory store. Requires admin role.

    Usage note (MVP): pass ?token=<access_token> obtained from /auth/login
    """
    # Enforce that caller is admin
    require_role(UserRole.admin)(token)  # raises if unauthorized
    db.reset()
    return APIMessage(message="Database reset complete")

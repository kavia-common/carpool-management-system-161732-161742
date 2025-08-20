from typing import List, Optional
from fastapi import APIRouter
from src.services.notifications_service import notifications_service
from src.models.common import Notification
from src.models.enums import UserRole
from src.core.security import require_role, require_auth

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("", response_model=Notification, summary="Send notification", description="Send a notification to a user.")
def send_notification(user_id: str, title: str, body: str, token: Optional[str] = None) -> Notification:
    """Create and store a notification for a user. Requires admin."""
    require_role(UserRole.admin)(token)
    return notifications_service.send_notification(user_id=user_id, title=title, body=body)


@router.get("/{user_id}", response_model=List[Notification], summary="List notifications", description="List notifications for a user.")
def list_notifications(user_id: str, token: Optional[str] = None) -> List[Notification]:
    """List notifications for a user. Requires authentication."""
    require_auth(token)
    return notifications_service.list_notifications(user_id=user_id)

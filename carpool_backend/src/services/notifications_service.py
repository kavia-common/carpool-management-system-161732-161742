import uuid
from typing import List
from src.db.memory import db
from src.models.common import Notification


class NotificationsService:
    """Service for creating and listing notifications."""

    # PUBLIC_INTERFACE
    def send_notification(self, user_id: str, title: str, body: str) -> Notification:
        """Create a notification entry."""
        notif = Notification(id=str(uuid.uuid4()), user_id=user_id, title=title, body=body)
        return db.add_notification(notif)

    # PUBLIC_INTERFACE
    def list_notifications(self, user_id: str) -> List[Notification]:
        """List notifications for a user."""
        return db.list_notifications_for_user(user_id)


notifications_service = NotificationsService()

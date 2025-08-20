import uuid
import logging
from typing import List, Dict, Optional
from src.db.memory import db
from src.models.common import Notification

logger = logging.getLogger("notifications")


class NotificationsService:
    """Service for creating and listing notifications.

    This MVP implementation stores notifications in the in-memory DB and also
    emits a log entry to simulate an external provider call (no-op provider).
    """

    # PUBLIC_INTERFACE
    def send_notification(self, user_id: str, title: str, body: str) -> Notification:
        """Create a notification entry and log it to simulate delivery.

        This is a no-op/log provider: it doesn't call any external service.
        """
        notif = Notification(id=str(uuid.uuid4()), user_id=user_id, title=title, body=body)
        # Store for retrieval
        db.add_notification(notif)
        # Log the "delivery"
        logger.info("NOOP Notification sent | user_id=%s title=%s body=%s id=%s", user_id, title, body, notif.id)
        return notif

    # PUBLIC_INTERFACE
    def list_notifications(self, user_id: str) -> List[Notification]:
        """List notifications for a user."""
        return db.list_notifications_for_user(user_id)

    # PUBLIC_INTERFACE
    def test_send(self, target: Optional[str] = None) -> Dict[str, str]:
        """Send a test notification via the no-op provider.

        Parameters:
        - target: optional test target (e.g., email/phone/push token) for logging only.

        Returns:
        - dict with status and target echoed.
        """
        logger.info("NOOP Notification test ping | target=%s", target or "default")
        return {"status": "ok", "provider": "noop", "target": target or "default"}


notifications_service = NotificationsService()

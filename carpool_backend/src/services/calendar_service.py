from typing import List, Dict
from datetime import datetime, timedelta


class CalendarService:
    """Service responsible for calendar integrations and data."""

    # PUBLIC_INTERFACE
    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Return a placeholder list of upcoming events for the next `days` days."""
        now = datetime.utcnow()
        return [
            {
                "id": f"evt-{i}",
                "title": f"Practice Day {i}",
                "start": (now + timedelta(days=i)).isoformat(),
                "end": (now + timedelta(days=i, hours=2)).isoformat(),
                "location": "sports_club",
            }
            for i in range(1, days + 1)
        ]


calendar_service = CalendarService()

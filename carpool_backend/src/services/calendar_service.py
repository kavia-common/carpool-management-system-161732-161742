from typing import List, Dict, Optional
from datetime import datetime, timedelta


class CalendarService:
    """Service responsible for calendar integrations and data.
    
    This mock service keeps in-memory calendar connection sources per user and returns
    fabricated 'club' and 'ride' events for demonstration. No external calls are made.
    """

    def __init__(self) -> None:
        # user_id -> list of connected sources (strings/URLs)
        self._connections: Dict[str, List[str]] = {}

    # PUBLIC_INTERFACE
    def connect_source(self, user_id: str, source: str) -> Dict:
        """Connect a calendar source (URL or raw ICS string) for a user.
        
        For MVP, we just store the source string to simulate a connection and return a summary.
        """
        if not user_id:
            raise ValueError("user_id is required")
        if not source or not isinstance(source, str):
            raise ValueError("source must be a non-empty string (URL or ical payload)")
        self._connections.setdefault(user_id, [])
        # Avoid duplicates by simple presence check
        if source not in self._connections[user_id]:
            self._connections[user_id].append(source)
        return {
            "user_id": user_id,
            "connected_sources": len(self._connections[user_id]),
            "sources": self._connections[user_id][-3:],  # echo up to last 3 for debug
            "status": "connected",
        }

    # PUBLIC_INTERFACE
    def get_upcoming_events(self, days: int = 7, user_id: Optional[str] = None) -> List[Dict]:
        """Return placeholder upcoming events for the next `days` days.
        
        If a user_id is provided, include some mock 'ride' events and indicate if club sources are connected.
        """
        now = datetime.utcnow()

        # Base club events (shared)
        club_events = [
            {
                "id": f"club-{i}",
                "type": "club",
                "title": f"Club Practice #{i}",
                "start": (now + timedelta(days=i, hours=17)).isoformat(),
                "end": (now + timedelta(days=i, hours=19)).isoformat(),
                "location": "sports_club",
                "meta": {"category": "practice"},
            }
            for i in range(1, min(days, 7) + 1)
        ]

        # User-specific ride events (if user_id provided)
        ride_events: List[Dict] = []
        if user_id:
            # Fabricate 2 ride events in the next 'days' window.
            for j in range(1, min(days, 5), 2):
                ride_events.append(
                    {
                        "id": f"ride-{user_id}-{j}",
                        "type": "ride",
                        "title": "Carpool to Practice",
                        "start": (now + timedelta(days=j, hours=16)).isoformat(),
                        "end": (now + timedelta(days=j, hours=16, minutes=45)).isoformat(),
                        "location": "school",
                        "assigned_to": user_id,
                    }
                )
            # If user has connected club sources, annotate the first club event
            if self._connections.get(user_id):
                for evt in club_events[:1]:
                    evt["meta"]["source_connected"] = True
                    evt["meta"]["sources_count"] = len(self._connections[user_id])

        # Merge and sort by start time
        merged = club_events + ride_events
        merged.sort(key=lambda e: e.get("start", ""))

        # Trim to the requested window where start <= now + days
        window_end = now + timedelta(days=days)
        result = [
            e for e in merged
            if _parse_iso(e.get("start")) is not None and _parse_iso(e["start"]) <= window_end
        ]
        return result


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    """Helper to parse ISO strings safely."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


calendar_service = CalendarService()

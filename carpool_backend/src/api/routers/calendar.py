from typing import List, Dict, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from src.services.calendar_service import calendar_service
from src.core.security import require_auth

router = APIRouter(prefix="/calendar", tags=["Calendar"])


class CalendarSyncRequest(BaseModel):
    """Payload for connecting/syncing a calendar source for a user."""
    user_id: str = Field(..., description="User ID to associate the calendar with")
    source: str = Field(..., description="Calendar source. Can be a URL or raw iCal/ICS text")


class CalendarSyncResponse(BaseModel):
    """Response after connecting a calendar source."""
    user_id: str = Field(..., description="User ID")
    connected_sources: int = Field(..., description="Total number of connected sources for the user")
    sources: List[str] = Field(default_factory=list, description="Sample of recently added sources")
    status: str = Field(..., description="Connection status")


@router.post(
    "/sync",
    response_model=CalendarSyncResponse,
    summary="Connect calendar source",
    description="Accept a calendar source (URL/ical) and connect it to the user's calendar (mock adapter)."
)
def sync_calendar(payload: CalendarSyncRequest, token: Optional[str] = None) -> CalendarSyncResponse:
    """Connect a calendar source for the specified user. Requires authentication.
    
    MVP usage: pass ?token={access_token} as query.
    """
    # Ensure caller is authenticated; in a real system we'd compare user_id to current user or check admin.
    require_auth(token)
    result = calendar_service.connect_source(user_id=payload.user_id, source=payload.source)
    return CalendarSyncResponse(**result)


@router.get(
    "/events",
    response_model=List[Dict],
    summary="List upcoming events",
    description="Return upcoming calendar events for youth sporting clubs, optionally merged with user-specific ride events."
)
def get_events(
    days: int = Query(7, ge=1, le=30, description="Number of days to look ahead"),
    user_id: Optional[str] = Query(None, description="Optional user to include personalized ride events"),
) -> List[Dict]:
    """Get upcoming events for the next N days. If user_id is provided, includes mock ride events for that user."""
    return calendar_service.get_upcoming_events(days=days, user_id=user_id)

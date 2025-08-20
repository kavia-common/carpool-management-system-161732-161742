from typing import List, Dict
from fastapi import APIRouter, Query
from src.services.calendar_service import calendar_service

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/events", response_model=List[Dict], summary="List upcoming events", description="Return upcoming calendar events for youth sporting clubs.")
def get_events(days: int = Query(7, ge=1, le=30, description="Number of days to look ahead")) -> List[Dict]:
    """Get upcoming events for the next N days."""
    return calendar_service.get_upcoming_events(days=days)

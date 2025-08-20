from fastapi import APIRouter
from src.db.memory import db
from src.models.common import APIMessage

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/reset", response_model=APIMessage, summary="Reset in-memory DB", description="Reset the in-memory database to an empty state.")
def reset_db() -> APIMessage:
    """Reset the in-memory store."""
    db.reset()
    return APIMessage(message="Database reset complete")

from datetime import datetime
from pydantic import BaseModel, Field


class APIMessage(BaseModel):
    """Generic API message payload."""
    message: str = Field(..., description="Human-readable message")


class EntityMeta(BaseModel):
    """Common metadata for entities."""
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


class IDModel(BaseModel):
    """Base model with string ID field."""
    id: str = Field(..., description="Unique identifier")


class PaginatedResponse(BaseModel):
    """Generic pagination response wrapper."""
    total: int = Field(..., description="Total items available")
    items: list = Field(default_factory=list, description="Items on the current page")


class Notification(BaseModel):
    """Notification entity."""
    id: str = Field(..., description="Notification ID")
    user_id: str = Field(..., description="User to notify")
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification body")
    read: bool = Field(default=False, description="Has this notification been read")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")

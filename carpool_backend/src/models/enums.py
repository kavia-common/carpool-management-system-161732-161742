from enum import Enum


class UserRole(str, Enum):
    """Enumeration of user roles in the system."""
    admin = "admin"
    driver = "driver"
    parent = "parent"


class RideStatus(str, Enum):
    """Enumeration of ride status values."""
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class LocationPreset(str, Enum):
    """Common preset locations to select from."""
    home = "home"
    school = "school"
    sports_club = "sports_club"
    community_center = "community_center"
    custom = "custom"


class TimeSlotPreset(str, Enum):
    """Common preset time slots to select from."""
    morning_pickup = "morning_pickup"
    afternoon_dropoff = "afternoon_dropoff"
    evening_practice = "evening_practice"
    custom = "custom"

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.models.enums import RideStatus, LocationPreset, TimeSlotPreset
from src.models.common import EntityMeta


class Location(BaseModel):
    """Flexible location representation supporting presets and custom text."""
    preset: LocationPreset = Field(..., description="Preset location or 'custom'")
    custom_label: Optional[str] = Field(None, description="Custom location label when preset is 'custom'")
    address: Optional[str] = Field(None, description="Optional address details")


class TimeSlot(BaseModel):
    """Flexible time representation supporting presets and custom datetime."""
    preset: TimeSlotPreset = Field(..., description="Preset time slot or 'custom'")
    custom_time: Optional[datetime] = Field(None, description="Custom time when preset is 'custom'")


class RideOfferCreate(BaseModel):
    """Payload to create a ride offer by a driver/parent."""
    driver_id: str = Field(..., description="User ID of the offering driver")
    seats_available: int = Field(..., ge=1, description="Number of available seats")
    pickup_location: Location = Field(..., description="Pickup location")
    dropoff_location: Location = Field(..., description="Dropoff location")
    time_slot: TimeSlot = Field(..., description="Time of the ride")


class RideOffer(RideOfferCreate):
    """Ride offer entity."""
    id: str = Field(..., description="Ride offer ID")
    status: RideStatus = Field(default=RideStatus.pending, description="Ride status")
    meta: EntityMeta = Field(default_factory=EntityMeta, description="Metadata timestamps")


class RideRequestCreate(BaseModel):
    """Payload to create a ride request by a parent."""
    requester_id: str = Field(..., description="User ID of the requesting parent")
    seats_requested: int = Field(..., ge=1, description="Number of seats requested")
    from_location: Location = Field(..., description="Pickup location")
    to_location: Location = Field(..., description="Dropoff location")
    time_slot: TimeSlot = Field(..., description="Desired time of the ride")


class RideRequest(RideRequestCreate):
    """Ride request entity."""
    id: str = Field(..., description="Ride request ID")
    status: RideStatus = Field(default=RideStatus.pending, description="Request status")
    matched_offer_id: Optional[str] = Field(None, description="Matched ride offer ID if any")
    meta: EntityMeta = Field(default_factory=EntityMeta, description="Metadata timestamps")


class RidesMeta(BaseModel):
    """Static metadata for rides: available preset locations and time slots."""
    locations: List[LocationPreset] = Field(..., description="Available preset locations")
    time_slots: List[TimeSlotPreset] = Field(..., description="Available preset time slots")

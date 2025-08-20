from typing import List
from fastapi import HTTPException, status

from src.db.memory import db
from src.models.ride import (
    RideOffer,
    RideOfferCreate,
    RideRequest,
    RideRequestCreate,
    RidesMeta,
)
from src.models.enums import RideStatus, LocationPreset, TimeSlotPreset


class RidesService:
    """Service providing ride-related operations."""

    # PUBLIC_INTERFACE
    def get_meta(self) -> RidesMeta:
        """Return predefined locations and time slots."""
        return RidesMeta(
            locations=[
                LocationPreset.home,
                LocationPreset.school,
                LocationPreset.sports_club,
                LocationPreset.community_center,
                LocationPreset.custom,
            ],
            time_slots=[
                TimeSlotPreset.morning_pickup,
                TimeSlotPreset.afternoon_dropoff,
                TimeSlotPreset.evening_practice,
                TimeSlotPreset.custom,
            ],
        )

    # PUBLIC_INTERFACE
    def create_offer(self, payload: RideOfferCreate) -> RideOffer:
        """Create a new ride offer."""
        return db.create_ride_offer(payload)

    # PUBLIC_INTERFACE
    def list_offers(self) -> List[RideOffer]:
        """List all ride offers."""
        return db.list_ride_offers()

    # PUBLIC_INTERFACE
    def create_request(self, payload: RideRequestCreate) -> RideRequest:
        """Create a new ride request."""
        return db.create_ride_request(payload)

    # PUBLIC_INTERFACE
    def list_requests(self) -> List[RideRequest]:
        """List all ride requests."""
        return db.list_ride_requests()

    # PUBLIC_INTERFACE
    def confirm_request(self, request_id: str, offer_id: str) -> RideRequest:
        """Confirm a ride request against an offer, performing seat allocation checks."""
        req = db.get_ride_request(request_id)
        if not req:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride request not found")
        offer = db.get_ride_offer(offer_id)
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride offer not found")
        if req.status not in (RideStatus.pending,):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not in confirmable state")
        if offer.status not in (RideStatus.pending, RideStatus.confirmed):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offer not in a confirmable state")

        # Check seat availability
        allocated = db.get_allocated_seats(offer_id)
        if allocated + req.seats_requested > offer.seats_available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient seats available")

        # Optional: naive compatibility check (match presets and time slot)
        if req.time_slot.preset != offer.time_slot.preset:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Time slot mismatch")
        if req.from_location.preset != offer.pickup_location.preset or req.to_location.preset != offer.dropoff_location.preset:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location mismatch")

        # Allocate seats and update statuses
        db.allocate_seats(offer_id, req.seats_requested)
        req.status = RideStatus.confirmed
        req.matched_offer_id = offer_id
        req.meta.touch()
        db.update_ride_request(req)

        # If fully allocated, set offer to confirmed (or keep confirmed)
        total_alloc = db.get_allocated_seats(offer_id)
        if total_alloc >= offer.seats_available:
            offer.status = RideStatus.confirmed
            offer.meta.touch()
            db.update_ride_offer(offer)
        elif offer.status == RideStatus.pending:
            # Move offer to confirmed once first request is confirmed (optional policy)
            offer.status = RideStatus.confirmed
            offer.meta.touch()
            db.update_ride_offer(offer)

        return req

    # PUBLIC_INTERFACE
    def cancel_request(self, request_id: str) -> RideRequest:
        """Cancel a ride request and release any allocated seats."""
        req = db.get_ride_request(request_id)
        if not req:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride request not found")
        if req.status == RideStatus.cancelled:
            return req
        if req.matched_offer_id:
            # Release seats
            db.release_seats(req.matched_offer_id, req.seats_requested)
        req.status = RideStatus.cancelled
        req.meta.touch()
        db.update_ride_request(req)
        return req

    # PUBLIC_INTERFACE
    def cancel_offer(self, offer_id: str) -> RideOffer:
        """Cancel an offer; does not cascade to requests for MVP but prevents further confirmations."""
        offer = db.get_ride_offer(offer_id)
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride offer not found")
        if offer.status == RideStatus.cancelled:
            return offer
        offer.status = RideStatus.cancelled
        offer.meta.touch()
        db.update_ride_offer(offer)
        return offer


rides_service = RidesService()

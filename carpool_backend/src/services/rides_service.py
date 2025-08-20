from typing import List
from src.db.memory import db
from src.models.ride import RideOffer, RideOfferCreate, RideRequest, RideRequestCreate


class RidesService:
    """Service providing ride-related operations."""

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


rides_service = RidesService()

from typing import List, Optional
from fastapi import APIRouter, status
from src.services.rides_service import rides_service
from src.models.ride import RideOffer, RideOfferCreate, RideRequest, RideRequestCreate, RidesMeta
from src.core.security import require_auth

router = APIRouter(prefix="/rides", tags=["Rides"])


@router.get("/meta", response_model=RidesMeta, summary="Rides metadata", description="Predefined locations and time slot presets.")
def get_meta() -> RidesMeta:
    """Return preset locations and time slots for quick selection."""
    return rides_service.get_meta()


@router.post("/offers", response_model=RideOffer, status_code=status.HTTP_201_CREATED, summary="Create ride offer", description="Create a new ride offer.")
def create_offer(payload: RideOfferCreate, token: Optional[str] = None) -> RideOffer:
    """Create ride offer. Requires authentication."""
    require_auth(token)
    return rides_service.create_offer(payload)


@router.get("/offers", response_model=List[RideOffer], summary="List ride offers", description="List all ride offers.")
def list_offers() -> List[RideOffer]:
    """List ride offers."""
    return rides_service.list_offers()


@router.post("/requests", response_model=RideRequest, status_code=status.HTTP_201_CREATED, summary="Create ride request", description="Create a new ride request.")
def create_request(payload: RideRequestCreate, token: Optional[str] = None) -> RideRequest:
    """Create ride request. Requires authentication."""
    require_auth(token)
    return rides_service.create_request(payload)


@router.get("/requests", response_model=List[RideRequest], summary="List ride requests", description="List all ride requests.")
def list_requests() -> List[RideRequest]:
    """List ride requests."""
    return rides_service.list_requests()


@router.post("/requests/{request_id}/confirm", response_model=RideRequest, summary="Confirm request", description="Confirm a ride request against a specific offer by passing offer_id.")
def confirm_request(request_id: str, offer_id: str, token: Optional[str] = None) -> RideRequest:
    """Confirm a ride request with a given offer. Requires authentication."""
    require_auth(token)
    return rides_service.confirm_request(request_id=request_id, offer_id=offer_id)


@router.post("/requests/{request_id}/cancel", response_model=RideRequest, summary="Cancel request", description="Cancel a ride request and release any seats.")
def cancel_request(request_id: str, token: Optional[str] = None) -> RideRequest:
    """Cancel a ride request. Requires authentication."""
    require_auth(token)
    return rides_service.cancel_request(request_id=request_id)


@router.post("/offers/{offer_id}/cancel", response_model=RideOffer, summary="Cancel offer", description="Cancel a ride offer to prevent further confirmations.")
def cancel_offer(offer_id: str, token: Optional[str] = None) -> RideOffer:
    """Cancel a ride offer. Requires authentication (driver or admin in future iterations)."""
    require_auth(token)
    return rides_service.cancel_offer(offer_id=offer_id)

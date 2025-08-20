from typing import List, Optional
from fastapi import APIRouter, status
from src.services.rides_service import rides_service
from src.models.ride import RideOffer, RideOfferCreate, RideRequest, RideRequestCreate
from src.core.security import require_auth

router = APIRouter(prefix="/rides", tags=["Rides"])


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

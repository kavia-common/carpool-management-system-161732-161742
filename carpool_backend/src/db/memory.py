import uuid
from typing import Dict, List, Optional, Tuple

from src.models.user import User, UserCreate, UserUpdate
from src.models.ride import RideOffer, RideOfferCreate, RideRequest, RideRequestCreate
from src.models.common import Notification


class InMemoryDB:
    """
    Simple in-memory database replacement for early development and testing.
    Thread-safety is not guaranteed; for demo purposes only.
    """

    def __init__(self) -> None:
        self.users: Dict[str, User] = {}
        self.passwords: Dict[str, str] = {}  # user_id -> password_hash
        self.ride_offers: Dict[str, RideOffer] = {}
        self.ride_requests: Dict[str, RideRequest] = {}
        self.notifications: Dict[str, Notification] = {}

    # PUBLIC_INTERFACE
    def reset(self) -> None:
        """Reset the in-memory database to empty state."""
        self.__init__()

    # PUBLIC_INTERFACE
    def create_user(self, payload: UserCreate, password_hash: str) -> User:
        """Create and store a new user."""
        user_id = str(uuid.uuid4())
        user = User(id=user_id, email=payload.email, full_name=payload.full_name, role=payload.role)
        self.users[user_id] = user
        self.passwords[user_id] = password_hash
        return user

    # PUBLIC_INTERFACE
    def update_user(self, user_id: str, payload: UserUpdate, new_password_hash: Optional[str]) -> Optional[User]:
        """Update user fields if exists."""
        user = self.users.get(user_id)
        if not user:
            return None
        changed = False
        if payload.full_name is not None:
            user.full_name = payload.full_name
            changed = True
        if payload.role is not None:
            user.role = payload.role
            changed = True
        if new_password_hash is not None:
            self.passwords[user_id] = new_password_hash
        if changed:
            user.meta.touch()
        return user

    # PUBLIC_INTERFACE
    def get_user_by_email(self, email: str) -> Optional[Tuple[User, str]]:
        """Get user and password hash by email."""
        for u in self.users.values():
            if u.email == email:
                return u, self.passwords.get(u.id, "")
        return None

    # PUBLIC_INTERFACE
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    # PUBLIC_INTERFACE
    def list_users(self) -> List[User]:
        """List all users."""
        return list(self.users.values())

    # PUBLIC_INTERFACE
    def delete_user(self, user_id: str) -> bool:
        """Delete user if exists."""
        existed = user_id in self.users
        if existed:
            del self.users[user_id]
            self.passwords.pop(user_id, None)
        return existed

    # PUBLIC_INTERFACE
    def create_ride_offer(self, payload: RideOfferCreate) -> RideOffer:
        """Create and store a new ride offer."""
        offer_id = str(uuid.uuid4())
        offer = RideOffer(id=offer_id, **payload.model_dump())
        self.ride_offers[offer_id] = offer
        return offer

    # PUBLIC_INTERFACE
    def list_ride_offers(self) -> List[RideOffer]:
        """List all ride offers."""
        return list(self.ride_offers.values())

    # PUBLIC_INTERFACE
    def get_ride_offer(self, offer_id: str) -> Optional[RideOffer]:
        """Get a ride offer by ID."""
        return self.ride_offers.get(offer_id)

    # PUBLIC_INTERFACE
    def create_ride_request(self, payload: RideRequestCreate) -> RideRequest:
        """Create and store a new ride request."""
        request_id = str(uuid.uuid4())
        req = RideRequest(id=request_id, **payload.model_dump())
        self.ride_requests[request_id] = req
        return req

    # PUBLIC_INTERFACE
    def list_ride_requests(self) -> List[RideRequest]:
        """List all ride requests."""
        return list(self.ride_requests.values())

    # PUBLIC_INTERFACE
    def get_ride_request(self, request_id: str) -> Optional[RideRequest]:
        """Get a ride request by ID."""
        return self.ride_requests.get(request_id)

    # PUBLIC_INTERFACE
    def add_notification(self, notif: Notification) -> Notification:
        """Add a notification."""
        self.notifications[notif.id] = notif
        return notif

    # PUBLIC_INTERFACE
    def list_notifications_for_user(self, user_id: str) -> List[Notification]:
        """List notifications for a user."""
        return [n for n in self.notifications.values() if n.user_id == user_id]


# Singleton instance for app-wide use
db = InMemoryDB()

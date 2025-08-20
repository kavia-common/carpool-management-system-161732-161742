from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.api.routers.auth import router as auth_router
from src.api.routers.users import router as users_router
from src.api.routers.rides import router as rides_router
from src.api.routers.calendar import router as calendar_router
from src.api.routers.notifications import router as notifications_router
from src.api.routers.admin import router as admin_router
from src.db.memory import db
from src.models.enums import UserRole
from src.models.user import UserCreate
from src.core.security import hash_password

"""
FastAPI application entrypoint.

This module:
- Configures application metadata and OpenAPI tags
- Sets CORS to allow frontend integration (localhost:3000 by default)
- Seeds a default admin user for development
- Registers all API routers (auth, users, rides, calendar, notifications, admin)
- Exposes a health check and an OpenAPI JSON endpoint
"""

settings = get_settings()

openapi_tags = [
    {"name": "Auth", "description": "Authentication and current user"},
    {"name": "Users", "description": "User management"},
    {"name": "Rides", "description": "Ride offers and requests"},
    {"name": "Calendar", "description": "Calendar integrations"},
    {"name": "Notifications", "description": "Notifications API"},
    {"name": "Admin", "description": "Administrative tools"},
]

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Carpool Management System",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Build allowed origins list:
# - If CORS_ORIGINS is explicitly provided (not "*"), use those values plus localhost:3000
# - Otherwise allow all for early-stage development
_default_frontend = "http://localhost:3000"
if settings.cors_origins and settings.cors_origins != ["*"]:
    allowed = list({*settings.cors_origins, _default_frontend})
else:
    # When wildcard was provided or empty, still add wildcard to permit all
    allowed = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Health Check", tags=["Admin"])
def health_check():
    """Simple health check endpoint to verify API is running."""
    return {"message": "Healthy"}


def _seed_admin_user() -> None:
    """Seed an admin account if none exists. Uses default credentials for MVP."""
    # Check if an admin already exists
    existing_admin = next((u for u in db.list_users() if u.role == UserRole.admin), None)
    if existing_admin:
        return
    # Default seed values - for MVP/dev only
    email = "admin@carpool.local"
    full_name = "Admin User"
    default_password = "admin123"
    password_hash = hash_password(default_password)
    payload = UserCreate(email=email, full_name=full_name, role=UserRole.admin, password=default_password)
    db.create_user(payload, password_hash)


# Startup event to seed admin
@app.on_event("startup")
def on_startup():
    _seed_admin_user()


# Register routers (all current routers)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rides_router)
app.include_router(calendar_router)
app.include_router(notifications_router)
app.include_router(admin_router)


@app.get(
    "/openapi.json",
    include_in_schema=False,
    summary="OpenAPI Schema (JSON)",
    tags=["Admin"],
)
def get_openapi_override():
    """Return the current OpenAPI schema for tooling and frontend codegen."""
    return app.openapi()

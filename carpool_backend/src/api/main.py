from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.api.routers.auth import router as auth_router
from src.api.routers.users import router as users_router
from src.api.routers.rides import router as rides_router
from src.api.routers.calendar import router as calendar_router
from src.api.routers.notifications import router as notifications_router
from src.api.routers.admin import router as admin_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if settings.cors_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Health Check", tags=["Admin"])
def health_check():
    """Simple health check endpoint to verify API is running."""
    return {"message": "Healthy"}


# Register routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rides_router)
app.include_router(calendar_router)
app.include_router(notifications_router)
app.include_router(admin_router)

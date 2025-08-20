# Carpool Backend (FastAPI)

This service powers the Carpool Management System. It exposes RESTful endpoints for authentication, user and ride management, calendar integrations, notifications, and basic admin tools. The service is built with FastAPI and uses an in‑memory data store for the MVP.

## Features

- Authentication with a simple HMAC-signed access token (MVP).
- Role-based authorization (admin vs. general users).
- User CRUD for admins.
- Rides: offer and request rides, list offers/requests, confirm/cancel.
- Calendar: list upcoming events and connect calendar sources (mock).
- Notifications: send/list notifications (no-op provider).
- Admin: health check and in-memory DB reset.

## Quick Start

1) Requirements
- Python 3.11+
- pip

2) Install dependencies
- cd carpool_backend
- pip install -r requirements.txt

3) Run the API (development)
- uvicorn src.api.main:app --reload --port 8000

The API will be accessible at:
- http://localhost:8000
- OpenAPI schema: http://localhost:8000/openapi.json

A default admin user is seeded at startup:
- email: admin@carpool.local
- password: admin123

## Environment Variables

Configuration is read in src/core/config.py. Set these before running the app:

- SECRET_KEY
  - Used for password hashing and token signing in the MVP.
  - Default: "dev-secret-key"
  - Set to a strong value in production.
- ACCESS_TOKEN_EXPIRE_MINUTES
  - Token expiry in minutes.
  - Default: 60
- CORS_ORIGINS
  - Comma-separated list of allowed origins for CORS.
  - Default: "*" (allow all)
- ENV
  - Environment name for informational purposes (development/production).
  - Default: "development"

Example .env (if you manage env with your process manager):
SECRET_KEY=replace-with-strong-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000
ENV=development

## Authentication and Role Model

- Login: clients authenticate with POST /auth/login using email and password.
- Token: response contains access_token (a signed token used by the MVP).
- MVP token transport: pass token in query parameter ?token=ACCESS_TOKEN to protected endpoints.
  - Note: This is intentionally simplified for early development. In production, use Authorization: Bearer <token> headers and proper JWT validation.
- Roles:
  - admin: can manage users and access admin endpoints.
  - driver/parent: general users who can create ride offers and requests.

## API Endpoints

Below is a summary of the main endpoints. For complete schemas, refer to interfaces/openapi.json or GET /openapi.json from the running service.

- GET /
  - Health Check. Returns {"message": "Healthy"}.

- Auth
  - POST /auth/login
    - Body: { "email": string, "password": string }
    - Returns: { "access_token": string, "token_type": "bearer" }
  - GET /auth/me
    - Query: token (optional for MVP)
    - Returns the current user's profile.

- Users (admin only)
  - POST /users
    - Create user from payload { email, full_name, role, password }.
  - GET /users
    - List all users.
  - GET /users/{user_id}
    - Get a user by ID.
  - PUT /users/{user_id}
    - Update user fields (full_name, role, password).
  - DELETE /users/{user_id}
    - Delete a user.

- Rides
  - GET /rides/meta
    - Get presets for locations and time slots.
  - POST /rides/offers?token=...
    - Create a ride offer (auth required).
  - GET /rides/offers
    - List ride offers.
  - POST /rides/requests?token=...
    - Create a ride request (auth required).
  - GET /rides/requests
    - List ride requests.
  - POST /rides/requests/{request_id}/confirm?offer_id=...&token=...
    - Confirm a ride request with a specific offer (auth required).
  - POST /rides/requests/{request_id}/cancel?token=...
    - Cancel a ride request (auth required).
  - POST /rides/offers/{offer_id}/cancel?token=...
    - Cancel a ride offer (auth required).

- Calendar
  - POST /calendar/sync?token=...
    - Connect a calendar source for a user (mock implementation).
  - GET /calendar/events?days=7&user_id=optional
    - List upcoming events; optionally include user-specific ride events.

- Notifications
  - POST /notifications?user_id=...&title=...&body=...&token=...
    - Send a notification (admin only).
  - GET /notifications/{user_id}?token=...
    - List notifications for a user (auth required).
  - POST /notifications/test?target=optional&token=...
    - Test no-op provider (admin only).

- Admin
  - POST /admin/reset?token=...
    - Reset in-memory DB (admin only).

## Development vs Production

- Development
  - Use --reload with uvicorn (hot-reload).
  - Default CORS allows all origins to simplify local development.
  - Seeds default admin user (admin@carpool.local / admin123).

- Production
  - Set a strong SECRET_KEY and configure CORS_ORIGINS.
  - Run behind a production-grade ASGI server such as uvicorn or gunicorn with appropriate workers and TLS termination at the reverse proxy.
  - Consider persisting data with a real database; current implementation uses in-memory storage and will reset on process restart.
  - Replace query param token usage with Authorization headers, and adopt a robust JWT library with refresh tokens and proper revocation strategies.

## Known Limitations

- In-memory database only; data is lost when the service restarts.
- Tokens are passed via query parameters for the MVP; not secure for production.
- Password hashing uses a simplistic SHA-256 salted approach; replace with a hardened KDF such as bcrypt/argon2.
- Notifications provider is a no-op logger; no real external delivery.
- Calendar integration is a mock; no real remote calendar sync.

## Future Improvements

- Migrate to a persistent database and add migrations.
- Implement OAuth2/JWT with Authorization headers and refresh tokens.
- Enhance roles/permissions and per-resource authorization checks.
- Integrate real notification channels (email/SMS/push).
- Add rate limiting, request logging, and audit trails.
- Expand calendar adapters and ICS parsing.
- Add pagination and filtering to list endpoints.
- Comprehensive test coverage and CI/CD pipeline.

## Running Tests

- pytest
- flake8

## Project Structure

- src/api/main.py: FastAPI app initialization and router registration.
- src/api/routers/*: Route handlers for auth, users, rides, calendar, notifications, admin.
- src/core/config.py: Environment-driven settings.
- src/core/security.py: Token creation/validation, password hashing, auth helpers.
- src/services/*: Business logic for users, rides, notifications, calendar.
- src/models/*: Pydantic models/schemas and enums.
- src/db/memory.py: In-memory "database" for MVP.
- interfaces/openapi.json: Exported OpenAPI schema for tooling and frontend.

## Running With Frontend

- Ensure CORS_ORIGINS includes http://localhost:3000 when developing with the React frontend.
- Start backend (port 8000 by default), start frontend (port 3000), and configure the frontend's REACT_APP_API_BASE_URL to http://localhost:8000.

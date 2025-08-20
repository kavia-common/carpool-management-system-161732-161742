# carpool-management-system-161732-161742

Backend Auth (MVP) quickstart:
- Default seeded admin: email admin@carpool.local, password admin123
- Login: POST /auth/login with { "email": "...", "password": "..." } to receive access_token
- For MVP, pass the token as query param ?token=ACCESS_TOKEN to protected endpoints
- Admin-only endpoints: /admin/*, /users* (GET/POST/PUT/DELETE), notifications POST
- Auth-required endpoints: rides POST /rides/offers and /rides/requests, notifications GET

Environment variables:
- SECRET_KEY: used for password hashing and token signing (set in deployment)
- ACCESS_TOKEN_EXPIRE_MINUTES: token expiry minutes (default 60)
- CORS_ORIGINS: comma-separated list (default "*")
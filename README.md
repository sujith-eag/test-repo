# Shadow Protocol - Phase 1

A deployment-ready CTF platform foundation with a React frontend, Flask API backend, JWT authentication, scoring, submissions, and Docker deployment for Render.

## What Phase 1 includes

- User registration and login
- JWT-protected routes
- Challenge listing
- Flag submission
- Duplicate score prevention
- Scoreboard
- Personal submission history
- React app served by Flask in production
- Docker-based single-service deployment
- SQLite fallback for local development
- PostgreSQL support for Render

## What Phase 1 does not include yet

- Final event flags
- Intentional vulnerable labs
- robots.txt / humans.txt challenge content
- Header flag challenge
- SQL injection challenge
- Admin dashboard
- Hint system

## Environment variables

Required for production:

```bash
JWT_SECRET_KEY=replace-with-a-long-random-secret
```

Recommended for production:

```bash
DATABASE_URL=postgresql://...
```

If `DATABASE_URL` is not set, the app uses local SQLite.

## Local backend development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Backend runs on:

```text
http://localhost:7000
```

## Local frontend development

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

The Vite proxy sends `/api` requests to the Flask backend.

## Docker local run

```bash
docker build -t shadow-protocol .
docker run -p 10000:10000 -e JWT_SECRET_KEY=dev-secret shadow-protocol
```

Open:

```text
http://localhost:10000
```

## Render deployment

1. Push this repo to GitHub.
2. Create a Render Web Service.
3. Select Docker environment.
4. Set `JWT_SECRET_KEY`.
5. Attach Render PostgreSQL or use the included `render.yaml` blueprint.

## Phase 1 demo flags

These are test-only flags for verifying platform behavior:

```text
CTF{welcome_agent}
CTF{first_transmission}
CTF{echo_protocol}
```

Replace them during Phase 2 with real event content and keep organizer materials private.

## Test checklist

- Register works
- Login works
- `/api/auth/me` works with JWT
- Challenge list loads
- Wrong flag is rejected
- Correct flag awards points
- Duplicate correct flag does not award points again
- Scoreboard updates
- Submission history loads
- React routes refresh correctly
- Docker build succeeds
- Render deploy succeeds

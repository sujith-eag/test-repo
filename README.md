# Hawkins Shadow Protocol CTF

A Stranger Things-inspired cyber CTF event site built as a single deployable Render application.

## Overview

The site includes:

```text
React frontend
Flask backend
JWT authentication
Challenge board
Flag submission
Duplicate score protection
Scoreboard
Submission history
Themed vulnerable lab routes
Frontend, recon, crypto, and web exploitation challenges
Docker deployment
```

The theme uses Hawkins / gate / static / lab / walkie-inspired language, but the challenges are solvable through standard cyber techniques and do not require show knowledge.

## Local Docker setup

```bash
docker build -t shadow-protocol .
docker run --rm -p 10000:10000 \
  -e JWT_SECRET_KEY="local-dev-shadow-protocol-secret-key-32chars-minimum" \
  shadow-protocol
```

Open:

```text
http://localhost:10000
```

## Render deployment

Create a Render Web Service using Docker.

Required environment variable:

```text
JWT_SECRET_KEY=<strong random secret>
```

Optional environment variables:

```text
EVENT_NAME=Hawkins Shadow Protocol
REGISTRATION_ENABLED=true
SUBMISSIONS_ENABLED=true
SCOREBOARD_VISIBLE=true
DATABASE_URL=<postgresql-url>
```

SQLite is acceptable for short testing, but PostgreSQL is recommended for a real event.

## Main routes

```text
/                      Frontend app
/intel                 Mission briefing
/rules                 Event rules
/challenges            Challenge board
/submit                Submit flags
/scoreboard            Rankings
/submissions           User submission history
/api/health            Health check
/api/challenges        Challenge API
/api/submissions       Flag submission API
/robots.txt            Recon file
/humans.txt            Recon file
/vuln/*                Intentional challenge lab routes
```

## Important safety rule

Only `/vuln/*`, public assets, and normal application pages are intended challenge surfaces. The real auth/scoring platform should not be intentionally vulnerable.

## Files of interest

```text
backend/seed_event.py              Challenge seed and fallback flags
backend/routes/vuln_lab.py         Intentional lab routes
frontend/src/styles.css            CSS/source flags and styling
frontend/src/api.js                API client behavior
frontend/src/pages/                Frontend pages
frontend/public/assets/            Public recon assets
```

## Notes for organizers

- Keep judge guides private if the repo is public.
- Avoid flags that directly match challenge title/slug.
- Test every flag before the event.
- Avoid redeploying during the event if using SQLite.
- For persistent scoring, use Render PostgreSQL.
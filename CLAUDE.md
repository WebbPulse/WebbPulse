# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WebbPulse is a personal portfolio website with a blog and admin panel. It is a full-stack monorepo with a React/TypeScript frontend and a FastAPI/Python backend.

## Commands

### Frontend (`frontend/`)

```bash
npm run dev:local        # Local dev server on port 5173 (proxies /api to localhost:8000)
npm run build            # TypeScript compile + Vite production build
npm run lint             # ESLint check
npm run lint:fix         # ESLint with auto-fixes
npm run format           # Prettier format
npm run format:check     # Prettier check without fixing
npm run test             # Vitest in watch mode
npm run test:run         # Run tests once with coverage
npm run test:ui          # Vitest UI mode
```

Run a single test file:
```bash
npm run test:run -- --reporter=verbose path/to/test.spec.ts
```

### Backend (`backend/`)

```bash
# Start PostgreSQL locally
docker-compose up -d

# Run the server
uvicorn app.main:app --reload

# Tests
pytest tests/                                      # All tests
pytest tests/test_name.py::test_function_name -v   # Single test
python run_tests.py all                            # All tests
python run_tests.py unit|api|integration|auth      # By category
python run_tests.py coverage                       # With HTML coverage report
python run_tests.py lint                           # Flake8 + Black checks
python run_tests.py format                         # Black + isort formatting

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Architecture

### Frontend

- **Pages**: `/` (portfolio), `/blog`, `/blog/:slug`, `/admin`
- **API layer**: All API calls go through `src/services/api.ts` (`apiService`)
- **Dev proxy**: Vite proxies `/api/*` → `http://localhost:8000` in local dev; production uses `VITE_API_URL` env var

### Backend

- **REST API**: All routes under `/api/v1/` prefix. OpenAPI docs at `/docs`
- **Auth**: JWT tokens (python-jose/bcrypt). Users have an `is_admin` boolean flag
- **Database**: PostgreSQL via SQLAlchemy 2.0 ORM + Alembic migrations. Local dev uses Docker Compose
- **Rate limiting**: Custom middleware in `app/core/` with per-minute/hour/day limits
- **Email**: SendGrid integration for newsletter subscriptions

### Key files

| File | Purpose |
|---|---|
| `backend/app/main.py` | FastAPI app entrypoint — CORS, middleware, lifespan hooks |
| `backend/app/config.py` | Pydantic Settings — env vars including `DATABASE_URL` |
| `backend/app/database.py` | SQLAlchemy engine, session factory |
| `backend/app/api/v1/` | Route handlers by resource |
| `frontend/src/services/api.ts` | Centralized API client |
| `frontend/vite.config.ts` | Vite config with dev proxy |

### Deployment

- **CI/CD**: GitHub Actions (`.github/workflows/test-backend.yml`, `test-frontend.yml`)

## Conventions

- **Admin/management email**: Use `tyler@webbpulse.com` for all management addresses (DMARC reporting, contact forms, etc.)

### Test markers (backend)

pytest.ini defines markers: `unit`, `api`, `integration`, `auth`, `admin`. Run a category with `-m unit` etc., or use `python run_tests.py <category>`.


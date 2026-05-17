# WebbPulse

A full-stack personal portfolio and blog. Every section — projects, experience, skills, blog, and site copy — is driven from the API through an admin panel rather than hardcoded.

**Stack:** FastAPI (Python 3.11) · React (TypeScript) · PostgreSQL · AWS (Terraform)

**License:** MIT

---

## Structure

```
backend/    FastAPI app, SQLAlchemy models, Alembic migrations
frontend/   React + Vite + Tailwind CSS
terraform/  AWS infrastructure
docs/        Static assets (resume, etc.)
```

---

## Development

**Prerequisites:** Python 3.11, Node 18+, Docker (for local PostgreSQL)

### Backend

```bash
cd backend
docker-compose up -d              # start PostgreSQL
uvicorn app.main:app --reload     # http://localhost:8000 (docs at /docs)
```

```bash
# Migrations (always autogenerate, never write manually)
alembic revision --autogenerate -m "description"
alembic upgrade head

# Tests
pytest tests/                     # all
python run_tests.py unit          # by category: unit | api | integration | auth
python run_tests.py coverage      # HTML coverage report

# Linting
python run_tests.py lint          # flake8 + black
python run_tests.py format        # black + isort
```

### Frontend

```bash
cd frontend
npm install
npm run dev:local     # port 5173, proxies /api to localhost:8000
npm run build
npm run lint
npm run test:run
```

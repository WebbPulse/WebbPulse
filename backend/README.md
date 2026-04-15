# Portfolio Blog API Backend

A FastAPI-based backend for the portfolio website blog functionality, featuring PostgreSQL database integration.

## Features

- FastAPI REST API with automatic OpenAPI documentation
- PostgreSQL database with SQLAlchemy ORM
- User authentication and authorization
- Blog post management with categories
- Email subscription system
- Dockerized development environment
- PgAdmin for database management (optional)

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to backend directory
cd backend

# Copy environment template
cp env.example .env

# Edit .env file with your configuration
nano .env
```

### 2. Start Development Environment

```bash
# Run the development setup script
./dev-setup.sh
```

This script will:

- Start PostgreSQL database container
- Create virtual environment
- Install dependencies
- Initialize database tables

### 3. Start FastAPI Application

```bash
# Activate virtual environment
source venv/bin/activate

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application

- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Manual Setup

If you prefer to set up manually:

### 1. Start Database

```bash
# Start PostgreSQL
docker-compose up -d postgres

# Check database health
docker-compose exec postgres pg_isready -U portfolio_user -d portfolio_blog
```

### 2. Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
# Apply database migrations
python migrate.py upgrade

# Or using alembic directly
alembic upgrade head
```

### 4. Start Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration
POSTGRES_DB=portfolio_blog
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@webbpulse.com
SENDGRID_FROM_NAME=Tyler Webb Portfolio

# Application
DEBUG=true
LOG_SQL_QUERIES=false  # Set to true to see SQL queries in logs
```

## Database Management

### Using PgAdmin

1. Start pgAdmin with the tools profile:

   ```bash
   docker-compose --profile tools up -d pgadmin
   ```

2. Login with credentials from your .env file
3. Add server connection:
   - Host: postgres (container name)
   - Port: 5432
   - Database: portfolio_blog
   - Username: portfolio_user
   - Password: (from .env file)

### Using Command Line

```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U portfolio_user -d portfolio_blog

# View database logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Blog Posts

- `GET /api/v1/posts` - List all posts
- `POST /api/v1/posts` - Create new post
- `GET /api/v1/posts/{post_id}` - Get specific post
- `PUT /api/v1/posts/{post_id}` - Update post
- `DELETE /api/v1/posts/{post_id}` - Delete post

### Categories

- `GET /api/v1/categories` - List all categories
- `POST /api/v1/categories` - Create new category

### Subscribers

- `POST /api/v1/subscribers` - Subscribe to newsletter
- `GET /api/v1/subscribers` - List subscribers (admin only)

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core functionality (security, email)
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic models for validation
│   ├── utils/         # Utility functions
│   ├── config.py      # Configuration settings
│   ├── database.py    # Database connection and setup
│   └── main.py        # FastAPI application
├── tests/             # Test files
├── docker-compose.yml # Docker services
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

The application uses Alembic for database migrations. This ensures proper version control of database schema changes.

#### Using the Migration Script

```bash
# Apply all pending migrations
python migrate.py upgrade

# Create a new migration (auto-generate from model changes)
python migrate.py revision --autogenerate --message "Add new field to posts"

# Create a new migration manually
python migrate.py revision --message "Custom migration"

# Show current migration revision
python migrate.py current

# Show migration history
python migrate.py history

# Downgrade to a specific revision
python migrate.py downgrade --revision <revision_id>

# Mark database as being at a specific revision
python migrate.py stamp --revision <revision_id>
```

#### Using Alembic Directly

```bash
# Apply all pending migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Show current revision
alembic current

# Show history
alembic history
```

#### Migration Best Practices

1. **Always create migrations for schema changes** - Don't modify tables directly
2. **Test migrations** - Test both upgrade and downgrade operations
3. **Use descriptive messages** - Make migration purpose clear
4. **Review auto-generated migrations** - Check generated SQL before applying
5. **Backup before major migrations** - Always backup production data

## Production Deployment

### Environment Variables for Production

```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-production-secret-key
DEBUG=false
SENDGRID_API_KEY=your-production-sendgrid-key
CORS_ORIGINS=https://webbpulse.com,https://www.webbpulse.com
```

## Logging Configuration

The application uses a configurable logging system to control the verbosity of logs:

### Environment Variables

- `LOG_SQL_QUERIES`: Set to `true` to enable SQL query logging (default: `false`)
- `DEBUG`: Set to `true` for debug mode (default: `false`)

### Log Levels

- **INFO**: API requests, database connections, application events
- **WARNING**: SQLAlchemy warnings, connection pool issues
- **ERROR**: Database errors, authentication failures, critical issues

### SQLAlchemy Logging

By default, SQLAlchemy engine logs are suppressed to reduce noise. To enable SQL query logging:

```env
LOG_SQL_QUERIES=true
```

This will show:

- SQL queries being executed
- Query parameters
- Execution time

### Testing Logging

You can test the logging configuration:

```bash
python test_logging.py
```

## Troubleshooting

### Database Connection Issues

1. Check if PostgreSQL container is running:

   ```bash
   docker-compose ps
   ```

2. Check database logs:

   ```bash
   docker-compose logs postgres
   ```

3. Test database connection:
   ```bash
   python -c "from app.database import test_db_connection; print(test_db_connection())"
   ```

### Permission Issues

If you get permission errors:

```bash
# Make setup script executable
chmod +x dev-setup.sh

# Fix Docker permissions (if needed)
sudo usermod -aG docker $USER
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Run linting and tests
5. Submit a pull request

## License

This project is part of the Portfolio Website project.

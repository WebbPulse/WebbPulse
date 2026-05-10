import logging
import subprocess
import sys

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Use the DATABASE_URL from settings or construct it from individual components
database_url = settings.DATABASE_URL or settings.get_database_url()

# Create database engine
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=settings.LOG_SQL_QUERIES,  # Log SQL queries only when explicitly enabled
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def check_tables_exist():
    """Check if all required tables exist in the database"""
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # Import all models to get table names
        from .models import (  # noqa: F401
            category,
            certification,
            education,
            experience,
            post,
            project,
            site_content,
            skill,
            user,
        )

        # Get expected table names from models
        expected_tables = [
            "users",
            "categories",
            "posts",
            "projects",
            "experience",
            "skills",
            "education",
            "certifications",
            "site_content",
        ]

        missing_tables = [
            table for table in expected_tables if table not in existing_tables
        ]

        if missing_tables:
            logger.info(f"Missing tables: {missing_tables}")
            return False
        else:
            logger.info("All required tables exist")
            return True
    except Exception as e:
        logger.error(f"Error checking tables: {e}")
        return False


def run_migrations():
    """Run database migrations using Alembic"""
    try:
        logger.info("Running database migrations...")
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        if result.returncode == 0:
            logger.info("Database migrations completed successfully")
            return True
        else:
            logger.error(f"Migration failed: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False


def init_db():
    """Initialize database tables only if they don't exist"""
    try:
        # Check if tables already exist
        if check_tables_exist():
            logger.info("Database tables already exist, skipping creation")
            return

        # Import all models here to ensure they are registered
        from .models import (  # noqa: F401
            category,
            certification,
            education,
            experience,
            post,
            project,
            site_content,
            skill,
            user,
        )

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def test_db_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            from sqlalchemy import text

            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

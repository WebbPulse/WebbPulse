"""
Pytest configuration and fixtures for the Portfolio Blog API tests
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Set testing environment variable
os.environ["TESTING"] = "true"


# Register custom pytest marks
def pytest_configure(config):
    """Register custom pytest marks."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "admin: Admin functionality tests")


# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.config import settings
from app.core.security import create_access_token, get_password_hash
from app.database import Base, get_db
from app.main import app
from app.models import (
    Category,
    Certification,
    Education,
    Experience,
    Post,
    Project,
    SiteContent,
    Skill,
    User,
)

# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test database engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with a fresh database session."""

    def override_get_db():
        try:
            yield db_session
        except Exception:
            db_session.rollback()
            raise
        finally:
            pass  # Don't close the session here as it's managed by the fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123"),
        is_admin=False,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session: Session) -> User:
    """Create a test admin user."""
    admin_user = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password=get_password_hash("adminpassword123"),
        is_admin=True,
        is_active=True,
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    return admin_user


@pytest.fixture
def test_category(db_session: Session) -> Category:
    """Create a test category."""
    category = Category(
        name="Test Category",
        slug="test-category",
        description="A test category for blog posts",
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def test_post(db_session: Session, test_user: User, test_category: Category) -> Post:
    """Create a test post."""
    post = Post(
        title="Test Post",
        slug="test-post",
        content="# Test Post\n\nThis is a test post content.",
        excerpt="A test post excerpt",
        read_time="5 min read",
        author_id=test_user.id,
        category_id=test_category.id,
        published_at=datetime.now(timezone.utc),
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post


@pytest.fixture
def test_draft_post(
    db_session: Session, test_user: User, test_category: Category
) -> Post:
    """Create a test draft post (unpublished)."""
    post = Post(
        title="Test Draft Post",
        slug="test-draft-post",
        content="# Test Draft Post\n\nThis is a test draft post content.",
        excerpt="A test draft post excerpt",
        read_time="3 min read",
        author_id=test_user.id,
        category_id=test_category.id,
        published_at=None,  # Unpublished
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post


@pytest.fixture
def test_project(db_session: Session) -> Project:
    """Create a test project."""
    project = Project(
        title="Test Project",
        description="A test project description",
        technologies=["Python", "FastAPI", "React"],
        github_url="https://github.com/test/project",
        live_url="https://test-project.com",
        image="https://example.com/image.jpg",
        featured=True,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


@pytest.fixture
def test_experience(db_session: Session) -> Experience:
    """Create a test experience entry."""
    experience = Experience(
        title="Test Position",
        company="Test Company",
        location="Test City, Test State",
        period="Jan 2022 - Dec 2023",
        start_date=datetime(2022, 1, 1).date(),
        end_date=datetime(2023, 12, 31).date(),
        description="A test job description",
        technologies=["Python", "SQL", "AWS"],
        achievements=["Achievement 1", "Achievement 2"],
        is_active=True,
    )
    db_session.add(experience)
    db_session.commit()
    db_session.refresh(experience)
    return experience


@pytest.fixture
def test_education(db_session: Session) -> Education:
    """Create a test education entry."""
    entry = Education(
        degree="Test Degree",
        school="Test University",
        location="Test City, ST",
        period="Aug 2018 - May 2022",
        start_date=datetime(2018, 8, 1).date(),
        end_date=datetime(2022, 5, 31).date(),
        description="A test education description",
        order=10,
        is_active=True,
    )
    db_session.add(entry)
    db_session.commit()
    db_session.refresh(entry)
    return entry


@pytest.fixture
def test_certification(db_session: Session) -> Certification:
    """Create a test certification."""
    entry = Certification(
        name="Test Cert",
        issuer="Test Issuer",
        issued_date=datetime(2023, 1, 1).date(),
        credential_url="https://example.com/cred",
        order=10,
        is_active=True,
    )
    db_session.add(entry)
    db_session.commit()
    db_session.refresh(entry)
    return entry


@pytest.fixture
def test_site_content(db_session: Session) -> SiteContent:
    """Create the singleton site content row used by tests.

    The migration that seeds this row is skipped under SQLite test setup
    (create_all is used instead of running migrations), so each test that
    needs site content seeds it via this fixture.
    """
    content = SiteContent(
        id=1,
        hero_title="Hi, I'm Test",
        hero_subtitle="Test Subtitle",
        hero_description="Test description",
        about_paragraphs=["Paragraph one.", "Paragraph two."],
        about_values=[
            {"title": "Test Value", "description": "Why it matters", "icon": "✨"},
        ],
        profile_image_url="/headshot.jpg",
        resume_url=None,
        email="test@example.com",
        github_url="https://github.com/test",
        linkedin_url="https://linkedin.com/in/test",
        footer_tagline="Test tagline",
    )
    db_session.add(content)
    db_session.commit()
    db_session.refresh(content)
    return content


@pytest.fixture
def test_skill(db_session: Session) -> Skill:
    """Create a test skill."""
    skill = Skill(
        name="Test Skill",
        category="frontend",
        tier="working",
        icon="🧪",
        order=10,
        is_active=True,
    )
    db_session.add(skill)
    db_session.commit()
    db_session.refresh(skill)
    return skill


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Create authentication headers for a test user."""
    access_token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def admin_auth_headers(test_admin_user: User) -> dict:
    """Create authentication headers for a test admin user."""
    access_token = create_access_token(data={"sub": test_admin_user.username})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def invalid_auth_headers() -> dict:
    """Create invalid authentication headers."""
    return {"Authorization": "Bearer invalid_token"}


# Test data fixtures
@pytest.fixture
def sample_post_data() -> dict:
    """Sample post data for testing."""
    return {
        "title": "Sample Post",
        "slug": "sample-post",
        "content": "# Sample Post\n\nThis is sample content.",
        "excerpt": "A sample post excerpt",
        "read_time": "8 min read",
        "category_id": 1,
    }


@pytest.fixture
def sample_category_data() -> dict:
    """Sample category data for testing."""
    return {
        "name": "Sample Category",
        "slug": "sample-category",
        "description": "A sample category description",
    }


@pytest.fixture
def sample_project_data() -> dict:
    """Sample project data for testing."""
    return {
        "title": "Sample Project",
        "description": "A sample project description",
        "technologies": ["React", "TypeScript", "Node.js"],
        "github_url": "https://github.com/sample/project",
        "live_url": "https://sample-project.com",
        "image": "https://example.com/sample.jpg",
        "featured": True,
    }


@pytest.fixture
def sample_experience_data() -> dict:
    """Sample experience data for testing."""
    return {
        "title": "Sample Position",
        "company": "Sample Company",
        "location": "Sample City, Sample State",
        "period": "Jan 2022 - Dec 2023",
        "start_date": "2022-01-01",
        "end_date": "2023-12-31",
        "description": "A sample job description",
        "technologies": ["Python", "JavaScript", "Docker"],
        "achievements": ["Achievement 1", "Achievement 2"],
    }


@pytest.fixture
def sample_skill_data() -> dict:
    """Sample skill data for testing."""
    return {
        "name": "Sample Skill",
        "category": "backend",
        "tier": "working",
        "icon": "🔧",
        "order": 20,
    }


@pytest.fixture
def sample_education_data() -> dict:
    """Sample education data for testing."""
    return {
        "degree": "Sample Degree",
        "school": "Sample University",
        "location": "Sample City, ST",
        "period": "Aug 2018 - May 2022",
        "start_date": "2018-08-01",
        "end_date": "2022-05-31",
        "description": "Sample description",
        "order": 20,
    }


@pytest.fixture
def sample_certification_data() -> dict:
    """Sample certification data for testing."""
    return {
        "name": "Sample Certification",
        "issuer": "Sample Issuer",
        "issued_date": "2023-06-01",
        "credential_url": "https://example.com/cred/123",
        "order": 20,
    }

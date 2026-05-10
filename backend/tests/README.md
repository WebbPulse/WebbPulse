# Portfolio Blog API Testing

This directory contains comprehensive tests for the Portfolio Blog API backend. The testing suite is built with pytest and covers all major components of the application.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_auth_api.py         # Authentication and authorization tests
├── test_posts_api.py        # Blog posts API tests
├── test_projects_api.py     # Projects API tests
├── test_experience_api.py   # Experience API tests
├── test_core_security.py    # Security module unit tests
├── test_models.py           # Database model tests
└── README.md               # This file
```

## Test Categories

### 1. Unit Tests (`@pytest.mark.unit`)

- **Core Security**: Password hashing, JWT token creation/validation
- **Database Models**: Model creation, relationships, constraints
- **Individual Functions**: Isolated function testing

### 2. API Tests (`@pytest.mark.api`)

- **Posts API**: CRUD operations for blog posts and categories
- **Projects API**: CRUD operations for portfolio projects
- **Experience API**: CRUD operations for work experience
- **Authentication API**: Login, token validation, authorization

### 3. Integration Tests (`@pytest.mark.integration`)

- **Full Workflows**: Complete user journeys
- **Cross-Component**: Tests involving multiple components
- **Database Integration**: End-to-end database operations

### 4. Authentication Tests (`@pytest.mark.auth`)

- **Login/Logout**: User authentication flows
- **Token Management**: JWT token creation and validation
- **Authorization**: Role-based access control
- **Security**: Password security, token security

### 5. Performance Tests (`@pytest.mark.slow`)

- **Large Datasets**: Tests with significant data volumes
- **Performance Benchmarks**: Response time testing

## Running Tests

### Prerequisites

1. Install test dependencies:

```bash
pip install -r requirements.txt
```

2. Set up test environment variables (optional):

```bash
cp env.example .env.test
# Edit .env.test with test-specific values
```

### Basic Test Commands

#### Run All Tests

```bash
# From the backend directory
python -m pytest tests/ -v
```

#### Run Specific Test Categories

```bash
# Unit tests only
python -m pytest tests/ -m unit -v

# API tests only
python -m pytest tests/ -m api -v

# Integration tests only
python -m pytest tests/ -m integration -v

# Authentication tests only
python -m pytest tests/ -m auth -v

# Fast tests (excluding slow tests)
python -m pytest tests/ -m "not slow" -v
```

#### Run Tests with Coverage

```bash
# Generate coverage report
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html:htmlcov -v

# View HTML coverage report
open htmlcov/index.html
```

#### Run Specific Test Files

```bash
# Run only posts API tests
python -m pytest tests/test_posts_api.py -v

# Run only security tests
python -m pytest tests/test_core_security.py -v
```

#### Run Specific Test Functions

```bash
# Run a specific test function
python -m pytest tests/test_posts_api.py::TestPostsAPI::test_get_posts_public -v

# Run all tests in a specific class
python -m pytest tests/test_posts_api.py::TestPostsAPI -v
```

### Using the Test Runner Script

The `run_tests.py` script provides convenient shortcuts for common test scenarios:

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py unit      # Unit tests only
python run_tests.py api       # API tests only
python run_tests.py auth      # Authentication tests only
python run_tests.py fast      # Fast tests (no slow tests)
python run_tests.py coverage  # Tests with coverage report

# Code quality checks
python run_tests.py lint      # Run linting checks
python run_tests.py format    # Format code with black/isort
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)

- Test discovery patterns
- Coverage settings
- Custom markers
- Output formatting

### Test Fixtures (`conftest.py`)

- Database session management
- Test data creation
- Authentication helpers
- Mock configurations

### Test Database

- Uses SQLite for testing (faster than PostgreSQL)
- Automatic table creation/destruction
- Isolated test sessions
- No external dependencies

## Test Data and Fixtures

### Common Fixtures

- `db_session`: Fresh database session for each test
- `client`: FastAPI test client with database override
- `test_user`: Regular user for testing
- `test_admin_user`: Admin user for testing
- `test_category`: Sample category
- `test_post`: Sample published post
- `test_draft_post`: Sample unpublished post
- `test_project`: Sample project
- `test_experience`: Sample experience entry
- `auth_headers`: Authentication headers for regular user
- `admin_auth_headers`: Authentication headers for admin user

### Test Data Fixtures

- `sample_post_data`: Sample post creation data
- `sample_category_data`: Sample category creation data
- `sample_project_data`: Sample project creation data
- `sample_experience_data`: Sample experience creation data

## Mocking and External Dependencies

### Database Mocking

- SQLite test database for fast, isolated testing
- Automatic cleanup between tests
- No external database dependencies

## Test Coverage

The test suite aims for comprehensive coverage of:

### API Endpoints

- ✅ GET endpoints (public and admin)
- ✅ POST endpoints (creation)
- ✅ PUT endpoints (updates)
- ✅ DELETE endpoints (soft deletes)
- ✅ Authentication and authorization
- ✅ Input validation
- ✅ Error handling

### Business Logic

- ✅ Password hashing and verification
- ✅ JWT token creation and validation
- ✅ Slug generation
- ✅ Soft delete functionality
- ✅ Pagination
- ✅ Filtering and sorting

### Database Operations

- ✅ Model creation and relationships
- ✅ Constraint validation
- ✅ Foreign key relationships
- ✅ Timestamp management
- ✅ Soft delete operations

### Security

- ✅ Authentication flows
- ✅ Authorization checks
- ✅ Password security
- ✅ Token security
- ✅ Input sanitization

## Continuous Integration

### GitHub Actions

The test suite is integrated with GitHub Actions for automated testing:

```yaml
# .github/workflows/test-backend.yml
- name: Run Tests
  run: |
    cd backend
    python -m pytest tests/ --cov=app --cov-report=xml
```

### Pre-commit Hooks

Consider adding pre-commit hooks for:

- Running tests before commits
- Code formatting checks
- Linting validation

## Debugging Tests

### Verbose Output

```bash
python -m pytest tests/ -v -s
```

### Debug Specific Test

```bash
python -m pytest tests/test_posts_api.py::TestPostsAPI::test_get_posts_public -v -s --pdb
```

### Test Database Inspection

```bash
# Access test database directly
sqlite3 test.db
```

### Coverage Analysis

```bash
# Generate detailed coverage report
python -m pytest tests/ --cov=app --cov-report=html:htmlcov --cov-report=term-missing

# View coverage in browser
open htmlcov/index.html
```

## Best Practices

### Writing New Tests

1. **Use descriptive test names**: `test_create_post_with_valid_data`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Use appropriate markers**: `@pytest.mark.api`, `@pytest.mark.unit`
4. **Mock external dependencies**: Avoid real API calls
5. **Test edge cases**: Invalid data, error conditions
6. **Test both success and failure scenarios**

### Test Organization

1. **Group related tests in classes**: `TestPostsAPI`, `TestAuthAPI`
2. **Use fixtures for common setup**: Database sessions, test data
3. **Keep tests independent**: Each test should be self-contained
4. **Use meaningful assertions**: Test specific behavior, not implementation

### Performance Considerations

1. **Use `@pytest.mark.slow` for performance tests**
2. **Mock external services**: Avoid network calls
3. **Use SQLite for testing**: Faster than PostgreSQL
4. **Clean up resources**: Automatic cleanup in fixtures

## Troubleshooting

### Common Issues

#### Database Connection Errors

- Ensure SQLite is available
- Check file permissions for test database
- Verify database URL configuration

#### Import Errors

- Check Python path includes backend directory
- Verify all dependencies are installed
- Check for circular imports

#### Authentication Test Failures

- Verify JWT secret key is set
- Check token expiration settings
- Ensure user fixtures are properly created

#### Mock Failures

- Verify mock paths are correct
- Check that mocks are applied before function calls
- Ensure mocks are properly configured

### Getting Help

1. Check the test output for specific error messages
2. Review the test configuration in `conftest.py`
3. Verify that all dependencies are installed
4. Check the pytest documentation for advanced usage

## Contributing

When adding new features or fixing bugs:

1. **Write tests first**: Follow TDD principles
2. **Update existing tests**: Ensure all tests pass
3. **Add new test cases**: Cover new functionality
4. **Maintain coverage**: Aim for >90% code coverage
5. **Document changes**: Update this README if needed

## Test Metrics

### Coverage Goals

- **Overall Coverage**: >90%
- **API Endpoints**: 100%
- **Core Security**: 100%
- **Database Models**: >95%
- **Business Logic**: >90%

### Performance Goals

- **Test Suite Runtime**: <30 seconds
- **Individual Test**: <1 second
- **Database Operations**: <100ms
- **API Response**: <500ms

---

For more information about pytest, see the [official documentation](https://docs.pytest.org/).

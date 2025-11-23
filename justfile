# justfile for starter-fastapi

# Default recipe to display help information
default:
    @just --list

# Install dependencies
install:
    uv sync --all-extras

# Install dependencies including dev dependencies
install-dev:
    uv sync --all-extras

# Run the FastAPI application in development mode
dev:
    uv run uvicorn starter_fastapi.main:app --reload --host 0.0.0.0 --port 8000

# Run the FastAPI application in production mode
run:
    uv run uvicorn starter_fastapi.main:app --host 0.0.0.0 --port 8000

# Run all tests
test:
    uv run pytest

# Run tests with coverage report
test-cov:
    uv run pytest --cov=starter_fastapi --cov-report=term-missing --cov-report=html

# Run tests in watch mode
test-watch:
    uv run pytest-watch

# Run linting with ruff
lint:
    uv run ruff check .

# Run formatting with ruff
format:
    uv run ruff format .

# Run ruff check and format
lint-fix:
    uv run ruff check --fix .
    uv run ruff format .

# Run type checking with mypy
type-check:
    uv run mypy src/starter_fastapi

# Run all quality checks (lint, type-check, test)
check: lint type-check test

# Clean up generated files
clean:
    rm -rf .pytest_cache
    rm -rf .mypy_cache
    rm -rf .ruff_cache
    rm -rf htmlcov
    rm -rf .coverage
    rm -rf dist
    rm -rf build
    rm -rf *.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Build Docker image
docker-build:
    docker build -t starter-fastapi:latest .

# Run Docker container
docker-run:
    docker run -p 8000:8000 starter-fastapi:latest

# Run with docker-compose
docker-up:
    docker-compose up -d

# Stop docker-compose services
docker-down:
    docker-compose down

# Install pre-commit hooks
pre-commit-install:
    uv run pre-commit install

# Run pre-commit on all files
pre-commit-run:
    uv run pre-commit run --all-files

# Generate a new migration
migration-generate name:
    uv run alembic revision --autogenerate -m "{{name}}"

# Apply migrations
migrate:
    uv run alembic upgrade head

# Show current coverage
coverage-report:
    uv run coverage report
    uv run coverage html
    @echo "Coverage report generated in htmlcov/index.html"

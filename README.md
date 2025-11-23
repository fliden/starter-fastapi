# starter-fastapi

A production-ready FastAPI starter template with modern Python best practices.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLModel**: SQL databases with Python objects (ORM)
- **Alembic**: Database migrations made easy
- **uv**: Ultra-fast Python package installer and resolver
- **Ruff**: Lightning-fast Python linter and formatter
- **mypy**: Static type checking
- **pytest**: Comprehensive testing with async support and coverage
- **structlog**: Structured logging for better observability
- **pydantic-settings**: Type-safe configuration management
- **Docker**: Multi-stage builds for production deployment
- **just**: Command runner for common tasks
- **Pre-commit**: Git hooks for code quality

## Project Structure

```
starter-fastapi/
├── src/
│   └── starter_fastapi/
│       ├── api/                 # API layer
│       │   └── v1/             # API version 1
│       │       ├── endpoints/  # API endpoints
│       │       └── router.py   # Version router
│       ├── core/               # Core functionality
│       │   ├── config.py       # Configuration
│       │   ├── db.py           # Database configuration
│       │   ├── logging.py      # Logging setup
│       │   └── exceptions.py   # Custom exceptions
│       ├── migrations/         # Database migrations
│       │   └── versions/       # Migration scripts
│       ├── models/             # SQLModel models
│       ├── services/           # Business logic
│       └── main.py             # Application entry point
├── tests/                      # Test suite
├── .github/workflows/          # CI/CD workflows
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── pyproject.toml             # Project configuration
├── alembic.ini                # Alembic configuration
└── justfile                    # Task runner commands
```

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [just](https://github.com/casey/just) - Command runner (optional but recommended)

## Quick Start

### Installation

1. Install dependencies:

```bash
uv sync --all-extras
```

Or with just:

```bash
just install-dev
```

2. Copy the example environment file:

```bash
cp .env.example .env
```

3. Update the `.env` file with your configuration.

4. Apply database migrations:

```bash
uv run alembic upgrade head
```

### Running the Application

Development mode with auto-reload:

```bash
just dev
```

Or directly with uv:

```bash
uv run uvicorn starter_fastapi.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc

## Development

### Available Commands

```bash
just --list              # Show all available commands
just install-dev         # Install all dependencies
just dev                 # Run development server
just test                # Run tests
just test-cov            # Run tests with coverage
just lint                # Run linter
just format              # Format code
just lint-fix            # Fix linting issues and format
just type-check          # Run type checking
just check               # Run all checks (lint, type-check, test)
just clean               # Clean up generated files
```

### Code Quality

This project uses several tools to maintain code quality:

- **Ruff**: For linting and formatting
- **mypy**: For static type checking
- **pytest**: For testing

Run all checks:

```bash
just check
```

### Testing

Run tests:

```bash
just test
```

Run tests with coverage:

```bash
just test-cov
```

Coverage reports are generated in `htmlcov/index.html`.

### Pre-commit Hooks

Install pre-commit hooks:

```bash
just pre-commit-install
```

Run pre-commit manually:

```bash
just pre-commit-run
```

## Docker

### Build and Run

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to Google Cloud Run.

Build the Docker image:

```bash
just docker-build
```

Run the container:

```bash
just docker-run
```

### Docker Compose

Start services:

```bash
just docker-up
```

Stop services:

```bash
just docker-down
```

## API Documentation

Once the application is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Configuration

Configuration is managed through environment variables using `pydantic-settings`. See `.env.example` for all available options.

Key configuration areas:

- **Application**: Name, version, description, environment
- **Server**: Host, port, reload settings
- **CORS**: Allowed origins, credentials, methods, headers
- **Logging**: Level, format
- **API**: Versioning prefix

## Project Structure Details

### Core Modules

- `core/config.py`: Application settings using pydantic-settings
- `core/logging.py`: Structured logging configuration with structlog
- `core/exceptions.py`: Custom exception handlers

### API Layer

- `api/v1/`: API version 1 implementation
- `api/v1/endpoints/`: Individual endpoint modules
- `api/v1/router.py`: Main router for v1

### Models

SQLModel models for database tables and Pydantic models for request/response validation.

### Services

Business logic layer, separated from API endpoints for better testability and reusability.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run `just check` to ensure code quality
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Roadmap

Future enhancements to consider:

- [x] Database integration (SQLModel, SQLite, Alembic)
- [ ] Authentication & authorization (JWT, OAuth2)
- [ ] Caching (Redis)
- [ ] Background tasks (Celery, ARQ)
- [ ] Rate limiting
- [ ] API versioning middleware
- [ ] Prometheus metrics
- [ ] OpenTelemetry tracing
- [ ] GraphQL support
- [ ] WebSocket support

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

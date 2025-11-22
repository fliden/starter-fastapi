# Contributing to starter-fastapi

Thank you for your interest in contributing to starter-fastapi! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/starter-fastapi.git
cd starter-fastapi
```

2. **Install dependencies**

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync --all-extras
```

3. **Set up pre-commit hooks**

```bash
just pre-commit-install
```

4. **Copy environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your configuration.

## Development Workflow

### Running the Application

```bash
# Development mode with auto-reload
just dev

# Or directly with uv
uv run uvicorn starter_fastapi.main:app --reload
```

### Code Quality

Before submitting your changes, ensure all quality checks pass:

```bash
# Run all checks (linting, type checking, tests)
just check

# Or run individually
just lint          # Run linter
just format        # Format code
just type-check    # Run type checking
just test          # Run tests
just test-cov      # Run tests with coverage
```

### Testing

```bash
# Run all tests
just test

# Run tests with coverage report
just test-cov

# Run specific test file
uv run pytest tests/test_api/test_items.py

# Run specific test function
uv run pytest tests/test_api/test_items.py::test_create_item
```

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write descriptive docstrings for modules, classes, and functions
- Maximum line length: 100 characters

### Code Organization

- Keep functions small and focused on a single task
- Use meaningful variable and function names
- Separate business logic (services) from API endpoints
- Write comprehensive tests for new features

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(items): add filtering by price range

Add min_price and max_price query parameters to the list items endpoint
to allow filtering items by price range.

Closes #123
```

## Pull Request Process

1. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write code following the coding standards
   - Add tests for new features
   - Update documentation as needed

3. **Run quality checks**

```bash
just check
```

4. **Commit your changes**

```bash
git add .
git commit -m "feat(scope): description"
```

5. **Push to your fork**

```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## Project Structure

```
starter-fastapi/
├── src/starter_fastapi/    # Application source code
│   ├── api/                # API endpoints
│   ├── core/               # Core functionality (config, logging, etc.)
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic
│   └── main.py             # Application entry point
├── tests/                  # Test suite
│   ├── test_api/          # API endpoint tests
│   └── test_services/     # Service layer tests
└── ...
```

## Adding New Features

### Adding a New Endpoint

1. Create a new endpoint file in `src/starter_fastapi/api/v1/endpoints/`
2. Define your endpoint functions with proper request/response models
3. Register the router in `src/starter_fastapi/api/v1/router.py`
4. Add tests in `tests/test_api/`

### Adding a New Service

1. Create a new service file in `src/starter_fastapi/services/`
2. Implement business logic with proper error handling
3. Add tests in `tests/test_services/`

### Adding a New Model

1. Create a new model file in `src/starter_fastapi/models/`
2. Define Pydantic models with validation
3. Add tests to verify model validation

## Testing Guidelines

- Write tests for all new features
- Aim for high test coverage (>80%)
- Use fixtures to avoid code duplication
- Test both success and failure cases
- Test edge cases and boundary conditions

## Documentation

- Update README.md if adding new features or changing setup
- Add docstrings to all public functions and classes
- Update API documentation examples if needed

## Getting Help

If you need help or have questions:

- Check existing issues and pull requests
- Create a new issue with the "question" label
- Reach out to maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

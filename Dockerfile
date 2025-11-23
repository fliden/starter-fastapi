# Multi-stage Dockerfile for production-ready FastAPI application

# Stage 1: Base stage with Python and uv
FROM python:3.12-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_HTTP_TIMEOUT=600

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Stage 2: Builder stage
FROM base AS builder

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./
COPY .python-version ./

# Use uv export to generate requirements from lock file and install into system python
RUN uv export --frozen --no-dev --no-emit-project --format requirements-txt | uv pip install --system -r /dev/stdin

# Stage 3: Production stage
FROM base AS production

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/

# Set PYTHONPATH to include source directory
ENV PYTHONPATH=/app/src

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/v1/health')" || exit 1

# Run the application
CMD ["uvicorn", "starter_fastapi.main:app", "--host", "0.0.0.0", "--port", "8080"]

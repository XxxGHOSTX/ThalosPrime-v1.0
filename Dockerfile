# Dockerfile for Thalos Prime v1.0
# Multi-stage build for optimal image size

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt requirements-dev.txt pyproject.toml ./
COPY src/ ./src/
COPY README.md LICENSE ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --wheel-dir /wheels .

# Runtime stage
FROM python:3.11-slim

LABEL maintainer="Thalos Prime Team"
LABEL description="Thalos Prime - Deterministic AI Agent Session Management System"
LABEL version="1.0.0"

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /wheels/*.whl && \
    rm -rf /wheels

# Create app user for security
RUN useradd -m -u 1000 thalos && \
    mkdir -p /app/.thalos/sessions /app/logs && \
    chown -R thalos:thalos /app

# Switch to app user
USER thalos

# Copy necessary files
COPY --chown=thalos:thalos examples/ ./examples/
COPY --chown=thalos:thalos scripts/ ./scripts/

# Make scripts executable
RUN chmod +x scripts/*.sh 2>/dev/null || true

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV THALOS_HOME=/app
ENV THALOS_SESSION_DIR=/app/.thalos/sessions
ENV THALOS_LOG_DIR=/app/logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import thalos_prime; print('healthy')" || exit 1

# Default command
CMD ["thalos", "--help"]

# Expose port for API (when implemented)
EXPOSE 8000

# Volume for persistent data
VOLUME ["/app/.thalos", "/app/logs"]

# Lecture 7.5 – Dockerizing the Model Service (Best Practices for Images)

## Human Transcript

Okay, so you know the basics of Docker. Now let's build a production-ready image for our model service. And I'm going to show you all the best practices that teams at companies like Netflix, Uber, and Airbnb use for their ML services.

Let me start with a complete Dockerfile and then explain each section:

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.10-slim AS runtime

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser api/ ./api/
COPY --chown=appuser:appuser models/ ./models/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/models/churn_model.joblib \
    PORT=8000

# Switch to non-root user
USER appuser

# Expose port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run the application
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
```

Let me walk through the important decisions here.

Multi-stage build. We have two stages: builder and runtime. In the builder stage, we install build tools like compilers that are needed to install some Python packages. But we don't want those tools in the final image because they make it bigger and create security risks. So the runtime stage starts fresh and only copies the virtual environment with our installed packages.

Virtual environment. Notice we create a virtual environment in the builder stage. Some people skip this and install packages globally. But using a venv gives us a clean, isolated Python environment that's easy to copy to the runtime stage.

apt-get best practices. Look at the apt-get commands. We update, install, and then immediately remove the package lists with `rm -rf /var/lib/apt/lists/*`. This is called "cleaning up" and it reduces image size. Also, `--no-install-recommends` tells apt not to install suggested packages we don't need.

Non-root user. We create a user called `appuser` and run the application as that user. Why? Security. If someone exploits a vulnerability in your app, they're limited to what `appuser` can do instead of having root access to the whole container.

Environment variables. We use several important ones:
- `PYTHONDONTWRITEBYTECODE=1` prevents Python from writing `.pyc` files. Less clutter.
- `PYTHONUNBUFFERED=1` ensures logs appear immediately without buffering. Important for seeing logs in real time.
- `MODEL_PATH` and `PORT` make the app configurable without code changes.

Health check. The health check starts checking 60 seconds after the container starts (`start-period=60s`). This gives the model time to load. Then it checks every 30 seconds. If it fails 3 times in a row, the container is marked unhealthy.

Now let's talk about some more advanced practices.

Pinning versions. Your `requirements.txt` should have exact versions:

```
pandas==1.5.3
scikit-learn==1.2.2
fastapi==0.95.1
uvicorn==0.21.1
joblib==1.2.0
numpy==1.24.2
```

Don't use `>=` or `~=` in production images. You want reproducible builds. The same Dockerfile should produce the same image every time.

Layer ordering. Docker caches layers. Each instruction creates a layer. If nothing changed in a layer, Docker reuses the cached version. So put things that change less often earlier in the Dockerfile:

1. Base image (rarely changes)
2. System packages (rarely changes)
3. Python dependencies (changes when you update requirements.txt)
4. Application code (changes frequently)

This way, when you just change code, Docker reuses cached layers for everything else.

Reducing image size. A few more tips:

Use slim or alpine base images:
```dockerfile
FROM python:3.10-slim  # Good balance of size and compatibility
# FROM python:3.10-alpine  # Smaller but may have issues with some packages
```

Remove unnecessary files:
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt && \
    find /opt/venv -type d -name __pycache__ -exec rm -rf {} + && \
    find /opt/venv -type f -name "*.pyc" -delete
```

Use `.dockerignore` to exclude files from the build context:

```
# .dockerignore
.git
.gitignore
__pycache__
*.pyc
*.pyo
.pytest_cache
.coverage
htmlcov
.env
*.egg-info
dist
build
notebooks
tests
docs
README.md
*.md
.idea
.vscode
```

This makes builds faster and prevents accidentally including sensitive files.

Security scanning. Before pushing to a registry, scan your image for vulnerabilities:

```bash
# Using Docker's built-in scanner
docker scan churn-model:v1

# Using Trivy (popular open source scanner)
trivy image churn-model:v1
```

Fix any critical or high severity vulnerabilities before deploying.

Labels and metadata. Add labels to your image for documentation:

```dockerfile
LABEL maintainer="mlops-team@company.com" \
      version="1.0.0" \
      description="Churn prediction model service" \
      org.opencontainers.image.source="https://github.com/company/churn-model"
```

These labels show up when you inspect the image and help with image management.

Let's also look at a docker-compose file for local development:

```yaml
# docker-compose.yml
version: '3.8'

services:
  model-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models/churn_model.joblib
      - LOG_LEVEL=DEBUG
    volumes:
      - ./models:/app/models:ro  # Mount models directory (read-only)
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Optional: Add monitoring services
  prometheus:
    image: prom/prometheus:v2.40.0
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - model-api
```

With docker-compose, you can run everything with one command:

```bash
docker-compose up --build
```

One more important topic: handling secrets. Never put secrets in your Dockerfile or image. No API keys, no passwords, no tokens. Instead:

1. Use environment variables at runtime:
```bash
docker run -e API_KEY=secret123 churn-model:v1
```

2. Or use Docker secrets / Kubernetes secrets in production

3. Or mount a secrets file:
```bash
docker run -v /path/to/secrets:/app/secrets:ro churn-model:v1
```

Now, let me show you a complete build and push workflow:

```bash
# Build the image
docker build -t churn-model:v1.0.0 .

# Test locally
docker run -d -p 8000:8000 --name churn-test churn-model:v1.0.0
curl http://localhost:8000/health
docker logs churn-test
docker stop churn-test && docker rm churn-test

# Tag for registry
docker tag churn-model:v1.0.0 my-registry.com/churn-model:v1.0.0
docker tag churn-model:v1.0.0 my-registry.com/churn-model:latest

# Push to registry
docker push my-registry.com/churn-model:v1.0.0
docker push my-registry.com/churn-model:latest
```

Notice we tag with both a specific version and `latest`. The specific version is for production deployments. `latest` is convenient for development but don't use it in production. Always use specific versions in production so you know exactly what's running.

Alright, that's how you build a production-ready Docker image for your ML model. The key practices are: multi-stage builds, non-root user, proper layer ordering, version pinning, security scanning, and never including secrets in the image.

In the next lecture, we'll test our API locally before we move on to deployment.

Any questions? See you in the next one.

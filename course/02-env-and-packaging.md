# Module 02: Environment & Packaging

## 🎯 Goals

- Set up **reproducible Python environments** with `uv` or `poetry`
- Use **pyproject.toml** for modern dependency management
- Create **Docker base images** for training and serving
- Configure **pre-commit hooks** for code quality
- Build **multi-stage Dockerfiles** to minimize image size
- Lock dependencies for **deterministic builds**

---

## 📖 Key Terms

- **uv**: Ultra-fast Python package installer and resolver (Rust-based, faster than pip)
- **poetry**: Python dependency management with automatic virtual environments
- **pyproject.toml**: PEP 518 standard for Python project metadata and dependencies
- **pre-commit**: Framework for managing git hooks (linting, formatting, security checks)
- **Multi-stage build**: Docker pattern using separate stages (build vs runtime) to reduce final image size
- **Lock file**: Exact pinned versions of all dependencies (transitive included) for reproducibility

---

## 🔧 Commands First: Setup with `uv` (Recommended for Speed)

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create new project
cd ~/mlops-demo
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "mlops-demo"
version = "0.1.0"
description = "MLOps course demo project"
requires-python = ">=3.11"
dependencies = [
    "scikit-learn>=1.3.0",
    "pandas>=2.1.0",
    "mlflow>=2.9.0",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.11.0",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
    "pre-commit>=3.5.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]  # pycodestyle errors, pyflakes, isort

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
EOF

# Install dependencies
uv pip install -e ".[dev]"

# Generate lock file
uv pip freeze > requirements-lock.txt
```

**Why**: `uv` is 10-100x faster than pip. `pyproject.toml` is modern Python packaging standard. Lock file ensures reproducibility.

---

## ✅ Verify uv Setup

```bash
# Check Python version
python --version  # Should be 3.11+

# Check installed packages
uv pip list | grep -E 'mlflow|scikit-learn'
# Should show exact versions

# Verify lock file
wc -l requirements-lock.txt
# Should have 50+ lines (includes transitive deps)
```

---

## 🎨 Alternative: Setup with Poetry

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create project
poetry new mlops-demo
cd mlops-demo

# Add dependencies
poetry add scikit-learn pandas mlflow fastapi uvicorn
poetry add --group dev pytest black ruff mypy pre-commit

# Install
poetry install

# Activate shell
poetry shell

# Lock file automatically created as poetry.lock
```

**Why**: Poetry has better dependency resolution than pip and auto-manages virtual environments. Choose `uv` for speed or `poetry` for ergonomics.

---

## 🪝 Pre-commit Hooks (Catch Issues Before Commit)

```bash
# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
EOF

# Install hooks
pre-commit install

# Test hooks (run on all files)
pre-commit run --all-files
```

**Why**: Catches formatting, linting, secrets, and large files before they reach CI. Saves time and enforces standards.

---

## ✅ Verify Pre-commit

```bash
# Create bad file
echo "x=1" > test.py  # No spaces around =

# Try to commit
git add test.py
git commit -m "Test"
# Should fail with ruff/black errors

# Fix and retry
black test.py
git add test.py
git commit -m "Test"  # Now passes
```

---

## 🐳 Docker Base Image (Training)

```bash
# Create Dockerfile.train
cat > Dockerfile.train << 'EOF'
# Multi-stage build: builder + runtime
FROM python:3.11-slim as builder

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependencies
WORKDIR /app
COPY pyproject.toml requirements-lock.txt ./

# Install deps to /app/.venv
RUN uv venv /app/.venv && \
    uv pip install --no-cache -r requirements-lock.txt

# Runtime stage
FROM python:3.11-slim

# Copy only venv from builder
COPY --from=builder /app/.venv /app/.venv

# Set PATH to use venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy source code
COPY src/ ./src/
COPY data/ ./data/

# Run training
CMD ["python", "src/train.py"]
EOF

# Build image
docker build -f Dockerfile.train -t ${REGISTRY}/mlops-train:latest .
```

**Why**: Multi-stage build separates build tools from runtime, reducing final image size by 50-70%. Slim base (not alpine) for compatibility with ML libraries.

---

## 🐳 Docker Base Image (Serving)

```bash
# Create Dockerfile.serve
cat > Dockerfile.serve << 'EOF'
FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install serving dependencies
COPY pyproject.toml requirements-lock.txt ./
RUN uv venv /app/.venv && \
    uv pip install --no-cache -r requirements-lock.txt

ENV PATH="/app/.venv/bin:$PATH"

# Copy API code and model
COPY src/api.py ./
COPY models/ ./models/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Build
docker build -f Dockerfile.serve -t ${REGISTRY}/mlops-serve:latest .
```

**Why**: Separate images for training and serving. Serving image is optimized for fast startup and includes health checks for orchestrators.

---

## ✅ Verify Docker Images

```bash
# Check image sizes
docker images | grep mlops
# Should be <500MB for slim images

# Test training image
docker run --rm ${REGISTRY}/mlops-train:latest
# Should run training script

# Test serving image (if you have api.py)
docker run -d -p 8000:8000 --name api-test ${REGISTRY}/mlops-serve:latest
sleep 5
curl http://localhost:8000/health
# Should return {"status": "healthy"}

docker stop api-test && docker rm api-test
```

---

## 🏗️ Docker Compose for Local Dev

```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: mlops
      POSTGRES_PASSWORD: mlops
      POSTGRES_DB: mlops
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    command: >
      mlflow server
      --backend-store-uri postgresql://mlops:mlops@db:5432/mlops
      --default-artifact-root /mlflow/artifacts
      --host 0.0.0.0
      --port 5000
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/mlflow
    depends_on:
      - db

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  mlflow_data:
  minio_data:
EOF

# Start stack
docker compose up -d

# Verify
docker compose ps
curl http://localhost:5000  # MLflow UI
curl http://localhost:9001  # MinIO console
```

**Why**: Local stack mimics production. All services in containers with network isolation. One command to start entire environment.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Create a reproducible Python environment with pre-commit hooks and Docker.

1. **Setup project**:
```bash
mkdir -p ~/mlops-lab-02 && cd ~/mlops-lab-02
git init
```

2. **Add pyproject.toml**:
```bash
cat > pyproject.toml << 'EOF'
[project]
name = "lab02"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pandas>=2.1.0", "scikit-learn>=1.3.0"]

[project.optional-dependencies]
dev = ["black>=23.11.0", "ruff>=0.1.6"]
EOF

uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uv pip freeze > requirements-lock.txt
```

3. **Add pre-commit**:
```bash
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
EOF

pre-commit install
```

4. **Create sample code**:
```bash
cat > train.py << 'EOF'
import pandas as pd
from sklearn.datasets import load_iris

def main():
    data = load_iris(as_frame=True)
    print(f"Loaded {len(data.frame)} samples")

if __name__ == "__main__":
    main()
EOF

python train.py  # Should print "Loaded 150 samples"
```

5. **Test pre-commit**:
```bash
git add .
git commit -m "Add training script"
# Black should auto-format
```

6. **Create Dockerfile**:
```bash
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY train.py .
CMD ["python", "train.py"]
EOF

docker build -t lab02:latest .
docker run --rm lab02:latest
# Should print "Loaded 150 samples"
```

**Expected output**: Python env works, pre-commit runs on commit, Docker runs training script.

---

## ❓ Quiz (5 Questions)

1. **What is the benefit of multi-stage Docker builds?**
   - Answer: Separates build dependencies from runtime, reducing final image size and attack surface.

2. **Why use lock files (requirements-lock.txt or poetry.lock)?**
   - Answer: Pins transitive dependencies to exact versions for reproducible builds across environments.

3. **What does pre-commit do?**
   - Answer: Runs checks (linting, formatting, secrets scan) before git commit to catch issues early.

4. **Why use python:3.11-slim instead of python:3.11-alpine for ML?**
   - Answer: Slim uses glibc (better ML library compatibility); alpine uses musl (breaks numpy/scipy wheels).

5. **What's the advantage of uv over pip?**
   - Answer: 10-100x faster installation and resolution due to Rust implementation.

---

## ⚠️ Common Mistakes

1. **Using `pip install` without lock file** → Non-reproducible builds.  
   *Fix*: Always generate and commit `requirements-lock.txt` or `poetry.lock`.

2. **Alpine images for ML** → Binary incompatibilities with numpy/scipy.  
   *Fix*: Use `python:3.11-slim` or `python:3.11-slim-bullseye`.

3. **Skipping pre-commit hooks** → Bad code reaches CI/prod.  
   *Fix*: Run `pre-commit install` after cloning; enforce in CI.

4. **Large Docker images (>2GB)** → Slow pulls, wasted storage.  
   *Fix*: Multi-stage builds, `.dockerignore`, remove build tools from runtime.

5. **Hardcoding versions in Dockerfile** → Stale images.  
   *Fix*: Use `ARG` for versions, rebuild regularly.

---

## 🛠️ Troubleshooting

**Issue**: "Docker build fails with 'no such file or directory' for requirements-lock.txt"  
→ **Root cause**: File not copied or missing `.dockerignore` excluding it.  
→ **Fix**: Check `COPY` commands, ensure file exists, review `.dockerignore`.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Docker build failures"

**Issue**: "pre-commit hook too slow (>30 seconds)"  
→ **Root cause**: Hooks running on all files or mypy analyzing entire venv.  
→ **Fix**: Use `stages: [commit]` in config, exclude venv from mypy, or skip mypy in pre-commit.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Slow pre-commit"

---

## 📚 Key Takeaways

- **uv** is fastest for Python package management; **poetry** has best ergonomics
- **pyproject.toml** is modern standard for Python projects (replaces setup.py)
- **Lock files** are mandatory for reproducibility (pin transitive deps)
- **Pre-commit hooks** enforce quality before CI (formatting, linting, secrets)
- **Multi-stage Docker builds** minimize image size (builder vs runtime stages)
- **docker-compose** runs local MLOps stack (DB, MLflow, MinIO) in one command

---

## 🚀 Next Steps

- **Module 03**: Version data with DVC, validate quality with Great Expectations/Evidently
- **Module 04**: Track experiments with MLflow (params, metrics, models)
- **Hands-on**: Add DVC to track datasets in Churn Predictor project

---

**[← Module 01](01-mlops-foundations.md)** | **[Next: Module 03 →](03-data-versioning-and-quality.md)**

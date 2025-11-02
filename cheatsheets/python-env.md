# Python Environment Management Cheatsheet

## uv (Ultra-fast package manager)

### Installation
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Virtual Environment
```bash
# Create venv
uv venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

### Package Management
```bash
# Install package
uv pip install pandas

# Install from requirements
uv pip install -r requirements.txt

# Install editable
uv pip install -e .

# Install with extras
uv pip install -e ".[dev]"

# Freeze to lock file
uv pip freeze > requirements-lock.txt

# Uninstall
uv pip uninstall pandas

# List installed
uv pip list
```

---

## poetry (Modern dependency management)

### Installation
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Project Management
```bash
# Create new project
poetry new my-project
cd my-project

# Initialize in existing project
poetry init

# Install dependencies
poetry install

# Add dependency
poetry add pandas
poetry add --group dev pytest  # Dev dependency

# Remove dependency
poetry remove pandas

# Update dependencies
poetry update

# Show installed
poetry show
poetry show --tree  # With dependencies

# Activate venv
poetry shell

# Run command in venv
poetry run python script.py
```

### Lock File
```bash
# Generate/update lock
poetry lock

# Install from lock (CI/CD)
poetry install --no-root --only main
```

---

## pyproject.toml (Modern standard)

### Minimal Example
```toml
[project]
name = "my-mlops-project"
version = "0.1.0"
description = "MLOps project"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
    "mlflow>=2.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]
```

---

## pip (Traditional)

### Basic Commands
```bash
# Install
pip install pandas

# Install from requirements
pip install -r requirements.txt

# Freeze
pip freeze > requirements.txt

# Upgrade
pip install --upgrade pandas

# Uninstall
pip uninstall pandas

# List
pip list

# Show package info
pip show pandas
```

---

## conda (Data science focused)

### Environment Management
```bash
# Create environment
conda create -n mlops python=3.11

# Activate
conda activate mlops

# Deactivate
conda deactivate

# List environments
conda env list

# Remove environment
conda remove -n mlops --all
```

### Package Management
```bash
# Install
conda install pandas

# Install from environment.yml
conda env create -f environment.yml

# Export environment
conda env export > environment.yml

# Update
conda update pandas
conda update --all

# List
conda list
```

### environment.yml Example
```yaml
name: mlops
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pandas>=2.0
  - scikit-learn>=1.3
  - pip
  - pip:
      - mlflow>=2.9.0
```

---

## Docker for Python

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (caching)
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt

# Copy code
COPY . .

CMD ["python", "main.py"]
```

### Multi-stage Build
```dockerfile
# Builder stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY pyproject.toml requirements-lock.txt ./
RUN pip install --no-cache-dir --user -r requirements-lock.txt

# Runtime stage
FROM python:3.11-slim

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
```

---

## Quick Decision Matrix

| Use Case | Tool | Why |
|----------|------|-----|
| **Speed priority** | uv | 10-100x faster than pip |
| **Best ergonomics** | poetry | Auto venv, great dependency resolution |
| **Simple project** | pip + venv | Minimal, built-in |
| **Data science** | conda | Non-Python deps (CUDA, system libs) |
| **Production** | Docker | Reproducible, isolated |
| **CI/CD** | uv or poetry | Fast, lock files |

---

## Best Practices

1. **Always use virtual environments** (never install globally)
2. **Pin dependencies** (use lock files: requirements-lock.txt, poetry.lock)
3. **Separate dev and prod dependencies**
4. **Use pyproject.toml** (modern standard, tools support it)
5. **Test in Docker** (catch environment issues early)
6. **Version Python** (specify minimum in pyproject.toml)
7. **Cache dependencies in CI** (speed up builds)

---

## Common Issues

### "Module not found"
```bash
# Check venv is activated
which python  # Should be in .venv/

# Reinstall
pip install -e .
```

### "Permission denied"
```bash
# Never use sudo with pip!
# Use venv or --user flag
pip install --user pandas
```

### "Conflicting dependencies"
```bash
# Use poetry for better resolution
poetry add package-name

# Or use constraint files with pip
pip install -c constraints.txt -r requirements.txt
```

### "Different results on different machines"
```bash
# Lock dependencies
uv pip freeze > requirements-lock.txt

# Or use poetry.lock
poetry lock
```

---

## Resources

- [uv docs](https://astral.sh/uv)
- [poetry docs](https://python-poetry.org/docs/)
- [PEP 621 (pyproject.toml)](https://peps.python.org/pep-0621/)
- [pip docs](https://pip.pypa.io/)
- [conda docs](https://docs.conda.io/)

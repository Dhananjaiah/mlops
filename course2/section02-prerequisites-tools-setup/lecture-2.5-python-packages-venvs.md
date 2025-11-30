# Lecture 2.5 – Installing Required Python Packages & Virtual Environments

---

## Managing Dependencies Like a Pro

In this lecture, we're going to talk about Python packages and virtual environments. This might sound basic, but getting it right is crucial.

Here's why: one of the most common phrases in data science is "it works on my machine." Usually, that's because of dependency issues.

Let's fix that.

---

## Why Virtual Environments?

Imagine you have two projects:
- Project A needs pandas 1.5
- Project B needs pandas 2.0

If you install packages globally, one project will break.

Virtual environments solve this by creating isolated Python installations for each project.

```
Global Python          Project A venv      Project B venv
├── python 3.11        ├── python 3.11     ├── python 3.11
├── pip                ├── pip             ├── pip
└── (nothing else)     ├── pandas 1.5      ├── pandas 2.0
                       └── numpy 1.24      └── numpy 1.26
```

Each project has its own packages. No conflicts.

---

## Creating Virtual Environments

### Method 1: venv (Built-in)

The simplest method—uses Python's built-in `venv`:

```bash
# Navigate to project
cd ~/mlops-course/mlops-churn-prediction

# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your prompt changes to show (venv)
```

### Method 2: conda

If you use Anaconda or Miniconda:

```bash
# Create environment
conda create -n mlops-course python=3.11

# Activate
conda activate mlops-course
```

### Method 3: pyenv + virtualenv

For managing multiple Python versions:

```bash
# Install pyenv (macOS)
brew install pyenv pyenv-virtualenv

# Install Python version
pyenv install 3.11.6

# Create virtualenv
pyenv virtualenv 3.11.6 mlops-course

# Activate
pyenv activate mlops-course
```

### My Recommendation

For this course, use **venv**. It's simple and built-in.

If you work with many Python versions, learn pyenv later.

---

## Managing Packages

### Basic pip

The simplest way to manage packages:

```bash
# Install a package
pip install pandas

# Install specific version
pip install pandas==2.0.0

# Install from requirements file
pip install -r requirements.txt

# Show installed packages
pip list

# Show package info
pip show pandas

# Uninstall
pip uninstall pandas
```

### requirements.txt

The traditional way to track dependencies:

```txt
pandas==2.1.0
numpy==1.26.0
scikit-learn==1.3.2
mlflow==2.8.0
dvc==3.30.1
fastapi==0.104.1
uvicorn==0.24.0
pytest==7.4.3
black==23.11.0
```

Create it:
```bash
# Export current packages
pip freeze > requirements.txt

# Or create manually with only direct dependencies
```

**Problem with pip freeze**: It includes ALL packages, including dependencies of dependencies. This can be messy.

### Better: pip-tools

pip-tools separates direct dependencies from resolved dependencies:

```bash
# Install pip-tools
pip install pip-tools

# Create requirements.in (your direct dependencies)
cat > requirements.in << 'EOF'
pandas>=2.0
scikit-learn>=1.3
mlflow>=2.8
dvc>=3.30
fastapi>=0.104
uvicorn>=0.24
EOF

# Compile to requirements.txt (with all resolved dependencies)
pip-compile requirements.in

# Install
pip-sync requirements.txt
```

Now `requirements.in` has what you need, and `requirements.txt` has everything resolved.

### Modern: pyproject.toml

The modern way is to use `pyproject.toml` (we set this up in the last lecture):

```toml
[project]
dependencies = [
    "pandas>=2.0.0",
    "scikit-learn>=1.3.0",
    "mlflow>=2.8.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "black>=23.0.0"]
serving = ["fastapi>=0.104.0", "uvicorn>=0.24.0"]
```

Install with:
```bash
pip install -e ".[dev,serving]"
```

---

## Packages We Need

Let's install everything for this course:

### Core Data Science

```bash
pip install pandas numpy scikit-learn
```

- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: ML algorithms

### MLOps Tools

```bash
pip install mlflow dvc
```

- **mlflow**: Experiment tracking, model registry
- **dvc**: Data versioning

### API & Serving

```bash
pip install fastapi uvicorn pydantic
```

- **fastapi**: API framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation

### Development

```bash
pip install pytest black flake8 isort pre-commit
```

- **pytest**: Testing
- **black**: Code formatting
- **flake8**: Linting
- **isort**: Import sorting
- **pre-commit**: Git hooks

### Configuration

```bash
pip install pyyaml python-dotenv
```

- **pyyaml**: YAML parsing
- **python-dotenv**: Environment variables

### All at Once

```bash
pip install \
    pandas numpy scikit-learn \
    mlflow dvc \
    fastapi uvicorn pydantic \
    pytest black flake8 isort pre-commit \
    pyyaml python-dotenv
```

Or create `requirements.txt`:

```txt
# Core
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0

# MLOps
mlflow>=2.8.0
dvc>=3.30.0

# API
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0

# Development
pytest>=7.4.0
black>=23.11.0
flake8>=6.1.0
isort>=5.12.0
pre-commit>=3.5.0

# Config
pyyaml>=6.0
python-dotenv>=1.0.0
```

Then:
```bash
pip install -r requirements.txt
```

---

## Development vs Production Dependencies

Important concept: not all packages are needed everywhere.

### Development Only
- pytest (testing)
- black (formatting)
- flake8 (linting)
- jupyter (notebooks)

### Serving Only
- fastapi
- uvicorn

### Training Only
- scikit-learn
- mlflow (might be in both)

### Everywhere
- pandas
- numpy

Organize with optional dependencies or multiple requirements files:

```
requirements/
├── base.txt          # Core packages
├── dev.txt           # Development tools
├── serving.txt       # API serving
└── training.txt      # Model training
```

**requirements/base.txt**:
```txt
pandas>=2.0.0
numpy>=1.24.0
pyyaml>=6.0
```

**requirements/dev.txt**:
```txt
-r base.txt
pytest>=7.4.0
black>=23.11.0
```

**requirements/training.txt**:
```txt
-r base.txt
scikit-learn>=1.3.0
mlflow>=2.8.0
```

---

## Pinning Versions

Should you pin exact versions?

### Pros of Pinning
- Reproducible environments
- No surprises from updates
- Same behavior everywhere

### Cons of Pinning
- Manual updates required
- Might miss security patches
- Can conflict with other packages

### My Recommendation

**For development**: Use flexible versions (`pandas>=2.0`)
**For production**: Pin exact versions (`pandas==2.1.3`)

Use pip-compile to go from flexible to pinned:

```bash
# requirements.in has flexible versions
# requirements.txt has pinned versions
pip-compile requirements.in
```

---

## Checking Your Environment

Let's verify everything is installed correctly:

```python
#!/usr/bin/env python3
"""Verify all course packages are installed."""

def check_package(name, import_name=None):
    """Check if a package is installed."""
    import_name = import_name or name
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {name}: {version}")
        return True
    except ImportError:
        print(f"✗ {name}: NOT INSTALLED")
        return False

def main():
    packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("mlflow", "mlflow"),
        ("dvc", "dvc"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("pytest", "pytest"),
        ("black", "black"),
        ("yaml", "yaml"),
    ]
    
    print("\n📦 Checking installed packages...\n")
    
    all_ok = True
    for name, import_name in packages:
        if not check_package(name, import_name):
            all_ok = False
    
    print()
    if all_ok:
        print("✅ All packages installed!")
    else:
        print("❌ Some packages are missing. Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
```

Save as `check_packages.py` and run:

```bash
python check_packages.py
```

---

## Pre-commit Hooks

Let's set up pre-commit hooks to automatically format and lint code:

```bash
# Install pre-commit
pip install pre-commit
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203"]
```

Install the hooks:

```bash
pre-commit install
```

Now, every time you commit, it will:
- Fix trailing whitespace
- Format code with black
- Sort imports with isort
- Check for lint errors

Test it:
```bash
pre-commit run --all-files
```

---

## Common Issues and Fixes

### "Package not found" after installing

Make sure your virtual environment is activated:
```bash
which python  # Should show .../venv/bin/python
```

### Version conflicts

Try:
```bash
pip install --upgrade package-name
# or
pip install package-name --force-reinstall
```

### "Permission denied" on pip install

Never use `sudo pip install`. Instead:
```bash
pip install --user package-name
# or better, use virtual environment
```

### Slow pip installs

Use a mirror:
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package-name
```

Or cache downloads:
```bash
pip install --cache-dir ~/.cache/pip package-name
```

---

## Recap

- Virtual environments isolate project dependencies
- Use `venv` (built-in) for simplicity
- Track dependencies in `requirements.txt` or `pyproject.toml`
- Separate dev, serving, and training dependencies
- Pin versions for production
- Use pre-commit hooks for code quality

Key packages for this course:
- Data: pandas, numpy, scikit-learn
- MLOps: mlflow, dvc
- Serving: fastapi, uvicorn
- Dev: pytest, black, flake8

---

## What's Next

Now that we have our Python environment set up, let's talk about Git—the version control fundamentals you need for MLOps.

---

**Next Lecture**: [2.6 – Git Basics for MLOps (Branching, PRs, Tags)](lecture-2.6-git-basics.md)

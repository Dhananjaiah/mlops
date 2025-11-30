# Lecture 2.4 – Project Structure for an MLOps Course Project

---

## Why Structure Matters

Let me tell you about a common nightmare.

You inherit a data science project. There's one folder with 50 files: notebooks, scripts, CSVs, model files, random text files, and something called `final_final_v3_REAL.py`.

You have no idea what runs what, what depends on what, or where anything is.

This is what happens without structure.

Good structure means:
- Anyone can navigate your project
- Files have a logical home
- Automation is easier
- Debugging is faster

Let's build a proper structure.

---

## The Project We're Building

Remember, we're building a **Customer Churn Prediction System**.

Our project will include:
- Data processing scripts
- Model training code
- Model serving API
- Configuration files
- Tests
- Documentation
- Infrastructure configs

Let's organize all this properly.

---

## The Recommended Structure

Here's the structure we'll use:

```
mlops-churn-prediction/
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Python project config (or requirements.txt)
├── Makefile                 # Common commands
│
├── data/                    # Data directory (DVC tracked)
│   ├── raw/                 # Raw, immutable data
│   ├── processed/           # Cleaned, transformed data
│   └── features/            # Feature-engineered data
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── data/               # Data processing
│   │   ├── __init__.py
│   │   ├── load.py
│   │   ├── validate.py
│   │   └── preprocess.py
│   ├── features/           # Feature engineering
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models/             # Model training
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   └── utils/              # Utilities
│       ├── __init__.py
│       └── logging.py
│
├── serving/                 # Model serving
│   ├── app.py              # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
│
├── pipelines/              # Orchestration pipelines
│   ├── training/
│   │   └── pipeline.py
│   └── inference/
│       └── pipeline.py
│
├── notebooks/              # Jupyter notebooks (exploration only)
│   └── 01_exploration.ipynb
│
├── tests/                  # Tests
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_data.py
│   │   └── test_model.py
│   └── integration/
│       └── test_api.py
│
├── configs/                # Configuration files
│   ├── config.yaml
│   ├── model_config.yaml
│   └── logging.yaml
│
├── scripts/                # Utility scripts
│   ├── setup.sh
│   └── download_data.sh
│
├── infra/                  # Infrastructure
│   ├── docker-compose.yml
│   └── k8s/
│       ├── deployment.yaml
│       └── service.yaml
│
├── docs/                   # Additional documentation
│   ├── architecture.md
│   └── api.md
│
└── .github/                # GitHub specific
    └── workflows/
        └── ci.yml
```

Let me explain each part.

---

## Core Directories Explained

### `data/` – Data Storage

```
data/
├── raw/          # Original, immutable data
├── processed/    # Cleaned data
└── features/     # Feature-engineered data
```

**Rules**:
- Raw data is NEVER modified
- Each processing step has its own subdirectory
- This folder is tracked with DVC (not Git—files are too big)

### `src/` – Source Code

```
src/
├── data/         # Data loading and processing
├── features/     # Feature engineering
├── models/       # Model training and inference
└── utils/        # Shared utilities
```

**Rules**:
- Importable as a Python package (`from src.data import load`)
- Each module has a single responsibility
- No notebooks here—only clean Python scripts

### `serving/` – Model API

```
serving/
├── app.py        # FastAPI application
├── Dockerfile    # Container definition
└── requirements.txt
```

**Rules**:
- Self-contained—can be deployed independently
- Has its own Dockerfile and requirements
- Minimal dependencies (just what's needed for serving)

### `pipelines/` – Orchestration

```
pipelines/
├── training/     # Training pipeline
└── inference/    # Inference/batch pipeline
```

**Rules**:
- Pipeline definitions (Airflow DAGs, Kubeflow, etc.)
- Import from `src/` for actual logic
- Keep pipeline code separate from business logic

### `notebooks/` – Exploration Only

```
notebooks/
└── 01_exploration.ipynb
```

**Rules**:
- ONLY for exploration and prototyping
- Numbered for order (01, 02, etc.)
- Code that works gets moved to `src/`
- Notebooks are NOT production code

### `tests/` – Testing

```
tests/
├── unit/         # Unit tests
└── integration/  # Integration tests
```

**Rules**:
- Mirror the `src/` structure
- Unit tests are fast, isolated
- Integration tests test components together

### `configs/` – Configuration

```
configs/
├── config.yaml        # General config
├── model_config.yaml  # Model hyperparameters
└── logging.yaml       # Logging configuration
```

**Rules**:
- No hardcoded values in code
- Different configs for different environments
- YAML or JSON format

### `infra/` – Infrastructure

```
infra/
├── docker-compose.yml  # Local development
└── k8s/               # Kubernetes manifests
```

**Rules**:
- Everything to deploy the project
- Infrastructure as code
- Separate from application code

---

## Let's Create It

Let's set up this structure:

```bash
cd ~/mlops-course

# Create main project directory
mkdir -p mlops-churn-prediction
cd mlops-churn-prediction

# Create directory structure
mkdir -p data/{raw,processed,features}
mkdir -p src/{data,features,models,utils}
mkdir -p serving
mkdir -p pipelines/{training,inference}
mkdir -p notebooks
mkdir -p tests/{unit,integration}
mkdir -p configs
mkdir -p scripts
mkdir -p infra/k8s
mkdir -p docs
mkdir -p .github/workflows

# Create __init__.py files
touch src/__init__.py
touch src/data/__init__.py
touch src/features/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# Create placeholder files
touch README.md
touch .gitignore
touch Makefile
touch configs/config.yaml
touch serving/app.py
touch serving/Dockerfile
touch serving/requirements.txt
```

Verify the structure:

```bash
tree -a --dirsfirst
# or if you don't have tree:
find . -type f | head -30
```

---

## Important Files

### README.md

Every project needs a README. Here's a template:

```markdown
# Customer Churn Prediction

MLOps project for predicting customer churn.

## Quick Start

```bash
# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run training
make train

# Run API
make serve
```

## Project Structure

[Brief description of structure]

## Data

[How to get the data]

## Training

[How to train a model]

## Serving

[How to serve predictions]
```

### Makefile

A Makefile provides convenient commands:

```makefile
.PHONY: install train serve test clean

install:
	pip install -r requirements.txt

train:
	python -m src.models.train

serve:
	uvicorn serving.app:app --reload

test:
	pytest tests/

lint:
	flake8 src/ tests/
	black --check src/ tests/

format:
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

Now you can run `make train` instead of remembering the full command.

### .gitignore

We created this earlier, but here's a more complete version:

```
# Virtual environments
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.eggs/
dist/
build/

# Data
data/raw/*
data/processed/*
data/features/*
!data/*/.gitkeep

# Models
*.pkl
*.joblib
*.h5
*.pt
models/

# MLflow
mlruns/
mlartifacts/

# DVC
.dvc/cache/
.dvc/tmp/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
*.env
.envrc

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Coverage
.coverage
htmlcov/
```

---

## The src Package

Let's make `src` importable as a Python package.

Create `pyproject.toml` or `setup.py`:

**pyproject.toml** (modern approach):

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "churn-prediction"
version = "0.1.0"
description = "Customer churn prediction MLOps project"
requires-python = ">=3.9"

dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "mlflow>=2.8.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]
serving = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["src*"]
```

Install in development mode:

```bash
pip install -e ".[dev,serving]"
```

Now you can do:

```python
from src.data.load import load_data
from src.models.train import train_model
```

---

## Configuration Management

Let's set up a config file:

**configs/config.yaml**:

```yaml
# Project configuration

project:
  name: churn-prediction
  version: "0.1.0"

data:
  raw_path: data/raw
  processed_path: data/processed
  features_path: data/features

model:
  algorithm: random_forest
  params:
    n_estimators: 100
    max_depth: 10
    random_state: 42

training:
  test_size: 0.2
  cv_folds: 5

mlflow:
  tracking_uri: mlruns
  experiment_name: churn-prediction

serving:
  host: "0.0.0.0"
  port: 8000
```

Load it in code:

**src/utils/config.py**:

```python
"""Configuration loading utilities."""
import yaml
from pathlib import Path

def load_config(config_path: str = "configs/config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# Global config
CONFIG = load_config()
```

---

## Why This Structure?

Let me explain the reasoning:

### Separation of Concerns
- Data code is separate from model code
- Training is separate from serving
- Config is separate from logic

### Testability
- Small modules are easy to test
- `src/` can be tested without serving code
- Tests mirror the source structure

### Flexibility
- Notebooks for exploration, scripts for production
- Different requirements for different components
- Easy to add new components

### Industry Standard
- This structure is common in ML teams
- New team members will understand it
- Tools expect this layout

---

## Recap

A good MLOps project structure has:
- Clear separation of concerns
- Data directory (tracked with DVC)
- Source code as a package
- Separate serving code
- Pipeline definitions
- Tests that mirror source
- Configuration files
- Infrastructure as code
- Documentation

We've set up:
```
mlops-churn-prediction/
├── data/
├── src/
├── serving/
├── pipelines/
├── notebooks/
├── tests/
├── configs/
├── scripts/
├── infra/
├── docs/
└── .github/
```

---

## What's Next

Now that we have our structure, let's install all the Python packages we need and set up our virtual environments properly.

---

**Next Lecture**: [2.5 – Installing Required Python Packages & Virtual Environments](lecture-2.5-python-packages-venvs.md)

# Lecture 6.5 – Reproducing Results End-to-End

---

## The Reproducibility Challenge

"I got 92% accuracy!"
"Great! Can you reproduce it?"
"Um... let me try... now I'm getting 87%."

This happens all the time. True reproducibility requires controlling:
- Code version
- Data version
- Environment
- Random seeds
- Configuration

---

## The Three Pillars

### 1. Code Versioning

Always know what code was used:

```python
import mlflow
import subprocess

# Log git commit
git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
mlflow.set_tag("git_commit", git_commit)

# Log git status (any uncommitted changes?)
git_status = subprocess.check_output(['git', 'status', '--porcelain']).decode()
mlflow.set_tag("git_dirty", "true" if git_status else "false")
```

### 2. Data Versioning

Always know what data was used:

```python
import hashlib

def hash_dataframe(df):
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()

# Log data hash
data_hash = hash_dataframe(train_df)
mlflow.log_param("data_hash", data_hash)
mlflow.log_param("data_path", "data/v1/train.parquet")
```

Or use DVC:
```python
mlflow.log_param("dvc_version", "abc123")  # DVC commit
```

### 3. Environment Versioning

Always know what packages were used:

```python
import pkg_resources

# Log all package versions
packages = {p.key: p.version for p in pkg_resources.working_set}
mlflow.log_dict(packages, "environment/packages.json")

# Or log requirements file
mlflow.log_artifact("requirements.txt")
```

---

## Random Seeds

Control all sources of randomness:

```python
import random
import numpy as np
import torch

def set_seeds(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    
    # For extra determinism (may slow down)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# Set and log seed
SEED = 42
set_seeds(SEED)
mlflow.log_param("random_seed", SEED)
```

Also in sklearn:
```python
model = RandomForestClassifier(random_state=42)
train_test_split(X, y, random_state=42)
```

---

## Reproducibility Checklist

For every experiment, capture:

```python
def log_reproducibility_info():
    # Code
    mlflow.set_tag("git_commit", get_git_commit())
    mlflow.set_tag("git_branch", get_git_branch())
    
    # Data
    mlflow.log_param("data_version", DATA_VERSION)
    mlflow.log_param("train_rows", len(train_df))
    
    # Environment
    mlflow.log_param("python_version", sys.version)
    mlflow.log_artifact("requirements.txt")
    
    # Config
    mlflow.log_artifact("config.yaml")
    
    # Seeds
    mlflow.log_param("random_seed", SEED)
```

---

## Reproducing a Run

Given a run ID, reproduce it:

```python
def reproduce_run(run_id):
    client = MlflowClient()
    run = client.get_run(run_id)
    
    # Get git commit
    git_commit = run.data.tags.get("git_commit")
    print(f"Checkout: git checkout {git_commit}")
    
    # Get data version
    data_version = run.data.params.get("data_version")
    print(f"Data: dvc checkout {data_version}")
    
    # Get config
    config_path = client.download_artifacts(run_id, "config.yaml")
    print(f"Config: {config_path}")
    
    # Get environment
    reqs_path = client.download_artifacts(run_id, "requirements.txt")
    print(f"Install: pip install -r {reqs_path}")
```

---

## Testing Reproducibility

Verify your setup is reproducible:

```python
def test_reproducibility():
    # Run twice with same config
    run1 = train_model(config)
    run2 = train_model(config)
    
    # Metrics should match
    assert run1['accuracy'] == run2['accuracy'], "Results differ!"
    
    # Model weights should match (for deterministic training)
    # This may not always be possible for all models
```

---

## Recap

Reproducibility requires:
1. **Code**: Git commit tracked
2. **Data**: Data version tracked
3. **Environment**: Package versions tracked
4. **Seeds**: Random seeds set and logged
5. **Config**: Full configuration saved

With MLflow, all of this is one artifact away.

---

**Next Lecture**: [6.6 – How MLOps Enforces Reproducibility in a Team](lecture-6.6-team-reproducibility.md)

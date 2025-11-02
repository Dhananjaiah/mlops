# DVC + MLflow Cheatsheet

## DVC (Data Version Control)

### Installation & Setup
```bash
# Install
pip install 'dvc[s3]'  # With S3 support
pip install 'dvc[gs]'  # With GCS support

# Initialize
cd project/
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

### Remote Storage
```bash
# Add S3 remote
dvc remote add -d s3remote s3://mybucket/dvc-store

# Add MinIO (S3-compatible)
dvc remote add -d minio s3://mlops-artifacts
dvc remote modify minio endpointurl http://localhost:9000
dvc remote modify minio access_key_id minioadmin
dvc remote modify minio secret_access_key minioadmin

# Add local remote (for testing)
dvc remote add -d local /tmp/dvc-storage

# List remotes
dvc remote list

# Set default
dvc remote default s3remote

# Save config
git add .dvc/config
git commit -m "Configure DVC remote"
```

### Track Data
```bash
# Add file/folder to DVC
dvc add data/raw/train.csv
dvc add models/model.pkl

# Git tracks only .dvc files
git add data/raw/train.csv.dvc data/raw/.gitignore
git commit -m "Track training data"

# Push to remote
dvc push

# Pull from remote
dvc pull

# Check status
dvc status
```

### Pipelines
```bash
# Add stage
dvc stage add -n preprocess \
  -d src/preprocess.py \
  -d data/raw/train.csv \
  -o data/processed/train_processed.csv \
  python src/preprocess.py

# Run pipeline
dvc repro

# Force rerun
dvc repro --force

# Run specific stage
dvc repro preprocess

# Visualize DAG
dvc dag

# Show metrics
dvc metrics show
dvc metrics diff
```

### Common Commands
```bash
# Checkout specific version
git checkout <commit>
dvc checkout

# Remove tracked file
dvc remove data/raw/train.csv.dvc

# List tracked files
dvc list . data/

# Import from another repo
dvc import https://github.com/user/repo data/dataset.csv
```

---

## MLflow

### Installation & Setup
```bash
# Install
pip install mlflow

# Start server (local)
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000

# Start server (production)
mlflow server \
  --backend-store-uri postgresql://user:pass@host:5432/mlflow \
  --default-artifact-root s3://mybucket/mlflow \
  --host 0.0.0.0 \
  --port 5000

# Set tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### Tracking Experiments
```python
import mlflow

# Set experiment
mlflow.set_experiment("my-experiment")

# Start run
with mlflow.start_run(run_name="baseline"):
    # Log params
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)
    
    # Log multiple metrics over time
    for epoch in range(100):
        mlflow.log_metric("train_loss", loss, step=epoch)
    
    # Log artifacts
    mlflow.log_artifact("plot.png")
    mlflow.log_artifact("config.yaml")
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log tags
    mlflow.set_tag("version", "v1")
    mlflow.set_tag("author", "john")
```

### Query Experiments
```bash
# List experiments
mlflow experiments list

# List runs
mlflow runs list --experiment-name my-experiment

# Search runs (Python)
```
```python
import mlflow

runs = mlflow.search_runs(
    experiment_names=["my-experiment"],
    filter_string="metrics.accuracy > 0.9",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)
print(runs[["run_id", "metrics.accuracy", "params.learning_rate"]])
```

### Model Registry
```bash
# Register model
mlflow models register <model-uri> <model-name>

# List models
mlflow models list

# Get model versions
mlflow models list-versions --name MyModel
```

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_uri = "runs:/abc123/model"
result = mlflow.register_model(model_uri, "MyModel")

# Transition stage
client.transition_model_version_stage(
    name="MyModel",
    version="1",
    stage="Production",
    archive_existing_versions=True
)

# Load model
model = mlflow.sklearn.load_model("models:/MyModel/Production")
```

### Autologging
```python
import mlflow

# Enable autologging for sklearn
mlflow.sklearn.autolog()

# Train model (params, metrics, model auto-logged)
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
```

---

## DVC + MLflow Integration

### Track Data with DVC, Experiments with MLflow
```python
import mlflow
import subprocess

# Get DVC data version
dvc_hash = subprocess.check_output(
    ["dvc", "status", "data/train.csv", "--show-json"],
    text=True
)

mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    # Tag with DVC hash for lineage
    mlflow.set_tag("dvc_data_hash", dvc_hash)
    mlflow.set_tag("data_version", "v2.0")
    
    # Pull data
    subprocess.run(["dvc", "pull"])
    
    # Train model
    # ...
    
    # Log model to MLflow
    mlflow.sklearn.log_model(model, "model")
```

### DVC Pipeline with MLflow Logging
```yaml
# dvc.yaml
stages:
  train:
    cmd: python src/train.py
    deps:
      - src/train.py
      - data/processed/train.csv
    outs:
      - models/model.pkl
    params:
      - train.learning_rate
      - train.epochs
    metrics:
      - metrics.json:
          cache: false
```

```python
# src/train.py
import mlflow
import yaml

with open("params.yaml") as f:
    params = yaml.safe_load(f)["train"]

mlflow.set_experiment("dvc-pipeline")

with mlflow.start_run():
    # Log DVC params
    for key, value in params.items():
        mlflow.log_param(key, value)
    
    # Train model
    # ...
    
    # Log to both DVC and MLflow
    mlflow.log_metric("accuracy", accuracy)
    
    with open("metrics.json", "w") as f:
        json.dump({"accuracy": accuracy}, f)
```

---

## Common Workflows

### Experiment Tracking
```bash
# 1. Version data
dvc add data/train.csv
git add data/train.csv.dvc .gitignore
git commit -m "Add training data v1"
dvc push

# 2. Run experiments with MLflow
python train.py  # Logs to MLflow

# 3. Compare in MLflow UI
# Open http://localhost:5000

# 4. Select best model
# Register in MLflow Registry
```

### Model Retraining
```bash
# 1. New data arrives
dvc add data/train_new.csv
git add data/train_new.csv.dvc
git commit -m "Add new training data"
dvc push

# 2. Retrain (logs to new MLflow run)
python train.py --data data/train_new.csv

# 3. Compare new vs old model in MLflow

# 4. If better, promote to Production
```

### Reproducibility
```bash
# Go back to specific experiment
git checkout <commit>  # Code + data pointer
dvc checkout  # Download data
mlflow runs list  # Find run ID

# Reproduce exact results
python train.py  # Same code, data, params
```

---

## Quick Reference

### DVC
| Command | Purpose |
|---------|---------|
| `dvc add` | Track file/folder |
| `dvc push` | Upload to remote |
| `dvc pull` | Download from remote |
| `dvc repro` | Run pipeline |
| `dvc status` | Check changes |
| `dvc dag` | Show pipeline graph |

### MLflow
| Command | Purpose |
|---------|---------|
| `mlflow.log_param()` | Log hyperparameter |
| `mlflow.log_metric()` | Log metric |
| `mlflow.log_artifact()` | Log file |
| `mlflow.log_model()` | Log model |
| `mlflow.register_model()` | Add to registry |
| `mlflow.search_runs()` | Query experiments |

---

## Best Practices

1. **DVC for data/models**, **MLflow for experiments**
2. **Tag MLflow runs with DVC hashes** for full lineage
3. **Use DVC pipelines** for reproducibility
4. **Use MLflow Registry** for model governance
5. **Push to remotes** regularly (DVC and git)
6. **Document data versions** in git commit messages
7. **Automate** in CI/CD pipelines

---

## Troubleshooting

### DVC remote access denied
```bash
# Check credentials
aws s3 ls s3://mybucket/

# Set credentials
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx

# Or configure
dvc remote modify myremote access_key_id xxx
```

### MLflow not tracking
```bash
# Check tracking URI
echo $MLFLOW_TRACKING_URI

# Test connectivity
curl http://localhost:5000/health

# Check server logs
```

### Can't reproduce results
```bash
# Ensure same versions
git checkout <commit>
dvc checkout
pip install -r requirements-lock.txt

# Check random seeds are set
grep -r "random_state\|seed" src/
```

---

## Resources

- [DVC docs](https://dvc.org/doc)
- [MLflow docs](https://mlflow.org/docs/latest/index.html)
- [DVC with MLflow](https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial)

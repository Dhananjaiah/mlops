# Lecture 6.4 – Using MLflow to Track Experiments

---

## MLflow Overview

MLflow is the most popular open-source experiment tracking tool. It has four main components:

1. **MLflow Tracking**: Log experiments (what we cover now)
2. **MLflow Projects**: Package code for reproducibility
3. **MLflow Models**: Standard model packaging
4. **MLflow Registry**: Model versioning (covered later)

---

## Getting Started

### Installation

```bash
pip install mlflow
```

### Start the UI

```bash
mlflow ui
# Open http://localhost:5000
```

---

## Basic Tracking

### Logging Parameters and Metrics

```python
import mlflow

# Start a run
with mlflow.start_run(run_name="my_first_run"):
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)
    
    # Train model (your code)
    model = train_model(learning_rate=0.01, epochs=100)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.85)
    mlflow.log_metric("loss", 0.32)
```

### Logging Multiple Metrics Over Time

```python
for epoch in range(100):
    loss = train_epoch(model)
    mlflow.log_metric("loss", loss, step=epoch)
```

---

## Logging Artifacts

### Log Files

```python
# Log a single file
mlflow.log_artifact("config.yaml")

# Log a directory
mlflow.log_artifacts("outputs/")

# Log with custom path
mlflow.log_artifact("local/path/file.txt", artifact_path="custom/dir")
```

### Log Figures

```python
import matplotlib.pyplot as plt

plt.figure()
plt.plot(history['loss'])
plt.savefig("loss_curve.png")
mlflow.log_artifact("loss_curve.png")
```

### Log Models

```python
# Scikit-learn
mlflow.sklearn.log_model(model, "model")

# PyTorch
mlflow.pytorch.log_model(model, "model")

# TensorFlow/Keras
mlflow.tensorflow.log_model(model, "model")

# Generic (any Python object)
mlflow.pyfunc.log_model("model", python_model=my_model)
```

---

## Organizing Experiments

### Set Experiment

```python
# Create or use existing experiment
mlflow.set_experiment("churn-prediction")

# Now all runs go to this experiment
with mlflow.start_run():
    # ...
```

### Tags

```python
with mlflow.start_run():
    mlflow.set_tag("model_type", "random_forest")
    mlflow.set_tag("dataset_version", "v2")
    mlflow.set_tag("author", "alice")
```

---

## Complete Example

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import pandas as pd

# Set experiment
mlflow.set_experiment("churn-prediction")

def train_and_log(params, X_train, y_train, X_test, y_test):
    with mlflow.start_run(run_name=f"rf_{params['n_estimators']}_{params['max_depth']}"):
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        
        # Train
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
        mlflow.log_metric("precision", precision_score(y_test, y_pred))
        mlflow.log_metric("recall", recall_score(y_test, y_pred))
        mlflow.log_metric("auc", roc_auc_score(y_test, y_proba))
        
        # Log feature importance
        importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        importance.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        return mlflow.active_run().info.run_id

# Run experiments
for n_est in [100, 200]:
    for depth in [10, 20]:
        params = {"n_estimators": n_est, "max_depth": depth, "random_state": 42}
        run_id = train_and_log(params, X_train, y_train, X_test, y_test)
        print(f"Run {run_id}: n_estimators={n_est}, max_depth={depth}")
```

---

## Querying Runs

### Using the API

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get experiment
experiment = client.get_experiment_by_name("churn-prediction")

# Search runs
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="metrics.auc > 0.85",
    order_by=["metrics.auc DESC"],
    max_results=10
)

for run in runs:
    print(f"Run: {run.info.run_id}, AUC: {run.data.metrics['auc']}")
```

### Using pandas

```python
import mlflow

# Get all runs as DataFrame
runs_df = mlflow.search_runs(experiment_names=["churn-prediction"])

# Analyze
print(runs_df[['params.n_estimators', 'params.max_depth', 'metrics.auc']].head())
```

---

## Loading Models

```python
# Load by run ID
model = mlflow.sklearn.load_model(f"runs:/abc123/model")

# Load by model URI
model = mlflow.sklearn.load_model("models:/churn-model/Production")

# Make predictions
predictions = model.predict(X_new)
```

---

## MLflow Tracking Server

For team use, run a central server:

```bash
# With SQLite backend
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns

# With PostgreSQL and S3
mlflow server     --backend-store-uri postgresql://user:pass@host/mlflow     --default-artifact-root s3://bucket/mlflow     --host 0.0.0.0
```

Configure clients:
```python
mlflow.set_tracking_uri("http://mlflow-server:5000")
```

---

## Recap

MLflow tracking:
- Log parameters, metrics, artifacts
- Organize into experiments
- Query and compare runs
- Load models for inference

Key functions:
- `mlflow.start_run()`: Start tracking
- `mlflow.log_param()`, `log_params()`: Log parameters
- `mlflow.log_metric()`: Log metrics
- `mlflow.log_artifact()`: Log files
- `mlflow.sklearn.log_model()`: Log models

---

**Next Lecture**: [6.5 – Reproducing Results End-to-End (Same Code, Same Data, Same Model)](lecture-6.5-reproducibility.md)

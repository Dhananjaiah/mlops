# Module 04: Experiment Tracking & Reproducibility

## 🎯 Goals

- Track experiments with **MLflow** (params, metrics, artifacts)
- Log models and their **dependencies** automatically
- Compare experiments in **MLflow UI**
- Create **reproducible runs** with same results
- Use **MLflow Projects** for packaging
- Integrate **MLflow with DVC** for full lineage

---

## 📖 Key Terms

- **MLflow Tracking**: API for logging params, metrics, artifacts during ML runs
- **Experiment**: Collection of related runs (e.g., "churn-model-v1")
- **Run**: Single execution with specific params, producing metrics and artifacts
- **Artifact**: File output (model, plot, data) stored with run
- **Backend store**: Database for metadata (SQLite, PostgreSQL, MySQL)
- **Artifact store**: Storage for large files (local, S3, Azure Blob, GCS)
- **MLflow Project**: Packaging format for reproducible runs (MLproject file)

---

## 🔧 Commands First: Setup MLflow Locally

```bash
# Install MLflow
pip install mlflow

# Start MLflow server (local, file-based)
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000 &

# Or use environment variable for tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000

# Open UI
# Navigate to http://localhost:5000 in browser
```

**Why**: MLflow server provides centralized tracking and UI for team collaboration. Backend store (DB) holds metadata, artifact store holds models/files.

---

## 📝 Log First Experiment

```bash
# Create training script with MLflow
cat > src/train_mlflow.py << 'EOF'
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set experiment
mlflow.set_experiment("iris-classifier")

# Start run
with mlflow.start_run():
    # Log parameters
    n_estimators = 100
    max_depth = 5
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("random_state", 42)
    
    # Train model
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # Log model
    mlflow.sklearn.log_model(clf, "model")
    
    print(f"Accuracy: {accuracy:.3f}")
EOF

# Run
python src/train_mlflow.py
```

**Why**: `mlflow.start_run()` creates a tracked run. All logs go to MLflow server, visible in UI.

---

## ✅ Verify in MLflow UI

```bash
# Open http://localhost:5000
# Should see:
# - Experiment: "iris-classifier"
# - Run with params: n_estimators=100, max_depth=5
# - Metrics: accuracy, precision, recall
# - Artifacts: model/ directory

# Query runs via CLI
mlflow runs list --experiment-name iris-classifier

# Get best run
mlflow runs list --experiment-name iris-classifier --order-by "metrics.accuracy DESC" --max-results 1
```

---

## 🔄 Compare Multiple Runs

```bash
# Run with different hyperparameters
cat > src/train_sweep.py << 'EOF'
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("iris-classifier")

# Hyperparameter sweep
for n_estimators in [50, 100, 200]:
    for max_depth in [3, 5, 10]:
        with mlflow.start_run():
            mlflow.log_param("n_estimators", n_estimators)
            mlflow.log_param("max_depth", max_depth)
            
            clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
            clf.fit(X_train, y_train)
            
            accuracy = accuracy_score(y_test, clf.predict(X_test))
            mlflow.log_metric("accuracy", accuracy)
            mlflow.sklearn.log_model(clf, "model")
            
            print(f"n_estimators={n_estimators}, max_depth={max_depth}, accuracy={accuracy:.3f}")
EOF

python src/train_sweep.py
```

**Why**: MLflow UI shows all runs in table. Sort by accuracy, compare params side-by-side.

---

## 📊 Log Plots and Artifacts

```bash
# Enhanced training script
cat > src/train_with_plots.py << 'EOF'
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("iris-classifier")

with mlflow.start_run():
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    
    # Log confusion matrix as artifact
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    
    # Log feature importances
    import json
    importances = dict(zip([f"feature_{i}" for i in range(X.shape[1])], clf.feature_importances_.tolist()))
    with open("feature_importances.json", "w") as f:
        json.dump(importances, f)
    mlflow.log_artifact("feature_importances.json")
    
    mlflow.sklearn.log_model(clf, "model")
EOF

python src/train_with_plots.py
```

**Why**: Artifacts (plots, JSON, CSVs) are stored with run. View in MLflow UI under "Artifacts" tab.

---

## 🐳 MLflow with Docker (Production Setup)

```bash
# Use docker-compose from Module 02
# Ensure mlflow service is running:
docker compose ps | grep mlflow

# Set tracking URI to docker service
export MLFLOW_TRACKING_URI=http://localhost:5000

# Run training (logs to Dockerized MLflow)
python src/train_mlflow.py
```

**Why**: Team shares MLflow server. All experiments centralized, backed by PostgreSQL for durability.

---

## 🔁 Reproducibility: MLflow Projects

```bash
# Create MLproject file
cat > MLproject << 'EOF'
name: iris-classifier

python_env: python_env.yaml

entry_points:
  main:
    parameters:
      n_estimators: {type: int, default: 100}
      max_depth: {type: int, default: 5}
    command: "python src/train_mlflow.py {n_estimators} {max_depth}"
EOF

# Create environment file
cat > python_env.yaml << 'EOF'
python: "3.11"
dependencies:
  - scikit-learn=1.3.2
  - mlflow=2.9.2
  - pandas=2.1.3
EOF

# Run project (creates isolated env)
mlflow run . -P n_estimators=150 -P max_depth=7

# Run from Git
mlflow run https://github.com/user/repo -P n_estimators=100
```

**Why**: MLflow Projects package code + env for reproducibility. Anyone can run with same params and get same results.

---

## 🔗 Integrate DVC + MLflow

```bash
# Training script with DVC and MLflow
cat > src/train_dvc_mlflow.py << 'EOF'
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import subprocess

# Get DVC data hash (for lineage)
dvc_hash = subprocess.check_output(
    ["dvc", "status", "data/raw/customers.csv", "--show-json"],
    text=True
)

mlflow.set_experiment("churn-predictor")

with mlflow.start_run():
    # Log DVC hash
    mlflow.set_tag("dvc_hash", dvc_hash)
    
    # Load data
    df = pd.read_csv("data/raw/customers.csv")
    X = df[["age", "tenure", "monthly_charges"]]
    y = df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Metrics
    accuracy = accuracy_score(y_test, clf.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(clf, "model")
    
    print(f"Accuracy: {accuracy:.3f}")
EOF
```

**Why**: Tag runs with DVC hashes for full lineage: code (git SHA) + data (DVC hash) + params.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Track experiments, compare runs, log artifacts.

1. **Start MLflow**:
```bash
mkdir -p ~/mlops-lab-04 && cd ~/mlops-lab-04
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000 &
export MLFLOW_TRACKING_URI=http://localhost:5000
```

2. **Create training script**:
```bash
cat > train.py << 'EOF'
import mlflow
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment("lab04")

with mlflow.start_run():
    mlflow.log_param("C", 1.0)
    clf = LogisticRegression(C=1.0, random_state=42)
    clf.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, clf.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(clf, "model")
    print(f"Accuracy: {accuracy:.3f}")
EOF

python train.py
```

3. **Run multiple experiments**:
```bash
for c in 0.1 1.0 10.0; do
  python -c "
import mlflow
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment('lab04')
with mlflow.start_run():
    mlflow.log_param('C', $c)
    clf = LogisticRegression(C=$c, random_state=42)
    clf.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, clf.predict(X_test))
    mlflow.log_metric('accuracy', accuracy)
    mlflow.sklearn.log_model(clf, 'model')
    print(f'C=$c, Accuracy={accuracy:.3f}')
"
done
```

4. **View in UI**:
```bash
# Open http://localhost:5000
# See 4 runs with different C values
# Sort by accuracy
```

**Expected output**: MLflow UI shows runs, sortable by metrics, with logged models.

---

## ❓ Quiz (5 Questions)

1. **What does MLflow log by default when you call `mlflow.sklearn.log_model()`?**
   - Answer: Model binary, Python environment (dependencies), signature (input/output schema).

2. **Where are artifacts stored in MLflow?**
   - Answer: Artifact store (local directory, S3, Azure Blob, GCS), configured via `--default-artifact-root`.

3. **How do you compare runs in MLflow UI?**
   - Answer: Select multiple runs, click "Compare", view params/metrics side-by-side in table and charts.

4. **What is an MLflow Project?**
   - Answer: Packaging format (MLproject file) for reproducible runs with specified environment and parameters.

5. **How do you ensure reproducibility?**
   - Answer: Log code version (git SHA), data version (DVC hash), params, random seed, and environment (requirements.txt).

---

## ⚠️ Common Mistakes

1. **Not logging params** → Can't compare runs or reproduce results.  
   *Fix*: Always `mlflow.log_param()` for every hyperparameter.

2. **Logging to local file store in prod** → Lost on container restart.  
   *Fix*: Use remote artifact store (S3, GCS) and PostgreSQL backend.

3. **Not setting random seeds** → Non-reproducible results.  
   *Fix*: Set seeds in Python, NumPy, TensorFlow, PyTorch, and log as param.

4. **Ignoring model signature** → Type mismatches at serving time.  
   *Fix*: Use `mlflow.infer_signature(X_train, y_pred)` when logging model.

5. **Not tagging runs** → Hard to find specific experiments later.  
   *Fix*: Use `mlflow.set_tag("purpose", "baseline")` for organization.

---

## 🛠️ Troubleshooting

**Issue**: "MLflow UI shows no experiments"  
→ **Root cause**: Wrong tracking URI or backend store not accessible.  
→ **Fix**: Check `MLFLOW_TRACKING_URI`, verify DB connection, ensure server is running.  
→ **See**: `/troubleshooting/triage-matrix.md` row "MLflow offline or empty"

**Issue**: "Artifact upload fails"  
→ **Root cause**: No permissions for S3 bucket or artifact root doesn't exist.  
→ **Fix**: Check AWS credentials, create bucket, verify `dvc remote` or MLflow artifact store config.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Artifact upload fails"

---

## 📚 Key Takeaways

- **MLflow Tracking** logs params, metrics, artifacts for every run
- **MLflow UI** visualizes and compares experiments
- **MLflow Projects** package code + env for reproducibility
- **Backend store** (PostgreSQL) holds metadata; **artifact store** (S3) holds files
- Combine **DVC (data) + git (code) + MLflow (experiments)** for full lineage
- Always log **params, metrics, random seeds, data versions** for reproducibility

---

## 🚀 Next Steps

- **Module 05**: Orchestrate training with Airflow or Kubeflow Pipelines
- **Module 06**: Build systematic training/evaluation pipelines
- **Hands-on**: Integrate MLflow into Churn Predictor project for experiment tracking

---

**[← Module 03](03-data-versioning-and-quality.md)** | **[Next: Module 05 →](05-pipelines-orchestration.md)**

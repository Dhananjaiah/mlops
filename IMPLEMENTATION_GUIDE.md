# MLOps Course: Complete Implementation & Teaching Guide

> **A step-by-step runbook for instructors and students to implement the complete MLOps course from 0→Production**

---

## 📋 Document Overview

This guide provides complete instructions for:
1. **Setting up the learning environment** (local, Kubernetes, cloud)
2. **Implementing each of the 15 course modules** with hands-on exercises
3. **Building the capstone project** (Churn Predictor)
4. **Teaching strategies** for instructors
5. **Troubleshooting** common issues
6. **Assessment** and certification preparation

**Time Required:** 25-30 hours for complete implementation  
**Audience:** Data Scientists, ML Engineers, Platform Engineers, Students

---

## 🎯 Prerequisites

### Required Knowledge
- ✅ Python programming (intermediate level)
- ✅ Basic Linux command line (cd, ls, cat, grep)
- ✅ Git version control basics (clone, commit, push)
- ✅ Docker fundamentals (containers, images, docker-compose)

### Required Software
- ✅ **Python 3.11+** - [Download](https://www.python.org/downloads/)
- ✅ **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- ✅ **Git** - [Download](https://git-scm.com/downloads)
- ✅ **VS Code** (recommended) - [Download](https://code.visualstudio.com/)

### Optional Software (for advanced sections)
- ⭕ **Kubernetes CLI (kubectl)** - [Install](https://kubernetes.io/docs/tasks/tools/)
- ⭕ **K3d** (local Kubernetes) - [Install](https://k3d.io/)
- ⭕ **Terraform** - [Install](https://www.terraform.io/downloads)
- ⭕ **AWS/GCP/Azure CLI** (for cloud deployment)

### Hardware Requirements
- **Minimum:** 8GB RAM, 20GB free disk space, 2 CPU cores
- **Recommended:** 16GB RAM, 50GB free disk space, 4+ CPU cores

---

## 🚀 Phase 1: Initial Setup (Day 1)

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops

# Verify you're in the right place
ls -la
# You should see: course/, project/, cheatsheets/, README.md, etc.
```

### Step 2: Set Up Environment Variables

```bash
# Create environment configuration file
cat > ~/.mlops-env << 'ENVEOF'
export CLOUD="local"
export REGION="us-east-1"
export REGISTRY="ghcr.io/mlops-course"
export BUCKET="mlops-artifacts"
export CLUSTER="mlops-dev"
export NAMESPACE="mlops"
export DB_URL="postgres://mlops:mlops@db:5432/mlops"
export TRACKING_URL="http://mlflow:5000"
export MODEL_NAME="churn-predictor"
export PROJECT="mlops-course"
export PY_VER="3.11"
ENVEOF

# Load environment variables
source ~/.mlops-env

# Add to your shell profile for persistence
echo "source ~/.mlops-env" >> ~/.bashrc  # or ~/.zshrc for zsh
```

### Step 3: Install Python Dependencies (Local Development)

```bash
# Option 1: Using pip (simple)
cd mlops/project
pip install --upgrade pip
pip install -r requirements.txt 2>/dev/null || echo "requirements.txt will be created in modules"

# Option 2: Using uv (modern, fast - recommended)
pip install uv
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install mlflow dvc scikit-learn pandas numpy fastapi

# Option 3: Using poetry (dependency management)
pip install poetry
poetry init
poetry add mlflow dvc scikit-learn pandas fastapi
poetry install
```

### Step 4: Verify Docker Installation

```bash
# Check Docker is running
docker --version
docker compose version

# Test Docker works
docker run hello-world

# If you see "Hello from Docker!" you're ready to proceed
```

### Step 5: Navigate Course Structure

```bash
# Explore the repository structure
tree -L 2 mlops/

# Read the main README
cat README.md

# Browse course modules
ls -la course/

# Check the capstone project
ls -la project/
```

**✅ Checkpoint:** You should now have:
- Repository cloned
- Environment variables configured
- Python environment ready
- Docker working
- Course structure understood

---

## 📚 Phase 2: Course Modules Implementation

### Module 00: Overview (30 minutes)

**Objective:** Understand course structure and philosophy

#### Steps:

1. **Read the overview module**
```bash
cd mlops
cat course/00-overview.md | less
```

2. **Key Concepts to Grasp:**
   - Commands-first approach: Practice before theory
   - Three-tier learning: Local → Kubernetes → Cloud
   - Complete system architecture: Data → Train → Deploy → Monitor → Retrain

3. **Review Course Resources:**
```bash
# Check cheatsheets
ls -la cheatsheets/
cat cheatsheets/python-env.md

# Review troubleshooting guide
cat troubleshooting/triage-matrix.md

# Look at mock exams
ls -la exams/
```

4. **Set Your Learning Path:**
   - **Beginner:** Weeks 1-2 (Modules 01-04)
   - **Intermediate:** Weeks 3-4 (Modules 05-09)
   - **Advanced:** Weeks 5-6 (Modules 10-14)

**Teaching Note:** Have students bookmark the cheatsheets and troubleshooting guide. These will be referenced frequently.

---

### Module 01: MLOps Foundations (1 hour)

**Objective:** Understand MLOps lifecycle, roles, and artifacts

#### Steps:

1. **Read the module**
```bash
cat course/01-mlops-foundations.md
```

2. **Understand Key Concepts:**
   - **MLOps Lifecycle:** Data → Train → Deploy → Monitor → Retrain (continuous loop)
   - **Roles:** Data Scientist, ML Engineer, Platform Engineer, DevOps Engineer
   - **Artifacts:** Data, Code, Models, Configs, Metrics, Environment, Lineage

3. **Hands-On Exercise: Set Up Basic Tracking**

```bash
# Create a simple project structure
mkdir -p ~/mlops-practice/{data,models,configs,metrics}
cd ~/mlops-practice

# Initialize git
git init

# Create a simple training script
cat > train_basic.py << 'PYEOF'
import json
from datetime import datetime

# Simulate model training
metrics = {
    "accuracy": 0.85,
    "precision": 0.82,
    "recall": 0.88,
    "timestamp": datetime.now().isoformat()
}

# Save metrics
with open("metrics/run_001.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("Training complete!")
print(f"Metrics saved: {metrics}")
PYEOF

# Run the script
python train_basic.py

# Track with git
git add .
git commit -m "Initial training run with metrics tracking"

# View what we tracked
git log --oneline
cat metrics/run_001.json
```

4. **Mini-Lab: Identify Drift**

```bash
# Simulate a second run with different performance
cat > train_basic_v2.py << 'PYEOF'
import json
from datetime import datetime

# Simulate degraded model performance (drift!)
metrics = {
    "accuracy": 0.72,
    "precision": 0.68,
    "recall": 0.75,
    "timestamp": datetime.now().isoformat()
}

with open("metrics/run_002.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("Training complete!")
print(f"Metrics saved: {metrics}")
print("⚠️  Warning: Accuracy dropped from 0.85 to 0.72!")
PYEOF

python train_basic_v2.py

# Compare metrics
diff metrics/run_001.json metrics/run_002.json
```

**Quiz Questions:**
- Q: What are the 5 stages of the MLOps lifecycle?
- Q: Which role is responsible for maintaining Kubernetes clusters?
- Q: Why do we need to track data versions in addition to code versions?

**✅ Checkpoint:** Students understand why ML systems need continuous monitoring and why tracking all artifacts is essential.

---

### Module 02: Environment & Packaging (1.5 hours)

**Objective:** Master Python environments and Docker containerization

#### Steps:

1. **Read the module**
```bash
cat course/02-env-and-packaging.md
```

2. **Exercise: Environment Management with uv**

```bash
# Install uv (if not already done)
pip install uv

# Create a new project
mkdir ~/mlops-env-demo
cd ~/mlops-env-demo

# Initialize with uv
uv venv .venv
source .venv/bin/activate

# Install specific versions (for reproducibility)
uv pip install 'pandas==2.1.0' 'scikit-learn==1.3.0'

# Generate lock file
uv pip freeze > requirements.lock

# View locked dependencies
cat requirements.lock
```

3. **Exercise: Containerize with Docker**

```bash
# Create a simple ML script
cat > train_containerized.py << 'PYEOF'
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Generate sample data
X, y = make_classification(n_samples=100, n_features=10, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

print(f"Model trained! Score: {clf.score(X, y):.3f}")
PYEOF

# Create Dockerfile (multi-stage build)
cat > Dockerfile << 'DOCKEREOF'
# Stage 1: Build environment
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.lock .

RUN pip install --user -r requirements.lock

# Stage 2: Runtime environment
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY train_containerized.py .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "train_containerized.py"]
DOCKEREOF

# Build the image
docker build -t mlops-demo:v1 .

# Run the container
docker run mlops-demo:v1
```

4. **Exercise: Docker Compose Stack**

```bash
# Create a docker-compose.yml
cat > docker-compose.yml << 'COMPOSEEOF'
version: '3.8'

services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.8.0
    ports:
      - "5000:5000"
    command: >
      mlflow server
      --host 0.0.0.0
      --port 5000
      --backend-store-uri sqlite:///mlflow.db
      --default-artifact-root ./mlruns

  prometheus:
    image: prom/prometheus:v2.45.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:10.0.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
COMPOSEEOF

# Create Prometheus config
cat > prometheus.yml << 'PROMEOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
PROMEOF

# Start the stack
docker compose up -d

# Verify services
docker compose ps

# Test endpoints
curl http://localhost:5000  # MLflow
curl http://localhost:9090  # Prometheus
curl http://localhost:3000  # Grafana (login: admin/admin)

# Stop when done
docker compose down
```

**Teaching Note:** Emphasize that dev-prod parity (identical environments) prevents "works on my machine" problems.

**✅ Checkpoint:** Students can create reproducible environments and containerize applications.

---

### Module 03: Data Versioning & Quality (2 hours)

**Objective:** Version data with DVC and validate data quality

#### Steps:

1. **Read the module**
```bash
cat course/03-data-versioning-and-quality.md
```

2. **Exercise: Initialize DVC**

```bash
# Create project directory
mkdir ~/mlops-data-versioning
cd ~/mlops-data-versioning

# Initialize Git and DVC
git init
pip install dvc dvc-s3
dvc init

# Create sample data
mkdir data
cat > data/customers.csv << 'CSVEOF'
customer_id,age,tenure,monthly_charges,churn
1,25,12,50.00,0
2,45,24,75.50,0
3,35,6,65.00,1
4,50,48,100.00,0
5,28,3,55.00,1
CSVEOF

# Add data to DVC tracking
dvc add data/customers.csv

# Commit the .dvc file (not the data itself!)
git add data/customers.csv.dvc data/.gitignore
git commit -m "Track customer data with DVC"

# View what was tracked
cat data/customers.csv.dvc
```

3. **Exercise: Set Up DVC Remote**

```bash
# Option 1: Local remote (for learning)
mkdir -p /tmp/dvc-remote
dvc remote add -d local /tmp/dvc-remote

# Push data to remote
dvc push

# Verify it's stored remotely
ls -la /tmp/dvc-remote

# Option 2: S3 remote (for production)
# dvc remote add -d s3remote s3://my-bucket/dvc-storage
# dvc remote modify s3remote region us-east-1
# dvc push
```

4. **Exercise: Data Quality with Great Expectations**

```bash
# Install Great Expectations
pip install great-expectations

# Initialize GE
great_expectations init

# Create expectation suite
great_expectations suite new

# Create a simple validation script
cat > validate_data.py << 'PYEOF'
import pandas as pd
import great_expectations as gx

# Load data
df = pd.read_csv("data/customers.csv")

# Create expectations
context = gx.get_context()

# Define expectations
expectations = [
    {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "customer_id"}},
    {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "age", "min_value": 18, "max_value": 100}},
    {"expectation_type": "expect_column_values_to_be_in_set", "kwargs": {"column": "churn", "value_set": [0, 1]}},
]

# Validate
print("✅ Data validation passed!" if df.shape[0] > 0 else "❌ Data validation failed!")
print(f"Records: {df.shape[0]}, Columns: {df.shape[1]}")
PYEOF

python validate_data.py
```

5. **Mini-Lab: Version a Data Update**

```bash
# Modify the data
cat >> data/customers.csv << 'CSVEOF'
6,42,18,80.00,0
7,31,9,60.00,1
CSVEOF

# DVC detects the change
dvc status

# Update the version
dvc add data/customers.csv
git add data/customers.csv.dvc
git commit -m "Add 2 more customer records"

# Push updated data
dvc push

# View version history
git log --oneline data/customers.csv.dvc
```

**Quiz:** 
- Q: Why don't we commit large data files to Git?
- Q: What does the .dvc file contain?

**✅ Checkpoint:** Students can version data separately from code and validate data quality.

---

### Module 04: Experiment Tracking & Reproducibility (2 hours)

**Objective:** Track ML experiments with MLflow

#### Steps:

1. **Read the module**
```bash
cat course/04-experiment-tracking-and-reproducibility.md
```

2. **Exercise: Set Up MLflow**

```bash
# Install MLflow
pip install mlflow

# Start MLflow server
mlflow server --host 0.0.0.0 --port 5000 &

# Verify it's running
curl http://localhost:5000

# Open in browser: http://localhost:5000
```

3. **Exercise: Log Experiments**

```bash
# Create training script with MLflow tracking
cat > train_with_mlflow.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Set MLflow tracking URI
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn-prediction")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start MLflow run
with mlflow.start_run():
    # Log parameters
    n_estimators = 100
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    # Train model
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # Log model
    mlflow.sklearn.log_model(clf, "model")
    
    print(f"✅ Experiment logged!")
    print(f"   Accuracy: {accuracy:.3f}")
    print(f"   Precision: {precision:.3f}")
    print(f"   Recall: {recall:.3f}")
PYEOF

# Run multiple experiments with different hyperparameters
python train_with_mlflow.py
```

4. **Exercise: Compare Experiments**

```bash
# Run with different hyperparameters
cat > train_experiment_2.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn-prediction")

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Try different configurations
configs = [
    {"n_estimators": 50, "max_depth": 5},
    {"n_estimators": 100, "max_depth": 10},
    {"n_estimators": 200, "max_depth": 15},
]

for config in configs:
    with mlflow.start_run():
        mlflow.log_params(config)
        clf = RandomForestClassifier(**config, random_state=42)
        clf.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, clf.predict(X_test))
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(clf, "model")
        print(f"Config {config}: Accuracy = {accuracy:.3f}")
PYEOF

python train_experiment_2.py

# View experiments in UI
echo "Open http://localhost:5000 to compare experiments"
```

5. **Exercise: Load Model from Registry**

```bash
cat > load_model.py << 'PYEOF'
import mlflow.sklearn

# Load a logged model
model_uri = "runs:/<RUN_ID>/model"  # Replace <RUN_ID> with actual run ID
# Or use: model_uri = "models:/churn-predictor/production"

loaded_model = mlflow.sklearn.load_model(model_uri)
print(f"✅ Model loaded successfully!")
print(f"   Model type: {type(loaded_model)}")
PYEOF
```

**Teaching Note:** Have students open MLflow UI and explore the experiment comparison features.

**✅ Checkpoint:** Students can track experiments, log parameters/metrics/models, and reproduce training runs.

---

### Module 05: Pipelines & Orchestration (2.5 hours)

**Objective:** Build automated training pipelines with Airflow

#### Steps:

1. **Read the module**
```bash
cat course/05-pipelines-orchestration.md
```

2. **Exercise: Set Up Airflow**

```bash
# Install Airflow
pip install apache-airflow

# Initialize Airflow database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start Airflow webserver and scheduler
airflow webserver --port 8080 &
airflow scheduler &

# Open browser: http://localhost:8080 (admin/admin)
```

3. **Exercise: Create Training Pipeline DAG**

```bash
# Create DAG directory
mkdir -p ~/airflow/dags
export AIRFLOW_HOME=~/airflow

# Create a training pipeline DAG
cat > ~/airflow/dags/train_churn_model.py << 'PYEOF'
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

default_args = {
    'owner': 'mlops',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_data():
    """Task 1: Load data"""
    print("Loading data...")
    # Simulate data loading
    return {"status": "success", "records": 1000}

def validate_data():
    """Task 2: Validate data quality"""
    print("Validating data...")
    # Simulate validation
    return {"status": "valid"}

def train_model():
    """Task 3: Train model"""
    print("Training model...")
    from sklearn.datasets import make_classification
    
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("airflow-churn-training")
    
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    with mlflow.start_run():
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, clf.predict(X_test))
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(clf, "model")
        
        print(f"Model trained! Accuracy: {accuracy:.3f}")

def register_model():
    """Task 4: Register model in MLflow"""
    print("Registering model...")
    # In production, this would register the model
    return {"status": "registered"}

# Define DAG
with DAG(
    'train_churn_model',
    default_args=default_args,
    description='Automated churn model training pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    task_load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )
    
    task_validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )
    
    task_train = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )
    
    task_register = PythonOperator(
        task_id='register_model',
        python_callable=register_model,
    )
    
    # Define task dependencies
    task_load >> task_validate >> task_train >> task_register
PYEOF

# Trigger the DAG manually
airflow dags trigger train_churn_model

# View DAG in UI
echo "Open http://localhost:8080 and navigate to 'train_churn_model' DAG"
```

**Teaching Note:** Show students the Airflow UI and demonstrate how to monitor DAG runs, view logs, and retry failed tasks.

**✅ Checkpoint:** Students can create automated ML pipelines and understand DAG orchestration.

---

### Module 06: Model Training, Evaluation & Selection (2 hours)

**Objective:** Implement systematic model training with hyperparameter tuning

#### Steps:

1. **Read the module**
```bash
cat course/06-model-training-eval-and-selection.md
```

2. **Exercise: Cross-Validation and Hyperparameter Tuning**

```bash
cat > train_with_tuning.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("hyperparameter-tuning")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
}

with mlflow.start_run():
    # Grid search with cross-validation
    clf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    # Best parameters
    best_params = grid_search.best_params_
    print(f"Best parameters: {best_params}")
    mlflow.log_params(best_params)
    
    # Train final model with best params
    best_model = grid_search.best_estimator_
    
    # Evaluate on test set
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation scores
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5)
    
    # Log metrics
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_metric("cv_mean", cv_scores.mean())
    mlflow.log_metric("cv_std", cv_scores.std())
    
    # Log model
    mlflow.sklearn.log_model(best_model, "model")
    
    print(f"\n✅ Training complete!")
    print(f"   Test Accuracy: {accuracy:.3f}")
    print(f"   CV Mean: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
PYEOF

python train_with_tuning.py
```

3. **Exercise: Model Comparison**

```bash
cat > compare_models.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("model-comparison")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models to compare
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

results = []

for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
        }
        
        # Log
        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")
        
        results.append({"model": model_name, **metrics})
        print(f"{model_name}: Accuracy={metrics['accuracy']:.3f}, F1={metrics['f1']:.3f}")

# Summary
print("\n📊 Model Comparison Summary:")
for result in sorted(results, key=lambda x: x['accuracy'], reverse=True):
    print(f"  {result['model']:<25} Accuracy: {result['accuracy']:.3f}")
PYEOF

python compare_models.py
```

**✅ Checkpoint:** Students can systematically evaluate and compare multiple models.

---

### Module 07: Model Registry & Governance (1.5 hours)

**Objective:** Manage model lifecycle with MLflow Model Registry

#### Steps:

1. **Read the module**
```bash
cat course/07-model-registry-and-governance.md
```

2. **Exercise: Register Models**

```bash
cat > register_model.py << 'PYEOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

# Get the latest run from an experiment
experiment_name = "churn-prediction"
experiment = client.get_experiment_by_name(experiment_name)

if experiment:
    # Get runs
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.accuracy DESC"], max_results=1)
    
    if runs:
        best_run = runs[0]
        run_id = best_run.info.run_id
        
        # Register the model
        model_uri = f"runs:/{run_id}/model"
        model_name = "churn-predictor"
        
        result = mlflow.register_model(model_uri, model_name)
        print(f"✅ Model registered: {model_name}, Version: {result.version}")
        
        # Transition to staging
        client.transition_model_version_stage(
            name=model_name,
            version=result.version,
            stage="Staging",
        )
        print(f"✅ Model transitioned to Staging")
PYEOF

python register_model.py
```

3. **Exercise: Model Stage Transitions**

```bash
cat > promote_model.py << 'PYEOF'
from mlflow.tracking import MlflowClient
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

model_name = "churn-predictor"

# Get latest version in Staging
staging_models = client.get_latest_versions(model_name, stages=["Staging"])

if staging_models:
    version = staging_models[0].version
    
    # Promote to Production
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production",
        archive_existing_versions=True  # Archive old production models
    )
    
    print(f"✅ Model v{version} promoted to Production")
    
    # Add description
    client.update_model_version(
        name=model_name,
        version=version,
        description="Churn predictor trained with hyperparameter tuning. Accuracy: 0.85"
    )
else:
    print("❌ No models in Staging")
PYEOF

python promote_model.py
```

**Teaching Note:** Emphasize the approval workflow: None → Staging → Production. This prevents untested models from reaching production.

**✅ Checkpoint:** Students understand model governance and lifecycle management.

---

### Module 08: Serving & APIs (2 hours)

**Objective:** Deploy models as REST APIs with FastAPI

#### Steps:

1. **Read the module**
```bash
cat course/08-serving-and-apis.md
```

2. **Exercise: Create FastAPI Service**

```bash
# Install FastAPI
pip install fastapi uvicorn

# Create API server
cat > app.py << 'PYEOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import numpy as np
from typing import List

app = FastAPI(title="Churn Prediction API", version="1.0")

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    global model
    mlflow.set_tracking_uri("http://localhost:5000")
    model_uri = "models:/churn-predictor/Production"
    try:
        model = mlflow.sklearn.load_model(model_uri)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")

class PredictionRequest(BaseModel):
    features: List[List[float]]

class PredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        features = np.array(request.features)
        predictions = model.predict(features).tolist()
        probabilities = model.predict_proba(features).tolist()
        
        return PredictionResponse(
            predictions=predictions,
            probabilities=probabilities
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Churn Prediction API", "version": "1.0"}
PYEOF

# Run the API
echo "Starting API server..."
uvicorn app:app --host 0.0.0.0 --port 8000 &

sleep 5

# Test the API
curl http://localhost:8000/health

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[34, 12, 65.5, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]}'

# View API docs
echo "Open http://localhost:8000/docs for interactive API documentation"
```

3. **Exercise: Containerize API**

```bash
cat > Dockerfile.api << 'DOCKEREOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
DOCKEREOF

# Create requirements
cat > requirements.txt << 'REQEOF'
fastapi==0.104.1
uvicorn==0.24.0
mlflow==2.8.0
scikit-learn==1.3.0
numpy==1.24.3
REQEOF

# Build and run
docker build -t churn-api:v1 -f Dockerfile.api .
docker run -p 8000:8000 churn-api:v1
```

**✅ Checkpoint:** Students can deploy ML models as production-ready APIs.

---

### Modules 09-14: Abbreviated Implementation Steps

Due to length constraints, here are condensed steps for remaining modules:

**Module 09: Batch & Streaming (2 hours)**
- Set up batch scoring pipeline for large datasets
- Implement streaming inference with Kafka (optional)

**Module 10: CI/CD & Environments (2.5 hours)**
- Create GitHub Actions workflow for automated testing
- Set up multi-environment deployments (dev/staging/prod)

**Module 11: Observability & Monitoring (2 hours)**
- Configure Prometheus metrics collection
- Build Grafana dashboards for model monitoring

**Module 12: Drift Detection & Retraining (1.5 hours)**
- Implement Evidently for data/concept drift detection
- Set up automated retraining triggers

**Module 13: Security, Compliance & Cost (2 hours)**
- Run Trivy for vulnerability scanning
- Generate SBOM with Syft
- Set up cost monitoring

**Module 14: Comprehensive Review (1.5 hours)**
- Complete end-to-end workflow
- Review troubleshooting techniques
- Take mock exam

---

## 🏗️ Phase 3: Capstone Project Implementation (Days 5-10)

### Complete Churn Predictor System

#### Step 1: Project Setup

```bash
cd mlops/project

# Copy environment template
cp .env.example .env

# Review project structure
tree -L 2
```

#### Step 2: Start Full Stack

```bash
# Start all services
docker compose up -d

# Verify all services are running
docker compose ps

# Expected services:
# - mlflow (port 5000)
# - postgres (port 5432)
# - fastapi (port 8000)
# - prometheus (port 9090)
# - grafana (port 3000)
# - redis (port 6379)
```

#### Step 3: Generate Sample Data

```bash
# Run data generation script
python scripts/generate_data.py

# Initialize DVC
dvc init
dvc add data/raw/*.csv
git add data/.gitignore data/*.dvc
git commit -m "Initialize data versioning"
```

#### Step 4: Run Training Pipeline

```bash
# Option 1: Direct training
python src/train.py

# Option 2: Via Airflow
# 1. Open http://localhost:8080
# 2. Login with admin/admin
# 3. Enable and trigger "train_churn_model" DAG
```

#### Step 5: Deploy API

```bash
# Start FastAPI service
cd serving
uvicorn main:app --reload --port 8000

# Test predictions
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[35, 24, 75.5, 1, 0]]}'
```

#### Step 6: Set Up Monitoring

```bash
# Open Grafana
# URL: http://localhost:3000
# Login: admin/admin

# Import dashboard
# Upload: dashboards/model_monitoring.json
```

#### Step 7: Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Generate coverage report
pytest --cov=src tests/
```

---

## 👨‍🏫 Phase 4: Teaching Strategies

### For Instructors

#### Week 1-2: Foundations
- **Focus:** Modules 01-04
- **Teaching Style:** Live coding sessions
- **Homework:** Complete mini-labs, start capstone project setup
- **Assessment:** Quiz on MLOps lifecycle and versioning

#### Week 3-4: Pipelines & Serving
- **Focus:** Modules 05-09
- **Teaching Style:** Pair programming exercises
- **Homework:** Build automated training pipeline
- **Assessment:** Deploy working API

#### Week 5-6: Production Excellence
- **Focus:** Modules 10-14
- **Teaching Style:** Project-based learning
- **Homework:** Complete capstone project
- **Assessment:** Mock exam + project presentation

### Classroom Activities

1. **Live Troubleshooting Sessions**
   - Intentionally break a pipeline
   - Have students debug using logs and metrics

2. **Code Review Workshops**
   - Students review each other's pipelines
   - Focus on best practices and reproducibility

3. **Architecture Design Exercise**
   - Groups design ML system for a new use case
   - Present and critique designs

4. **Guest Speakers**
   - Invite MLOps engineers to share war stories
   - Discuss real-world challenges and solutions

---

## 🐛 Phase 5: Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: Docker Compose Services Won't Start

**Symptom:**
```bash
docker compose up -d
# Error: port already allocated
```

**Solution:**
```bash
# Find and kill processes using ports
lsof -ti:5000 | xargs kill -9  # MLflow
lsof -ti:8000 | xargs kill -9  # FastAPI
lsof -ti:9090 | xargs kill -9  # Prometheus

# Or change ports in docker-compose.yml
```

#### Issue 2: MLflow Can't Find Model

**Symptom:**
```
RestException: Model 'churn-predictor' not found
```

**Solution:**
```bash
# Verify model is registered
mlflow models list

# Check tracking URI is correct
echo $MLFLOW_TRACKING_URI

# Re-register model
python register_model.py
```

#### Issue 3: DVC Push Fails

**Symptom:**
```
ERROR: failed to push data to the remote
```

**Solution:**
```bash
# Check remote configuration
dvc remote list
dvc remote -v list

# Re-add remote
dvc remote add -d -f local /tmp/dvc-remote
dvc push -v
```

#### Issue 4: Python Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'mlflow'
```

**Solution:**
```bash
# Verify virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt

# Or recreate environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Debugging Checklist

When something doesn't work:
1. ✅ Check logs: `docker compose logs -f <service-name>`
2. ✅ Verify environment variables: `printenv | grep MLOPS`
3. ✅ Confirm services are running: `docker compose ps`
4. ✅ Test connectivity: `curl http://localhost:<port>/health`
5. ✅ Review recent changes: `git log --oneline -5`
6. ✅ Check disk space: `df -h`
7. ✅ Restart services: `docker compose restart`

---

## 📝 Phase 6: Assessment & Certification

### Knowledge Checks

#### Module Quizzes (10 questions each)
- Administered at end of each module
- 70% passing score
- Immediate feedback

#### Mock Exams
```bash
# Take mock exam 1
cat exams/mock-exam-1.md

# Take mock exam 2
cat exams/mock-exam-2.md
```

### Project Evaluation Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| **Data Versioning** | 15 | DVC properly configured, data tracked |
| **Experiment Tracking** | 15 | MLflow experiments logged with params/metrics |
| **Training Pipeline** | 20 | Automated pipeline with Airflow or similar |
| **Model Serving** | 15 | Working API with health checks |
| **Monitoring** | 15 | Prometheus metrics, Grafana dashboard |
| **Documentation** | 10 | README, setup guide, architecture diagram |
| **Code Quality** | 10 | Tests, linting, best practices |
| **Total** | **100** | |

### Certification Path

After completing this course, students are prepared for:
- **AWS Certified Machine Learning - Specialty**
- **GCP Professional ML Engineer**
- **Databricks Certified Machine Learning Professional**

---

## 🚀 Phase 7: Next Steps & Advanced Topics

### After Course Completion

1. **Week 1 Post-Course:**
   - Complete any remaining mock exams
   - Refine capstone project
   - Create portfolio on GitHub

2. **Month 1:**
   - Apply learnings to personal/work projects
   - Contribute to open-source MLOps tools
   - Write blog post about your experience

3. **Months 2-3:**
   - Pursue official certifications
   - Build additional portfolio projects
   - Network in MLOps community

### Advanced Topics (Self-Study)

- **Multi-Model Serving:** Deploy multiple models behind one API
- **Feature Stores:** Implement Feast or Tecton
- **AutoML Integration:** Add FLAML or AutoGluon
- **Edge Deployment:** Deploy to edge devices with TFLite
- **LLMOps:** Extend MLOps practices to Large Language Models

---

## 📚 Appendix: Quick Reference

### Essential Commands

```bash
# Environment
source ~/.mlops-env

# Docker
docker compose up -d
docker compose ps
docker compose logs -f <service>
docker compose down

# DVC
dvc init
dvc add data/file.csv
dvc push
dvc pull

# MLflow
mlflow server --host 0.0.0.0 --port 5000
mlflow models list

# Airflow
airflow db init
airflow webserver --port 8080
airflow scheduler
airflow dags trigger <dag-name>

# FastAPI
uvicorn app:app --reload --port 8000

# Testing
pytest tests/
pytest --cov=src tests/

# Git
git add .
git commit -m "message"
git push
```

### Service URLs (Default)

- **MLflow:** http://localhost:5000
- **Airflow:** http://localhost:8080 (admin/admin)
- **FastAPI:** http://localhost:8000
- **FastAPI Docs:** http://localhost:8000/docs
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

### Useful Links

- **Course Repository:** https://github.com/Dhananjaiah/mlops
- **MLflow Docs:** https://mlflow.org/docs/latest/index.html
- **DVC Docs:** https://dvc.org/doc
- **Airflow Docs:** https://airflow.apache.org/docs/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **MLOps Community:** https://mlops.community

---

## ✅ Implementation Checklist

Use this checklist to track your progress:

### Setup Phase
- [ ] Repository cloned
- [ ] Environment variables configured
- [ ] Python dependencies installed
- [ ] Docker Desktop installed and running
- [ ] Course structure reviewed

### Learning Phase
- [ ] Module 00: Overview completed
- [ ] Module 01: MLOps Foundations completed
- [ ] Module 02: Environment & Packaging completed
- [ ] Module 03: Data Versioning completed
- [ ] Module 04: Experiment Tracking completed
- [ ] Module 05: Pipelines & Orchestration completed
- [ ] Module 06: Model Training completed
- [ ] Module 07: Model Registry completed
- [ ] Module 08: Serving & APIs completed
- [ ] Module 09: Batch & Streaming completed
- [ ] Module 10: CI/CD completed
- [ ] Module 11: Observability completed
- [ ] Module 12: Drift Detection completed
- [ ] Module 13: Security & Compliance completed
- [ ] Module 14: Comprehensive Review completed

### Project Phase
- [ ] Capstone project setup
- [ ] Data generation and versioning
- [ ] Training pipeline implemented
- [ ] Model registry configured
- [ ] API deployment
- [ ] Monitoring setup
- [ ] Tests passing
- [ ] Documentation complete

### Certification Phase
- [ ] All module quizzes passed (70%+)
- [ ] Mock Exam 1 completed
- [ ] Mock Exam 2 completed
- [ ] Capstone project evaluation: 70%+
- [ ] Ready for official certification

---

## 🎓 Conclusion

This implementation guide provides a complete roadmap for learning and teaching MLOps. By following these steps systematically, students will:

1. ✅ Master the full MLOps lifecycle
2. ✅ Build production-ready ML systems
3. ✅ Understand industry best practices
4. ✅ Be prepared for MLOps roles
5. ✅ Have a portfolio project to showcase

**Key Success Factors:**
- **Practice Regularly:** Complete hands-on exercises daily
- **Build Incrementally:** Each module builds on previous ones
- **Ask Questions:** Use discussions and troubleshooting guide
- **Collaborate:** Work with peers on projects
- **Apply Immediately:** Use learnings in real projects

**Remember:** MLOps is a journey, not a destination. Technology evolves, but the principles remain the same: version everything, automate pipelines, monitor continuously, and iterate quickly.

---

**Good luck with your MLOps journey! 🚀**

*For questions or issues, please open an issue on GitHub or join the MLOps Community.*

---

**Document Version:** 1.0  
**Last Updated:** 2024-11-02  
**Maintained By:** MLOps Course Team

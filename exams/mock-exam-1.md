# MLOps Certification Mock Exam 1

**Duration**: 90 minutes  
**Total Points**: 100  
**Passing Score**: 70%

---

## Instructions
- Complete all tasks in order
- Commands should work in a Linux/macOS environment
- Save all code and config files for verification
- Use the provided environment variables where applicable

---

## Section 1: Environment Setup (15 points)

### Task 1.1 (5 points)
Create a Python project with the following:
- `pyproject.toml` with dependencies: pandas>=2.1.0, scikit-learn>=1.3.0, mlflow>=2.9.0
- Lock file with exact dependency versions
- Pre-commit hooks for black and ruff

**Deliverables**: `pyproject.toml`, `requirements-lock.txt`, `.pre-commit-config.yaml`

### Task 1.2 (5 points)
Create a Dockerfile for training:
- Base image: `python:3.11-slim`
- Multi-stage build (builder + runtime)
- Install dependencies from lock file
- Copy training script
- CMD to run training

**Deliverables**: `Dockerfile.train`

### Task 1.3 (5 points)
Write a `.gitignore` file that:
- Ignores Python cache files
- Ignores virtual environments
- Ignores data files (data/*.csv) but tracks .dvc files
- Ignores model binaries

**Deliverables**: `.gitignore`

---

## Section 2: Data Versioning (15 points)

### Task 2.1 (7 points)
Initialize DVC and track a dataset:
```bash
# Given: data/train.csv exists
# TODO:
# 1. Initialize DVC
# 2. Add S3 remote: s3://mlops-exam/dvc-store
# 3. Track data/train.csv
# 4. Push to remote
```

**Deliverables**: Commands used, `.dvc/config`, `data/train.csv.dvc`

### Task 2.2 (8 points)
Create a DVC pipeline with stages:
- **preprocess**: Input `data/raw/train.csv`, Output `data/processed/train_clean.csv`
- **train**: Input `data/processed/train_clean.csv`, Output `models/model.pkl`
- Parameters from `params.yaml` (learning_rate, n_estimators)

**Deliverables**: `dvc.yaml`, `params.yaml`

---

## Section 3: Experiment Tracking (20 points)

### Task 3.1 (10 points)
Write a training script that:
- Loads data from `data/processed/train_clean.csv`
- Trains a RandomForestClassifier
- Logs to MLflow:
  - Params: n_estimators, max_depth, random_state
  - Metrics: accuracy, precision, recall, f1
  - Model artifact
  - Confusion matrix plot

**Deliverables**: `src/train.py`

### Task 3.2 (5 points)
Query MLflow to find the best model:
- Experiment name: "exam-training"
- Filter: accuracy > 0.85
- Sort by: accuracy descending
- Return top 3 runs

**Deliverables**: Python code or CLI command

### Task 3.3 (5 points)
Register the best model to MLflow Registry:
- Model name: "ExamClassifier"
- Transition to "Staging"
- Add description: "Best model from exam, accuracy=X.XX"

**Deliverables**: Python code

---

## Section 4: Model Serving (20 points)

### Task 4.1 (12 points)
Create a FastAPI application with:
- `/health` endpoint (returns {"status": "healthy"})
- `/ready` endpoint (checks model is loaded)
- `/predict` POST endpoint:
  - Input: `{"features": [[...]]}`
  - Validation with Pydantic
  - Returns: `{"predictions": [...], "model_version": "..."}`
- Prometheus `/metrics` endpoint

**Deliverables**: `src/api.py`

### Task 4.2 (8 points)
Create Kubernetes deployment manifest:
- Deployment name: exam-api
- Image: ghcr.io/exam/api:latest
- Replicas: 3
- Resource requests: cpu=100m, memory=256Mi
- Resource limits: cpu=1, memory=1Gi
- Liveness probe: `/health`
- Readiness probe: `/ready`
- Environment variable: MLFLOW_TRACKING_URI

**Deliverables**: `k8s/deployment.yaml`

---

## Section 5: CI/CD (15 points)

### Task 5.1 (10 points)
Create a GitHub Actions workflow that:
- Triggers on push to `main`
- Jobs:
  - **test**: Run pytest with coverage
  - **scan**: Run Trivy (fail on HIGH/CRITICAL CVEs)
  - **build**: Build and push Docker image (only if tests pass)
  - **deploy**: Deploy to dev environment

**Deliverables**: `.github/workflows/ci-cd.yml`

### Task 5.2 (5 points)
Write a test for the API predict endpoint:
- Mock model loading
- Test successful prediction
- Test invalid input (should return 422)

**Deliverables**: `tests/test_api.py`

---

## Section 6: Monitoring & Drift (15 points)

### Task 6.1 (8 points)
Create a Prometheus alert rule for:
- **HighErrorRate**: api_errors_total rate > 0.05 for 5 minutes
- **HighLatency**: P95 latency > 1 second for 5 minutes
- **ModelNotLoaded**: model_loaded == 0 for 1 minute

**Deliverables**: `alerts.yml`

### Task 6.2 (7 points)
Write a drift detection script using Evidently:
- Load reference data from `data/baseline.csv`
- Load current data from `data/current.csv`
- Generate DataDriftPreset report
- Save HTML report
- Exit with code 1 if drift detected

**Deliverables**: `src/detect_drift.py`

---

## Bonus Section (10 points)

### Bonus 1 (5 points)
Create a batch scoring script:
- Read data in chunks (10,000 rows)
- Load model from MLflow Registry (Production stage)
- Score all rows
- Add columns: `prediction`, `prediction_time`
- Save to output CSV

**Deliverables**: `src/batch_score.py`

### Bonus 2 (5 points)
Write a Makefile with targets:
- `install`: Install dependencies
- `test`: Run tests
- `lint`: Run black + ruff
- `docker-build`: Build Docker image
- `deploy-dev`: Deploy to K8s dev

**Deliverables**: `Makefile`

---

## Solutions

Solutions are provided in a separate file: `mock-exam-1-solutions.md`

---

## Evaluation Criteria

| Section | Points | Criteria |
|---------|--------|----------|
| **Environment Setup** | 15 | Correct configs, working Dockerfile, proper .gitignore |
| **Data Versioning** | 15 | DVC initialized, pipeline works, reproducible |
| **Experiment Tracking** | 20 | MLflow logs all required data, queries work |
| **Model Serving** | 20 | API works, K8s manifest valid, health checks present |
| **CI/CD** | 15 | Workflow runs, tests execute, security scans present |
| **Monitoring & Drift** | 15 | Alerts configured correctly, drift detection works |
| **Bonus** | 10 | Extra features implemented correctly |

**Total**: 110 points (100 + 10 bonus)  
**Pass**: 70/100

---

## Time Management Suggestions

- **Section 1**: 15 minutes
- **Section 2**: 20 minutes
- **Section 3**: 25 minutes
- **Section 4**: 20 minutes
- **Section 5**: 15 minutes
- **Section 6**: 15 minutes
- **Review**: 10 minutes (if time remaining)

---

## Good Luck!

Remember:
- Test your code as you go
- Check the troubleshooting matrix if stuck
- Refer to cheatsheets for quick syntax reference
- Partial credit given for working code

---

**[Back to Exams](./README.md)** | **[Solutions →](mock-exam-1-solutions.md)**

# Module 10: CI/CD & Environments

## 🎯 Goals

- Build **CI/CD pipelines** with GitHub Actions
- Implement **multi-environment** deployments (dev, staging, prod)
- Automate **testing** (unit, integration, model tests)
- Add **security scanning** (secrets, CVEs, SBOM)
- Enable **manual approval** gates for production
- Use **GitOps** for declarative deployments

---

## 📖 Key Terms

- **CI (Continuous Integration)**: Automated build, test, scan on every commit
- **CD (Continuous Delivery/Deployment)**: Automated deployment to environments
- **Environment**: Isolated deployment target (dev, staging, prod)
- **GitOps**: Using Git as single source of truth for infrastructure/config
- **SBOM (Software Bill of Materials)**: List of all dependencies and versions
- **CVE (Common Vulnerabilities and Exposures)**: Known security vulnerabilities

---

## 🔧 Commands First: GitHub Actions Workflow

```bash
# Create CI/CD workflow
mkdir -p .github/workflows

cat > .github/workflows/ci-cd.yml << 'EOF'
name: ML CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]"
      
      - name: Lint
        run: |
          ruff check src/
          black --check src/
      
      - name: Unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml
      
      - name: Model tests
        run: pytest tests/model/ -v
  
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          path: ./
          format: spdx-json
      
      - name: Scan for CVEs
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on HIGH/CRITICAL
      
      - name: Secrets scan
        uses: gitleaks/gitleaks-action@v2

  build-and-push:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Log in to registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.api
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-dev:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to dev
        run: |
          kubectl config use-context dev-cluster
          kubectl set image deployment/mlops-api \
            mlops-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n mlops-dev
          kubectl rollout status deployment/mlops-api -n mlops-dev

  deploy-prod:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to prod
        run: |
          kubectl config use-context prod-cluster
          kubectl set image deployment/mlops-api \
            mlops-api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n mlops-prod
          kubectl rollout status deployment/mlops-api -n mlops-prod
EOF
```

**Why**: GitHub Actions automates everything from test → scan → build → deploy. Environments enable manual approvals.

---

## 🧪 Model Testing

```bash
# Create model tests
mkdir -p tests/model

cat > tests/model/test_model_quality.py << 'EOF'
import mlflow.sklearn
import pytest
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

@pytest.fixture
def test_data():
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_test, y_test

def test_model_accuracy(test_data):
    """Test model meets minimum accuracy threshold"""
    X_test, y_test = test_data
    
    model = mlflow.sklearn.load_model("models:/IrisClassifier/Production")
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    assert accuracy >= 0.85, f"Model accuracy {accuracy:.3f} below threshold 0.85"

def test_model_prediction_shape(test_data):
    """Test predictions have correct shape"""
    X_test, y_test = test_data
    
    model = mlflow.sklearn.load_model("models:/IrisClassifier/Production")
    predictions = model.predict(X_test)
    
    assert predictions.shape == y_test.shape, "Prediction shape mismatch"

def test_model_prediction_range():
    """Test predictions are in valid range"""
    model = mlflow.sklearn.load_model("models:/IrisClassifier/Production")
    X = [[5.1, 3.5, 1.4, 0.2]]
    prediction = model.predict(X)[0]
    
    assert 0 <= prediction <= 2, f"Prediction {prediction} out of range [0, 2]"
EOF

# Run model tests
pytest tests/model/ -v
```

**Why**: Model tests validate quality before deployment. Catch regressions, ensure predictions are valid.

---

## 🌍 Multi-Environment Configuration

```bash
# Create environment configs
mkdir -p configs/environments

cat > configs/environments/dev.yaml << 'EOF'
environment: development
replicas: 1
resources:
  requests:
    cpu: "100m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
mlflow_uri: http://mlflow.mlops-dev.svc.cluster.local:5000
model_name: ChurnPredictor
model_stage: Staging
log_level: DEBUG
EOF

cat > configs/environments/prod.yaml << 'EOF'
environment: production
replicas: 3
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "2"
    memory: "4Gi"
mlflow_uri: http://mlflow.mlops-prod.svc.cluster.local:5000
model_name: ChurnPredictor
model_stage: Production
log_level: INFO
autoscaling:
  enabled: true
  min_replicas: 3
  max_replicas: 10
  target_cpu_percent: 70
EOF
```

**Why**: Separate configs per environment. Dev uses Staging models, Prod uses Production models.

---

## 🔐 Security Scanning in CI

```bash
# Add pre-commit config for local checks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/']
  
  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.2
    hooks:
      - id: python-safety-dependencies-check
EOF

# Install and run
pre-commit install
pre-commit run --all-files
```

**Why**: Catch secrets and vulnerabilities before commit. Security left-shift (catch early).

---

## 🎯 Canary Deployments

```bash
# Create canary deployment
cat > k8s/canary-deployment.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: mlops-api
  namespace: mlops-prod
spec:
  selector:
    app: mlops-api
  ports:
    - port: 80
      targetPort: 8000

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-api-stable
  namespace: mlops-prod
spec:
  replicas: 9  # 90% traffic
  selector:
    matchLabels:
      app: mlops-api
      version: stable
  template:
    metadata:
      labels:
        app: mlops-api
        version: stable
    spec:
      containers:
      - name: api
        image: ghcr.io/mlops-course/mlops-api:v1.0
        ports:
        - containerPort: 8000

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-api-canary
  namespace: mlops-prod
spec:
  replicas: 1  # 10% traffic
  selector:
    matchLabels:
      app: mlops-api
      version: canary
  template:
    metadata:
      labels:
        app: mlops-api
        version: canary
    spec:
      containers:
      - name: api
        image: ghcr.io/mlops-course/mlops-api:v2.0-candidate
        ports:
        - containerPort: 8000
EOF

# Deploy
kubectl apply -f k8s/canary-deployment.yaml

# Monitor canary metrics
# If good: gradually increase canary replicas
# If bad: rollback (delete canary deployment)
```

**Why**: Canary deployments reduce risk. Test new version with small traffic before full rollout.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Set up CI/CD pipeline with GitHub Actions.

1. **Create workflow**:
```bash
mkdir -p ~/mlops-lab-10/.github/workflows
# Copy ci-cd.yml from above
```

2. **Add tests**:
```bash
mkdir -p tests
cat > tests/test_api.py << 'EOF'
def test_health():
    assert True  # Placeholder
EOF
```

3. **Commit and push**:
```bash
git add .github tests
git commit -m "Add CI/CD pipeline"
git push
# Check Actions tab on GitHub
```

**Expected output**: CI runs, tests pass, security scans complete.

---

## ❓ Quiz (5 Questions)

1. **What is the difference between CI and CD?**
   - Answer: CI = automated build/test on commit. CD = automated deployment to environments.

2. **Why require manual approval for production?**
   - Answer: Human oversight prevents accidental deployments of untested code.

3. **What is SBOM?**
   - Answer: Software Bill of Materials—list of all dependencies and versions for security/compliance.

4. **Why use canary deployments?**
   - Answer: Test new version with small traffic percentage, rollback quickly if issues detected.

5. **What is GitOps?**
   - Answer: Using Git as single source of truth; infrastructure/config changes via Git commits.

---

## ⚠️ Common Mistakes

1. **No environment separation** → Dev changes affect prod.  
   *Fix*: Separate namespaces, clusters, or accounts per environment.

2. **Skipping security scans** → Deploy vulnerable code.  
   *Fix*: Add Trivy, Gitleaks, SBOM generation to CI.

3. **No rollback plan** → Stuck with bad deployment.  
   *Fix*: Use K8s rollout undo, canary patterns, blue-green deployments.

4. **Hardcoded secrets in CI** → Leaked credentials.  
   *Fix*: Use GitHub Secrets, Vault, or cloud secret managers.

5. **No model tests** → Deploy broken models.  
   *Fix*: Add model accuracy/shape/range tests to CI.

---

## 🛠️ Troubleshooting

**Issue**: "CI pipeline fails on security scan"  
→ **Root cause**: HIGH/CRITICAL CVE in dependencies.  
→ **Fix**: Update vulnerable packages, or suppress false positives with config.  
→ **See**: `/troubleshooting/triage-matrix.md` row "CI security scan failures"

**Issue**: "Deployment stuck in pending"  
→ **Root cause**: Image pull failure, insufficient resources, or pod crash.  
→ **Fix**: Check `kubectl describe pod`, verify image exists, increase resources.  
→ **See**: `/troubleshooting/triage-matrix.md` row "K8s deployment stuck"

---

## 📚 Key Takeaways

- **CI/CD automates** build → test → scan → deploy
- **GitHub Actions** provides workflows with matrix builds, caching, environments
- **Security scanning** (Trivy, Gitleaks, SBOM) catches vulnerabilities early
- **Multi-environment** configs ensure dev != prod
- **Manual approval** gates protect production
- **Canary deployments** reduce risk with gradual rollouts

---

## 🚀 Next Steps

- **Module 11**: Observability with Prometheus, Grafana, OpenTelemetry
- **Module 12**: Drift detection and automated retraining
- **Hands-on**: Deploy Churn Predictor with full CI/CD pipeline

---

**[← Module 09](09-batch-streaming-and-scheduled-jobs.md)** | **[Next: Module 11 →](11-observability-and-monitoring.md)**

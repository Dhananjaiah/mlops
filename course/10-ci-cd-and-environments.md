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

## 🎓 Lessons with Transcript

### What We're Doing in This Module

**Welcome to CI/CD & Environments!** This is where we automate the path from code commit to production deployment. We're learning to build pipelines that test, scan, and deploy code safely across multiple environments.

### Lesson 1: Continuous Integration - Catching Issues Early

**Transcript:**
"Without CI, you find bugs late - maybe in staging, maybe in production, maybe never. CI runs automated checks on every commit. Your test suite runs, linters check code style, type checkers verify correctness, security scanners look for vulnerabilities. If anything fails, the commit is marked as failing and can't be merged. This catches issues immediately, when context is fresh. The developer who introduced the bug fixes it right away, not three weeks later when they've forgotten the code. For ML, CI also runs model tests - does it handle edge cases? Does it maintain accuracy on test data? CI is your safety net."

**What you're learning:** How continuous integration prevents bugs from entering the codebase through automated testing.

### Lesson 2: Multiple Environments - Dev, Staging, Production

**Transcript:**
"You never deploy directly to production. You need environments to test progressively. Dev is where you experiment - it's okay if things break. Staging mirrors production - same infrastructure, same scale, but with test data. You deploy to staging first, run integration tests, verify everything works. Only then do you promote to production. Each environment has its own configuration - different database URLs, different scaling, different models. But the code is identical. This separation lets you catch environment-specific issues before they affect users. If something works in staging, you have high confidence it'll work in production."

**What you're learning:** Why multiple environments enable safe, progressive deployment.

### Lesson 3: GitOps - Git as the Source of Truth

**Transcript:**
"GitOps means your Git repository defines everything - code, configuration, infrastructure. Want to deploy a new model? Update the config file specifying the model version, commit it, and automation deploys it. Want to roll back? Revert the commit. This makes deployments auditable - you can see exactly what changed and when. It also makes rollbacks trivial - just git revert. For ML, your registry might have 20 model versions, but your config file specifies which one is active in each environment. Changing that file triggers deployment. No manual kubectl commands, no SSH into servers - Git is the control plane."

**What you're learning:** How GitOps makes deployments auditable, repeatable, and reversible.

### Lesson 4: Security Scanning - SBOM and CVE Detection

**Transcript:**
"Before deploying, you must scan for security issues. SBOM - Software Bill of Materials - lists every dependency and version in your container. Tools like Syft generate this. Then Grype or Trivy scan the SBOM against CVE databases to find known vulnerabilities. If you're using pandas 1.2.0 which has a high-severity CVE, the scan fails your pipeline. You must update to a patched version before deploying. This prevents you from running software with known exploits. For ML, this is critical because we use many dependencies - scikit-learn, numpy, pandas - all with potential vulnerabilities."

**What you're learning:** How to scan for security vulnerabilities before deployment using SBOM and CVE scanning.

### Lesson 5: Progressive Deployment - Canary and Blue-Green

**Transcript:**
"Even after testing in staging, production deployments can fail. Canary deployments reduce risk by rolling out gradually. You deploy the new model to 5% of traffic. If metrics look good, expand to 25%, then 50%, then 100%. If anything goes wrong, you only affected a small percentage. Blue-green deployment is different - you run two environments, blue (old) and green (new). All traffic goes to blue. You deploy to green, test it, then switch traffic over. If issues occur, switch back instantly. These patterns give you progressive confidence and quick rollback options. For ML, they're essential because models can fail in unexpected ways with real data."

**What you're learning:** How canary and blue-green deployments minimize risk during production rollouts.

### Key Definition - What We're Doing Overall

**In this module, we're automating safe deployments.** We're building CI pipelines that test and scan every commit. We're setting up multiple environments for progressive testing. We're adopting GitOps so all changes are auditable and reversible. We're scanning for security vulnerabilities before deployment. And we're implementing progressive deployment patterns like canary and blue-green to minimize production risk.

**By the end of this lesson, you should understand:** How to build GitHub Actions CI pipelines with testing and security scans, how to configure multiple environments with environment-specific configs, how to implement GitOps workflows, and how to do canary deployments. CI/CD transforms manual, error-prone deployment into automated, safe, auditable processes - it's essential for any production ML system.

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

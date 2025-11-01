# Module 13: Security, Compliance & Cost

## 🎯 Goals

- Scan for **vulnerabilities** (CVEs) in dependencies
- Generate **SBOM** (Software Bill of Materials)
- Detect **secrets** in code and commits
- Implement **PII detection** and data privacy
- Set up **RBAC** (Role-Based Access Control)
- Monitor and optimize **costs**

---

## 📖 Key Terms

- **CVE**: Common Vulnerabilities and Exposures (known security flaws)
- **SBOM**: Software Bill of Materials (inventory of dependencies)
- **PII**: Personally Identifiable Information (names, emails, SSNs)
- **RBAC**: Role-Based Access Control (permissions by role)
- **Secrets**: API keys, passwords, tokens (must never be in code)
- **FinOps**: Financial operations for cloud cost optimization

---

## 🔧 Commands First: Vulnerability Scanning

```bash
# Install Trivy (CVE scanner)
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Scan Docker image
trivy image mlops-api:latest --severity HIGH,CRITICAL

# Scan filesystem
trivy fs . --severity HIGH,CRITICAL

# Scan in CI (fail on HIGH/CRITICAL)
trivy image mlops-api:latest --exit-code 1 --severity CRITICAL

# Generate report
trivy image mlops-api:latest --format json --output trivy-report.json
```

**Why**: Trivy detects CVEs in OS packages and language dependencies. Fail builds on critical vulnerabilities.

---

## 📋 Generate SBOM

```bash
# Install Syft (SBOM generator)
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Generate SBOM for Docker image
syft mlops-api:latest -o spdx-json=sbom.spdx.json

# Generate for filesystem
syft dir:. -o spdx-json=sbom-fs.spdx.json

# View SBOM
cat sbom.spdx.json | jq '.packages[] | {name, version}'
```

**Why**: SBOM provides inventory of all dependencies for compliance, audits, and vulnerability tracking.

---

## 🔐 Secrets Scanning

```bash
# Install Gitleaks
brew install gitleaks  # or download binary

# Scan repository
gitleaks detect --source . --report-path gitleaks-report.json

# Scan commits
gitleaks protect --staged

# Add to pre-commit (prevents commits with secrets)
cat >> .pre-commit-config.yaml << 'EOF'
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
EOF

pre-commit install
```

**Why**: Gitleaks prevents secrets from reaching git. Scan history to find accidentally committed secrets.

---

## 🛡️ PII Detection

```bash
# Install presidio (PII detection)
pip install presidio-analyzer presidio-anonymizer

cat > src/detect_pii.py << 'EOF'
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import pandas as pd

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def detect_pii(text):
    """Detect PII in text"""
    results = analyzer.analyze(text=text, language='en')
    return [(r.entity_type, r.start, r.end, r.score) for r in results]

def anonymize_pii(text):
    """Anonymize PII in text"""
    results = analyzer.analyze(text=text, language='en')
    return anonymizer.anonymize(text=text, analyzer_results=results).text

# Example
text = "My name is John Doe and my email is john.doe@example.com"
print("PII detected:", detect_pii(text))
print("Anonymized:", anonymize_pii(text))

# Apply to DataFrame
df = pd.DataFrame({
    'customer_id': [1, 2],
    'name': ['Jane Smith', 'Bob Johnson'],
    'email': ['jane@example.com', 'bob@example.com']
})

df['name_anon'] = df['name'].apply(anonymize_pii)
df['email_anon'] = df['email'].apply(anonymize_pii)
print(df)
EOF

python src/detect_pii.py
```

**Why**: PII detection prevents leaking sensitive data in logs, models, or analytics. Compliance with GDPR, CCPA.

---

## 🔑 RBAC and Access Control

```bash
# Kubernetes RBAC for MLOps namespace
cat > rbac.yaml << 'EOF'
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mlops-deployer
  namespace: mlops

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: mlops-deployer-role
  namespace: mlops
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["services", "pods"]
    verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: mlops-deployer-binding
  namespace: mlops
subjects:
  - kind: ServiceAccount
    name: mlops-deployer
    namespace: mlops
roleRef:
  kind: Role
  name: mlops-deployer-role
  apiGroup: rbac.authorization.k8s.io
EOF

kubectl apply -f rbac.yaml

# MLflow access control (using basic auth)
cat > mlflow_auth.py << 'EOF'
import mlflow
from mlflow.server import app

# Configure authentication
app.config['BASIC_AUTH_USERNAME'] = 'mlops-user'
app.config['BASIC_AUTH_PASSWORD'] = 'secure-password'
EOF
```

**Why**: RBAC limits who can deploy, access data, or modify models. Principle of least privilege.

---

## 💰 Cost Monitoring

```bash
# Install kubecost for K8s cost tracking
kubectl create namespace kubecost
kubectl apply -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/master/kubecost.yaml -n kubecost

# Set resource limits to prevent runaway costs
cat > resource-limits.yaml << 'EOF'
apiVersion: v1
kind: LimitRange
metadata:
  name: mlops-limits
  namespace: mlops
spec:
  limits:
    - max:
        cpu: "4"
        memory: "8Gi"
      min:
        cpu: "100m"
        memory: "128Mi"
      type: Container
EOF

kubectl apply -f resource-limits.yaml

# Cloud cost alerts (AWS example)
cat > cloudwatch-cost-alert.json << 'EOF'
{
  "AlarmName": "MLOpsCostAlert",
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 1,
  "MetricName": "EstimatedCharges",
  "Namespace": "AWS/Billing",
  "Period": 86400,
  "Statistic": "Maximum",
  "Threshold": 1000.0,
  "ActionsEnabled": true,
  "AlarmActions": ["arn:aws:sns:us-east-1:123456789:billing-alerts"]
}
EOF

aws cloudwatch put-metric-alarm --cli-input-json file://cloudwatch-cost-alert.json
```

**Why**: Cost monitoring prevents budget overruns. Set alerts before costs spike.

---

## 📊 Audit Logging

```bash
# MLflow audit log
cat > src/audit_log.py << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient
import logging

logging.basicConfig(
    filename='mlops-audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(user)s - %(action)s - %(resource)s'
)

def log_action(user, action, resource):
    logging.info(f"User {user} performed {action} on {resource}")

# Example: Log model registration
client = MlflowClient()
model_name = "ChurnPredictor"
# ... register model ...
log_action("john.doe", "register_model", model_name)

# Example: Log stage transition
# ... transition to production ...
log_action("jane.smith", "promote_to_production", f"{model_name}_v2")
EOF

# Kubernetes audit policy
cat > audit-policy.yaml << 'EOF'
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: Metadata
    namespaces: ["mlops"]
    verbs: ["create", "update", "delete", "patch"]
    resources:
      - group: ""
        resources: ["pods", "services"]
      - group: "apps"
        resources: ["deployments"]
EOF
```

**Why**: Audit logs track who did what, when. Critical for compliance and security investigations.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Scan for vulnerabilities and secrets.

1. **Scan Docker image**:
```bash
mkdir -p ~/mlops-lab-13 && cd ~/mlops-lab-13
trivy image python:3.11-slim --severity HIGH,CRITICAL
```

2. **Generate SBOM**:
```bash
syft python:3.11-slim -o spdx-json=sbom.json
cat sbom.json | jq '.packages | length'  # Count dependencies
```

3. **Scan for secrets**:
```bash
echo "api_key = 'sk-1234567890abcdef'" > config.py
gitleaks detect --source . --no-git
# Should detect potential secret
rm config.py
```

**Expected output**: Trivy finds CVEs, Syft generates SBOM, Gitleaks detects secret.

---

## ❓ Quiz (5 Questions)

1. **What is SBOM?**
   - Answer: Software Bill of Materials—inventory of all dependencies and versions.

2. **Why scan for CVEs?**
   - Answer: Detect known vulnerabilities before attackers exploit them.

3. **What is PII?**
   - Answer: Personally Identifiable Information (names, emails, SSNs) that must be protected.

4. **Why use RBAC?**
   - Answer: Limit access based on roles (least privilege), prevent unauthorized actions.

5. **How to prevent cost overruns?**
   - Answer: Set resource limits, budget alerts, right-size resources, auto-scale down.

---

## ⚠️ Common Mistakes

1. **Ignoring security scans** → Deploy vulnerable code.  
   *Fix*: Add Trivy/Grype to CI, fail on HIGH/CRITICAL.

2. **Hardcoding secrets** → Leaked credentials.  
   *Fix*: Use secrets managers (Vault, AWS Secrets Manager), scan with Gitleaks.

3. **No PII protection** → Compliance violations.  
   *Fix*: Anonymize PII, encrypt at rest, limit access.

4. **Overprivileged service accounts** → Blast radius from compromises.  
   *Fix*: Use RBAC, grant minimum necessary permissions.

5. **No cost monitoring** → Surprise bills.  
   *Fix*: Set budgets, alerts, regularly review spend.

---

## 🛠️ Troubleshooting

**Issue**: "CI fails on CVE scan"  
→ **Root cause**: HIGH/CRITICAL vulnerability in dependency.  
→ **Fix**: Update vulnerable package, or suppress if false positive with config.  
→ **See**: `/troubleshooting/triage-matrix.md` row "CVE scan failures"

**Issue**: "Service account can't deploy"  
→ **Root cause**: Missing RBAC permissions.  
→ **Fix**: Check Role, RoleBinding, verify service account name.  
→ **See**: `/troubleshooting/triage-matrix.md` row "RBAC permission denied"

---

## 📚 Key Takeaways

- **Scan for CVEs** with Trivy/Grype in CI
- **Generate SBOM** for compliance and audits
- **Detect secrets** with Gitleaks pre-commit hooks
- **Protect PII** with anonymization and encryption
- **Use RBAC** for least-privilege access control
- **Monitor costs** with budgets and alerts

---

## 🚀 Next Steps

- **Module 14**: Comprehensive review tying all modules together
- **Capstone Project**: Complete end-to-end Churn Predictor with full MLOps
- **Exams**: Test knowledge with mock certification exams

---

**[← Module 12](12-drift-detection-and-retraining.md)** | **[Next: Module 14 →](14-comprehensive-review.md)**

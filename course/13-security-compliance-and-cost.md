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

## 🎓 Lessons with Transcript

### What We're Doing in This Module

**Welcome to Security, Compliance & Cost!** This is where we make ML systems production-grade by addressing security vulnerabilities, meeting compliance requirements, and optimizing costs. These aren't optional - they're essential for any real production system.

### Lesson 1: Vulnerability Scanning - CVEs and SBOMs

**Transcript:**
"Every library you use - scikit-learn, pandas, numpy - can have security vulnerabilities. CVE databases track known flaws with severity ratings. Before deploying, you must scan for these. First, generate an SBOM - Software Bill of Materials - using Syft. This lists every dependency in your container, including transitive dependencies. Then scan the SBOM with Grype or Trivy against CVE databases. If you're using a library with a high-severity CVE, the scan fails. You must update to a patched version before deployment. This prevents you from running exploitable software in production. In regulated industries like healthcare or finance, SBOM generation is a compliance requirement."

**What you're learning:** How to detect and remediate security vulnerabilities before deployment.

### Lesson 2: Secrets Management - Never Commit Credentials

**Transcript:**
"The worst security mistake is hardcoding secrets. Someone commits AWS keys to GitHub, and within hours, they're discovered and exploited. Use environment variables or secrets managers like AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault. Your code reads secrets at runtime from these systems, never from config files. Tools like Gitleaks scan your repository for accidentally committed secrets - API keys, passwords, tokens. Run Gitleaks in CI to block commits containing secrets. For ML, you need secrets for cloud storage (S3 credentials), databases (connection strings), and ML platforms (MLflow tokens). All must be externalized."

**What you're learning:** How to manage secrets securely using environment variables and secret managers.

### Lesson 3: PII Detection and Data Privacy

**Transcript:**
"ML models often train on personal data - names, emails, addresses, medical records. Regulations like GDPR and HIPAA require protecting PII. Use tools like Microsoft Presidio to detect PII in datasets. It recognizes patterns like social security numbers, credit cards, and email addresses. You can then anonymize, pseudonymize, or remove PII before training. Also implement data access controls - not everyone should see raw data. Use RBAC to limit who can access datasets, models, and predictions. For production systems, log only aggregate metrics, never individual predictions with PII. Privacy violations have massive fines and reputational damage."

**What you're learning:** How to detect PII and implement privacy protections in ML systems.

### Lesson 4: Compliance - Auditability and Documentation

**Transcript:**
"Regulated industries require proof of due diligence. Model cards document what model does, on what data it was trained, its performance, and limitations. This is compliance documentation. Lineage tracking shows exactly what data and code produced what model. Audit logs record who accessed what and when. Together, these provide auditability - you can answer 'how was this decision made?' for any prediction. This isn't just bureaucracy. When a model makes a mistake, you need to trace back to debug. When regulators ask questions, you need documentation. Build these practices from day one."

**What you're learning:** How to meet compliance requirements through documentation and auditability.

### Lesson 5: FinOps - Cost Optimization for ML

**Transcript:**
"ML is expensive - GPU training, large storage for datasets and models, high-traffic APIs. Without cost controls, bills explode. FinOps practices include: setting resource limits so training jobs can't spin up 100 GPUs accidentally, using autoscaling to scale down during low traffic, choosing cheaper storage tiers for old artifacts, setting budget alerts so you know when costs spike. For training, use spot instances that cost 70% less but can be interrupted. For storage, use lifecycle policies to move old data to cheaper tiers. For serving, right-size your containers - don't use 8-core machines if 2-core suffices. Cost optimization isn't optional at scale."

**What you're learning:** How to control and optimize costs for ML infrastructure.

### Key Definition - What We're Doing Overall

**In this module, we're hardening ML systems for production.** We're scanning for security vulnerabilities with SBOM and CVE tools. We're managing secrets securely with environment variables and secret managers. We're detecting and protecting PII to meet privacy regulations. We're implementing compliance through model cards, lineage, and audit logs. And we're optimizing costs with resource limits, autoscaling, and storage lifecycle policies.

**By the end of this lesson, you should understand:** How to generate SBOMs and scan for CVEs, how to use secrets managers instead of hardcoding credentials, how to detect and protect PII, how to meet compliance requirements with documentation, and how to optimize ML infrastructure costs. Security, compliance, and cost aren't afterthoughts - they're essential from day one for any production ML system.

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

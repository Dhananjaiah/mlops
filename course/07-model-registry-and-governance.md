# Module 07: Model Registry & Governance

## 🎯 Goals

- Register models in **MLflow Model Registry**
- Manage model **versions** and **lifecycle stages**
- Implement **approval workflows** for production deployment
- Track model **lineage** (data, code, params)
- Document **model cards** for transparency
- Set up **model governance** policies

---

## 📖 Key Terms

- **Model Registry**: Centralized repository for versioned models with metadata
- **Model version**: Specific instance of a registered model (v1, v2, etc.)
- **Stage**: Lifecycle phase (None, Staging, Production, Archived)
- **Stage transition**: Moving model between stages (e.g., Staging → Production)
- **Model lineage**: Traceable path from data + code → model → deployment
- **Model card**: Documentation of model purpose, performance, limitations, ethics
- **Governance**: Policies ensuring compliance, fairness, and accountability

---

## 🎓 Lessons with Transcript

### What We're Doing in This Module

**Welcome to Model Registry & Governance!** This is where we add structure to model deployment. Instead of ad-hoc "which model file should I deploy?", we have a centralized registry with approval workflows and documentation.

### Lesson 1: The Model Registry - Central Source of Truth

**Transcript:**
"Without a registry, models are scattered everywhere. Training outputs go to various directories, different people save models with different names, production uses a model file someone emailed last month. This is chaos. A model registry is a single source of truth for all models. Every trained model gets registered with a name and version number. You register 'churn-predictor' version 1, then version 2, then version 3. Each version has metadata - who trained it, what data was used, what metrics it achieved. When you need to deploy or debug, you go to the registry. No more searching filesystems or Slack conversations for model files."

**What you're learning:** Why centralized model registration solves the "where is the model?" problem.

### Lesson 2: Stages - Model Lifecycle Management

**Transcript:**
"Not every model should go straight to production. MLflow Registry has stages to manage the lifecycle. A newly trained model starts in 'None' stage - it exists but isn't approved. When you validate it, you promote to 'Staging' - it's ready for testing in a staging environment. After testing passes, you promote to 'Production' - it's approved for user traffic. When you deploy a newer version, the old one moves to 'Archived'. This stage system creates approval gates. You can't accidentally deploy an untested model to production because it has to pass through staging first. This is governance."

**What you're learning:** How stage transitions create controlled approval workflows for model deployment.

### Lesson 3: Model Lineage - Traceability from Data to Deployment

**Transcript:**
"Lineage answers 'where did this model come from?' For any production model, you need to trace back to the exact training run, which links to the code commit, data version, and hyperparameters used. MLflow Registry connects these dots. Each model version links to its source run ID. That run has tags for git SHA, DVC data version, and training config. If a production model misbehaves, you can trace it back to see 'it was trained on dataset v12 with code commit abc123 using these parameters.' This makes debugging possible. It also meets compliance requirements - regulators ask 'how did you build this model?' and you can show complete lineage."

**What you're learning:** How model registries enable complete traceability for debugging and compliance.

### Lesson 4: Model Cards - Documenting Purpose and Limitations

**Transcript:**
"A model isn't just weights and biases - it has context. What problem does it solve? What data was it trained on? What are its performance metrics? What are known limitations and biases? Model cards document all this in a standard format. They're like README files for models. When someone wants to use your model, they read the card to understand if it fits their use case. When an issue occurs, the card helps debug - 'this model was only trained on US data, but we're using it in Europe, that explains the poor performance.' Model cards are also compliance tools - they document fairness evaluations and ethical considerations."

**What you're learning:** Why model documentation is essential for safe, appropriate model usage.

### Lesson 5: Governance Policies - Enforcing Standards

**Transcript:**
"Governance is about enforcing standards automatically. You might have policies like 'no model can be promoted to production unless it has 90%+ accuracy and passes fairness checks' or 'all production models must have model cards' or 'staging-to-production transitions require approval from two reviewers.' MLflow webhooks can enforce these. When someone tries to promote a model, a webhook checks if conditions are met. If not, it blocks the transition and sends an alert. This prevents human error. A tired engineer can't accidentally deploy a bad model at 2 AM because the system enforces the rules."

**What you're learning:** How automated governance policies prevent deployment of unqualified models.

### Key Definition - What We're Doing Overall

**In this module, we're adding structure to model management.** We're using a centralized registry as the single source of truth for models. We're implementing stage-based lifecycle management with approval gates. We're tracking complete lineage from data to deployed model. We're documenting models with model cards. And we're enforcing governance policies that prevent deployment of unqualified models.

**By the end of this lesson, you should understand:** How to register models in MLflow Registry, how to transition models through stages, how to query model lineage for debugging, how to create model cards, and how to implement governance policies with webhooks. A model registry transforms chaotic model management into a controlled, auditable process - it's essential for any organization running ML in production.

---

## 🔧 Commands First: Register Model

```bash
# Register model from MLflow run
cat > src/register_model.py << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Get best run from experiment
runs = mlflow.search_runs(
    experiment_names=["model-selection"],
    order_by=["metrics.accuracy DESC"],
    max_results=1
)

best_run_id = runs.iloc[0]['run_id']
best_accuracy = runs.iloc[0]['metrics.accuracy']

print(f"Best run: {best_run_id} (accuracy: {best_accuracy:.3f})")

# Register model
model_name = "ChurnPredictor"
model_uri = f"runs:/{best_run_id}/model"

result = mlflow.register_model(model_uri, model_name)

print(f"Model registered:")
print(f"  Name: {result.name}")
print(f"  Version: {result.version}")
print(f"  Run ID: {best_run_id}")
EOF

python src/register_model.py
```

**Why**: Model Registry centralizes approved models. Versioning tracks changes. Stages control deployment.

---

## 🔄 Manage Model Stages

```bash
# Transition model to Staging
cat > src/transition_stage.py << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient("http://localhost:5000")

model_name = "ChurnPredictor"

# Get latest version
latest_versions = client.get_latest_versions(model_name, stages=["None"])
if latest_versions:
    version = latest_versions[0].version
    
    # Transition to Staging
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Staging",
        archive_existing_versions=False
    )
    print(f"Model {model_name} version {version} transitioned to Staging")
    
    # Add description
    client.update_model_version(
        name=model_name,
        version=version,
        description="Random Forest with n_estimators=100, accuracy=0.95 on validation"
    )
else:
    print("No model versions found")
EOF

python src/transition_stage.py
```

**Why**: Staging allows testing in pre-prod. Production stage signals approved for deployment.

---

## ✅ Verify Model Registry

```bash
# List registered models
mlflow models list

# Get model details
cat > src/get_model_info.py << 'EOF'
from mlflow.tracking import MlflowClient

client = MlflowClient("http://localhost:5000")
model_name = "ChurnPredictor"

# Get all versions
versions = client.search_model_versions(f"name='{model_name}'")

print(f"Model: {model_name}")
for v in versions:
    print(f"  Version {v.version}: {v.current_stage} (run: {v.run_id})")
EOF

python src/get_model_info.py
```

---

## 🎭 Approval Workflow

```bash
# Create approval workflow
cat > src/approve_for_production.py << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient
import sys

def approve_for_production(model_name, version, approver, notes):
    """Approve model for production deployment"""
    client = MlflowClient("http://localhost:5000")
    
    # Check current stage
    model_version = client.get_model_version(model_name, version)
    if model_version.current_stage != "Staging":
        print(f"Error: Model must be in Staging (currently: {model_version.current_stage})")
        return False
    
    # Get model metrics from run
    run = client.get_run(model_version.run_id)
    accuracy = run.data.metrics.get('accuracy', 0)
    
    # Approval criteria
    if accuracy < 0.90:
        print(f"Error: Model accuracy {accuracy:.3f} below threshold 0.90")
        return False
    
    # Add approval tag
    client.set_model_version_tag(model_name, version, "approved_by", approver)
    client.set_model_version_tag(model_name, version, "approval_notes", notes)
    
    # Transition to Production (archive previous production versions)
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production",
        archive_existing_versions=True
    )
    
    print(f"Model {model_name} v{version} approved for Production by {approver}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python approve_for_production.py <model_name> <version> <approver> <notes>")
        sys.exit(1)
    
    approve_for_production(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
EOF

# Example approval
python src/approve_for_production.py ChurnPredictor 1 "john.doe@company.com" "Meets accuracy threshold, tested in staging"
```

**Why**: Approval workflow enforces quality gates. Tags record audit trail (who, when, why).

---

## 📋 Model Lineage Tracking

```bash
# Create lineage tracking
cat > src/track_lineage.py << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient
import json

def get_model_lineage(model_name, version):
    """Get full lineage for model version"""
    client = MlflowClient("http://localhost:5000")
    
    # Get model version
    mv = client.get_model_version(model_name, version)
    
    # Get run details
    run = client.get_run(mv.run_id)
    
    lineage = {
        "model": {
            "name": model_name,
            "version": version,
            "stage": mv.current_stage,
            "created_at": mv.creation_timestamp,
        },
        "training_run": {
            "run_id": mv.run_id,
            "experiment_id": run.info.experiment_id,
            "start_time": run.info.start_time,
        },
        "code": {
            "git_commit": run.data.tags.get("mlflow.source.git.commit", "N/A"),
            "source": run.data.tags.get("mlflow.source.name", "N/A"),
        },
        "data": {
            "dvc_hash": run.data.tags.get("dvc_hash", "N/A"),
            "dataset_version": run.data.tags.get("dataset_version", "N/A"),
        },
        "parameters": run.data.params,
        "metrics": run.data.metrics,
    }
    
    return lineage

# Example
lineage = get_model_lineage("ChurnPredictor", "1")
print(json.dumps(lineage, indent=2))
EOF

python src/track_lineage.py
```

**Why**: Lineage enables reproducibility, debugging, and compliance audits.

---

## 📄 Model Card Documentation

```bash
# Create model card template
cat > model_card_template.md << 'EOF'
# Model Card: {{MODEL_NAME}}

## Model Details
- **Version**: {{VERSION}}
- **Date**: {{DATE}}
- **Model Type**: {{MODEL_TYPE}}
- **Framework**: {{FRAMEWORK}}
- **Owner**: {{OWNER}}

## Intended Use
**Primary Use**: {{PRIMARY_USE}}
**Out-of-Scope Uses**: {{OUT_OF_SCOPE}}

## Training Data
- **Dataset**: {{DATASET_NAME}}
- **Size**: {{NUM_SAMPLES}} samples
- **Time Period**: {{TIME_PERIOD}}
- **Preprocessing**: {{PREPROCESSING}}

## Performance Metrics
- **Accuracy**: {{ACCURACY}}
- **Precision**: {{PRECISION}}
- **Recall**: {{RECALL}}
- **F1 Score**: {{F1_SCORE}}
- **AUC-ROC**: {{AUC}}

## Fairness & Bias
- **Protected Attributes**: {{PROTECTED_ATTRS}}
- **Bias Metrics**: {{BIAS_METRICS}}
- **Mitigation**: {{MITIGATION}}

## Limitations
{{LIMITATIONS}}

## Ethical Considerations
{{ETHICAL_CONSIDERATIONS}}

## Caveats & Recommendations
{{CAVEATS}}

## References
- Run ID: {{RUN_ID}}
- Experiment: {{EXPERIMENT}}
- Code: {{GIT_COMMIT}}
EOF

# Generate model card from run
cat > src/generate_model_card.py << 'EOF'
from mlflow.tracking import MlflowClient
from datetime import datetime

def generate_model_card(model_name, version, output_path="model_card.md"):
    """Generate model card from MLflow metadata"""
    client = MlflowClient("http://localhost:5000")
    
    mv = client.get_model_version(model_name, version)
    run = client.get_run(mv.run_id)
    
    # Read template
    with open("model_card_template.md", "r") as f:
        template = f.read()
    
    # Fill template
    card = template.replace("{{MODEL_NAME}}", model_name)
    card = card.replace("{{VERSION}}", str(version))
    card = card.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
    card = card.replace("{{MODEL_TYPE}}", run.data.params.get("model_type", "N/A"))
    card = card.replace("{{ACCURACY}}", str(run.data.metrics.get("accuracy", "N/A")))
    card = card.replace("{{PRECISION}}", str(run.data.metrics.get("precision", "N/A")))
    card = card.replace("{{RECALL}}", str(run.data.metrics.get("recall", "N/A")))
    card = card.replace("{{F1_SCORE}}", str(run.data.metrics.get("f1", "N/A")))
    card = card.replace("{{RUN_ID}}", mv.run_id)
    card = card.replace("{{GIT_COMMIT}}", run.data.tags.get("mlflow.source.git.commit", "N/A"))
    
    # Fill remaining with placeholders
    import re
    card = re.sub(r'\{\{[A-Z_]+\}\}', '[TO BE FILLED]', card)
    
    with open(output_path, "w") as f:
        f.write(card)
    
    print(f"Model card generated: {output_path}")

generate_model_card("ChurnPredictor", "1")
EOF

python src/generate_model_card.py
```

**Why**: Model cards document purpose, performance, limitations for transparency and compliance.

---

## 🏢 Governance Policies

```bash
# Create governance checker
cat > src/check_governance.py << 'EOF'
from mlflow.tracking import MlflowClient

def check_governance_compliance(model_name, version):
    """Check if model meets governance requirements"""
    client = MlflowClient("http://localhost:5000")
    
    mv = client.get_model_version(model_name, version)
    run = client.get_run(mv.run_id)
    
    issues = []
    
    # 1. Check for required tags
    required_tags = ["approved_by", "dataset_version"]
    for tag in required_tags:
        if not client.get_model_version_tag(model_name, version, tag):
            issues.append(f"Missing required tag: {tag}")
    
    # 2. Check metrics meet thresholds
    accuracy = run.data.metrics.get('accuracy', 0)
    if accuracy < 0.85:
        issues.append(f"Accuracy {accuracy:.3f} below threshold 0.85")
    
    # 3. Check for model card
    artifacts = client.list_artifacts(mv.run_id)
    has_model_card = any("model_card" in a.path for a in artifacts)
    if not has_model_card:
        issues.append("Missing model card documentation")
    
    # 4. Check code is versioned
    git_commit = run.data.tags.get("mlflow.source.git.commit")
    if not git_commit:
        issues.append("Code not versioned (no git commit)")
    
    if issues:
        print(f"Governance check FAILED for {model_name} v{version}:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"Governance check PASSED for {model_name} v{version}")
        return True

# Example
check_governance_compliance("ChurnPredictor", "1")
EOF

python src/check_governance.py
```

**Why**: Automated governance checks enforce policies (documentation, performance, approval).

---

## 🧪 Mini-Lab (10 min)

**Goal**: Register model, transition stages, document with model card.

1. **Register model**:
```bash
mkdir -p ~/mlops-lab-07 && cd ~/mlops-lab-07
# Train a model first (from Module 06)
# Then register it
python register_model.py
```

2. **Transition to Staging**:
```bash
python transition_stage.py
```

3. **Check model in registry**:
```bash
# Open http://localhost:5000
# Navigate to "Models" tab
# See registered model with versions and stages
```

4. **Approve for Production**:
```bash
python approve_for_production.py ChurnPredictor 1 "me@company.com" "Tested successfully"
```

5. **Generate model card**:
```bash
python generate_model_card.py
cat model_card.md
```

**Expected output**: Model in registry with stages, approval tags, and model card.

---

## ❓ Quiz (5 Questions)

1. **What are the MLflow Model Registry stages?**
   - Answer: None, Staging, Production, Archived.

2. **Why use staging before production?**
   - Answer: Test model in pre-prod environment, catch issues before affecting users.

3. **What is model lineage?**
   - Answer: Traceable path from data + code + params → model → deployment.

4. **What should a model card include?**
   - Answer: Purpose, performance metrics, training data, limitations, bias analysis, ethical considerations.

5. **Why automate governance checks?**
   - Answer: Ensure all models meet compliance requirements (metrics, documentation, approval) before production.

---

## ⚠️ Common Mistakes

1. **Skipping staging** → Deploy untested models to production.  
   *Fix*: Always test in staging first.

2. **Not documenting models** → No context for debugging or compliance.  
   *Fix*: Generate model card for every production model.

3. **No approval workflow** → Anyone can deploy anything.  
   *Fix*: Require approval tags before production transition.

4. **Losing lineage** → Can't reproduce or debug models.  
   *Fix*: Tag runs with git commit, data version, config.

5. **Not archiving old models** → Registry cluttered.  
   *Fix*: Archive previous versions when promoting new to production.

---

## 🛠️ Troubleshooting

**Issue**: "Model registration fails"  
→ **Root cause**: MLflow server not running or artifact not found.  
→ **Fix**: Check `mlflow server` is running, verify run_id exists, check artifact path.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Model registration fails"

**Issue**: "Stage transition denied"  
→ **Root cause**: Model doesn't meet governance criteria.  
→ **Fix**: Run governance check, address issues, add required tags/metrics.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Stage transition fails"

---

## 📚 Key Takeaways

- **Model Registry** centralizes versioned models with lifecycle stages
- **Stages** (None, Staging, Production, Archived) control deployment flow
- **Approval workflows** enforce quality gates before production
- **Model lineage** (code + data + params) enables reproducibility
- **Model cards** document purpose, performance, limitations, ethics
- **Governance policies** automate compliance checks

---

## 🚀 Next Steps

- **Module 08**: Serve models via FastAPI, KServe, or BentoML APIs
- **Module 09**: Batch and streaming inference
- **Hands-on**: Register Churn Predictor model and generate model card

---

**[← Module 06](06-model-training-eval-and-selection.md)** | **[Next: Module 08 →](08-serving-and-apis.md)**

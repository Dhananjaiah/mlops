# Lecture 8.6 – Governance Basics: Who Can Promote a Model? How?

## Human Transcript

Alright, let's close out this section on versioning with something that often gets overlooked: governance. Who can do what with your models and data? And how do you enforce it?

This might sound bureaucratic, but it's actually critical. I've seen companies get into serious trouble because anyone could push a model to production without oversight. Model makes biased predictions? Nobody knew who deployed it or when. Model uses data it shouldn't? No record of who approved it.

Governance is about accountability and control. Not bureaucracy for its own sake, but ensuring that your ML systems are safe, compliant, and trustworthy.

Let's break this down into key questions:

Who can train models? In research environments, often anyone with access to the data can train models. But in production environments, you might want to restrict this.

```python
# Example: Role-based training access
TRAINING_ROLES = {
    "data_scientist": ["train_model", "log_experiments"],
    "ml_engineer": ["train_model", "log_experiments", "create_pipelines"],
    "analyst": ["view_experiments"]  # Can't train, just view
}

def check_permission(user, action):
    role = get_user_role(user)
    if action not in TRAINING_ROLES.get(role, []):
        raise PermissionError(f"User {user} ({role}) cannot {action}")
```

Who can register models? Registering a model makes it available for deployment. This is a significant step.

```python
def register_model(user, model_name, run_id):
    # Only ML engineers and above can register
    if get_user_role(user) not in ["ml_engineer", "mlops_engineer", "admin"]:
        raise PermissionError("Not authorized to register models")
    
    # Log the registration for audit
    audit_log({
        "action": "model_registration",
        "user": user,
        "model": model_name,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    })
    
    # Proceed with registration
    mlflow.register_model(f"runs:/{run_id}/model", model_name)
```

Who can promote to staging? Usually the model creator or their team lead.

Who can promote to production? This is the critical one. In many organizations, production promotion requires:

1. Technical review - Does the model meet performance standards?
2. Business review - Does the model align with business requirements?
3. Compliance review - Does the model meet regulatory requirements?

```python
class ModelApprovalWorkflow:
    def __init__(self, model_name, version):
        self.model_name = model_name
        self.version = version
        self.approvals = {}
    
    def request_approval(self, reviewer, approval_type):
        """Send approval request."""
        notification = {
            "model": self.model_name,
            "version": self.version,
            "approval_type": approval_type,
            "requester": get_current_user()
        }
        send_to_reviewer(reviewer, notification)
    
    def approve(self, reviewer, approval_type):
        """Record approval."""
        self.approvals[approval_type] = {
            "reviewer": reviewer,
            "timestamp": datetime.now().isoformat(),
            "status": "approved"
        }
        self._check_complete()
    
    def reject(self, reviewer, approval_type, reason):
        """Record rejection."""
        self.approvals[approval_type] = {
            "reviewer": reviewer,
            "timestamp": datetime.now().isoformat(),
            "status": "rejected",
            "reason": reason
        }
    
    def _check_complete(self):
        """Check if all required approvals are in."""
        required = ["technical", "business", "compliance"]
        
        for approval_type in required:
            if approval_type not in self.approvals:
                return False
            if self.approvals[approval_type]["status"] != "approved":
                return False
        
        # All approved - promote to production
        self._promote_to_production()
        return True
    
    def _promote_to_production(self):
        client = MlflowClient()
        client.transition_model_version_stage(
            name=self.model_name,
            version=self.version,
            stage="Production"
        )
```

Audit trails. Every action should be logged:

```python
import json
from datetime import datetime

def audit_log(event):
    """Log an event for audit purposes."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": get_current_user(),
        "session_id": get_session_id(),
        "ip_address": get_ip_address(),
        **event
    }
    
    # Write to audit log (could be database, file, cloud logging)
    with open("audit.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    # Also send to centralized logging
    send_to_cloudwatch(log_entry)

# Usage throughout your code
audit_log({
    "action": "model_promotion",
    "model": "churn-predictor",
    "from_stage": "Staging",
    "to_stage": "Production",
    "version": 5
})
```

What data can be used? Data governance is equally important. Not all data should be used for training.

```python
DATA_CLASSIFICATION = {
    "public": ["train", "evaluate", "feature_engineering"],
    "internal": ["train", "evaluate"],
    "confidential": ["evaluate"],  # Can evaluate, not train
    "restricted": []  # Cannot use in ML
}

def validate_data_usage(dataset_name, intended_use):
    classification = get_data_classification(dataset_name)
    
    if intended_use not in DATA_CLASSIFICATION.get(classification, []):
        raise PermissionError(
            f"Cannot use {classification} data for {intended_use}"
        )
    
    audit_log({
        "action": "data_access",
        "dataset": dataset_name,
        "classification": classification,
        "use": intended_use
    })
```

Model access control. Not everyone should be able to use every model:

```python
MODEL_ACCESS = {
    "fraud-detector": ["fraud_team", "risk_team", "production_api"],
    "customer-churn": ["marketing_team", "retention_team", "production_api"],
    "internal-testing": ["data_science_team"]
}

def check_model_access(model_name, requester):
    allowed = MODEL_ACCESS.get(model_name, [])
    user_groups = get_user_groups(requester)
    
    if not any(group in allowed for group in user_groups):
        audit_log({
            "action": "unauthorized_model_access",
            "model": model_name,
            "requester": requester
        })
        raise PermissionError(f"Access denied to model {model_name}")
    
    return True
```

Implementing governance in practice. Here's how teams typically implement this:

MLflow with approval webhooks:

```python
# Configure webhook for stage transitions
mlflow.tracking.MlflowClient().create_webhook(
    events=["TRANSITION_REQUEST"],
    http_url_spec={
        "url": "https://your-server.com/model-approval",
        "authorization": "Bearer token"
    }
)

# Your webhook handler
@app.post("/model-approval")
async def handle_transition(request: TransitionRequest):
    if request.to_stage == "Production":
        # Require approval workflow
        workflow = ModelApprovalWorkflow(
            request.model_name,
            request.version
        )
        workflow.request_approval("tech_lead@company.com", "technical")
        workflow.request_approval("product_owner@company.com", "business")
        return {"status": "pending_approval"}
    else:
        # Allow other transitions
        return {"status": "approved"}
```

Four-eyes principle. Many organizations require at least two people to approve production changes:

```python
def check_four_eyes(approvals):
    """Ensure different people approved."""
    approvers = set(a["reviewer"] for a in approvals.values())
    if len(approvers) < 2:
        raise ValueError("Production promotion requires at least 2 different approvers")
```

Time-based restrictions. Prevent production deployments at risky times:

```python
from datetime import datetime, time

def check_deployment_window():
    now = datetime.now()
    
    # No Friday afternoon deployments
    if now.weekday() == 4 and now.hour >= 14:
        raise ValueError("No deployments after 2 PM on Fridays")
    
    # No weekend deployments
    if now.weekday() >= 5:
        raise ValueError("No weekend deployments")
    
    # No deployments during business peak hours
    if time(9, 0) <= now.time() <= time(11, 0):
        raise ValueError("No deployments during peak hours (9-11 AM)")
```

Documentation requirements. Require documentation before production:

```python
def validate_model_documentation(model_name, version):
    """Check that model is properly documented."""
    client = MlflowClient()
    model_version = client.get_model_version(model_name, version)
    
    required_tags = [
        "model_owner",
        "business_purpose",
        "training_data_source",
        "expected_users"
    ]
    
    missing = [tag for tag in required_tags if tag not in model_version.tags]
    
    if missing:
        raise ValueError(f"Missing required documentation: {missing}")
    
    if not model_version.description or len(model_version.description) < 50:
        raise ValueError("Model description must be at least 50 characters")
```

Alright, that's governance basics. The key points: control who can do what, require approvals for production, maintain audit trails, and enforce data access policies.

This wraps up Section 8 on versioning, registries, and governance. You now know how to track your code, data, and models together, manage model lifecycles, handle artifacts, and put controls in place.

In the next section, we'll talk about automated training pipelines and orchestration. How do you make all this happen automatically, reliably, and at scale?

See you there!

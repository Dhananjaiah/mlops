# Lecture 8.4 – Model States: Staging, Production, Archived

## Human Transcript

Alright, let's talk about model lifecycle states. In the last lecture, I mentioned staging, production, and archived. But what do these actually mean and how do you use them in practice?

First, why do we need states at all? Can't we just deploy the latest model?

Short answer: no. Long answer: absolutely not.

Here's why. You train a new model. It looks great in your testing. You deploy it to production immediately. Two hours later, customers are complaining. The model is making bad predictions in edge cases you didn't test for. Now you're scrambling to roll back, but you're not sure what you're rolling back to.

Model states create gates. They force you to pause and validate before moving forward. They create clear points where you can roll back if something goes wrong.

Let me walk you through the typical lifecycle:

None or Development. This is where all models start. You're training, experimenting, iterating. Models at this stage are not ready for any real use.

Staging. The model has passed initial testing and is ready for more serious validation. It might be deployed to a staging environment where it handles real traffic but doesn't affect business decisions. Or it might be tested against production data offline.

Production. The model is live and making real predictions that affect the business. This is the goal state. Only models that have been thoroughly validated should reach here.

Archived. The model was in production but has been replaced. We keep it around for reference and potential rollback, but it's not actively used.

Let's see how this works in practice:

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# A new model starts with no stage
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="fraud-detector"
)
# Stage is "None"

# After initial testing, move to staging
client.transition_model_version_stage(
    name="fraud-detector",
    version=5,
    stage="Staging"
)

# In your staging environment, load this model
staging_model = mlflow.sklearn.load_model("models:/fraud-detector/Staging")

# Run validation tests against staging model
# ...

# After validation passes, promote to production
client.transition_model_version_stage(
    name="fraud-detector",
    version=5,
    stage="Production"
)

# The old production model should be archived
client.transition_model_version_stage(
    name="fraud-detector",
    version=4,
    stage="Archived"
)
```

What happens at each stage? Let me give you a more detailed breakdown:

Staging validation typically includes:

Performance testing. Run the model against a validation dataset. Compare metrics to the current production model. Is it at least as good? Hopefully better.

```python
def validate_for_staging(model, val_data, prod_metrics):
    predictions = model.predict(val_data.X)
    new_metrics = calculate_metrics(val_data.y, predictions)
    
    # Must meet minimum thresholds
    if new_metrics['accuracy'] < 0.85:
        return False, "Accuracy below threshold"
    
    # Should be better than or equal to production
    if new_metrics['f1'] < prod_metrics['f1'] * 0.95:  # Allow 5% margin
        return False, "F1 score regression"
    
    return True, "Validation passed"
```

Latency testing. How fast does the model make predictions? If it's slower than the current production model, you might have problems.

```python
import time

def test_latency(model, test_samples, max_latency_ms=50):
    times = []
    for sample in test_samples:
        start = time.time()
        model.predict([sample])
        end = time.time()
        times.append((end - start) * 1000)
    
    p99 = sorted(times)[int(len(times) * 0.99)]
    return p99 < max_latency_ms, f"P99 latency: {p99:.2f}ms"
```

Memory and resource testing. Does the model fit in the memory of your production servers?

Before promoting to production:

Shadow deployment. Run the staging model alongside production, making predictions on real traffic but not using them. Compare the predictions.

```python
def shadow_deployment_check(staging_predictions, production_predictions):
    # How often do they agree?
    agreement = (staging_predictions == production_predictions).mean()
    
    if agreement < 0.90:
        # They disagree a lot - investigate why
        return False, f"Only {agreement:.1%} agreement with production"
    
    return True, f"Agreement: {agreement:.1%}"
```

Canary deployment. Send a small percentage of real traffic to the new model. Monitor closely.

Manual review. For critical models, require human approval before production promotion.

```python
def request_production_approval(model_name, version, validator_email):
    """Send approval request to model validator."""
    subject = f"Model Approval Required: {model_name} v{version}"
    body = f"""
    Model {model_name} version {version} is ready for production review.
    
    Validation Results:
    - Accuracy: 87.3%
    - F1 Score: 0.85
    - Latency P99: 45ms
    - Shadow agreement: 94%
    
    Please review and approve/reject in the MLflow UI.
    """
    send_email(validator_email, subject, body)
```

Now, let's talk about rollback. This is why we keep archived models. Things go wrong sometimes. You need to be able to revert quickly.

```python
def rollback_to_previous(model_name):
    client = MlflowClient()
    
    # Find current production and most recent archived
    current_prod = client.get_latest_versions(model_name, stages=["Production"])[0]
    archived = client.search_model_versions(
        f"name='{model_name}'",
        order_by=["version DESC"]
    )
    previous_prod = [v for v in archived if v.current_stage == "Archived"][0]
    
    # Swap them
    client.transition_model_version_stage(
        name=model_name,
        version=current_prod.version,
        stage="Archived"
    )
    client.transition_model_version_stage(
        name=model_name,
        version=previous_prod.version,
        stage="Production"
    )
    
    print(f"Rolled back from v{current_prod.version} to v{previous_prod.version}")
```

Some organizations have more states. Here's an example with additional stages:

Development → Testing → Staging → Canary → Production → Deprecated → Archived

Testing is automated testing in a test environment.
Canary is serving a small percentage of production traffic.
Deprecated is a model that's being phased out but still serving some traffic.

You can implement custom stages with MLflow using tags:

```python
# MLflow only has None, Staging, Production, Archived
# But you can add custom states via tags

def set_custom_stage(model_name, version, custom_stage):
    client = MlflowClient()
    client.set_model_version_tag(
        name=model_name,
        version=version,
        key="custom_stage",
        value=custom_stage  # "canary", "deprecated", etc.
    )

def get_models_in_custom_stage(model_name, custom_stage):
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{model_name}'")
    return [v for v in versions if v.tags.get("custom_stage") == custom_stage]
```

Finally, who can promote models? This is a governance question. In small teams, anyone might be able to promote. In larger organizations, you want controls:

```python
# Example: Check if user is authorized
def promote_to_production(model_name, version, user_id):
    authorized_users = get_authorized_promoters(model_name)
    
    if user_id not in authorized_users:
        raise PermissionError(f"User {user_id} not authorized to promote {model_name}")
    
    # Also require recent validation
    validation_record = get_validation_record(model_name, version)
    if not validation_record or validation_record['status'] != 'passed':
        raise ValueError(f"Model v{version} has not passed validation")
    
    # Proceed with promotion
    client.transition_model_version_stage(...)
```

Alright, that's model states. The key points: use states as gates to ensure quality, always test before promoting, have a rollback plan, and control who can promote to production.

Next, we'll talk about storing and retrieving artifacts in your ML pipelines.

Questions? Let's keep moving.

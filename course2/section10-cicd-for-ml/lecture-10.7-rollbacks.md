# Lecture 10.7 – Rollbacks: When a New Model Fails

## Human Transcript

Things will go wrong. A model that looked great in testing fails in production. You need to roll back fast.

Automated rollback triggers:

```python
def check_rollback_conditions(metrics, thresholds):
    triggers = []
    
    if metrics['error_rate'] > thresholds['critical_error_rate']:
        triggers.append('error_rate_critical')
    
    if metrics['latency_p99'] > thresholds['critical_latency']:
        triggers.append('latency_critical')
    
    if metrics['accuracy'] < thresholds['min_accuracy']:
        triggers.append('accuracy_degradation')
    
    return len(triggers) > 0, triggers

# In monitoring loop
should_rollback, reasons = check_rollback_conditions(current_metrics, thresholds)
if should_rollback:
    logger.critical(f"Rollback triggered: {reasons}")
    execute_rollback()
    send_alert(f"Model rolled back due to: {reasons}")
```

Kubernetes rollback:

```bash
# Automatic rollback
kubectl rollout undo deployment/churn-model

# Rollback to specific revision
kubectl rollout undo deployment/churn-model --to-revision=2
```

Model registry rollback:

```python
def rollback_model(model_name):
    client = MlflowClient()
    
    # Get current production
    current = client.get_latest_versions(model_name, stages=["Production"])[0]
    
    # Get previous production (now archived)
    archived = client.search_model_versions(f"name='{model_name}'")
    previous = [v for v in archived if v.current_stage == "Archived"][0]
    
    # Swap stages
    client.transition_model_version_stage(model_name, current.version, "Archived")
    client.transition_model_version_stage(model_name, previous.version, "Production")
    
    return previous.version
```

Key practices:
1. Always keep the previous version ready
2. Monitor aggressively in the first hour after deployment
3. Have automated rollback triggers
4. Practice rollbacks regularly
5. Document every rollback and its cause

Rollbacks should be boring and automatic. If they're stressful, your process needs improvement.

This wraps up Section 10 on CI/CD for ML. You now know how to test, build, deploy, and roll back ML systems safely.

# Lecture 10.5 – Continuous Delivery of Models & APIs (Staging → Prod)

## Human Transcript

Now let's talk about getting your models from staging to production safely. This is continuous delivery for ML.

The key principle: never deploy directly to production. Always go through staging first.

Here's a typical deployment flow:

```yaml
name: Deploy Model

on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Model version to deploy'
        required: true
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy-staging:
    if: inputs.environment == 'staging'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/churn-model \
            churn-model=$REGISTRY/churn-model:${{ inputs.model_version }} \
            --namespace staging

      - name: Run smoke tests
        run: |
          sleep 30
          curl -f https://staging-api.example.com/health
          python tests/smoke/test_staging.py

  deploy-production:
    if: inputs.environment == 'production'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Require approval
        uses: trstringer/manual-approval@v1
        with:
          approvers: ml-team
          
      - name: Deploy to production
        run: |
          kubectl set image deployment/churn-model \
            churn-model=$REGISTRY/churn-model:${{ inputs.model_version }} \
            --namespace production
```

Automated promotion based on metrics:

```python
def should_promote_to_production(staging_metrics, thresholds):
    checks = {
        'accuracy': staging_metrics['accuracy'] >= thresholds['min_accuracy'],
        'latency_p99': staging_metrics['latency_p99'] <= thresholds['max_latency'],
        'error_rate': staging_metrics['error_rate'] <= thresholds['max_error_rate'],
        'uptime': staging_metrics['uptime'] >= thresholds['min_uptime']
    }
    
    all_passed = all(checks.values())
    return all_passed, checks
```

The staging environment should mirror production as closely as possible. Same infrastructure, same data patterns, just with test traffic.

Key practices:
1. Deploy to staging automatically after tests pass
2. Run integration tests against staging
3. Monitor staging for a period (hours to days)
4. Require approval for production deployment
5. Have automated rollback triggers

This ensures your models work in a production-like environment before they touch real users.

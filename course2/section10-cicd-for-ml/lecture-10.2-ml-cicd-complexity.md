# Lecture 10.2 – Extra Complexity in ML CI/CD (Data, Drift, Longer Runs)

## Human Transcript

Now that we've covered the basics of CI/CD, let's talk about why ML systems are harder. Because they are. ML CI/CD has challenges that traditional software doesn't have.

Let me walk you through the main differences.

Code plus data plus model. In traditional software, you test code. Input data is usually small, synthetic, and controlled. But in ML:
- Your code depends on data
- The behavior depends on what data was used for training
- The output (model) is itself an artifact that needs to be tested

```
Traditional CI/CD:
  Code → Test → Deploy Binary

ML CI/CD:
  Code → Test Code → Validate Data → Train Model → Test Model → Deploy Model
```

Data is a first-class citizen. In ML, bad data means bad models. You need to validate data as part of CI/CD:

```python
# Data validation in CI/CD
def validate_training_data(data_path):
    df = pd.read_parquet(data_path)
    
    # Schema validation
    expected_columns = ['feature1', 'feature2', 'target']
    assert set(expected_columns).issubset(df.columns), "Missing columns"
    
    # Type validation
    assert df['feature1'].dtype == 'float64'
    assert df['target'].dtype == 'int64'
    
    # Statistical validation
    assert df['feature1'].mean() > 0, "Unexpected feature1 mean"
    assert df['target'].value_counts(normalize=True).min() > 0.1, "Class imbalance too severe"
    
    # Freshness validation
    assert df['timestamp'].max() > datetime.now() - timedelta(days=7), "Data is stale"
```

Model behavior changes. In traditional software, if you don't change the code, the behavior doesn't change. In ML:
- Same code + different data = different model
- Same code + same data + different random seed = different model
- Same model + different input distribution = different behavior

This means you need to test not just "does it run" but "does it behave correctly":

```python
# Model behavior tests
def test_model_behavior(model, test_data):
    predictions = model.predict(test_data.X)
    
    # Accuracy shouldn't drop below threshold
    accuracy = accuracy_score(test_data.y, predictions)
    assert accuracy > 0.80, f"Accuracy too low: {accuracy}"
    
    # Predictions should be in expected range
    assert set(predictions).issubset({0, 1}), "Unexpected prediction values"
    
    # Model should not be biased
    for group in ['male', 'female']:
        group_data = test_data[test_data['gender'] == group]
        group_acc = accuracy_score(group_data.y, model.predict(group_data.X))
        assert abs(group_acc - accuracy) < 0.05, f"Bias detected for {group}"
```

Longer running tests. Unit tests for regular code run in milliseconds. But ML tests might involve:
- Loading large datasets: seconds to minutes
- Training models: minutes to hours
- Running inference on test sets: seconds to minutes

This means you can't run everything on every commit:

```yaml
# GitHub Actions: Fast tests on every PR
on:
  pull_request:

jobs:
  fast-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run unit tests
        run: pytest tests/unit -v
      
      - name: Run fast integration tests
        run: pytest tests/integration -v -m "not slow"
```

```yaml
# Slower tests run nightly or on main
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily

jobs:
  full-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run all tests including slow ones
        run: pytest tests/ -v
      
      - name: Run model training tests
        run: pytest tests/model -v --training
```

Data drift. What worked yesterday might not work tomorrow. The world changes. Customer behavior changes. CI/CD needs to account for this:

```python
# Check for data drift before training
def check_data_drift(current_data, reference_data):
    from scipy import stats
    
    drift_detected = False
    
    for column in current_data.columns:
        if current_data[column].dtype in ['float64', 'int64']:
            # KS test for numerical columns
            statistic, p_value = stats.ks_2samp(
                reference_data[column],
                current_data[column]
            )
            if p_value < 0.05:
                print(f"Drift detected in {column}: p={p_value}")
                drift_detected = True
    
    return drift_detected
```

Expensive resources. Training ML models often requires GPUs, lots of memory, or specialized hardware. CI/CD needs to manage these:

```yaml
# Use GPU runners only when needed
jobs:
  unit-tests:
    runs-on: ubuntu-latest  # Regular runner
    steps:
      - run: pytest tests/unit
  
  training-tests:
    runs-on: [self-hosted, gpu]  # GPU runner
    steps:
      - run: pytest tests/training --gpu
```

Non-determinism. ML has inherent randomness. Same code can produce different results:

```python
# Make tests deterministic
import numpy as np
import random
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

# In tests
def test_model_training():
    set_seed(42)
    model = train_model(data)
    
    # With fixed seed, we can check exact values
    assert model.score(X_test, y_test) == pytest.approx(0.85, rel=0.01)
```

Model versioning. Unlike regular binaries, models need careful versioning:

```yaml
# CI/CD for model artifacts
steps:
  - name: Train model
    run: python train.py
  
  - name: Version model
    run: |
      MODEL_VERSION="${{ github.sha }}-$(date +%Y%m%d)"
      echo "MODEL_VERSION=$MODEL_VERSION" >> $GITHUB_ENV
  
  - name: Upload model artifact
    uses: actions/upload-artifact@v3
    with:
      name: model-${{ env.MODEL_VERSION }}
      path: models/
```

Quality gates specific to ML. Beyond code coverage, you need model quality gates:

```python
# Quality gates for models
def model_quality_gate(metrics, thresholds):
    gates = {
        'accuracy': metrics['accuracy'] >= thresholds['min_accuracy'],
        'latency': metrics['p99_latency'] <= thresholds['max_latency'],
        'bias': metrics['max_group_disparity'] <= thresholds['max_bias'],
        'model_size': metrics['model_size_mb'] <= thresholds['max_size'],
    }
    
    failed_gates = [k for k, v in gates.items() if not v]
    
    if failed_gates:
        raise QualityGateError(f"Failed gates: {failed_gates}")
    
    return True
```

A/B testing integration. New models often need A/B testing before full rollout:

```yaml
# Deploy to A/B test instead of direct production
steps:
  - name: Deploy to A/B test
    run: |
      # Deploy as variant B, 10% traffic
      kubectl apply -f k8s/canary-deployment.yaml
      
  - name: Wait for A/B results
    run: |
      # Check metrics after 2 hours
      sleep 7200
      python scripts/check_ab_results.py
```

These extra complexities mean ML CI/CD takes more thought and more infrastructure than traditional CI/CD. But the principles are the same: automate everything, fail fast, and keep production safe.

In the next lecture, we'll look at how to write tests specifically for ML code.

Questions so far?

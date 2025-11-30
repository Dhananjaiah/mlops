# Lecture 6.6 – How MLOps Enforces Reproducibility in a Team

---

## Team Challenges

Individual reproducibility is hard. Team reproducibility is harder.

"My model works on my machine."
"What environment are you using?"
"Uh... I don't remember."

MLOps's job: Make reproducibility automatic and mandatory.

---

## Enforcement Strategies

### 1. Central Tracking Server

Everyone logs to the same place:

```python
# Set in team's base config
MLFLOW_TRACKING_URI = "http://mlflow.company.com"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
```

### 2. Required Tags

Block runs without required information:

```python
REQUIRED_TAGS = ['git_commit', 'data_version', 'author']

def validate_run():
    tags = mlflow.active_run().data.tags
    missing = [t for t in REQUIRED_TAGS if t not in tags]
    if missing:
        raise ValueError(f"Missing required tags: {missing}")
```

### 3. CI/CD Validation

Check reproducibility in CI:

```yaml
# .github/workflows/ml-validation.yml
- name: Check MLflow logging
  run: |
    python -c "
    import mlflow
    run = mlflow.get_run('${{ env.RUN_ID }}')
    assert 'git_commit' in run.data.tags
    assert 'data_version' in run.data.params
    "
```

### 4. Containerized Training

Force identical environments:

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
COPY configs/ configs/
ENTRYPOINT ["python", "scripts/train.py"]
```

```bash
# Everyone runs in same container
docker run train-container --config configs/experiment.yaml
```

---

## Team Standards

### Standard Experiment Template

```python
# templates/experiment.py
import mlflow
from src.reproducibility import log_reproducibility_info, validate_required_tags

def run_experiment(config):
    mlflow.set_experiment(config['experiment_name'])
    
    with mlflow.start_run():
        # Automatic reproducibility logging
        log_reproducibility_info()
        
        # Your experiment code
        train_and_evaluate(config)
        
        # Validate before closing
        validate_required_tags()
```

### Code Review Checklist

- [ ] MLflow logging for all parameters
- [ ] Data version tracked
- [ ] Random seed set
- [ ] Config file committed
- [ ] Requirements.txt updated

---

## Section 6 Complete! 🎉

You now understand:
- Why notebooks fail in production
- How to structure experiments
- Experiment tracking concepts
- Using MLflow
- Achieving reproducibility
- Team reproducibility practices

---

**Next Section**: [Section 7 – Model Packaging: From Script to Service](../section07-model-packaging/lecture-7.1-python-package.md)

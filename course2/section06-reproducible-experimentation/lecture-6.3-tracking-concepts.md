# Lecture 6.3 – Experiment Tracking Concepts (Runs, Params, Metrics, Artifacts)

---

## Why Track Experiments?

A data scientist runs 50 experiments. A week later:

"Which experiment had the best recall?"
"What parameters did I use for that one good run?"
"What data version was that?"

Without tracking, these questions are hard to answer. With tracking, they're trivial.

---

## Core Concepts

### Run

A **run** is a single execution of your training script.

Each run has:
- Unique ID
- Start/end time
- Parameters used
- Metrics achieved
- Artifacts produced

### Parameters

**Parameters** are the inputs to your experiment:

- Model hyperparameters (n_estimators, learning_rate)
- Data parameters (test_size, random_state)
- Feature settings (which features used)
- Configuration values

### Metrics

**Metrics** are the outputs you measure:

- Performance metrics (accuracy, precision, recall, AUC)
- Training metrics (loss, training time)
- Custom metrics (business metrics)

### Artifacts

**Artifacts** are files produced by the run:

- Model files (model.pkl, model.h5)
- Plots (confusion_matrix.png)
- Data samples
- Configuration files

---

## Example: Tracking a Run

```python
# Without tracking
model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X_train, y_train)
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy}")  # Lost to console

# With tracking
import mlflow

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Log metrics
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    
    # Log artifacts
    mlflow.sklearn.log_model(model, "model")
    
# Now all of this is recorded and searchable!
```

---

## Organizing Experiments

### Experiments

Group related runs into **experiments**:

```
MLflow Structure:
├── Experiment: churn-prediction-v1
│   ├── Run: baseline_rf
│   ├── Run: deeper_trees
│   └── Run: more_features
│
├── Experiment: churn-prediction-v2
│   ├── Run: xgboost_baseline
│   └── Run: xgboost_tuned
```

### Tags

Add **tags** for additional organization:

```python
mlflow.set_tag("model_type", "random_forest")
mlflow.set_tag("author", "alice")
mlflow.set_tag("purpose", "baseline")
```

---

## What to Track

### Always Track

| Category | Examples |
|----------|----------|
| Model params | n_estimators, learning_rate, max_depth |
| Data info | Data path, data version, row count |
| Training config | CV folds, random seed |
| Primary metrics | Accuracy, AUC, F1 |
| Environment | Python version, package versions |

### Nice to Track

| Category | Examples |
|----------|----------|
| Feature list | Which features used |
| Training time | How long it took |
| Resource usage | CPU, memory |
| Secondary metrics | Per-class metrics |
| Plots | Confusion matrix, ROC curve |

### Track with Model

| Artifact | Purpose |
|----------|---------|
| Model file | The trained model |
| Preprocessors | Scalers, encoders |
| Config file | Full configuration |
| Requirements | Dependencies |

---

## Comparing Experiments

The real power: comparing runs.

```
┌────────────────────────────────────────────────────────────────────┐
│                    Experiment Comparison                            │
├──────────┬───────────────┬───────────┬──────────┬─────────────────┤
│ Run      │ n_estimators  │ max_depth │ Accuracy │ AUC             │
├──────────┼───────────────┼───────────┼──────────┼─────────────────┤
│ baseline │ 100           │ 10        │ 0.82     │ 0.87            │
│ deep     │ 100           │ 20        │ 0.83     │ 0.88            │
│ wide     │ 200           │ 10        │ 0.84     │ 0.89 ← Best!    │
│ both     │ 200           │ 20        │ 0.83     │ 0.88            │
└──────────┴───────────────┴───────────┴──────────┴─────────────────┘
```

Questions you can answer:
- Which run had the best AUC?
- How does max_depth affect accuracy?
- What's the difference between run A and run B?

---

## Reproducibility

With tracking, you can reproduce any run:

```python
# Get run details
run = mlflow.get_run(run_id="abc123")

# Get parameters
params = run.data.params
# {'n_estimators': '100', 'max_depth': '10', ...}

# Get metrics
metrics = run.data.metrics
# {'accuracy': 0.82, 'auc': 0.87}

# Load model
model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
```

---

## Recap

Experiment tracking captures:
- **Runs**: Individual executions
- **Parameters**: Inputs to the experiment
- **Metrics**: Measured outcomes
- **Artifacts**: Produced files

Benefits:
- Compare experiments easily
- Reproduce any run
- Know what produced what
- Collaborate effectively

---

## What's Next

Let's implement this with MLflow.

---

**Next Lecture**: [6.4 – Using MLflow (or Similar) to Track Experiments](lecture-6.4-mlflow-tracking.md)

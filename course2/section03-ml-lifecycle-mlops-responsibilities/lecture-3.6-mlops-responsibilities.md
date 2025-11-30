# Lecture 3.6 – MLOps Responsibilities in Each Lifecycle Stage

---

## Where Do You Fit?

We've covered the ML lifecycle. We've talked about roles. Now let's be very specific:

**What is MLOps responsible for at each stage?**

This clarity will help you know:
- What to focus on
- Who to work with
- What to deliver

---

## Overview

Here's the summary view:

| Stage | MLOps Involvement | Primary Responsibility |
|-------|-------------------|----------------------|
| Business Understanding | Low | Attend meetings, understand requirements |
| Data Understanding | Medium | Data access, infrastructure setup |
| Data Preparation | High | Pipelines, versioning, quality checks |
| Modeling | Medium | Experiment tracking, compute resources |
| Evaluation | Medium | Validation pipelines, approval workflows |
| Deployment | Very High | CI/CD, serving, monitoring, everything |

Let's dive into each.

---

## Stage 1: Business Understanding

### What Happens
Stakeholders define the problem and success criteria.

### MLOps Role: Observer/Advisor

**What you do**:
- Attend kickoff meetings
- Understand the requirements
- Ask about operational constraints
- Raise feasibility concerns early

**Questions to ask**:
- "How often do you need predictions?"
- "What latency is acceptable?"
- "How will you use the predictions?"
- "What happens if the model is wrong?"

**Deliverables**: None directly, but take notes on operational requirements.

**Interaction**: Mostly listen. Speak up about infrastructure constraints.

---

## Stage 2: Data Understanding

### What Happens
Data scientists explore available data and assess quality.

### MLOps Role: Infrastructure Provider

**What you do**:
- Set up data access (credentials, permissions)
- Provide exploration environments (notebooks, compute)
- Help identify data sources
- Start thinking about data pipelines

**Deliverables**:
- Access to data sources
- Development environment setup
- Initial data documentation

**Questions to ask**:
- "Where does this data come from?"
- "How often is it updated?"
- "Are there any access restrictions?"
- "What's the data volume?"

**Interaction**: Work with Data Engineering to provide access. Support Data Science exploration.

---

## Stage 3: Data Preparation

### What Happens
Data is cleaned, transformed, and features are engineered.

### MLOps Role: Pipeline Builder (HIGH)

**What you do**:
- Build automated data pipelines
- Set up data versioning (DVC)
- Implement data validation checks
- Create feature engineering pipelines
- Establish data contracts with upstream

**Deliverables**:
- Automated data pipelines (Airflow, etc.)
- Data versioning setup
- Data quality checks
- Feature store (if applicable)
- Documentation of data schemas

**Key activities**:
```python
# Example: Data validation with Great Expectations
import great_expectations as ge

df = ge.read_csv("data/processed/customers.csv")
df.expect_column_values_to_not_be_null("customer_id")
df.expect_column_values_to_be_between("age", 18, 120)
df.expect_column_values_to_be_in_set("country", ["US", "CA", "UK", "DE"])
```

**Interaction**: Close collaboration with Data Engineering. Define data contracts together.

---

## Stage 4: Modeling

### What Happens
Data scientists build and tune models.

### MLOps Role: Platform Provider (MEDIUM)

**What you do**:
- Provide experiment tracking (MLflow)
- Manage compute resources for training
- Set up GPU access if needed
- Ensure reproducibility standards
- Monitor experiment storage costs

**Deliverables**:
- MLflow (or similar) setup and running
- Training compute available
- Guidelines for logging experiments
- Templates for reproducible training

**Key activities**:
```python
# Example: MLflow tracking setup for data scientists
import mlflow

mlflow.set_tracking_uri("http://mlflow.company.com")
mlflow.set_experiment("churn-prediction")

with mlflow.start_run():
    mlflow.log_params({"n_estimators": 100, "max_depth": 10})
    model.fit(X_train, y_train)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
```

**Interaction**: Support Data Scientists. Ensure they can focus on modeling, not infrastructure.

---

## Stage 5: Evaluation

### What Happens
Model is validated against business requirements.

### MLOps Role: Process Manager (MEDIUM)

**What you do**:
- Build automated evaluation pipelines
- Implement validation gates
- Set up approval workflows
- Generate model documentation
- Prepare for deployment

**Deliverables**:
- Automated evaluation pipeline
- Model validation checks
- Model cards / documentation
- Approval workflow (if required)

**Key activities**:
```python
# Example: Automated evaluation pipeline
def evaluate_model(model, X_test, y_test, thresholds):
    """Evaluate model against required thresholds."""
    predictions = model.predict(X_test)
    
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
    }
    
    # Check against thresholds
    passed = all(
        metrics[m] >= thresholds[m] 
        for m in thresholds
    )
    
    return {"metrics": metrics, "passed": passed}
```

**Interaction**: Work with Data Scientists on evaluation criteria. Work with stakeholders on approval process.

---

## Stage 6: Deployment

### What Happens
Model goes to production.

### MLOps Role: Owner (VERY HIGH)

This is where MLOps shines. You own this stage.

**What you do**:
- Package models for deployment
- Build CI/CD pipelines
- Set up serving infrastructure
- Implement monitoring
- Configure alerting
- Plan rollback procedures
- Document everything

**Deliverables**:
- Deployed model (API or batch)
- CI/CD pipeline
- Monitoring dashboard
- Alerting rules
- Runbook for incidents
- Deployment documentation

**Key activities**:

```yaml
# Example: GitHub Actions CI/CD
name: Deploy Model
on:
  push:
    branches: [main]
    
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build and push Docker image
        run: |
          docker build -t model-api:${{ github.sha }} .
          docker push registry.com/model-api:${{ github.sha }}
          
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/model-api model=registry.com/model-api:${{ github.sha }}
```

**Interaction**: Own this. Coordinate with DevOps for infrastructure. Communicate with stakeholders on availability.

---

## Stage 7: Operations (Ongoing)

### What Happens
Model runs in production. Things happen.

### MLOps Role: Operator (VERY HIGH)

**What you do**:
- Monitor model performance
- Detect and alert on drift
- Trigger retraining when needed
- Handle incidents
- Plan capacity
- Manage costs
- Iterate and improve

**Deliverables**:
- Operational dashboards
- Incident reports
- Retraining schedules
- Cost reports
- Improvement roadmap

**Key activities**:
```python
# Example: Drift detection
from evidently import ColumnDriftMetric
from evidently.report import Report

report = Report(metrics=[
    ColumnDriftMetric(column_name="feature1"),
    ColumnDriftMetric(column_name="feature2"),
])

report.run(reference_data=training_data, current_data=production_data)

if report.as_dict()["metrics"][0]["result"]["drift_detected"]:
    send_alert("Data drift detected in feature1!")
```

**Interaction**: On-call for ML systems. Report to stakeholders on model health. Work with Data Scientists on retraining.

---

## The RACI Matrix

Let's create a RACI (Responsible, Accountable, Consulted, Informed) matrix:

| Activity | Data Eng | Data Sci | MLOps | DevOps | Product |
|----------|:--------:|:--------:|:-----:|:------:|:-------:|
| Define requirements | C | C | C | I | A/R |
| Explore data | I | A/R | C | I | I |
| Build data pipelines | A/R | C | R | C | I |
| Version data | C | C | A/R | I | I |
| Build models | I | A/R | C | I | I |
| Track experiments | I | R | A/R | I | I |
| Evaluate models | I | A/R | R | I | C |
| Package models | I | C | A/R | C | I |
| Deploy models | I | I | A/R | C | I |
| Monitor models | I | C | A/R | C | I |
| Handle incidents | I | C | A/R | R | I |
| Retrain models | I | R | A/R | I | I |

**Legend**:
- A = Accountable (ultimate owner)
- R = Responsible (does the work)
- C = Consulted (input needed)
- I = Informed (kept in loop)

---

## What MLOps Owns vs Supports

### MLOps Owns

✓ Experiment tracking infrastructure
✓ Data versioning setup
✓ Model registry
✓ CI/CD for ML
✓ Model deployment
✓ Model monitoring
✓ Alerting and incident response
✓ Retraining pipelines

### MLOps Supports

⊕ Data pipeline development (with Data Eng)
⊕ Model evaluation (with Data Sci)
⊕ Infrastructure provisioning (with DevOps)
⊕ Requirements gathering (with Product)

### MLOps Does Not Own

✗ Business requirements
✗ Model architecture decisions
✗ Feature engineering logic
✗ Raw data infrastructure
✗ Product features

---

## Recap

MLOps responsibilities by stage:

1. **Business Understanding**: Low—understand requirements
2. **Data Understanding**: Medium—provide infrastructure
3. **Data Preparation**: High—pipelines, versioning, validation
4. **Modeling**: Medium—experiment tracking, compute
5. **Evaluation**: Medium—validation pipelines, approvals
6. **Deployment**: Very High—CI/CD, serving, monitoring (THIS IS YOUR STAGE)
7. **Operations**: Very High—monitoring, drift, retraining, incidents

MLOps owns the path from trained model to production and keeping it healthy.

---

## Section 3 Complete! 🎉

You now understand:
- How to frame ML problems correctly
- The ML lifecycle (CRISP-DM)
- Where things break in real life
- MLOps vs DevOps
- Online vs Batch systems
- MLOps responsibilities at each stage

---

**Next Section**: [Section 4 – Course Project Overview: Real-World Use Case](../section04-project-overview-use-case/lecture-4.1-defining-use-case.md)

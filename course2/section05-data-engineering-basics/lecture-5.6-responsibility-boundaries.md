# Lecture 5.6 – Where Data Engineer Ends and MLOps Starts (Responsibility Boundaries)

---

## The Handoff Problem

In companies, responsibilities overlap and sometimes conflict.

Data Engineer: "That's MLOps's job."
MLOps: "No, that's Data Engineering's job."
Result: Nobody does it.

Let's clarify boundaries.

---

## The Data to Model Journey

```
Raw Data → Clean Data → Features → Training → Model → Serving → Monitoring
│                              │                              │
└───── Data Engineering ───────┴────────── MLOps ─────────────┘
                               │
                        OVERLAP ZONE
```

---

## Data Engineering Responsibilities

### Core Responsibilities

| Area | Description |
|------|-------------|
| Data Collection | Get data from sources into storage |
| Data Pipelines | Build and maintain ETL/ELT |
| Data Infrastructure | Manage data warehouses, lakes |
| Data Quality | Ensure data meets quality standards |
| Data Catalog | Document data assets |

### Typical Tasks

```
✓ Build pipeline to ingest customer data
✓ Set up data warehouse tables
✓ Implement data quality checks on sources
✓ Create data documentation
✓ Optimize query performance
✓ Manage data access controls
✓ Handle schema migrations
```

### Tools They Own

- Airflow (for data pipelines)
- dbt (transformations)
- Spark (large-scale processing)
- Data warehouse (Snowflake, BigQuery)
- Data catalog (DataHub, Amundsen)

---

## MLOps Responsibilities

### Core Responsibilities

| Area | Description |
|------|-------------|
| ML Pipelines | Training, validation, deployment |
| Model Management | Registry, versioning, lifecycle |
| Model Serving | Deploy and serve predictions |
| Model Monitoring | Track performance, drift |
| ML Infrastructure | Training compute, serving infra |

### Typical Tasks

```
✓ Build training pipeline
✓ Set up experiment tracking (MLflow)
✓ Configure model registry
✓ Deploy model to production
✓ Set up model monitoring
✓ Implement retraining triggers
✓ Manage model rollbacks
```

### Tools They Own

- MLflow (experiment tracking, registry)
- Training infrastructure
- Model serving (FastAPI, KFServing)
- Model monitoring (Evidently)
- ML-specific CI/CD

---

## The Overlap Zone

Some areas are genuinely shared. Here's how to divide them:

### Feature Engineering

**Data Engineering view**: "Features are just transformations on data. We do transformations."

**MLOps view**: "Features are model inputs. We need to manage them for ML."

**Resolution**:

| Task | Owner | Rationale |
|------|-------|-----------|
| Base aggregations (daily totals) | Data Eng | Standard data transformations |
| ML-specific features | MLOps/DS | Requires ML knowledge |
| Feature store infrastructure | MLOps | ML-specific system |
| Feature computation at scale | Data Eng | Spark expertise |
| Feature versioning | MLOps | Tied to model versions |

### Data Validation

**Shared responsibility**:

| Task | Owner |
|------|-------|
| Source data quality | Data Eng |
| Schema enforcement | Data Eng |
| Feature quality | MLOps |
| Training data validation | MLOps |
| Data drift detection | MLOps |

### Pipeline Orchestration

**If company has ONE orchestrator (e.g., Airflow)**:

| Task | Owner |
|------|-------|
| Airflow infrastructure | Data Eng or Platform |
| Data pipeline DAGs | Data Eng |
| Training pipeline DAGs | MLOps |
| Scheduling coordination | Both (communication!) |

---

## The Contract

The key to clarity: **Data Contracts**.

Data Engineering delivers data, MLOps consumes it. The contract defines:

```yaml
# contract: customer_features_for_ml

producer: data-engineering
consumer: mlops-team

interface:
  table: features.customer_features
  update_frequency: daily by 6 AM UTC
  
schema:
  customer_id: string (not null)
  days_as_customer: int
  events_per_day: float
  # ... etc

quality:
  freshness: < 24 hours
  completeness: > 99%
  
sla:
  availability: 99.9%
  
change_process:
  notification: 2 weeks advance
  approval: mlops-team sign-off
```

With a contract, both teams know:
- What Data Eng delivers
- What MLOps expects
- Who's responsible for what

---

## Collaboration Patterns

### Pattern 1: Clear Handoff

```
Data Engineering            MLOps
     │                        │
     │  [Feature Table]       │
     └────────►───────────────┘
               Handoff point
```

Data Eng builds feature table. MLOps consumes it.

**Pros**: Clear ownership
**Cons**: May be slow to iterate

### Pattern 2: Embedded Collaboration

```
        Cross-Functional Team
┌─────────────────────────────────────┐
│  Data Eng  │  Data Sci  │  MLOps   │
│            │            │          │
│     └──────┴────────────┴──────┘   │
│         Work together daily         │
└─────────────────────────────────────┘
```

Same team handles data through to deployment.

**Pros**: Fast iteration, shared context
**Cons**: May miss enterprise data standards

### Pattern 3: Platform Model

```
        Data Platform Team                ML Platform Team
              │                                  │
              │  Provides infrastructure         │  Provides infrastructure
              │                                  │
              ▼                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Product/Feature Teams                     │
│              Use both platforms to build products            │
└─────────────────────────────────────────────────────────────┘
```

Central platforms, decentralized product teams.

**Pros**: Scalable, standardized
**Cons**: Coordination overhead

---

## Common Friction Points

### "The Data Is Late"

MLOps needs data by 6 AM for training. Data pipeline finishes at 8 AM.

**Solution**: SLA in data contract. Alert if breached. Plan buffer time.

### "The Schema Changed"

Data Eng added a column. MLOps pipeline broke.

**Solution**: Schema versioning. Change notification process. Automated schema validation.

### "Feature Doesn't Exist"

MLOps needs `events_per_day`. Data Eng never heard of it.

**Solution**: Feature request process. Feature store (if mature). Clear ownership.

### "Data Quality Dropped"

Null rate went from 1% to 20%. MLOps found out when model degraded.

**Solution**: Data quality monitoring. Alerts. Data contracts with quality thresholds.

---

## Practical Guidelines

### What MLOps Should NOT Do

❌ Build core data pipelines (that's Data Eng)
❌ Manage data warehouse infrastructure
❌ Fix source data quality issues
❌ Own the data catalog

### What Data Engineering Should NOT Do

❌ Build model training pipelines
❌ Deploy ML models
❌ Monitor model performance
❌ Manage experiment tracking

### What Both Should Do

✓ Communicate regularly
✓ Maintain data contracts
✓ Alert each other on issues
✓ Collaborate on feature engineering
✓ Share on-call responsibilities (for shared systems)

---

## For Our Churn Project

Here's our division:

| Component | Owner | Notes |
|-----------|-------|-------|
| Source data pipelines | Data Eng | Ingest from DBs, APIs |
| Data warehouse tables | Data Eng | raw.*, staging.* |
| Feature table | Shared | Data Eng computes, MLOps defines |
| Training pipeline | MLOps | From features to model |
| Experiment tracking | MLOps | MLflow |
| Model serving | MLOps | FastAPI, batch scoring |
| Model monitoring | MLOps | Drift detection |
| Data quality (source) | Data Eng | Great Expectations on sources |
| Data quality (features) | MLOps | Validation in training pipeline |

---

## Section 5 Complete! 🎉

You now understand:
- Data types and storage options
- Data ingestion patterns
- Data quality and validation
- Feature engineering basics
- Feature stores
- Responsibility boundaries

You have the data engineering foundation for MLOps.

---

**Next Section**: [Section 6 – Reproducible Experimentation: From Notebook to Pipeline](../section06-reproducible-experimentation/lecture-6.1-notebook-problems.md)

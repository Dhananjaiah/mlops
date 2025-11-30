# Lecture 4.4 – High-Level Architecture for Our Project (Big Diagram)

---

## The Complete Picture

Let's put together everything we've discussed into one cohesive architecture.

This is the system we'll build throughout this course. By the end, you'll understand every component and how they connect.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CHURN PREDICTION SYSTEM - ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          DATA SOURCES                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Customer │  │  Usage   │  │ Support  │  │ Billing  │            │   │
│  │  │    DB    │  │   Logs   │  │ Tickets  │  │   API    │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  │       │             │             │             │                   │   │
│  └───────┼─────────────┼─────────────┼─────────────┼───────────────────┘   │
│          │             │             │             │                        │
│          └─────────────┴──────┬──────┴─────────────┘                        │
│                               ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      DATA INGESTION LAYER                            │   │
│  │                         (Airflow DAGs)                               │   │
│  │  ┌────────────────────────────────────────────────────────────┐     │   │
│  │  │  extract_customers  →  extract_usage  →  extract_support   │     │   │
│  │  └────────────────────────────────────────────────────────────┘     │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       DATA STORAGE LAYER                             │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │              Data Warehouse (BigQuery/Snowflake)              │   │   │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │   │   │
│  │  │  │  raw.       │ │ staging.    │ │ features.   │            │   │   │
│  │  │  │  customers  │ │ validated   │ │ customer_   │            │   │   │
│  │  │  │  raw.usage  │ │ _data       │ │ features    │            │   │   │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘            │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │              Model & Artifact Storage (S3/GCS)                │   │   │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │   │   │
│  │  │  │  models/    │ │ data/       │ │ artifacts/  │            │   │   │
│  │  │  │  v1.0.0/    │ │ train/      │ │ metrics/    │            │   │   │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘            │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│          ┌──────────────────────┼──────────────────────┐                   │
│          ▼                      ▼                      ▼                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │  TRAINING        │  │  MODEL REGISTRY  │  │  EXPERIMENT      │         │
│  │  PIPELINE        │  │                  │  │  TRACKING        │         │
│  │  ┌────────────┐  │  │  ┌────────────┐  │  │  ┌────────────┐  │         │
│  │  │ validate   │  │  │  │ Staging    │  │  │  │  MLflow    │  │         │
│  │  │ preprocess │  │  │  │ Production │  │  │  │  Server    │  │         │
│  │  │ train      │  │  │  │ Archived   │  │  │  │            │  │         │
│  │  │ evaluate   │  │  │  └────────────┘  │  │  └────────────┘  │         │
│  │  │ register   │  │  │  (MLflow)        │  │                  │         │
│  │  └────────────┘  │  │                  │  │                  │         │
│  │  (Kubeflow/      │  └────────┬─────────┘  └──────────────────┘         │
│  │   Airflow)       │           │                                          │
│  └──────────────────┘           │                                          │
│                                 ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       SERVING LAYER                                  │   │
│  │  ┌────────────────────────────────────────────────────────────┐     │   │
│  │  │                    Batch Scoring Job                        │     │   │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐           │     │   │
│  │  │  │ Load Model │→│Score All   │→│Write to    │           │     │   │
│  │  │  │ from Reg.  │  │ Customers  │  │ Predictions│           │     │   │
│  │  │  └────────────┘  └────────────┘  │    DB      │           │     │   │
│  │  │                                  └────────────┘           │     │   │
│  │  └────────────────────────────────────────────────────────────┘     │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────┐     │   │
│  │  │                    Online API (Optional)                    │     │   │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐           │     │   │
│  │  │  │  FastAPI   │→│ Load Model │→│  Predict   │           │     │   │
│  │  │  │  /predict  │  │ (cached)   │  │  Response  │           │     │   │
│  │  │  └────────────┘  └────────────┘  └────────────┘           │     │   │
│  │  └────────────────────────────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     MONITORING & OBSERVABILITY                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │ Prometheus │  │  Grafana   │  │  Evidently │  │   Alerts   │    │   │
│  │  │  Metrics   │→│ Dashboards │  │   Drift    │→│   (Slack)  │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       CONSUMER LAYER                                 │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                   CS Dashboard (Grafana)                      │   │   │
│  │  │  ┌──────────────────────────────────────────────────────┐    │   │   │
│  │  │  │  High Risk Customers  │  Risk Trends  │  Save Rate   │    │   │   │
│  │  │  └──────────────────────────────────────────────────────┘    │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dive

Let me explain each layer:

### Layer 1: Data Sources

These are external systems we read from:
- **Customer DB**: PostgreSQL with customer master data
- **Usage Logs**: Event stream processed into daily aggregates
- **Support Tickets**: Zendesk data synced daily
- **Billing API**: Stripe data synced daily

**Our responsibility**: Connect to these, not manage them.

### Layer 2: Data Ingestion

Airflow orchestrates data movement:
- DAGs run on schedule
- Extract from sources
- Load to data warehouse
- Handle failures and retries

**Key components**:
- Airflow scheduler
- Airflow workers
- Connection credentials (secure)

### Layer 3: Data Storage

Two types of storage:

**Data Warehouse** (BigQuery/Snowflake):
- Raw data (as-is from sources)
- Staged data (validated)
- Features (engineered for ML)

**Object Storage** (S3/GCS):
- Model artifacts
- Training data snapshots
- Evaluation artifacts

### Layer 4: Training Pipeline

Automated model training:
1. Validate input data
2. Preprocess and engineer features
3. Train model with tracked parameters
4. Evaluate against thresholds
5. Register in model registry

**Tools**: Kubeflow Pipelines or Airflow

### Layer 5: Model Registry

Central model management:
- **Staging**: Models being tested
- **Production**: Currently deployed model
- **Archived**: Previous versions

**Tool**: MLflow Model Registry

### Layer 6: Experiment Tracking

Record all experiments:
- Parameters
- Metrics
- Artifacts
- Code version

**Tool**: MLflow Tracking Server

### Layer 7: Serving Layer

Two serving modes:

**Batch Scoring** (Primary):
- Weekly job (Sunday night)
- Score all customers
- Write to predictions database

**Online API** (Secondary):
- Real-time predictions
- FastAPI service
- For ad-hoc queries

### Layer 8: Monitoring

Observe everything:
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Evidently**: Drift detection
- **Alerts**: Slack notifications

### Layer 9: Consumer Layer

End user interface:
- Grafana dashboard for Customer Success
- List of at-risk customers
- Risk score trends
- Save rate tracking

---

## Technology Choices

Here's our stack:

| Component | Technology | Alternative |
|-----------|------------|-------------|
| Orchestration | Airflow | Prefect, Dagster |
| Data Warehouse | BigQuery | Snowflake, Redshift |
| Object Storage | GCS | S3, Azure Blob |
| Experiment Tracking | MLflow | W&B, Neptune |
| Model Registry | MLflow | SageMaker, Vertex AI |
| Training Pipeline | Airflow + Python | Kubeflow, Vertex AI |
| Batch Serving | Airflow + Python | Spark, Dataflow |
| Online Serving | FastAPI | Flask, BentoML |
| Containerization | Docker | Podman |
| Orchestration (K8s) | Kubernetes | Docker Compose |
| Monitoring | Prometheus + Grafana | Datadog, CloudWatch |
| Drift Detection | Evidently | Arize, WhyLabs |

---

## Data Flow

Let me trace a complete flow:

### Training Flow

```
1. Airflow triggers weekly training DAG
2. Extract latest data from sources
3. Validate data quality (fail if issues)
4. Engineer features (save to feature table)
5. Split train/test
6. Train model with MLflow tracking
7. Evaluate model against thresholds
8. If pass: Register model as "Staging"
9. Run integration tests
10. If pass: Promote to "Production"
```

### Batch Scoring Flow

```
1. Airflow triggers Monday 2 AM scoring DAG
2. Load "Production" model from registry
3. Load current customer features
4. Generate predictions for all customers
5. Calculate risk tiers (High/Medium/Low)
6. Write to predictions database
7. Send notification to CS team
8. Update monitoring metrics
```

### Monitoring Flow

```
1. Scoring job emits metrics to Prometheus
2. Grafana displays dashboards
3. Evidently runs drift detection (daily)
4. If drift detected: Alert to Slack
5. If severe drift: Trigger retraining
6. Monthly: Compare predictions to outcomes
```

---

## Infrastructure

Where does this run?

### Development

- Local Docker Compose
- Local MLflow
- Sample data

### Staging

- Kubernetes cluster (GKE/EKS)
- Full stack deployment
- Anonymized production data

### Production

- Kubernetes cluster (separate)
- Full redundancy
- Real data, real users

---

## Network Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           VPC / Network                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Kubernetes Cluster                            │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │    │
│  │  │   Airflow   │  │   MLflow    │  │  FastAPI    │             │    │
│  │  │  namespace  │  │  namespace  │  │  namespace  │             │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │    │
│  │                                                                  │    │
│  │  ┌─────────────┐  ┌─────────────┐                               │    │
│  │  │ Prometheus  │  │   Grafana   │                               │    │
│  │  │  namespace  │  │  namespace  │                               │    │
│  │  └─────────────┘  └─────────────┘                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                           │                                              │
│                           │  Internal Network                            │
│                           │                                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Managed Services                              │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │    │
│  │  │   BigQuery  │  │     GCS     │  │  Cloud SQL  │             │    │
│  │  │   (Data)    │  │  (Storage)  │  │  (Metadata) │             │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                           │
                           │  External Access
                           ▼
                    Load Balancer
                           │
                   ┌───────┴───────┐
                   ▼               ▼
              CS Dashboard    API Endpoint
              (Grafana)       (FastAPI)
```

---

## Recap

Our architecture has:

**Data Layer**:
- Multiple source systems
- Airflow for ingestion
- Data warehouse + object storage

**ML Layer**:
- Training pipeline
- Experiment tracking (MLflow)
- Model registry

**Serving Layer**:
- Batch scoring (primary)
- Online API (secondary)

**Monitoring Layer**:
- Prometheus + Grafana
- Drift detection
- Alerting

**Consumer Layer**:
- CS dashboard
- Risk reports

---

## What's Next

Now let's see where this project fits in a real company's technology stack.

---

**Next Lecture**: [4.5 – Where This Project Fits in a Real Company's Stack](lecture-4.5-enterprise-fit.md)

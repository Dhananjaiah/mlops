# Lecture 1.4 – End-to-End ML System Architecture (From Data to Dashboard)

---

## The Big Picture

In this lecture, we're going to zoom out and look at the entire ML system—from data all the way to a dashboard showing model performance.

This is important because when you're working on one piece (say, model training), you need to understand how it connects to everything else.

Let's build this picture together.

---

## The Five Stages of an ML System

Every production ML system has five main stages:

1. **Data** – Where does the data come from? How is it stored?
2. **Training** – How is the model trained? How do we track experiments?
3. **Evaluation & Validation** – Is the model good enough? How do we decide?
4. **Deployment** – How does the model get to production?
5. **Monitoring** – How do we know it's working?

Let me walk you through each one.

---

## Stage 1: Data

Everything starts with data.

### Data Sources

Data can come from many places:
- **Databases**: PostgreSQL, MySQL, MongoDB
- **Data Warehouses**: Snowflake, BigQuery, Redshift
- **Data Lakes**: S3, Azure Blob, Google Cloud Storage
- **Streaming**: Kafka, Kinesis, Pub/Sub
- **APIs**: Third-party services, internal services
- **Files**: CSVs, Parquet files, Excel (yes, really)

In a real company, your ML model might need data from multiple sources.

### Data Pipelines

Raw data is rarely ML-ready. You need to:
- Clean it (handle missing values, fix errors)
- Transform it (aggregate, join, filter)
- Engineer features (create the inputs your model needs)

This is done by **data pipelines**—automated processes that run regularly.

Tools: Airflow, Prefect, dbt, Spark, custom scripts

### Data Storage for ML

Once processed, data needs to be stored somewhere the ML system can access:
- **Feature Store**: A specialized system for storing and serving features (e.g., Feast, Tecton)
- **Data Lake**: Raw and processed data in files
- **Data Warehouse**: Structured, queryable data

### Data Versioning

Here's something critical: **you need to version your data**.

Why? Because if you train a model today and want to reproduce it in six months, you need the exact same data. If the data changed, you'll get different results.

Tools: DVC, Delta Lake, LakeFS

---

## Stage 2: Training

Once you have data, you train models.

### Experimentation

Data scientists run many experiments:
- Try different algorithms
- Try different hyperparameters
- Try different features

Each experiment needs to be tracked:
- What parameters were used?
- What data was used?
- What metrics did it achieve?

Tools: MLflow, Weights & Biases, Neptune

### Training Pipelines

Production training isn't running a notebook manually. It's an **automated pipeline** that:

1. Loads data
2. Preprocesses it
3. Trains the model
4. Evaluates the model
5. Saves the model artifact

This pipeline should be:
- Version controlled
- Reproducible
- Schedulable

Tools: Kubeflow Pipelines, Airflow, Metaflow, Vertex AI Pipelines

### Training Infrastructure

Training needs compute resources:
- **Local**: Your laptop (for small experiments)
- **Cloud VMs**: EC2, GCE, Azure VMs
- **Managed Services**: SageMaker, Vertex AI, Azure ML
- **Kubernetes**: For custom, scalable training

For deep learning, you might need GPUs or TPUs.

### Model Artifacts

The output of training is a **model artifact**:
- The trained weights
- Preprocessing objects (scalers, encoders)
- Metadata (training date, parameters, metrics)

These need to be saved somewhere:
- Model Registry (MLflow, SageMaker, Vertex AI)
- Object Storage (S3, GCS)

---

## Stage 3: Evaluation & Validation

Before a model goes to production, it needs to be validated.

### Offline Evaluation

This is what most data scientists are familiar with:
- Accuracy, precision, recall, F1
- AUC-ROC, log loss
- Custom business metrics

You evaluate on a held-out test set.

### Model Validation Checks

But there's more to check:
- **Performance threshold**: Is accuracy above X%?
- **Fairness**: Does the model treat different groups equitably?
- **Robustness**: Does it handle edge cases?
- **Speed**: Can it make predictions fast enough?
- **Size**: Is the model small enough to deploy?

### Comparison to Baseline

A new model should be compared to:
- The current production model
- A simple baseline (e.g., always predict the majority class)

If the new model isn't significantly better, maybe don't deploy it.

### Approval Process

In mature organizations, there's a formal approval process:
- Automated checks pass
- Human reviews (for high-risk models)
- Sign-off before promotion to production

---

## Stage 4: Deployment

Now the model needs to get into production.

### Model Packaging

The model needs to be packaged so it can be deployed:
- Serialize the model (pickle, joblib, ONNX, SavedModel)
- Create a container (Docker)
- Include dependencies (Python packages)

### Serving Patterns

How will the model serve predictions?

**Online Serving (Real-time)**
- Model is deployed as an API
- Receives requests, returns predictions in milliseconds
- Example: Fraud detection at payment time

**Batch Serving (Offline)**
- Model runs on a schedule (e.g., nightly)
- Processes large volumes of data
- Saves predictions to a database
- Example: Customer churn scores updated daily

**Streaming Serving (Near-real-time)**
- Model processes events from a stream
- Lower latency than batch, but not instant
- Example: Processing sensor data

### Deployment Infrastructure

Where does the model run?

- **Simple**: A VM with a Flask/FastAPI app
- **Containers**: Docker containers orchestrated by Kubernetes
- **Serverless**: AWS Lambda, Google Cloud Functions
- **Managed ML Serving**: SageMaker Endpoints, Vertex AI, Azure ML

### Deployment Strategies

How do you update the model?

- **Big Bang**: Replace old model with new model all at once (risky)
- **Blue-Green**: Run both, switch traffic (safer)
- **Canary**: Send small % of traffic to new model, gradually increase (safest)
- **Shadow**: New model runs alongside, but doesn't serve users (for testing)

---

## Stage 5: Monitoring

Once deployed, you need to know if it's working.

### Infrastructure Monitoring

Basic stuff:
- Is the server running?
- CPU/memory usage
- Request latency
- Error rates

Tools: Prometheus, Grafana, CloudWatch, Datadog

### Application Monitoring

ML-specific application metrics:
- Number of predictions made
- Input data distribution
- Output prediction distribution
- API response times

### Model Performance Monitoring

This is the ML-specific part:
- **Data Drift**: Is the input data changing?
- **Concept Drift**: Is the relationship between input and output changing?
- **Model Accuracy**: If you have labels, how accurate is the model?

Tools: Evidently, Arize, Fiddler, WhyLabs

### Alerting

When something goes wrong, you need to know:
- Set up alerts on key metrics
- PagerDuty, Slack notifications, email
- Define SLOs (Service Level Objectives)

### Feedback Loop

The best systems have a feedback loop:
- Collect labels for predictions (from users, from downstream systems)
- Feed this back into training data
- Trigger retraining when performance drops

---

## The Architecture Diagram

Let me describe what this looks like visually:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  [Data Sources]  →  [Data Pipelines]  →  [Feature Store/Data Lake]      │
│   - Databases        - Airflow              - Feast                      │
│   - APIs             - dbt                  - S3/GCS                     │
│   - Streams          - Spark                - DVC (versioned)            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            TRAINING LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│  [Experiment Tracking]  →  [Training Pipeline]  →  [Model Registry]     │
│   - MLflow                  - Kubeflow             - MLflow Registry     │
│   - W&B                     - Airflow              - SageMaker           │
│                             - Metaflow             - Vertex AI           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           VALIDATION LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│  [Offline Evaluation]  →  [Validation Checks]  →  [Approval Process]    │
│   - Test metrics           - Fairness             - Automated gates      │
│   - Baseline comparison    - Speed tests          - Human review         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           DEPLOYMENT LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│  [Model Packaging]  →  [CI/CD Pipeline]  →  [Serving Infrastructure]    │
│   - Docker                 - GitHub Actions       - Kubernetes           │
│   - ONNX                   - Jenkins              - SageMaker            │
│                            - GitLab CI            - FastAPI              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           MONITORING LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│  [Infrastructure]  →  [Application]  →  [Model Performance]  → [Alerts] │
│   - Prometheus          - Custom metrics   - Evidently           - Slack │
│   - Grafana             - Latency          - Drift detection     - PD    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                            [Feedback Loop]
                        (Labels → Retraining Trigger)
```

---

## How Data Flows Through the System

Let me trace a single prediction through this system:

1. **User Request**: A user does something (e.g., opens the app)
2. **Feature Fetch**: System fetches the user's features from the feature store
3. **Model Call**: Features are sent to the model API
4. **Prediction**: Model returns a prediction
5. **Response**: Prediction is returned to the user (or used by another system)
6. **Logging**: The request, features, and prediction are logged
7. **Monitoring**: Metrics are updated (latency, prediction distribution)
8. **Later**: If we get feedback (did the prediction happen?), it's logged for future training

---

## This Seems Like a Lot...

I know what you're thinking: "This is a lot of components!"

You're right. And here's the truth: **you don't need all of this on Day 1.**

In this course, we'll start simple and add complexity gradually:

- **Phase 1**: Train locally, deploy manually
- **Phase 2**: Add experiment tracking and versioning
- **Phase 3**: Automate training with pipelines
- **Phase 4**: Add CI/CD for deployment
- **Phase 5**: Add monitoring

By the end, you'll have a system that looks like this diagram. But you'll understand every piece because you built it.

---

## Recap

An end-to-end ML system has five stages:

1. **Data**: Sources → Pipelines → Storage (versioned)
2. **Training**: Experiments → Pipelines → Model Registry
3. **Validation**: Evaluation → Checks → Approval
4. **Deployment**: Packaging → CI/CD → Serving
5. **Monitoring**: Infra → Application → Model → Alerts

Each stage has multiple components, but they all connect into one system.

---

## What's Next

Now that you see the big picture, let's zoom out even further.

In the next lecture, we'll look at **where MLOps fits in the overall Data and AI world**. How does it relate to Data Engineering? To DevOps? To AI Engineering?

Understanding this context will help you see how your work connects to the larger organization.

---

**Next Lecture**: [1.5 – Where Does MLOps Fit in the Overall Data/AI World?](lecture-1.5-mlops-in-data-ai-world.md)

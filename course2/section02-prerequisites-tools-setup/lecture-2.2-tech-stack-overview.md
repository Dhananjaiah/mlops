# Lecture 2.2 – Tech Stack Overview (Python, Git, Docker, CI/CD, Cloud/Kubernetes)

---

## The Tools of the Trade

In this lecture, I'll give you a bird's-eye view of all the technologies we'll use in this course.

Don't worry if some of these are new to you. We'll learn them as we go. This is just to set expectations and help you understand why we use each tool.

---

## The Core Stack

Here are the main categories of tools we'll use:

1. **Programming Language**: Python
2. **Version Control**: Git
3. **Containerization**: Docker
4. **CI/CD**: GitHub Actions
5. **Orchestration**: Airflow (or similar)
6. **Experiment Tracking**: MLflow
7. **Data Versioning**: DVC
8. **Model Serving**: FastAPI
9. **Monitoring**: Prometheus + Grafana
10. **Infrastructure** (optional): Kubernetes

Let's go through each one.

---

## 1. Python

### What It Is
Python is our primary programming language. Almost everything in this course is written in Python.

### Why We Use It
- **ML ecosystem**: Most ML libraries are in Python (scikit-learn, TensorFlow, PyTorch)
- **Simplicity**: Easy to read and write
- **Community**: Huge ecosystem, lots of resources
- **MLOps tools**: Most MLOps tools have Python SDKs

### What You'll Use It For
- Data processing scripts
- Model training code
- API services
- Pipeline definitions
- Automation scripts

### Key Libraries
- `pandas` – Data manipulation
- `scikit-learn` – ML models
- `mlflow` – Experiment tracking
- `fastapi` – Building APIs
- `pytest` – Testing

---

## 2. Git

### What It Is
Git is a version control system. It tracks changes to your code over time.

### Why We Use It
- **Track history**: See what changed and when
- **Collaboration**: Work with others without stepping on each other's toes
- **Branching**: Work on features in isolation
- **Rollback**: Go back if something breaks

### What You'll Use It For
- Storing all project code
- Tracking changes to training scripts
- Managing different versions of configurations
- Triggering CI/CD pipelines

### Key Concepts
- Repository (repo)
- Commit
- Branch
- Pull Request (PR)
- Merge

### Tools
- Git (command line)
- GitHub (hosting)

---

## 3. Docker

### What It Is
Docker creates "containers"—lightweight, isolated environments that package your code with all its dependencies.

### Why We Use It
- **Consistency**: "Works on my machine" → "Works everywhere"
- **Isolation**: Dependencies don't conflict
- **Reproducibility**: Same container = same behavior
- **Deployment**: Ship containers to any environment

### What You'll Use It For
- Packaging model services
- Creating reproducible training environments
- Running local development stacks
- Deploying to production

### Key Concepts
- Image (template)
- Container (running instance)
- Dockerfile (instructions to build image)
- Registry (where images are stored)

### Tools
- Docker Desktop
- Docker Compose (for multi-container setups)

---

## 4. CI/CD (GitHub Actions)

### What It Is
CI/CD stands for Continuous Integration / Continuous Delivery. It automates building, testing, and deploying your code.

### Why We Use It
- **Automation**: No manual "build and deploy" steps
- **Consistency**: Same process every time
- **Speed**: Fast feedback on changes
- **Quality**: Catch problems early

### What You'll Use It For
- Running tests automatically on every commit
- Building Docker images
- Deploying models to staging/production
- Checking code quality

### Key Concepts
- Pipeline / Workflow
- Trigger (when to run)
- Jobs and Steps
- Artifacts

### Tools
- GitHub Actions (we'll use this)
- Alternatives: Jenkins, GitLab CI, CircleCI

---

## 5. Orchestration (Airflow)

### What It Is
Orchestrators schedule and manage complex workflows. They handle dependencies, retries, and scheduling.

### Why We Use It
- **Automation**: Run pipelines on schedule
- **Dependencies**: "Run step B after step A completes"
- **Reliability**: Retry failed steps
- **Visibility**: See what's running, what failed

### What You'll Use It For
- Scheduling training pipelines
- Running data preprocessing
- Triggering model evaluations
- Coordinating multi-step workflows

### Key Concepts
- DAG (Directed Acyclic Graph)
- Task
- Schedule
- Dependencies

### Tools
- Apache Airflow (we'll use this)
- Alternatives: Prefect, Dagster, Kubeflow Pipelines

---

## 6. Experiment Tracking (MLflow)

### What It Is
MLflow tracks machine learning experiments—what parameters you used, what metrics you got, what artifacts you produced.

### Why We Use It
- **Organization**: Keep track of hundreds of experiments
- **Comparison**: Compare different model versions
- **Reproducibility**: Know exactly what produced a result
- **Model Registry**: Manage model versions and stages

### What You'll Use It For
- Logging training parameters
- Recording metrics (accuracy, loss, etc.)
- Storing model artifacts
- Managing model versions

### Key Concepts
- Experiment
- Run
- Parameters
- Metrics
- Artifacts
- Model Registry

### Tools
- MLflow (we'll use this)
- Alternatives: Weights & Biases, Neptune, Comet

---

## 7. Data Versioning (DVC)

### What It Is
DVC (Data Version Control) is like Git, but for data. It tracks data files and lets you version them.

### Why We Use It
- **Reproducibility**: Know exactly what data trained a model
- **Storage efficiency**: Don't put large files in Git
- **Collaboration**: Share data with teammates
- **Pipelines**: Define data processing pipelines

### What You'll Use It For
- Versioning training datasets
- Tracking data processing pipelines
- Storing data remotely (S3, GCS, etc.)

### Key Concepts
- `.dvc` files (pointers to data)
- Remote storage
- Data pipelines
- Caching

### Tools
- DVC (we'll use this)
- Alternatives: Delta Lake, LakeFS

---

## 8. Model Serving (FastAPI)

### What It Is
FastAPI is a Python web framework for building APIs. We'll use it to serve model predictions.

### Why We Use It
- **Speed**: Very fast performance
- **Easy to use**: Simple, Pythonic syntax
- **Documentation**: Auto-generates API docs
- **Type hints**: Built-in validation

### What You'll Use It For
- Creating prediction endpoints
- Health check endpoints
- Model metadata endpoints

### Key Concepts
- Endpoint / Route
- Request / Response
- JSON
- Validation

### Tools
- FastAPI (we'll use this)
- Alternatives: Flask, BentoML, Seldon Core

---

## 9. Monitoring (Prometheus + Grafana)

### What It Is
Prometheus collects metrics. Grafana visualizes them. Together, they give you visibility into your systems.

### Why We Use It
- **Visibility**: Know what's happening in production
- **Alerting**: Get notified when things go wrong
- **Debugging**: Diagnose issues quickly
- **Trends**: See patterns over time

### What You'll Use It For
- Tracking API latency
- Monitoring error rates
- Watching model predictions
- Creating dashboards

### Key Concepts
- Metrics
- Time series
- Queries
- Dashboards
- Alerts

### Tools
- Prometheus (metrics collection)
- Grafana (visualization)
- Alternatives: Datadog, New Relic, CloudWatch

---

## 10. Infrastructure (Kubernetes) – Optional

### What It Is
Kubernetes (K8s) orchestrates containers. It manages where containers run, how they scale, and how they communicate.

### Why We Use It
- **Scaling**: Run more containers when needed
- **Resilience**: Restart failed containers
- **Standardization**: Same deployment patterns everywhere
- **Industry standard**: Most companies use K8s

### What You'll Use It For
- Deploying model services
- Managing multiple environments
- Scaling based on load

### Key Concepts
- Pod
- Deployment
- Service
- Namespace
- ConfigMap / Secret

### Tools
- Kubernetes
- kubectl (command line)
- K3d / kind (local K8s)

**Note**: Kubernetes is optional. We'll cover it, but you can do everything locally with Docker Compose too.

---

## The Stack Diagram

Here's how all these tools fit together:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Development                                   │
│   [Python] → [Git] → [DVC] → [MLflow]                              │
│   (Code)    (Version) (Data)  (Experiments)                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        CI/CD                                         │
│   [GitHub Actions]                                                   │
│   (Test → Build → Deploy)                                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Production                                    │
│   [Docker] → [Kubernetes/Docker Compose]                            │
│   (Package)  (Orchestrate)                                          │
│              │                                                       │
│              ▼                                                       │
│   [FastAPI] → [Prometheus] → [Grafana]                              │
│   (Serve)    (Collect)       (Visualize)                            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Orchestration                                 │
│   [Airflow]                                                          │
│   (Schedule training, data pipelines)                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## What We'll Install

In the next lecture, we'll set up your local environment. Here's what you'll install:

**Required**:
- Python 3.9+
- Git
- Docker Desktop
- VS Code (or your preferred editor)

**Python Packages** (via pip/poetry):
- pandas, scikit-learn
- mlflow
- dvc
- fastapi, uvicorn
- pytest
- And more as we go

**Later**:
- kubectl (for Kubernetes)
- k3d (local Kubernetes)

---

## Don't Be Overwhelmed

This is a lot of tools. But remember:

1. **We'll learn them one at a time** – You don't need to know everything now
2. **They all serve a purpose** – Each tool solves a specific problem
3. **You'll use them in context** – Learning by doing is the best way
4. **Many are interchangeable** – If you prefer different tools, the concepts transfer

---

## Recap

Our tech stack:
- **Python**: Programming language
- **Git**: Code versioning
- **Docker**: Containerization
- **GitHub Actions**: CI/CD
- **Airflow**: Orchestration
- **MLflow**: Experiment tracking
- **DVC**: Data versioning
- **FastAPI**: Model serving
- **Prometheus + Grafana**: Monitoring
- **Kubernetes**: Infrastructure (optional)

---

## What's Next

Time to set up your local environment!

In the next lecture, we'll install everything you need and make sure it's working.

---

**Next Lecture**: [2.3 – Setting Up Local Dev Environment](lecture-2.3-local-dev-setup.md)

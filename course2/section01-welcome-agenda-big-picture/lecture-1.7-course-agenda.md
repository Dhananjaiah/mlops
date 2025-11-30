# Lecture 1.7 – Agenda of the Entire Course (What We'll Build Step by Step)

---

## The Journey Ahead

Alright! We've covered a lot of ground in this foundation section. You now understand:

- What MLOps is
- Why it matters
- The architecture of ML systems
- Where MLOps fits in the bigger picture
- Who does what

Now let me show you exactly what we'll build together in this course.

---

## Our Project: Customer Churn Prediction

Throughout this course, we'll build a **Customer Churn Prediction System**.

Why churn prediction?

1. It's a real business problem (every company cares about retaining customers)
2. It's complex enough to need all the MLOps practices
3. It's simple enough that we won't get lost in ML complexity

By the end, you'll have a system that:
- Ingests customer data
- Trains and evaluates models
- Deploys models to production
- Monitors model performance
- Automatically retrains when needed

Let's walk through each section.

---

## Section 1: Welcome, Agenda & Big Picture ✓

**Status**: You're finishing it now!

**What we covered**:
- Course introduction
- What is MLOps (the story, not definition)
- Why MLOps matters
- ML system architecture
- MLOps in the data/AI world
- Roles and responsibilities
- This agenda

---

## Section 2: Prerequisites, Tools & Environment Setup

**What you'll learn**:
- What skills you need (and don't need)
- The tech stack we'll use
- Setting up your local development environment
- Project structure best practices
- Python packages and virtual environments
- Git basics for MLOps
- How to follow along with just a laptop

**What you'll build**:
- Your development environment
- The project folder structure
- Your first Git repository for the project

**Time**: ~2-3 hours

---

## Section 3: Understanding the ML Lifecycle & MLOps Responsibilities

**What you'll learn**:
- How to frame business problems as ML problems
- The classic ML lifecycle (CRISP-DM)
- Where things break in real life
- MLOps vs DevOps
- Online vs batch ML systems
- MLOps responsibilities at each stage

**What you'll do**:
- Map our churn prediction project to the ML lifecycle
- Identify where MLOps fits in each stage

**Time**: ~1.5-2 hours

---

## Section 4: Course Project Overview: Real-World Use Case

**What you'll learn**:
- How to define an ML use case properly
- Business requirements and success metrics
- Data sources and data contracts
- High-level architecture design
- Enterprise context
- What to automate vs keep manual

**What you'll build**:
- Project requirements document
- Architecture diagram
- Data contract definition

**Time**: ~2 hours

---

## Section 5: Data Engineering Basics for MLOps

**What you'll learn**:
- Data types and storage options
- Data ingestion patterns
- Data quality and validation
- Feature engineering basics
- Introduction to feature stores
- Responsibility boundaries with data engineering

**What you'll build**:
- Data loading scripts
- Basic data validation checks
- Feature engineering pipeline

**Time**: ~2.5-3 hours

---

## Section 6: Reproducible Experimentation: From Notebook to Pipeline

**What you'll learn**:
- Problems with notebooks in production
- Structuring experiments properly
- Experiment tracking concepts
- Using MLflow for tracking
- Reproducibility practices
- Team reproducibility enforcement

**What you'll build**:
- Organized experiment structure
- MLflow tracking setup
- Reproducible training script

**Time**: ~2.5-3 hours

---

## Section 7: Model Packaging: From Script to Service

**What you'll learn**:
- Creating reusable Python packages
- Writing clean inference functions
- Building REST APIs with FastAPI
- Docker basics for MLOps
- Dockerizing model services
- Local testing practices

**What you'll build**:
- Model Python package
- FastAPI service
- Docker container for the model
- Local testing setup

**Time**: ~3-4 hours

---

## Section 8: Data & Model Versioning, Registry & Artifacts

**What you'll learn**:
- Why versioning matters
- Git for code, DVC for data
- Model registries
- Model states and lifecycle
- Artifact storage and retrieval
- Governance basics

**What you'll build**:
- DVC setup for data versioning
- MLflow model registry configuration
- Model promotion workflow

**Time**: ~2.5-3 hours

---

## Section 9: Automated Training Pipelines & Orchestration

**What you'll learn**:
- Why pipelines are essential
- Pipeline building blocks (tasks, DAGs)
- Common orchestrators (Airflow, etc.)
- Designing training pipelines
- Implementing pipelines
- Scheduling and failure handling
- MLOps vs Data Engineering in orchestration

**What you'll build**:
- Complete training pipeline
- Scheduled execution
- Failure handling and retries

**Time**: ~3-4 hours

---

## Section 10: CI/CD for ML Systems (MLOps Delivery)

**What you'll learn**:
- CI/CD basics for ML
- Extra complexity in ML CI/CD
- Writing ML tests (unit, integration, smoke)
- Building and pushing Docker images
- Continuous delivery of models
- Blue/green and canary deployments
- Rollback procedures

**What you'll build**:
- GitHub Actions CI/CD pipeline
- Automated tests
- Deployment workflow
- Rollback capability

**Time**: ~3-4 hours

---

## Section 11: Deployment Architectures & Serving Patterns

**What you'll learn**:
- Online vs offline vs near-real-time serving
- Monolith vs microservice architectures
- VM vs Docker Swarm vs Kubernetes
- Kubernetes basics for MLOps
- Model serving frameworks overview
- Production deployment design

**What you'll build**:
- Production-like deployment architecture
- Kubernetes deployment manifests
- Service configuration

**Time**: ~3-4 hours

---

## Section 12: Monitoring, Observability & Model Health

**What you'll learn**:
- What to monitor in ML systems
- Infrastructure and application metrics
- Model-specific metrics (drift, skew)
- Logging and tracing
- Building dashboards
- Alerts and incident response
- Retraining triggers

**What you'll build**:
- Prometheus metrics
- Grafana dashboard
- Alerting rules
- Retraining trigger logic

**Time**: ~3-4 hours

---

## Section 13: Governance, Security, and Responsible MLOps

**What you'll learn**:
- Access control and secrets management
- Compliance basics (PII, audit logs)
- Explainability and model cards
- Approval workflows
- Handling data deletion requests
- Organizational best practices

**What you'll build**:
- Secrets management setup
- Model card documentation
- Approval workflow configuration

**Time**: ~2-3 hours

---

## Section 14: Putting It All Together: End-to-End Capstone

**What you'll learn**:
- Final architecture review
- Code walkthrough
- Running the full pipeline
- Common failures and debugging
- Interview presentation tips
- Enterprise integration patterns

**What you'll do**:
- Complete end-to-end walkthrough
- Debug common issues
- Document the project for portfolio

**Time**: ~3-4 hours

---

## Section 15: Career, Interviews & Next Steps

**What you'll learn**:
- MLOps job roles and titles
- Interview storytelling
- Portfolio building
- Extending the project
- Learning path after this course

**What you'll get**:
- Career guidance
- Interview preparation
- Next steps for continued learning

**Time**: ~1.5-2 hours

---

## The Timeline

If you're going through this course:

| Pace | Sections per Week | Total Time |
|------|-------------------|------------|
| Intensive | 2-3 | 4-5 weeks |
| Moderate | 1-2 | 8-10 weeks |
| Relaxed | 1 | 12-15 weeks |

I recommend the moderate pace. It gives you time to practice and absorb.

---

## The Skills You'll Gain

By the end, you'll be proficient in:

**Tools**:
- Python, Git, Docker
- MLflow for experiment tracking and model registry
- DVC for data versioning
- FastAPI for model serving
- Airflow (or similar) for orchestration
- GitHub Actions for CI/CD
- Prometheus & Grafana for monitoring
- Kubernetes basics

**Practices**:
- Reproducible experimentation
- Data and model versioning
- Automated training pipelines
- CI/CD for ML
- Model deployment patterns
- Production monitoring
- Governance and compliance

**Thinking**:
- Systems thinking for ML
- Debugging production issues
- Designing for reliability
- Balancing automation vs manual effort

---

## What You'll Have at the End

A complete, working system:

```
Your MLOps Portfolio Project
├── Data pipeline (ingestion, validation)
├── Experiment tracking (MLflow)
├── Training pipeline (orchestrated)
├── Model registry (versioned, staged)
├── Model service (FastAPI, Dockerized)
├── CI/CD pipeline (GitHub Actions)
├── Monitoring (Prometheus, Grafana)
├── Documentation (README, model cards)
└── Your ability to explain it all in an interview
```

This is a portfolio project you can show to employers.

---

## Let's Get Started!

Enough overview. Let's start building.

In Section 2, we'll set up your development environment and get you ready to code.

See you there!

---

## Section 1 Complete! 🎉

Congratulations on finishing Section 1!

**Quick Review**:
- MLOps bridges the gap from model to production
- It combines ML, DevOps, and Data Engineering
- ML systems have five stages: Data → Training → Validation → Deployment → Monitoring
- MLOps fits in the larger data/AI ecosystem
- Team members have different roles—know who does what
- This course builds a complete system step by step

---

**Next Section**: [Section 2 – Prerequisites, Tools & Environment Setup](../section02-prerequisites-tools-setup/lecture-2.1-skills-needed.md)

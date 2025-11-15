# MLOps Project Execution Guide

**🎯 Clear Step-by-Step Instructions to Execute This Project**

> This guide answers: "How do I actually run this project?" and "Who does what?"

---

## 📚 Table of Contents

1. [Quick Overview](#quick-overview)
2. [Who Does What - Roles & Responsibilities](#who-does-what---roles--responsibilities)
3. [What's New - Recent Additions](#whats-new---recent-additions)
4. [Execution Paths by Persona](#execution-paths-by-persona)
5. [Step-by-Step Execution](#step-by-step-execution)
6. [Folder Structure Explained](#folder-structure-explained)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Quick Overview

### What Is This Project?

This is a **complete MLOps learning system** consisting of:
- 📘 **Course Materials**: 15 modules teaching MLOps from zero to production
- 🚀 **Capstone Project**: A real-world churn prediction system
- 🔧 **Ready-to-Use Tools**: Docker, Kubernetes, CI/CD configurations
- 📊 **Data Engineering Pipeline**: Complete data processing workflow

### What You'll Accomplish

By following this guide, you will:
1. ✅ Set up your development environment
2. ✅ Run a complete data engineering pipeline
3. ✅ Train and deploy a machine learning model
4. ✅ Create a REST API for predictions
5. ✅ Monitor and track your ML system
6. ✅ Understand the complete MLOps workflow

### Time Required

- **Quick Start**: 30 minutes (get something running)
- **Complete Walkthrough**: 2-3 hours (understand everything)
- **Full Course**: 25-30 hours (master MLOps)

---

## Who Does What - Roles & Responsibilities

### Understanding the Roles

Different people use this project for different purposes. Here's who does what:

#### 👨‍🎓 **Student / Learner**
**What you do:**
- Follow the course modules (course/00-*.md to course/14-*.md)
- Complete mini-labs and exercises
- Build the capstone project step-by-step
- Take quizzes and mock exams

**Your path:** [Student Path](#for-students--learners)

#### 🔧 **DevOps Engineer (New to Data/ML)**
**What you do:**
- Start with data engineering basics
- Learn how ML systems differ from traditional apps
- Focus on deployment, monitoring, and infrastructure
- Apply your existing Docker/K8s knowledge

**Your path:** [DevOps Engineer Path](#for-devops-engineers-new-to-ml)

#### 📊 **Data Engineer / ML Engineer**
**What you do:**
- Focus on data pipelines and feature engineering
- Learn model deployment and serving
- Implement monitoring and drift detection
- Build production ML systems

**Your path:** [Data/ML Engineer Path](#for-dataml-engineers)

#### 🏫 **Instructor / Teacher**
**What you do:**
- Review the comprehensive implementation guide
- Prepare lab environments
- Guide students through exercises
- Evaluate student progress

**Your path:** [Instructor Path](#for-instructors)

---

## What's New - Recent Additions

### Files and Folders Added in Recent Pull Requests

Understanding what was recently added helps you know what to explore:

#### **New Documentation**
- `DATA_PIPELINE_VISUAL_GUIDE.md` - Visual flowchart of data engineering
- `DATA_ENGINEERING_README.md` - Quick start for data engineering
- `IMPLEMENTATION_GUIDE.md` - Comprehensive 1700+ line implementation guide
- `course/00.5-data-engineering-for-beginners.md` - New beginner module

#### **New Scripts**
- `project/scripts/00_generate_sample_data.py` - Creates sample customer data
- `project/scripts/run_data_pipeline.py` - Runs complete data pipeline
- Scripts handle: data generation, cleaning, feature engineering, model training

#### **New Folders**
- `project/outputs/` - Stores visualizations and results
- `project/data/train/` - Training data splits
- `project/data/test/` - Test data splits
- `project/data/processed/` - Cleaned and processed data

#### **Purpose of Each Addition**

| File/Folder | Purpose | When to Use |
|------------|---------|-------------|
| DATA_PIPELINE_VISUAL_GUIDE.md | Understand data flow | When learning data engineering |
| DATA_ENGINEERING_README.md | Quick start guide | First time running data pipeline |
| 00_generate_sample_data.py | Create practice data | Setting up for first time |
| run_data_pipeline.py | Execute full pipeline | After setup, to see everything work |
| project/outputs/ | View results | After running pipeline |

---

## Execution Paths by Persona

### For Students / Learners

**"I want to learn MLOps from scratch"**

#### Phase 1: Quick Start (30 minutes)
```bash
# 1. Clone the repository
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops

# 2. Read the overview
cat README.md

# 3. Start with Module 00
cd course
cat 00-overview.md
```

#### Phase 2: Hands-On Practice (2-3 hours)
```bash
# 1. Set up project environment
cd project
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pandas numpy matplotlib seaborn scikit-learn

# 2. Generate sample data
python scripts/00_generate_sample_data.py

# 3. Run the data pipeline
python scripts/run_data_pipeline.py

# 4. Check the results
ls -l outputs/
# You'll see visualizations and model metrics
```

#### Phase 3: Course Modules (25-30 hours)
```bash
# Follow modules in order:
# - course/00-overview.md
# - course/00.5-data-engineering-for-beginners.md (if new to data)
# - course/01-mlops-foundations.md
# - course/02-env-and-packaging.md
# ... and so on

# Each module includes:
# - Learning objectives
# - Key concepts
# - Hands-on commands
# - Mini-lab exercises
# - Quiz questions
```

**Your Learning Path:**
1. Start → Read course/00-overview.md
2. Complete Phase 1 & 2 above (get hands dirty first!)
3. Follow modules 00-14 sequentially
4. Build capstone project alongside course
5. Take mock exams (exams/mock-exam-1.md)

---

### For DevOps Engineers (New to ML)

**"I know Docker/K8s but not machine learning"**

#### Your Starting Point
```bash
# 1. Start with data engineering basics
cd mlops/course
cat 00.5-data-engineering-for-beginners.md

# 2. Quick start with the visual guide
cd ../project
cat DATA_ENGINEERING_README.md
cat DATA_PIPELINE_VISUAL_GUIDE.md
```

#### Your Focus Areas

**Week 1: Understand Data**
```bash
# Learn what data scientists do
# Module: course/00.5-data-engineering-for-beginners.md

# Run the data pipeline to see it in action
cd project
python scripts/00_generate_sample_data.py
python scripts/run_data_pipeline.py

# Examine outputs
cat outputs/experiment_results.json
```

**Week 2: Understand ML Models**
```bash
# Learn basics of model training
# Module: course/04-experiment-tracking-and-reproducibility.md

# Run a simple training
python src/train.py  # (when implemented)
```

**Week 3-4: Apply Your Expertise**
```bash
# Now focus on what you know: deployment, monitoring, CI/CD
# Modules: 
# - course/08-serving-and-apis.md
# - course/10-ci-cd-and-environments.md
# - course/11-observability-and-monitoring.md

# Deploy with Docker
make compose-up
docker compose ps

# Deploy to Kubernetes
kubectl create namespace mlops-dev
kubectl apply -k infra/k8s/overlays/dev/
```

**Your Key Advantage:** You already know 50% of MLOps (the Ops part). You just need to learn:
- What data scientists need
- How models are trained
- What makes ML systems different (drift, retraining, etc.)

---

### For Data/ML Engineers

**"I know ML/data science but not production deployment"**

#### Your Starting Point
```bash
# 1. Review the project structure
cd mlops/project
cat README.md

# 2. Examine the data pipeline
cat DATA_PIPELINE_VISUAL_GUIDE.md

# 3. Run your first pipeline
python scripts/run_data_pipeline.py
```

#### Your Focus Areas

**Week 1: Data Engineering**
```bash
# You might know this already, but review:
# Module: course/03-data-versioning-and-quality.md

# Learn DVC for data versioning
dvc init
dvc add data/raw/customers.csv
dvc push
```

**Week 2: Experiment Tracking**
```bash
# Module: course/04-experiment-tracking-and-reproducibility.md

# Learn MLflow (industry standard)
mlflow server --backend-store-uri sqlite:///mlflow.db
mlflow experiments list
```

**Week 3-4: Production Deployment**
```bash
# This is where you need to focus
# Modules:
# - course/08-serving-and-apis.md
# - course/09-batch-streaming-and-scheduled-jobs.md
# - course/10-ci-cd-and-environments.md

# Deploy your model as an API
uvicorn src.api:app --reload

# Test the API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[34, 12, 65.5]]}'
```

**Your Key Advantage:** You know how to build and evaluate models. You need to learn:
- How to deploy models as services
- How to monitor models in production
- How to handle model drift and retraining
- Infrastructure as code (Terraform, Kubernetes)

---

### For Instructors

**"I need to teach this course to others"**

#### Your Preparation Steps

**Step 1: Master the Content**
```bash
# 1. Read the comprehensive implementation guide
cat IMPLEMENTATION_GUIDE.md  # 1700+ lines, everything you need

# 2. Review course structure
ls course/  # 15 modules

# 3. Test the capstone project
cd project
make quickstart  # Sets up everything
```

**Step 2: Set Up Lab Environment**
```bash
# Option A: Local labs (students' laptops)
# - Ensure students have Docker Desktop
# - Provide setup scripts
# - Test on multiple OS (Windows, Mac, Linux)

# Option B: Cloud labs (AWS/GCP/Azure)
# - Use provided Terraform configs
# - Create student namespaces in Kubernetes
# - Set up cost monitoring

# Option C: Hybrid
# - Basic modules: local
# - Advanced modules (K8s, cloud): shared cluster
```

**Step 3: Customize Content**
```bash
# All content is in markdown - easy to edit
# Adjust based on:
# - Student background (add/skip prerequisites)
# - Time available (full course vs workshop)
# - Tools (swap tools based on org standards)
```

**Teaching Strategies:**
1. **Week 1-2**: Foundations + hands-on basics
2. **Week 3-4**: Pipelines and deployment
3. **Week 5-6**: Advanced topics + capstone
4. **Assessment**: Mini-labs + final project + mock exams

**Resources You Have:**
- `IMPLEMENTATION_GUIDE.md` - Your primary teaching resource
- `troubleshooting/triage-matrix.md` - Help students debug
- `cheatsheets/` - Give students quick references
- `exams/` - Assess learning

---

## Step-by-Step Execution

### Prerequisites Check

Before starting, verify you have:
```bash
# Python 3.11+
python --version  # Should show 3.11 or higher

# Git
git --version

# Docker (optional but recommended)
docker --version

# Text editor
code --version  # VS Code
# OR vim, nano, etc.
```

### Step 1: Clone and Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops

# 2. Explore structure
ls -la
# You should see:
# - README.md (main documentation)
# - course/ (15 modules)
# - project/ (capstone project)
# - cheatsheets/ (quick references)
# - troubleshooting/ (help when stuck)
```

### Step 2: Quick Win - Run Data Pipeline (10 minutes)

Get something working immediately for motivation:

```bash
# 1. Navigate to project
cd project

# 2. Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install required libraries
pip install pandas numpy matplotlib seaborn scikit-learn

# 4. Generate sample data
python scripts/00_generate_sample_data.py
# Creates: data/raw/customers_sample.csv (10,000 customer records)

# 5. Run complete pipeline
python scripts/run_data_pipeline.py
# This will:
# - Load data
# - Clean data (handle missing values, outliers)
# - Engineer features
# - Split train/test
# - Train model
# - Evaluate performance
# - Generate visualizations

# 6. Check results
ls -l outputs/
# You should see:
# - 01_eda_overview.png (data exploration charts)
# - 02_confusion_matrix.png (model performance)
# - 03_feature_importance.png (which features matter)
# - experiment_results.json (metrics)
```

**What you just accomplished:**
✅ Ran a complete ML pipeline end-to-end  
✅ Generated insights from data  
✅ Trained a churn prediction model  
✅ Evaluated model accuracy  
✅ Created visualizations  

**Time taken:** ~2 minutes (after dependencies installed)

### Step 3: Understand What Happened (15 minutes)

```bash
# 1. Read the visual guide
cat DATA_PIPELINE_VISUAL_GUIDE.md
# Shows the flow: Data → Clean → Features → Model → Predictions

# 2. Examine the generated data
head -20 data/raw/customers_sample.csv
# Fields: customer_id, age, tenure, monthly_charges, total_charges, churn

# 3. Check processed data
head -20 data/processed/customers_processed.csv
# Notice: missing values filled, outliers handled

# 4. View results
cat outputs/experiment_results.json
# Shows: accuracy, precision, recall, F1-score

# 5. Look at visualizations (open in image viewer)
# outputs/01_eda_overview.png - data distribution
# outputs/02_confusion_matrix.png - model predictions
# outputs/03_feature_importance.png - key factors
```

### Step 4: Explore the Course (30 minutes)

```bash
# 1. Start with overview
cat course/00-overview.md
# Understand: course structure, time required, what you'll learn

# 2. If new to data/ML, read beginner module
cat course/00.5-data-engineering-for-beginners.md
# DevOps engineers: this is essential
# Data engineers: skip if already familiar

# 3. Understand MLOps foundations
cat course/01-mlops-foundations.md
# Learn: ML lifecycle, roles, challenges, dev vs prod

# 4. Check module structure
ls course/
# 15 modules covering:
# - Data versioning (DVC)
# - Experiment tracking (MLflow)
# - Pipelines (Airflow, Kubeflow)
# - Model serving (FastAPI, KServe)
# - Monitoring (Prometheus, Grafana)
# - CI/CD, security, cost optimization
```

### Step 5: Set Up Full Development Environment (1 hour)

For more advanced work, set up Docker services:

```bash
# 1. Navigate to project
cd project

# 2. Copy environment variables
cp .env.example .env
# Edit .env if needed (default values work for local)

# 3. Start all services with Docker Compose
make compose-up
# OR: docker compose up -d

# This starts:
# - MLflow (port 5000) - experiment tracking
# - Prometheus (port 9090) - metrics
# - Grafana (port 3000) - dashboards
# - PostgreSQL - database
# - MinIO - S3-compatible storage

# 4. Verify services
make compose-ps
# OR: docker compose ps

# 5. Check health
curl http://localhost:5000  # MLflow
curl http://localhost:9090  # Prometheus
curl http://localhost:3000  # Grafana (login: admin/admin)
```

### Step 6: Train Model with Tracking (30 minutes)

```bash
# With MLflow running, train a tracked model
python src/train.py  # (when implemented)

# View in MLflow UI
open http://localhost:5000
# You'll see:
# - Experiments
# - Parameters used
# - Metrics (accuracy, precision, etc.)
# - Artifacts (model files, plots)
```

### Step 7: Deploy and Test API (30 minutes)

```bash
# 1. Start API server (when implemented)
make run-api
# OR: uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

# 2. Check API documentation
open http://localhost:8000/docs
# Interactive Swagger UI to test endpoints

# 3. Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      [34, 12, 65.5],
      [45, 24, 89.0]
    ]
  }'

# Expected response:
# {"predictions": [0, 0], "model_version": "1.0"}
# 0 = customer won't churn, 1 = customer will churn
```

### Step 8: Monitor Your System (15 minutes)

```bash
# 1. View Prometheus metrics
open http://localhost:9090
# Query: prediction_requests_total
# Query: prediction_latency_seconds

# 2. View Grafana dashboards
open http://localhost:3000
# Login: admin / admin
# Check pre-built dashboards (if available)

# 3. Check logs
make compose-logs
# OR: docker compose logs -f
```

---

## Folder Structure Explained

### Understanding the Repository Layout

```
mlops/
├── README.md                          # Start here - main documentation
├── PROJECT_EXECUTION_GUIDE.md         # This file - how to execute
├── IMPLEMENTATION_GUIDE.md            # Comprehensive implementation (1700+ lines)
├── COURSE_SUMMARY.md                  # Quick course overview
│
├── course/                            # Learning modules (15 total)
│   ├── 00-overview.md                 # Course introduction
│   ├── 00.5-data-engineering-for-beginners.md  # NEW: For DevOps engineers
│   ├── 01-mlops-foundations.md        # MLOps basics
│   ├── 02-env-and-packaging.md        # Python environments
│   ├── 03-data-versioning-and-quality.md
│   ├── 04-experiment-tracking-and-reproducibility.md
│   ├── 05-pipelines-orchestration.md
│   ├── 06-model-training-eval-and-selection.md
│   ├── 07-model-registry-and-governance.md
│   ├── 08-serving-and-apis.md
│   ├── 09-batch-streaming-and-scheduled-jobs.md
│   ├── 10-ci-cd-and-environments.md
│   ├── 11-observability-and-monitoring.md
│   ├── 12-drift-detection-and-retraining.md
│   ├── 13-security-compliance-and-cost.md
│   └── 14-comprehensive-review.md
│
├── project/                           # Capstone project (Churn Predictor)
│   ├── README.md                      # Project-specific documentation
│   ├── DATA_ENGINEERING_README.md     # NEW: Quick start for data pipeline
│   ├── DATA_PIPELINE_VISUAL_GUIDE.md  # NEW: Visual flow diagram
│   ├── Makefile                       # Commands (make help for list)
│   ├── docker-compose.yml             # Local development stack
│   ├── .env.example                   # Environment variables template
│   │
│   ├── data/                          # Data directory (gitignored, DVC tracked)
│   │   ├── raw/                       # Original data
│   │   ├── processed/                 # Cleaned data
│   │   ├── train/                     # Training split
│   │   └── test/                      # Test split
│   │
│   ├── scripts/                       # Utility scripts
│   │   ├── 00_generate_sample_data.py # NEW: Create practice data
│   │   └── run_data_pipeline.py       # NEW: Complete pipeline runner
│   │
│   ├── src/                           # Source code
│   │   ├── api.py                     # FastAPI serving
│   │   ├── train.py                   # Model training (to implement)
│   │   ├── preprocess.py              # Data preprocessing (to implement)
│   │   ├── batch_score.py             # Batch predictions (to implement)
│   │   └── detect_drift.py            # Drift detection (to implement)
│   │
│   ├── outputs/                       # NEW: Generated visualizations and results
│   │   ├── 01_eda_overview.png
│   │   ├── 02_confusion_matrix.png
│   │   ├── 03_feature_importance.png
│   │   └── experiment_results.json
│   │
│   ├── models/                        # Trained models (DVC tracked)
│   ├── notebooks/                     # Jupyter notebooks for exploration
│   ├── serving/                       # Serving configurations
│   ├── tests/                         # Test suites
│   └── infra/                         # Infrastructure as code
│       ├── terraform/                 # Cloud infrastructure
│       └── k8s/                       # Kubernetes manifests
│
├── cheatsheets/                       # Quick reference cards
│   ├── python-env.md
│   ├── dvc-mlflow.md
│   ├── docker-k8s.md
│   └── linux.md                       # NEW: Linux basics
│
├── troubleshooting/                   # Debugging help
│   └── triage-matrix.md               # Common issues and solutions
│
└── exams/                             # Assessment
    └── mock-exam-1.md                 # Practice certification
```

### Key Files Purpose

| File | Purpose | When to Use |
|------|---------|-------------|
| `README.md` (root) | Project overview, quick start | First thing to read |
| `PROJECT_EXECUTION_GUIDE.md` | Detailed execution steps | When ready to execute |
| `IMPLEMENTATION_GUIDE.md` | Complete implementation guide | For instructors, deep dive |
| `course/*.md` | Learning modules | Sequential learning |
| `project/README.md` | Project documentation | Working on capstone |
| `DATA_ENGINEERING_README.md` | Data pipeline quick start | First data pipeline run |
| `DATA_PIPELINE_VISUAL_GUIDE.md` | Visual data flow | Understanding data process |
| `Makefile` | Common commands | Daily development |
| `docker-compose.yml` | Service orchestration | Local development |

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Python module not found"
```bash
# Solution: Ensure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Verify
which python  # Should point to .venv/bin/python
python -c "import pandas"  # Should not error
```

#### Issue 2: "Port already in use"
```bash
# Solution: Check what's using the port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
kill -9 <PID>  # Replace <PID> with actual process ID
# OR: uvicorn src.api:app --port 8001
```

#### Issue 3: "Docker services won't start"
```bash
# Solution: Check Docker is running
docker ps

# If not, start Docker Desktop
# Then try again:
docker compose up -d

# Check logs for specific service
docker compose logs <service_name>
```

#### Issue 4: "Script fails with 'No such file or directory'"
```bash
# Solution: Create required directories
mkdir -p data/raw data/processed data/train data/test outputs

# OR: Run from correct directory
cd /path/to/mlops/project
python scripts/run_data_pipeline.py
```

#### Issue 5: "Out of memory when training model"
```bash
# Solution: Reduce data size
# Edit scripts/00_generate_sample_data.py
# Change: n_samples=10000 to n_samples=1000

# Regenerate data
python scripts/00_generate_sample_data.py
```

### Getting Help

1. **Check troubleshooting guide**: `troubleshooting/triage-matrix.md`
2. **Review cheatsheets**: `cheatsheets/` directory
3. **Search issues**: https://github.com/Dhananjaiah/mlops/issues
4. **Ask in discussions**: https://github.com/Dhananjaiah/mlops/discussions
5. **Read full implementation guide**: `IMPLEMENTATION_GUIDE.md`

---

## Next Steps

### After Completing This Guide

You've now:
✅ Set up your environment  
✅ Run your first data pipeline  
✅ Understand the project structure  
✅ Know which path to follow based on your role  

### Continue Your Journey

#### Path 1: Complete the Course
```bash
# Follow modules sequentially
cd course
cat 01-mlops-foundations.md  # Start here
# Work through 01 → 14
```

#### Path 2: Build the Capstone Project
```bash
# Implement remaining components
cd project/src
# Implement: train.py, preprocess.py, etc.
# Follow: project/README.md
```

#### Path 3: Deploy to Production
```bash
# Set up CI/CD
# Module: course/10-ci-cd-and-environments.md

# Deploy to Kubernetes
# Module: course/08-serving-and-apis.md

# Set up monitoring
# Module: course/11-observability-and-monitoring.md
```

#### Path 4: Advanced Topics
```bash
# Drift detection and automated retraining
# Module: course/12-drift-detection-and-retraining.md

# Security and compliance
# Module: course/13-security-compliance-and-cost.md
```

### Certification Preparation
```bash
# Take mock exams
cat exams/mock-exam-1.md
# Time yourself: 90 minutes
# Score yourself: aim for 80%+
```

### Community Contribution
```bash
# Share your learnings
# - Write a blog post about your journey
# - Create additional examples
# - Submit PRs for improvements
# - Help others in discussions
```

---

## Quick Reference Commands

### Daily Development
```bash
# Navigate to project
cd mlops/project

# Activate environment
source .venv/bin/activate

# Start services
make compose-up

# Run pipeline
python scripts/run_data_pipeline.py

# Train model
make run-train

# Start API
make run-api

# Run tests
make test

# View logs
make compose-logs

# Stop services
make compose-down
```

### Useful Make Targets
```bash
make help              # List all available commands
make quickstart        # Set up everything quickly
make install           # Install dependencies
make lint              # Check code quality
make test              # Run tests
make docker-build      # Build Docker images
make deploy-dev        # Deploy to dev environment
make clean             # Clean generated files
```

---

## Summary

This guide provided:
✅ Role-based execution paths  
✅ Step-by-step instructions  
✅ Explanation of new files/folders  
✅ Troubleshooting help  
✅ Next steps for continuing  

### Remember:
- **Students**: Follow the course modules sequentially
- **DevOps Engineers**: Start with data engineering basics
- **Data Engineers**: Focus on deployment and production
- **Instructors**: Use IMPLEMENTATION_GUIDE.md as primary resource

### Support:
- Issues: https://github.com/Dhananjaiah/mlops/issues
- Discussions: https://github.com/Dhananjaiah/mlops/discussions
- Documentation: All guides in this repository

**Happy Learning! 🚀**

---

*Last Updated: 2025-11-15*  
*Version: 1.0*

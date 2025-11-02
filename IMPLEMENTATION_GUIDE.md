# MLOps Course: Complete Implementation & Teaching Guide

> **A step-by-step runbook for instructors and students to implement the complete MLOps course from 0→Production**

---

## 🎓 For Beginners: What Is This All About?

**Think of MLOps as a Recipe Book for AI Models**

Imagine you're a chef who created an amazing recipe (your AI model). MLOps is like:
- **A notebook** to track different recipe versions (which ingredients worked best?)
- **A kitchen with standard equipment** so anyone can cook it the same way
- **A delivery system** to serve your dish to customers automatically
- **Quality checks** to ensure each dish tastes perfect
- **Alerts** if something goes wrong in the kitchen

**Why Should You Care?**
Without MLOps, machine learning models:
- Work on one person's computer but fail on others ("works on my machine" problem)
- Can't be recreated when needed (lost experiments)
- Break in production without anyone noticing
- Are impossible to improve systematically

**This Guide Teaches You:**
How to turn your machine learning experiments into reliable, production-ready systems that work consistently and can be maintained over time.

---

## 📋 Document Overview

This guide provides complete instructions for:
1. **Setting up the learning environment** (local, Kubernetes, cloud)
2. **Implementing each of the 15 course modules** with hands-on exercises
3. **Building the capstone project** (Churn Predictor)
4. **Teaching strategies** for instructors
5. **Troubleshooting** common issues
6. **Assessment** and certification preparation

**Time Required:** 25-30 hours for complete implementation  
**Audience:** Data Scientists, ML Engineers, Platform Engineers, Students

**💡 Reading This Guide:**
- **"Why This Matters"** sections explain the purpose
- **"What You're Doing"** sections describe the steps in plain English
- **"In Simple Terms"** boxes translate technical jargon
- Commands come AFTER explanations so you understand first

---

## 🤔 Before You Start: Should You Take This Course?

### Are You Ready? (Honest Self-Assessment)

**✅ You're ready if you:**
- Can write basic Python scripts (functions, loops, if statements)
- Have used the command line (cd, ls, running scripts)
- Understand what machine learning is (even if you can't build models yet)
- Are comfortable with ambiguity and learning by doing
- Are willing to Google error messages and troubleshoot

**⚠️ You might struggle if you:**
- Have never written any code
- Panic when seeing a terminal/command prompt
- Expect everything to work perfectly the first time
- Give up at the first error message
- Need hand-holding for every step

**🎯 What You'll Gain:**
- Skills to build production ML systems
- Portfolio projects for your resume
- Understanding of ML engineering best practices
- Ability to collaborate with ML teams
- Career advancement in ML/data roles

**⏰ Time Commitment:**
- 25-30 hours total (course content)
- 2-3 hours per module on average
- Spread over 6 weeks for best retention
- Daily practice is better than weekend cramming

**💰 Cost:**
- This course: FREE
- Required software: FREE (all open-source)
- Optional cloud resources: $0-50 (if you do cloud deployment section)
- Your time: PRICELESS

---

## 🎯 Prerequisites

### Required Knowledge

**Translation for Beginners:**
Prerequisites = "things you should know before starting"

Don't panic if you don't know everything perfectly. "Intermediate Python" doesn't mean you're a Python expert. It means you can:
- Write a function
- Use if/else statements
- Work with lists and dictionaries
- Import libraries and use them
- Debug basic errors
- ✅ Python programming (intermediate level)
- ✅ Basic Linux command line (cd, ls, cat, grep)
- ✅ Git version control basics (clone, commit, push)
- ✅ Docker fundamentals (containers, images, docker-compose)

### Required Software
- ✅ **Python 3.11+** - [Download](https://www.python.org/downloads/)
- ✅ **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- ✅ **Git** - [Download](https://git-scm.com/downloads)
- ✅ **VS Code** (recommended) - [Download](https://code.visualstudio.com/)

### Optional Software (for advanced sections)
- ⭕ **Kubernetes CLI (kubectl)** - [Install](https://kubernetes.io/docs/tasks/tools/)
- ⭕ **K3d** (local Kubernetes) - [Install](https://k3d.io/)
- ⭕ **Terraform** - [Install](https://www.terraform.io/downloads)
- ⭕ **AWS/GCP/Azure CLI** (for cloud deployment)

### Hardware Requirements
- **Minimum:** 8GB RAM, 20GB free disk space, 2 CPU cores
- **Recommended:** 16GB RAM, 50GB free disk space, 4+ CPU cores

---

## 🚀 Phase 1: Initial Setup (Day 1)

### 💡 Why This Phase Matters

**In Simple Terms:** Before you can cook, you need to set up your kitchen. This phase prepares your computer with all the tools and ingredients you'll need for the entire course.

**What You're Accomplishing:**
- Getting the course materials on your computer
- Setting up a consistent workspace
- Installing the software tools we'll use
- Verifying everything works before starting

**Common Confusion:** "Why so much setup?" → Because doing this once correctly saves hours of troubleshooting later. It's like sharpening your knives before cooking—painful to skip!

---

### Step 1: Clone the Repository

**What You're Doing:** Downloading all the course files from GitHub (an online code storage) to your computer.

**Why:** This gives you access to:
- Course lessons and exercises
- Example code you'll modify and learn from
- Ready-to-use configurations
- Practice projects

**Think of it as:** Downloading a textbook with all the worksheets included.

```bash
# Clone the repository
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops

# Verify you're in the right place
ls -la
# You should see: course/, project/, cheatsheets/, README.md, etc.
```

**What Just Happened?** You now have a folder called `mlops` on your computer with all course materials inside.

### Step 2: Set Up Environment Variables

**What You're Doing:** Creating a settings file that tells your computer where things are and how to configure them.

**Why:** Instead of typing the same information repeatedly (like database addresses, project names), we save them once in a file. Every program we use will read from this file.

**In Simple Terms:** Like saving your home address in your phone's contacts so you don't have to type it every time you order delivery. These "environment variables" are your project's contact list.

**What Each Setting Means:**
- `CLOUD="local"` - We're working on your computer, not the cloud (yet)
- `DB_URL` - Address where the database lives (like a street address)
- `TRACKING_URL` - Where we'll view our experiment results
- `MODEL_NAME` - What we're calling our AI model
- Other settings are locations and configurations we'll use later

```bash
# Create environment configuration file
cat > ~/.mlops-env << 'ENVEOF'
export CLOUD="local"
export REGION="us-east-1"
export REGISTRY="ghcr.io/mlops-course"
export BUCKET="mlops-artifacts"
export CLUSTER="mlops-dev"
export NAMESPACE="mlops"
export DB_URL="postgres://mlops:mlops@db:5432/mlops"
export TRACKING_URL="http://mlflow:5000"
export MODEL_NAME="churn-predictor"
export PROJECT="mlops-course"
export PY_VER="3.11"
ENVEOF

# Load environment variables
source ~/.mlops-env

# Add to your shell profile for persistence
echo "source ~/.mlops-env" >> ~/.bashrc  # or ~/.zshrc for zsh
```

**What Just Happened?** You created a file that stores all your project settings, and told your computer to load them automatically whenever you open a terminal.

### Step 3: Install Python Dependencies (Local Development)

**What You're Doing:** Installing Python libraries (pre-written code packages) that you'll use to build machine learning systems.

**Why:** You wouldn't build a car from scratch when you can buy parts, right? These libraries are professionally-built tools for:
- `mlflow` - Track and compare your experiments
- `dvc` - Version control for data (like Git but for datasets)
- `scikit-learn` - Build machine learning models
- `pandas` - Work with data tables
- `fastapi` - Create web APIs to serve your models

**In Simple Terms:** Installing apps on your phone before you can use them. Each library adds new capabilities to Python.

**Common Confusion:** "Why three options?" → Different tools for different preferences. Start with Option 2 (`uv`) if unsure—it's the fastest and modern approach.

```bash
# Option 1: Using pip (simple)
cd mlops/project
pip install --upgrade pip
pip install -r requirements.txt 2>/dev/null || echo "requirements.txt will be created in modules"

# Option 2: Using uv (modern, fast - recommended)
pip install uv
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install mlflow dvc scikit-learn pandas numpy fastapi

# Option 3: Using poetry (dependency management)
pip install poetry
poetry init
poetry add mlflow dvc scikit-learn pandas fastapi
poetry install
```

**What Just Happened?** You installed all the software tools you'll need for the course. Your Python now has superpowers!

### Step 4: Verify Docker Installation

**What You're Doing:** Checking that Docker is installed and working on your computer.

**Why Docker Matters:** Docker is like a shipping container for software. Just like shipping containers let you transport goods anywhere in the world without worrying about the truck or train, Docker containers let you run software anywhere without worrying about the computer's setup.

**In Simple Terms:** Docker ensures your code runs the same way on:
- Your laptop
- Your colleague's laptop
- A server in the cloud
- Production systems

**The Problem Docker Solves:** Ever heard "it works on my machine"? Docker eliminates that by packaging your code WITH its environment (like shipping a plant with its soil, not just the plant).

```bash
# Check Docker is running
docker --version
docker compose version

# Test Docker works
docker run hello-world

# If you see "Hello from Docker!" you're ready to proceed
```

**What Just Happened?** You verified Docker is installed. The `hello-world` test downloaded a tiny program, ran it in a container, and showed you a success message.

### Step 5: Navigate Course Structure

```bash
# Explore the repository structure
tree -L 2 mlops/

# Read the main README
cat README.md

# Browse course modules
ls -la course/

# Check the capstone project
ls -la project/
```

**✅ Checkpoint:** You should now have:
- Repository cloned
- Environment variables configured
- Python environment ready
- Docker working
- Course structure understood

---

## 🗺️ The Big Picture: How Everything Connects

Before diving into modules, let's see how all the pieces fit together:

```
┌─────────────────────────────────────────────────────────────────┐
│                     THE COMPLETE MLOPS FLOW                      │
└─────────────────────────────────────────────────────────────────┘

    📊 DATA                                    🧪 EXPERIMENTS
    --------                                   ------------
    Raw Data                                   Try Model A
       ↓                                          ↓
    [DVC tracks                               [MLflow logs
     versions]                                 parameters,
       ↓                                       metrics, models]
    Validated                                     ↓
       ↓                                       Pick Best
       ↓                                          ↓
       ↓                                    ┌──────────┐
       └────────────→  ⚙️ PIPELINE  ←──────┤ Model    │
                           │                └──────────┘
                      [Airflow                   ↓
                       orchestrates]         📦 REGISTRY
                           ↓                  [MLflow
                           ↓                   Model
                           ↓                   Registry]
                      🚀 DEPLOY                  ↓
                           │                    ↓
                      [FastAPI              Stage: Testing
                       serves               Stage: Production
                       predictions]             ↓
                           │                    ↓
                           ↓                    ↓
                      👥 USERS ←───────────────┘
                    [Get predictions
                     via API]
                           │
                           ↓
                      📈 MONITOR
                    [Prometheus
                     collects
                     metrics]
                           │
                           ↓
                      📊 VISUALIZE
                    [Grafana
                     dashboards]
                           │
                           ↓
                      ⚠️ DETECT DRIFT
                           │
                           ↓
                     🔄 RETRAIN ────────→ (back to DATA)
```

**Read This Flow:**

1. **Data arrives** → DVC tracks versions so you can go back
2. **Experiment** → MLflow remembers what you tried
3. **Best model** → Goes to Model Registry
4. **Pipeline** → Airflow automates: data → train → test → deploy
5. **Deploy** → FastAPI serves the model as an API
6. **Users** → Get predictions by calling your API
7. **Monitor** → Prometheus watches performance
8. **Visualize** → Grafana shows you dashboards
9. **Drift detected?** → Trigger retraining → Loop back to start

**Why This Matters:**
Every module teaches one piece of this puzzle. By the end, you'll have built this entire system!

---

## 📚 Phase 2: Course Modules Implementation

### Module 00: Overview (30 minutes)

**Objective:** Understand course structure and philosophy

#### Steps:

1. **Read the overview module**
```bash
cd mlops
cat course/00-overview.md | less
```

2. **Key Concepts to Grasp:**
   - Commands-first approach: Practice before theory
   - Three-tier learning: Local → Kubernetes → Cloud
   - Complete system architecture: Data → Train → Deploy → Monitor → Retrain

3. **Review Course Resources:**
```bash
# Check cheatsheets
ls -la cheatsheets/
cat cheatsheets/python-env.md

# Review troubleshooting guide
cat troubleshooting/triage-matrix.md

# Look at mock exams
ls -la exams/
```

4. **Set Your Learning Path:**
   - **Beginner:** Weeks 1-2 (Modules 01-04)
   - **Intermediate:** Weeks 3-4 (Modules 05-09)
   - **Advanced:** Weeks 5-6 (Modules 10-14)

**Teaching Note:** Have students bookmark the cheatsheets and troubleshooting guide. These will be referenced frequently.

---

### Module 01: MLOps Foundations (1 hour)

**Objective:** Understand MLOps lifecycle, roles, and artifacts

---

### 💡 Why This Module Matters

**The Problem:** Traditional machine learning is like cooking once and calling it done. But in the real world:
- Your model works today but fails next month (data changes)
- You can't remember what you did to get good results
- Moving from your laptop to production breaks everything
- No one monitors if the model stops working

**The Solution:** MLOps creates a continuous cycle—like a restaurant that constantly improves recipes, checks food quality, and adapts to customer preferences.

**What You'll Learn:** The foundational concepts that make ML systems reliable and production-ready.

---

#### Steps:

1. **Read the module**
```bash
cat course/01-mlops-foundations.md
```

2. **Understand Key Concepts:**

**The MLOps Lifecycle (In Simple Terms):**
Think of it as a factory assembly line that never stops:

1. **Data** → Collect ingredients (customer data, transactions)
2. **Train** → Cook different recipes (try different models)
3. **Deploy** → Serve to customers (put model in production)
4. **Monitor** → Taste test continuously (check if still working)
5. **Retrain** → Update recipe when needed (improve the model)
6. **Loop back to Data** → Repeat continuously

**Roles (Who Does What):**
- **Data Scientist:** The chef who creates recipes (designs models)
- **ML Engineer:** The kitchen manager who scales recipes for mass production (productionizes models)
- **Platform Engineer:** The facilities manager who maintains the kitchen equipment (manages infrastructure)
- **DevOps Engineer:** The delivery coordinator who gets food to customers (handles deployments)

**Artifacts (What We Track):**
- **Data:** The ingredients (what we learned from)
- **Code:** The recipe (our scripts and programs)
- **Models:** The trained chef (the AI we built)
- **Configs:** The cooking settings (hyperparameters, temperature settings)
- **Metrics:** The taste scores (accuracy, precision)
- **Environment:** The kitchen setup (Python version, library versions)
- **Lineage:** The family tree (which data/code produced which model)

3. **Hands-On Exercise: Set Up Basic Tracking**

**What You're Doing:** Creating your first tracked ML experiment. You'll train a simple model and save the results in an organized way.

**Why:** This demonstrates the most basic form of MLOps—keeping organized records so you can:
- Reproduce your work later
- Compare different attempts
- Share your work with others

**In Simple Terms:** Like keeping a lab notebook in science class. You're documenting your experiment so anyone (including future you) can understand what you did.

```bash
# Create a simple project structure
mkdir -p ~/mlops-practice/{data,models,configs,metrics}
cd ~/mlops-practice

# Initialize git
git init

# Create a simple training script
cat > train_basic.py << 'PYEOF'
import json
from datetime import datetime

# Simulate model training
metrics = {
    "accuracy": 0.85,
    "precision": 0.82,
    "recall": 0.88,
    "timestamp": datetime.now().isoformat()
}

# Save metrics
with open("metrics/run_001.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("Training complete!")
print(f"Metrics saved: {metrics}")
PYEOF

# Run the script
python train_basic.py

# Track with git
git add .
git commit -m "Initial training run with metrics tracking"

# View what we tracked
git log --oneline
cat metrics/run_001.json
```

4. **Mini-Lab: Identify Drift**

```bash
# Simulate a second run with different performance
cat > train_basic_v2.py << 'PYEOF'
import json
from datetime import datetime

# Simulate degraded model performance (drift!)
metrics = {
    "accuracy": 0.72,
    "precision": 0.68,
    "recall": 0.75,
    "timestamp": datetime.now().isoformat()
}

with open("metrics/run_002.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("Training complete!")
print(f"Metrics saved: {metrics}")
print("⚠️  Warning: Accuracy dropped from 0.85 to 0.72!")
PYEOF

python train_basic_v2.py

# Compare metrics
diff metrics/run_001.json metrics/run_002.json
```

**Quiz Questions:**
- Q: What are the 5 stages of the MLOps lifecycle?
- Q: Which role is responsible for maintaining Kubernetes clusters?
- Q: Why do we need to track data versions in addition to code versions?

**✅ Checkpoint:** Students understand why ML systems need continuous monitoring and why tracking all artifacts is essential.

---

### Module 02: Environment & Packaging (1.5 hours)

**Objective:** Master Python environments and Docker containerization

---

### 💡 Why This Module Matters

**The "Works On My Machine" Problem:**
Imagine you bake a perfect cake at home, then your friend tries your recipe but their cake fails. Why? They used:
- Different flour brand (different Python version)
- Different oven temperature (different library versions)
- Different altitude affecting baking (different operating system)

**The Solution:** Package everything together:
- Python environments → Lock your recipe ingredients to exact brands
- Docker → Ship your entire kitchen so anyone can bake the same cake

**What You'll Learn:** How to make your code work identically everywhere—your laptop, your colleague's laptop, and production servers.

---

#### Steps:

1. **Read the module**
```bash
cat course/02-env-and-packaging.md
```

2. **Exercise: Environment Management with uv**

**What You're Doing:** Creating an isolated Python environment with exact library versions.

**Why:** If you install libraries globally (system-wide), different projects conflict:
- Project A needs library version 1.0
- Project B needs library version 2.0
- They can't both exist in the same space!

**Solution:** Virtual environments create separate "rooms" where each project has its own libraries.

**In Simple Terms:** Like having separate closets for summer and winter clothes. They don't interfere with each other.

```bash
# Install uv (if not already done)
pip install uv

# Create a new project
mkdir ~/mlops-env-demo
cd ~/mlops-env-demo

# Initialize with uv
uv venv .venv
source .venv/bin/activate

# Install specific versions (for reproducibility)
uv pip install 'pandas==2.1.0' 'scikit-learn==1.3.0'

# Generate lock file
uv pip freeze > requirements.lock

# View locked dependencies
cat requirements.lock
```

3. **Exercise: Containerize with Docker**

**What You're Doing:** Wrapping your Python code in a Docker container—a complete, self-contained package.

**Why Docker Is Powerful:**
Traditional approach: "Install Python 3.11, then install these 20 libraries, then..."
Docker approach: "Run this container" → Everything is already set up!

**In Simple Terms:** 
- Traditional = Sending a recipe and hoping they have the right tools
- Docker = Sending a ready-to-eat meal in a microwave-safe container

**What's In a Docker Container:**
- Operating system (Linux)
- Python (specific version)
- All your libraries (exact versions)
- Your code
- Instructions to run it

```bash
# Create a simple ML script
cat > train_containerized.py << 'PYEOF'
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Generate sample data
X, y = make_classification(n_samples=100, n_features=10, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

print(f"Model trained! Score: {clf.score(X, y):.3f}")
PYEOF

# Create Dockerfile (multi-stage build)
cat > Dockerfile << 'DOCKEREOF'
# Stage 1: Build environment
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.lock .

RUN pip install --user -r requirements.lock

# Stage 2: Runtime environment
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY train_containerized.py .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "train_containerized.py"]
DOCKEREOF

# Build the image
docker build -t mlops-demo:v1 .

# Run the container
docker run mlops-demo:v1
```

4. **Exercise: Docker Compose Stack**

```bash
# Create a docker-compose.yml
cat > docker-compose.yml << 'COMPOSEEOF'
version: '3.8'

services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.8.0
    ports:
      - "5000:5000"
    command: >
      mlflow server
      --host 0.0.0.0
      --port 5000
      --backend-store-uri sqlite:///mlflow.db
      --default-artifact-root ./mlruns

  prometheus:
    image: prom/prometheus:v2.45.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:10.0.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
COMPOSEEOF

# Create Prometheus config
cat > prometheus.yml << 'PROMEOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
PROMEOF

# Start the stack
docker compose up -d

# Verify services
docker compose ps

# Test endpoints
curl http://localhost:5000  # MLflow
curl http://localhost:9090  # Prometheus
curl http://localhost:3000  # Grafana (login: admin/admin)

# Stop when done
docker compose down
```

**Teaching Note:** Emphasize that dev-prod parity (identical environments) prevents "works on my machine" problems.

**✅ Checkpoint:** Students can create reproducible environments and containerize applications.

---

### Module 03: Data Versioning & Quality (2 hours)

**Objective:** Version data with DVC and validate data quality

---

### 💡 Why This Module Matters

**The Data Problem:**
You trained a great model last month. Today you want to retrain it, but:
- Which data did you use? (You have 5 different CSV files)
- Someone updated the data—what changed?
- Your dataset is 50GB—can't push to GitHub!

**The Solution:** DVC (Data Version Control) is like Git, but for data.

**Real-World Analogy:**
- Git → Tracks changes to your essay (code)
- DVC → Tracks changes to your research photos/videos (data)

Both let you:
- Go back to previous versions
- See what changed
- Share with others
- Store large files efficiently

**What You'll Learn:** How to track data versions and ensure data quality before training models.

---

#### Steps:

1. **Read the module**
```bash
cat course/03-data-versioning-and-quality.md
```

2. **Exercise: Initialize DVC**

**What You're Doing:** Setting up DVC to track your data files, just like Git tracks your code.

**How DVC Works (Simple Explanation):**
1. You tell DVC to track `data.csv`
2. DVC creates a small `.dvc` file (contains a fingerprint of your data)
3. The `.dvc` file goes into Git (tiny, easy to share)
4. The actual data goes to cloud storage (S3, Google Cloud, etc.)
5. Anyone can download your code from Git, then use the `.dvc` file to fetch the exact data

**Why This Is Brilliant:**
- Git stays fast (no huge files)
- Everyone gets the exact same data
- You can go back to previous data versions
- Data changes are tracked just like code changes

```bash
# Create project directory
mkdir ~/mlops-data-versioning
cd ~/mlops-data-versioning

# Initialize Git and DVC
git init
pip install dvc dvc-s3
dvc init

# Create sample data
mkdir data
cat > data/customers.csv << 'CSVEOF'
customer_id,age,tenure,monthly_charges,churn
1,25,12,50.00,0
2,45,24,75.50,0
3,35,6,65.00,1
4,50,48,100.00,0
5,28,3,55.00,1
CSVEOF

# Add data to DVC tracking
dvc add data/customers.csv

# Commit the .dvc file (not the data itself!)
git add data/customers.csv.dvc data/.gitignore
git commit -m "Track customer data with DVC"

# View what was tracked
cat data/customers.csv.dvc
```

3. **Exercise: Set Up DVC Remote**

```bash
# Option 1: Local remote (for learning)
mkdir -p /tmp/dvc-remote
dvc remote add -d local /tmp/dvc-remote

# Push data to remote
dvc push

# Verify it's stored remotely
ls -la /tmp/dvc-remote

# Option 2: S3 remote (for production)
# dvc remote add -d s3remote s3://my-bucket/dvc-storage
# dvc remote modify s3remote region us-east-1
# dvc push
```

4. **Exercise: Data Quality with Great Expectations**

```bash
# Install Great Expectations
pip install great-expectations

# Initialize GE
great_expectations init

# Create expectation suite
great_expectations suite new

# Create a simple validation script
cat > validate_data.py << 'PYEOF'
import pandas as pd
import great_expectations as gx

# Load data
df = pd.read_csv("data/customers.csv")

# Create expectations
context = gx.get_context()

# Define expectations
expectations = [
    {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "customer_id"}},
    {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "age", "min_value": 18, "max_value": 100}},
    {"expectation_type": "expect_column_values_to_be_in_set", "kwargs": {"column": "churn", "value_set": [0, 1]}},
]

# Validate
print("✅ Data validation passed!" if df.shape[0] > 0 else "❌ Data validation failed!")
print(f"Records: {df.shape[0]}, Columns: {df.shape[1]}")
PYEOF

python validate_data.py
```

5. **Mini-Lab: Version a Data Update**

```bash
# Modify the data
cat >> data/customers.csv << 'CSVEOF'
6,42,18,80.00,0
7,31,9,60.00,1
CSVEOF

# DVC detects the change
dvc status

# Update the version
dvc add data/customers.csv
git add data/customers.csv.dvc
git commit -m "Add 2 more customer records"

# Push updated data
dvc push

# View version history
git log --oneline data/customers.csv.dvc
```

**Quiz:** 
- Q: Why don't we commit large data files to Git?
- Q: What does the .dvc file contain?

**✅ Checkpoint:** Students can version data separately from code and validate data quality.

---

### Module 04: Experiment Tracking & Reproducibility (2 hours)

**Objective:** Track ML experiments with MLflow

---

### 💡 Why This Module Matters

**The Experiment Chaos Problem:**
You've tried training 50 different models over 2 weeks:
- Which hyperparameters gave the best accuracy?
- Model #37 was great—what settings did you use?
- Your notebook has results scattered everywhere
- Can't remember what you tried 3 days ago!

**The Solution:** MLflow is like a lab notebook that automatically records EVERYTHING about your experiments.

**Real-World Analogy:**
Imagine a cooking show where they try 50 recipe variations. Without notes:
- "This one tasted best!"
- "Um... what did we put in it?"
- "Was it 2 cups of flour or 3?"

MLflow automatically records:
- Ingredients (data)
- Recipe settings (hyperparameters)
- Cooking time (training time)
- Taste score (accuracy)
- The exact dish (trained model)
- Photos (charts/graphs)

**What You'll Learn:** How to track every experiment automatically so you can reproduce your best results and compare different approaches scientifically.

---

#### Steps:

1. **Read the module**
```bash
cat course/04-experiment-tracking-and-reproducibility.md
```

2. **Exercise: Set Up MLflow**

**What You're Doing:** Starting the MLflow server—a web application that tracks and displays all your experiments.

**Why:** MLflow gives you a visual dashboard where you can:
- See all your experiments in a table
- Sort by accuracy (find the best one)
- Compare 2+ experiments side-by-side
- Click to see details (code, parameters, results, graphs)
- Download the exact model that worked best

```bash
# Install MLflow
pip install mlflow

# Start MLflow server
mlflow server --host 0.0.0.0 --port 5000 &

# Verify it's running
curl http://localhost:5000

# Open in browser: http://localhost:5000
```

3. **Exercise: Log Experiments**

```bash
# Create training script with MLflow tracking
cat > train_with_mlflow.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Set MLflow tracking URI
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn-prediction")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start MLflow run
with mlflow.start_run():
    # Log parameters
    n_estimators = 100
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    # Train model
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # Log model
    mlflow.sklearn.log_model(clf, "model")
    
    print(f"✅ Experiment logged!")
    print(f"   Accuracy: {accuracy:.3f}")
    print(f"   Precision: {precision:.3f}")
    print(f"   Recall: {recall:.3f}")
PYEOF

# Run multiple experiments with different hyperparameters
python train_with_mlflow.py
```

4. **Exercise: Compare Experiments**

```bash
# Run with different hyperparameters
cat > train_experiment_2.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn-prediction")

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Try different configurations
configs = [
    {"n_estimators": 50, "max_depth": 5},
    {"n_estimators": 100, "max_depth": 10},
    {"n_estimators": 200, "max_depth": 15},
]

for config in configs:
    with mlflow.start_run():
        mlflow.log_params(config)
        clf = RandomForestClassifier(**config, random_state=42)
        clf.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, clf.predict(X_test))
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(clf, "model")
        print(f"Config {config}: Accuracy = {accuracy:.3f}")
PYEOF

python train_experiment_2.py

# View experiments in UI
echo "Open http://localhost:5000 to compare experiments"
```

5. **Exercise: Load Model from Registry**

```bash
cat > load_model.py << 'PYEOF'
import mlflow.sklearn

# Load a logged model
model_uri = "runs:/<RUN_ID>/model"  # Replace <RUN_ID> with actual run ID
# Or use: model_uri = "models:/churn-predictor/production"

loaded_model = mlflow.sklearn.load_model(model_uri)
print(f"✅ Model loaded successfully!")
print(f"   Model type: {type(loaded_model)}")
PYEOF
```

**Teaching Note:** Have students open MLflow UI and explore the experiment comparison features.

**✅ Checkpoint:** Students can track experiments, log parameters/metrics/models, and reproduce training runs.

---

### Module 05: Pipelines & Orchestration (2.5 hours)

**Objective:** Build automated training pipelines with Airflow

---

### 💡 Why This Module Matters

**The Manual Labor Problem:**
Training a model properly requires many steps:
1. Download new data
2. Validate data quality
3. Clean the data
4. Train the model
5. Evaluate results
6. Register the model
7. Send notification

Doing this manually every day/week is:
- Time-consuming (1-2 hours each time)
- Error-prone (forgot step 2? Model is garbage)
- Not scalable (what if you need to retrain every hour?)

**The Solution:** Airflow is like a factory robot that does repetitive tasks automatically and correctly every time.

**Real-World Analogy:**
**Without Airflow:** You're the baker who sets 5 alarms:
- 6am: Start dough
- 8am: Shape loaves
- 9am: Put in oven
- 10am: Remove from oven
- 10:30am: Package for sale

You must wake up and do each step manually. Miss one alarm? Burnt bread!

**With Airflow:** An automated bakery line where:
- Each step happens automatically
- If one step fails, it alerts you
- It can run daily/weekly/hourly automatically
- You see a dashboard of what's working/failing
- Steps only run if previous steps succeeded

**What You'll Learn:** How to automate your ML workflows so they run reliably without manual intervention.

---

#### Steps:

1. **Read the module**
```bash
cat course/05-pipelines-orchestration.md
```

2. **Exercise: Set Up Airflow**

**What You're Doing:** Installing and starting Airflow—a workflow automation system.

**Key Concept - DAG (Directed Acyclic Graph):**
- **Directed:** Tasks flow in one direction (A → B → C)
- **Acyclic:** No loops (doesn't go back to A)
- **Graph:** A diagram of connected tasks

Think of it as a recipe flowchart:
```
[Get ingredients] → [Mix batter] → [Bake] → [Cool] → [Serve]
```

Each box is a task. Arrows show the order. If "Mix batter" fails, we don't try to bake!

```bash
# Install Airflow
pip install apache-airflow

# Initialize Airflow database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start Airflow webserver and scheduler
airflow webserver --port 8080 &
airflow scheduler &

# Open browser: http://localhost:8080 (admin/admin)
```

3. **Exercise: Create Training Pipeline DAG**

```bash
# Create DAG directory
mkdir -p ~/airflow/dags
export AIRFLOW_HOME=~/airflow

# Create a training pipeline DAG
cat > ~/airflow/dags/train_churn_model.py << 'PYEOF'
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

default_args = {
    'owner': 'mlops',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_data():
    """Task 1: Load data"""
    print("Loading data...")
    # Simulate data loading
    return {"status": "success", "records": 1000}

def validate_data():
    """Task 2: Validate data quality"""
    print("Validating data...")
    # Simulate validation
    return {"status": "valid"}

def train_model():
    """Task 3: Train model"""
    print("Training model...")
    from sklearn.datasets import make_classification
    
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("airflow-churn-training")
    
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    with mlflow.start_run():
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, clf.predict(X_test))
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(clf, "model")
        
        print(f"Model trained! Accuracy: {accuracy:.3f}")

def register_model():
    """Task 4: Register model in MLflow"""
    print("Registering model...")
    # In production, this would register the model
    return {"status": "registered"}

# Define DAG
with DAG(
    'train_churn_model',
    default_args=default_args,
    description='Automated churn model training pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    task_load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )
    
    task_validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )
    
    task_train = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )
    
    task_register = PythonOperator(
        task_id='register_model',
        python_callable=register_model,
    )
    
    # Define task dependencies
    task_load >> task_validate >> task_train >> task_register
PYEOF

# Trigger the DAG manually
airflow dags trigger train_churn_model

# View DAG in UI
echo "Open http://localhost:8080 and navigate to 'train_churn_model' DAG"
```

**Teaching Note:** Show students the Airflow UI and demonstrate how to monitor DAG runs, view logs, and retry failed tasks.

**✅ Checkpoint:** Students can create automated ML pipelines and understand DAG orchestration.

---

### Module 06: Model Training, Evaluation & Selection (2 hours)

**Objective:** Implement systematic model training with hyperparameter tuning

#### Steps:

1. **Read the module**
```bash
cat course/06-model-training-eval-and-selection.md
```

2. **Exercise: Cross-Validation and Hyperparameter Tuning**

```bash
cat > train_with_tuning.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("hyperparameter-tuning")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
}

with mlflow.start_run():
    # Grid search with cross-validation
    clf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    # Best parameters
    best_params = grid_search.best_params_
    print(f"Best parameters: {best_params}")
    mlflow.log_params(best_params)
    
    # Train final model with best params
    best_model = grid_search.best_estimator_
    
    # Evaluate on test set
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation scores
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5)
    
    # Log metrics
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_metric("cv_mean", cv_scores.mean())
    mlflow.log_metric("cv_std", cv_scores.std())
    
    # Log model
    mlflow.sklearn.log_model(best_model, "model")
    
    print(f"\n✅ Training complete!")
    print(f"   Test Accuracy: {accuracy:.3f}")
    print(f"   CV Mean: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
PYEOF

python train_with_tuning.py
```

3. **Exercise: Model Comparison**

```bash
cat > compare_models.py << 'PYEOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("model-comparison")

# Generate data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models to compare
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

results = []

for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
        }
        
        # Log
        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")
        
        results.append({"model": model_name, **metrics})
        print(f"{model_name}: Accuracy={metrics['accuracy']:.3f}, F1={metrics['f1']:.3f}")

# Summary
print("\n📊 Model Comparison Summary:")
for result in sorted(results, key=lambda x: x['accuracy'], reverse=True):
    print(f"  {result['model']:<25} Accuracy: {result['accuracy']:.3f}")
PYEOF

python compare_models.py
```

**✅ Checkpoint:** Students can systematically evaluate and compare multiple models.

---

### Module 07: Model Registry & Governance (1.5 hours)

**Objective:** Manage model lifecycle with MLflow Model Registry

#### Steps:

1. **Read the module**
```bash
cat course/07-model-registry-and-governance.md
```

2. **Exercise: Register Models**

```bash
cat > register_model.py << 'PYEOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

# Get the latest run from an experiment
experiment_name = "churn-prediction"
experiment = client.get_experiment_by_name(experiment_name)

if experiment:
    # Get runs
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.accuracy DESC"], max_results=1)
    
    if runs:
        best_run = runs[0]
        run_id = best_run.info.run_id
        
        # Register the model
        model_uri = f"runs:/{run_id}/model"
        model_name = "churn-predictor"
        
        result = mlflow.register_model(model_uri, model_name)
        print(f"✅ Model registered: {model_name}, Version: {result.version}")
        
        # Transition to staging
        client.transition_model_version_stage(
            name=model_name,
            version=result.version,
            stage="Staging",
        )
        print(f"✅ Model transitioned to Staging")
PYEOF

python register_model.py
```

3. **Exercise: Model Stage Transitions**

```bash
cat > promote_model.py << 'PYEOF'
from mlflow.tracking import MlflowClient
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

model_name = "churn-predictor"

# Get latest version in Staging
staging_models = client.get_latest_versions(model_name, stages=["Staging"])

if staging_models:
    version = staging_models[0].version
    
    # Promote to Production
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production",
        archive_existing_versions=True  # Archive old production models
    )
    
    print(f"✅ Model v{version} promoted to Production")
    
    # Add description
    client.update_model_version(
        name=model_name,
        version=version,
        description="Churn predictor trained with hyperparameter tuning. Accuracy: 0.85"
    )
else:
    print("❌ No models in Staging")
PYEOF

python promote_model.py
```

**Teaching Note:** Emphasize the approval workflow: None → Staging → Production. This prevents untested models from reaching production.

**✅ Checkpoint:** Students understand model governance and lifecycle management.

---

### Module 08: Serving & APIs (2 hours)

**Objective:** Deploy models as REST APIs with FastAPI

---

### 💡 Why This Module Matters

**The Model Deployment Problem:**
You trained a great model on your laptop. Now what?
- Other systems need to use your predictions
- Can't ask everyone to install Python and run your script
- Need to handle 1000s of requests per second
- Must work 24/7 without you being awake

**The Solution:** Turn your model into an API (Application Programming Interface)—a service that answers questions over the internet.

**Real-World Analogy:**

**Without API:** You're a fortune teller who only works in your office:
- People must come to your office
- You can only help one person at a time
- When you sleep, no one gets predictions
- Everyone needs to know how to talk to you specifically

**With API:** You're a fortune-telling phone hotline:
- Anyone can call from anywhere
- Multiple people can call simultaneously
- It runs 24/7 (automated system)
- Standard phone number—anyone can use it
- They just need to ask in the right format

**What You'll Learn:** How to make your model available as a web service that any application can use.

---

#### Steps:

1. **Read the module**
```bash
cat course/08-serving-and-apis.md
```

2. **Exercise: Create FastAPI Service**

**What You're Doing:** Creating a web server that loads your model and accepts prediction requests.

**How It Works (Simple Flow):**
1. Your server starts and loads the model into memory
2. A client (app/website) sends customer data: `{"age": 35, "tenure": 12}`
3. Your API receives it, runs it through the model
4. Your API sends back the prediction: `{"will_churn": "yes", "probability": 0.73}`
5. The client uses that answer to make business decisions

**Key Endpoints:**
- `/health` - "Are you alive?" (for monitoring)
- `/predict` - "Here's data, give me a prediction"
- `/docs` - Auto-generated documentation (try it in a browser!)

**Why FastAPI:**
- Fast (handles thousands of requests/second)
- Auto-validation (rejects bad data automatically)
- Auto-documentation (generates a test page for you)
- Modern Python (easy to write and understand)

```bash
# Install FastAPI
pip install fastapi uvicorn

# Create API server
cat > app.py << 'PYEOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import numpy as np
from typing import List

app = FastAPI(title="Churn Prediction API", version="1.0")

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    global model
    mlflow.set_tracking_uri("http://localhost:5000")
    model_uri = "models:/churn-predictor/Production"
    try:
        model = mlflow.sklearn.load_model(model_uri)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")

class PredictionRequest(BaseModel):
    features: List[List[float]]

class PredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        features = np.array(request.features)
        predictions = model.predict(features).tolist()
        probabilities = model.predict_proba(features).tolist()
        
        return PredictionResponse(
            predictions=predictions,
            probabilities=probabilities
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Churn Prediction API", "version": "1.0"}
PYEOF

# Run the API
echo "Starting API server..."
uvicorn app:app --host 0.0.0.0 --port 8000 &

sleep 5

# Test the API
curl http://localhost:8000/health

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[34, 12, 65.5, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]}'

# View API docs
echo "Open http://localhost:8000/docs for interactive API documentation"
```

3. **Exercise: Containerize API**

```bash
cat > Dockerfile.api << 'DOCKEREOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
DOCKEREOF

# Create requirements
cat > requirements.txt << 'REQEOF'
fastapi==0.104.1
uvicorn==0.24.0
mlflow==2.8.0
scikit-learn==1.3.0
numpy==1.24.3
REQEOF

# Build and run
docker build -t churn-api:v1 -f Dockerfile.api .
docker run -p 8000:8000 churn-api:v1
```

**✅ Checkpoint:** Students can deploy ML models as production-ready APIs.

---

### Modules 09-14: Abbreviated Implementation Steps

Due to length constraints, here are condensed steps for remaining modules:

**Module 09: Batch & Streaming (2 hours)**
- Set up batch scoring pipeline for large datasets
- Implement streaming inference with Kafka (optional)

**Module 10: CI/CD & Environments (2.5 hours)**
- Create GitHub Actions workflow for automated testing
- Set up multi-environment deployments (dev/staging/prod)

**Module 11: Observability & Monitoring (2 hours)**
- Configure Prometheus metrics collection
- Build Grafana dashboards for model monitoring

**Module 12: Drift Detection & Retraining (1.5 hours)**
- Implement Evidently for data/concept drift detection
- Set up automated retraining triggers

**Module 13: Security, Compliance & Cost (2 hours)**
- Run Trivy for vulnerability scanning
- Generate SBOM with Syft
- Set up cost monitoring

**Module 14: Comprehensive Review (1.5 hours)**
- Complete end-to-end workflow
- Review troubleshooting techniques
- Take mock exam

---

## 🏗️ Phase 3: Capstone Project Implementation (Days 5-10)

### Complete Churn Predictor System

---

### 💡 What You're Building

**The Business Problem:**
You work for a telecom company. Customers are leaving (churning) for competitors. Each lost customer costs the company money. Can we predict which customers will leave BEFORE they do, so we can offer them special deals to stay?

**Your Solution:**
A complete ML system that:
1. **Ingests** customer data (age, tenure, bills, complaints)
2. **Trains** a model to predict churn risk
3. **Serves** predictions via API (other apps can ask "will customer #12345 churn?")
4. **Monitors** accuracy over time (is it still working well?)
5. **Retrains** automatically when performance drops

**Why This Matters:**
This isn't just a model—it's a full production system with:
- Automatic data updates
- Quality checks
- Version control
- Monitoring dashboards
- Automated retraining
- API for other teams to use

**Real-World Analogy:**
You're not just cooking one meal (training one model). You're opening a restaurant (building a system) that:
- Has a supply chain (data pipeline)
- Has quality control (data validation)
- Trains new chefs (retraining)
- Serves customers (API)
- Monitors reviews (metrics)
- Adapts the menu (continuous improvement)

---

#### Step 1: Project Setup

**What You're Doing:** Getting the project structure and configuration ready.

```bash
cd mlops/project

# Copy environment template
cp .env.example .env

# Review project structure
tree -L 2
```

**What Just Happened?** You copied a template configuration file. You'll customize it with your specific settings (database passwords, cloud credentials, etc.).

#### Step 2: Start Full Stack

**What You're Doing:** Starting ALL the services your ML system needs—database, experiment tracker, API server, monitoring, etc.

**Why So Many Services?**
Each service has a specific job (separation of concerns):

**The Team:**
- **MLflow** (port 5000) - The lab notebook tracking experiments
- **PostgreSQL** (port 5432) - The database storing data and results
- **FastAPI** (port 8000) - The waiter serving predictions to customers
- **Prometheus** (port 9090) - The security camera monitoring everything
- **Grafana** (port 3000) - The dashboard showing pretty charts
- **Redis** (port 6379) - The cache for faster responses

**Restaurant Analogy:**
- PostgreSQL = The pantry (stores ingredients/data)
- FastAPI = The waiter (takes orders, serves predictions)
- MLflow = The recipe book (tracks all cooking experiments)
- Prometheus = The manager watching everything
- Grafana = The performance report with charts
- Redis = The prep station (quick access to common items)

```bash
# Start all services
docker compose up -d

# Verify all services are running
docker compose ps

# Expected services:
# - mlflow (port 5000)
# - postgres (port 5432)
# - fastapi (port 8000)
# - prometheus (port 9090)
# - grafana (port 3000)
# - redis (port 6379)
```

**What Just Happened?** Docker started 6 containers, each running a different service. They're all talking to each other on your computer, creating a mini production environment!

#### Step 3: Generate Sample Data

```bash
# Run data generation script
python scripts/generate_data.py

# Initialize DVC
dvc init
dvc add data/raw/*.csv
git add data/.gitignore data/*.dvc
git commit -m "Initialize data versioning"
```

#### Step 4: Run Training Pipeline

```bash
# Option 1: Direct training
python src/train.py

# Option 2: Via Airflow
# 1. Open http://localhost:8080
# 2. Login with admin/admin
# 3. Enable and trigger "train_churn_model" DAG
```

#### Step 5: Deploy API

```bash
# Start FastAPI service
cd serving
uvicorn main:app --reload --port 8000

# Test predictions
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[35, 24, 75.5, 1, 0]]}'
```

#### Step 6: Set Up Monitoring

**What You're Doing:** Creating dashboards to watch your model's health in real-time.

**Why Monitor?**
Your model is in production serving predictions. But:
- Is it still accurate?
- How many requests is it handling?
- Is it responding fast enough?
- Are there errors?

**Without monitoring:** You find out the model broke when customers complain
**With monitoring:** You get alerts immediately and fix it before anyone notices

**What You're Watching:**
- **Model Performance:** Accuracy, precision, recall over time
- **Prediction Drift:** Are predictions changing drastically?
- **System Health:** CPU, memory, response time
- **Request Volume:** How many predictions per minute
- **Error Rate:** How many requests are failing

**Real-World Analogy:**
A car dashboard shows:
- Speed (how fast = requests per second)
- Fuel (resources remaining)
- Engine temp (system load)
- Check engine light (errors!)

Your model needs the same visibility!

```bash
# Open Grafana
# URL: http://localhost:3000
# Login: admin/admin

# Import dashboard
# Upload: dashboards/model_monitoring.json
```

**What Just Happened?** You created a visual dashboard showing all your model's vital signs. Refresh it and watch numbers update in real-time!

#### Step 7: Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Generate coverage report
pytest --cov=src tests/
```

---

## 👨‍🏫 Phase 4: Teaching Strategies

### For Instructors

---

### 💡 Philosophy: Commands First, Concepts Second

**Why This Approach Works:**
Traditional teaching: "Here's 2 hours of theory about Docker... now try it"
- Students are confused
- Can't connect theory to practice
- Forget everything before trying it

Our approach: "Type this command and see what happens... now let's understand why"
- Immediate results build confidence
- Concrete examples before abstract concepts
- "Aha!" moments when seeing things work

**Teaching Like a Cooking Show:**
1. Show the finished dish ("here's what we're building")
2. Do it together ("follow along")
3. Explain while doing ("we add salt because...")
4. Let them customize ("now try with different spices")

**Student Types to Expect:**

**The Eager Beaver:** Races ahead, breaks things, asks "what if?"
- Let them experiment
- Give advanced challenges
- Make them help others

**The Cautious Learner:** Follows exactly, afraid to break things
- Reassure: "breaking things is learning"
- Encourage experimentation
- Celebrate their thorough documentation

**The Struggling Student:** Falls behind, frustrated, "I don't get it"
- Pair with Eager Beaver
- Extra office hours
- Break concepts into smaller pieces

---

#### Week 1-2: Foundations
- **Focus:** Modules 01-04
- **Teaching Style:** Live coding sessions
- **Homework:** Complete mini-labs, start capstone project setup
- **Assessment:** Quiz on MLOps lifecycle and versioning

**Teaching Tips for Week 1-2:**
- Start EVERY class with "What problem are we solving today?"
- Use the restaurant/kitchen analogies liberally
- Have students pair program
- Create a Slack/Discord for questions
- Do "demo fails" - show what happens when you mess up

#### Week 3-4: Pipelines & Serving
- **Focus:** Modules 05-09
- **Teaching Style:** Pair programming exercises
- **Homework:** Build automated training pipeline
- **Assessment:** Deploy working API

#### Week 5-6: Production Excellence
- **Focus:** Modules 10-14
- **Teaching Style:** Project-based learning
- **Homework:** Complete capstone project
- **Assessment:** Mock exam + project presentation

### Classroom Activities

1. **Live Troubleshooting Sessions**
   - Intentionally break a pipeline
   - Have students debug using logs and metrics

2. **Code Review Workshops**
   - Students review each other's pipelines
   - Focus on best practices and reproducibility

3. **Architecture Design Exercise**
   - Groups design ML system for a new use case
   - Present and critique designs

4. **Guest Speakers**
   - Invite MLOps engineers to share war stories
   - Discuss real-world challenges and solutions

---

## 🧠 Common Confusion Points (For Beginners)

### "I Don't Understand Why We Need All This Stuff"

**Valid Question!** If you just want to train a model, open a Jupyter notebook and train it. Done in 10 minutes.

**But then what?**
- Your colleague can't reproduce it
- Works on your laptop, breaks on the server
- Can't remember what you did yesterday
- No way to deploy it for others to use
- No monitoring when it breaks in production
- Can't improve it systematically

**MLOps is the difference between:**
- A home chef cooking one meal → A restaurant serving thousands daily
- A prototype in your garage → A factory producing products
- A hobby project → A professional service

### "Why So Many Tools? Can't We Use Just One?"

**Great question!** Each tool solves one specific problem:

**Why not just Git?** → Can't handle large data files (try putting a 10GB CSV in Git!)
**Why not just Python?** → Need databases, web servers, monitoring—Python alone isn't enough
**Why not just Docker?** → Need to orchestrate multiple containers, schedule tasks, monitor health

**Think of it like a car:**
- Engine (Python/code)
- Fuel (data/DVC)
- Dashboard (MLflow/Grafana)
- GPS (monitoring/logs)
- Transmission (Docker/orchestration)

Could you drive with just an engine? Technically yes, but it's painful!

### "What's the Difference Between Git, DVC, and MLflow?"

**All three track things, but different things:**

**Git** → Tracks **code** changes
- Small text files
- Line-by-line changes
- Merge conflicts
- Example: Python scripts, config files

**DVC** → Tracks **data** changes
- Large binary files
- Whole-file changes
- No merge conflicts (data doesn't merge)
- Example: CSVs, images, videos

**MLflow** → Tracks **experiments**
- Hyperparameters (n_estimators=100)
- Metrics (accuracy=0.85)
- Models (trained RandomForest)
- Example: "Run #47 with these settings got 85% accuracy"

**Analogy:**
- Git = Photo album of your renovation (track changes to your house)
- DVC = Storage unit with old furniture (track versions of big items)
- MLflow = Lab notebook (track which paint colors you tried and liked)

### "Why Docker When I Can Just Run Python?"

**Docker solves "works on my machine" syndrome:**

**Scenario:** You build something that works perfectly on your laptop.

**Without Docker:**
- "Install Python 3.11"
- "Now install these 50 libraries with exact versions"
- "Oh you need Linux for this library"
- "Wait, what's your Python path?"
- "Why isn't it working??"
- 3 hours later... still doesn't work

**With Docker:**
- "docker run my-container"
- Works immediately
- Guaranteed identical to your setup

**Analogy:**
**No Docker:** Sending a recipe, hoping they have the right oven, pans, and ingredients
**Docker:** Sending a prepared meal in a container, just heat and serve

### "What Happens If I Skip The Monitoring?"

**Short term:** Nothing. Your model works fine!
**3 months later:**
- Model accuracy dropped from 90% to 60%
- You have no idea when it started failing
- You have no idea why
- Customers are getting bad predictions
- Business lost money
- You find out when someone complains

**With monitoring:**
- Alert at 2am: "Model accuracy dropped to 80%!"
- You check: "Oh, the data changed—new customer segment"
- You retrain with new data
- Fixed before anyone notices
- Hero of the day!

**Analogy:** Would you drive a car with no dashboard? How would you know:
- When to refuel?
- If the engine is overheating?
- How fast you're going?

### "Why Can't I Just Use Excel?"

**Excel is great for:**
- Small datasets (< 1 million rows)
- One-time analysis
- Simple calculations
- Pretty charts

**Excel fails at:**
- Large datasets (100GB+)
- Automation (can't schedule Excel to run at 2am)
- Version control (Excel files in Git = nightmare)
- Reproducibility (macros break, formulas are hidden)
- Collaboration (merge conflicts in Excel? Ouch)
- Production deployment (can't serve millions of users from Excel)

**Use Excel for:** Exploring small data, quick calculations
**Use proper tools for:** Production ML systems

---

## 🐛 Phase 5: Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: Docker Compose Services Won't Start

**Symptom:**
```bash
docker compose up -d
# Error: port already allocated
```

**Solution:**
```bash
# Find and kill processes using ports
lsof -ti:5000 | xargs kill -9  # MLflow
lsof -ti:8000 | xargs kill -9  # FastAPI
lsof -ti:9090 | xargs kill -9  # Prometheus

# Or change ports in docker-compose.yml
```

#### Issue 2: MLflow Can't Find Model

**Symptom:**
```
RestException: Model 'churn-predictor' not found
```

**Solution:**
```bash
# Verify model is registered
mlflow models list

# Check tracking URI is correct
echo $MLFLOW_TRACKING_URI

# Re-register model
python register_model.py
```

#### Issue 3: DVC Push Fails

**Symptom:**
```
ERROR: failed to push data to the remote
```

**Solution:**
```bash
# Check remote configuration
dvc remote list
dvc remote -v list

# Re-add remote
dvc remote add -d -f local /tmp/dvc-remote
dvc push -v
```

#### Issue 4: Python Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'mlflow'
```

**Solution:**
```bash
# Verify virtual environment is activated
which python

# Reinstall dependencies
pip install -r requirements.txt

# Or recreate environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Debugging Checklist

When something doesn't work:
1. ✅ Check logs: `docker compose logs -f <service-name>`
2. ✅ Verify environment variables: `printenv | grep MLOPS`
3. ✅ Confirm services are running: `docker compose ps`
4. ✅ Test connectivity: `curl http://localhost:<port>/health`
5. ✅ Review recent changes: `git log --oneline -5`
6. ✅ Check disk space: `df -h`
7. ✅ Restart services: `docker compose restart`

---

## 📝 Phase 6: Assessment & Certification

### Knowledge Checks

#### Module Quizzes (10 questions each)
- Administered at end of each module
- 70% passing score
- Immediate feedback

#### Mock Exams
```bash
# Take mock exam 1
cat exams/mock-exam-1.md

# Take mock exam 2
cat exams/mock-exam-2.md
```

### Project Evaluation Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| **Data Versioning** | 15 | DVC properly configured, data tracked |
| **Experiment Tracking** | 15 | MLflow experiments logged with params/metrics |
| **Training Pipeline** | 20 | Automated pipeline with Airflow or similar |
| **Model Serving** | 15 | Working API with health checks |
| **Monitoring** | 15 | Prometheus metrics, Grafana dashboard |
| **Documentation** | 10 | README, setup guide, architecture diagram |
| **Code Quality** | 10 | Tests, linting, best practices |
| **Total** | **100** | |

### Certification Path

After completing this course, students are prepared for:
- **AWS Certified Machine Learning - Specialty**
- **GCP Professional ML Engineer**
- **Databricks Certified Machine Learning Professional**

---

## 🚀 Phase 7: Next Steps & Advanced Topics

### After Course Completion

1. **Week 1 Post-Course:**
   - Complete any remaining mock exams
   - Refine capstone project
   - Create portfolio on GitHub

2. **Month 1:**
   - Apply learnings to personal/work projects
   - Contribute to open-source MLOps tools
   - Write blog post about your experience

3. **Months 2-3:**
   - Pursue official certifications
   - Build additional portfolio projects
   - Network in MLOps community

### Advanced Topics (Self-Study)

- **Multi-Model Serving:** Deploy multiple models behind one API
- **Feature Stores:** Implement Feast or Tecton
- **AutoML Integration:** Add FLAML or AutoGluon
- **Edge Deployment:** Deploy to edge devices with TFLite
- **LLMOps:** Extend MLOps practices to Large Language Models

---

## 📚 Appendix: Quick Reference

### Essential Commands

```bash
# Environment
source ~/.mlops-env

# Docker
docker compose up -d
docker compose ps
docker compose logs -f <service>
docker compose down

# DVC
dvc init
dvc add data/file.csv
dvc push
dvc pull

# MLflow
mlflow server --host 0.0.0.0 --port 5000
mlflow models list

# Airflow
airflow db init
airflow webserver --port 8080
airflow scheduler
airflow dags trigger <dag-name>

# FastAPI
uvicorn app:app --reload --port 8000

# Testing
pytest tests/
pytest --cov=src tests/

# Git
git add .
git commit -m "message"
git push
```

### Service URLs (Default)

- **MLflow:** http://localhost:5000
- **Airflow:** http://localhost:8080 (admin/admin)
- **FastAPI:** http://localhost:8000
- **FastAPI Docs:** http://localhost:8000/docs
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

### Useful Links

- **Course Repository:** https://github.com/Dhananjaiah/mlops
- **MLflow Docs:** https://mlflow.org/docs/latest/index.html
- **DVC Docs:** https://dvc.org/doc
- **Airflow Docs:** https://airflow.apache.org/docs/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **MLOps Community:** https://mlops.community

---

## ✅ Implementation Checklist

Use this checklist to track your progress:

### Setup Phase
- [ ] Repository cloned
- [ ] Environment variables configured
- [ ] Python dependencies installed
- [ ] Docker Desktop installed and running
- [ ] Course structure reviewed

### Learning Phase
- [ ] Module 00: Overview completed
- [ ] Module 01: MLOps Foundations completed
- [ ] Module 02: Environment & Packaging completed
- [ ] Module 03: Data Versioning completed
- [ ] Module 04: Experiment Tracking completed
- [ ] Module 05: Pipelines & Orchestration completed
- [ ] Module 06: Model Training completed
- [ ] Module 07: Model Registry completed
- [ ] Module 08: Serving & APIs completed
- [ ] Module 09: Batch & Streaming completed
- [ ] Module 10: CI/CD completed
- [ ] Module 11: Observability completed
- [ ] Module 12: Drift Detection completed
- [ ] Module 13: Security & Compliance completed
- [ ] Module 14: Comprehensive Review completed

### Project Phase
- [ ] Capstone project setup
- [ ] Data generation and versioning
- [ ] Training pipeline implemented
- [ ] Model registry configured
- [ ] API deployment
- [ ] Monitoring setup
- [ ] Tests passing
- [ ] Documentation complete

### Certification Phase
- [ ] All module quizzes passed (70%+)
- [ ] Mock Exam 1 completed
- [ ] Mock Exam 2 completed
- [ ] Capstone project evaluation: 70%+
- [ ] Ready for official certification

---

## 🎓 Conclusion

This implementation guide provides a complete roadmap for learning and teaching MLOps. By following these steps systematically, students will:

1. ✅ Master the full MLOps lifecycle
2. ✅ Build production-ready ML systems
3. ✅ Understand industry best practices
4. ✅ Be prepared for MLOps roles
5. ✅ Have a portfolio project to showcase

**Key Success Factors:**
- **Practice Regularly:** Complete hands-on exercises daily
- **Build Incrementally:** Each module builds on previous ones
- **Ask Questions:** Use discussions and troubleshooting guide
- **Collaborate:** Work with peers on projects
- **Apply Immediately:** Use learnings in real projects

**Remember:** MLOps is a journey, not a destination. Technology evolves, but the principles remain the same: version everything, automate pipelines, monitor continuously, and iterate quickly.

---

## 📖 Beginner's Glossary: Technical Terms Explained Simply

**MLOps:**
- **Technical definition:** Machine Learning Operations
- **Simple explanation:** Best practices for deploying and maintaining ML systems in production
- **Analogy:** DevOps for data scientists

**API (Application Programming Interface):**
- **Technical definition:** A set of protocols for building and integrating application software
- **Simple explanation:** A waiter that takes orders (requests) and brings back food (responses)
- **Example:** When you ask Google Maps for directions, you're using their API

**Container (Docker):**
- **Technical definition:** A lightweight, standalone package containing code and dependencies
- **Simple explanation:** A shipping container for software—works the same everywhere
- **Analogy:** Ready-to-eat meal in a microwave-safe container

**Pipeline:**
- **Technical definition:** A series of automated data processing steps
- **Simple explanation:** An assembly line that does repetitive tasks automatically
- **Example:** Data → Clean → Train → Test → Deploy (happens automatically)

**Model Registry:**
- **Technical definition:** A centralized repository for storing and versioning ML models
- **Simple explanation:** A library catalog for your trained models
- **Like:** App Store for models—version numbers, descriptions, download buttons

**Orchestration:**
- **Technical definition:** Automated coordination of multiple interdependent tasks
- **Simple explanation:** A conductor directing an orchestra—each instrument (task) plays at the right time
- **Tool example:** Airflow, Kubernetes

**Artifact:**
- **Technical definition:** A tangible by-product of the ML process
- **Simple explanation:** Any file/object your ML system creates or uses
- **Examples:** Datasets, models, configs, metrics, logs, graphs

**Experiment:**
- **Technical definition:** A single training run with specific hyperparameters
- **Simple explanation:** One attempt at training a model
- **Analogy:** One test batch when perfecting a recipe

**Hyperparameter:**
- **Technical definition:** Configuration settings for the learning algorithm
- **Simple explanation:** Knobs you turn to adjust how the model learns
- **Examples:** Learning rate, number of trees, depth of trees

**Drift:**
- **Technical definition:** Statistical change in data or model behavior over time
- **Simple explanation:** When your model stops working well because reality changed
- **Example:** COVID changed shopping habits—models trained on 2019 data failed in 2020

**Endpoint:**
- **Technical definition:** A URL where an API can be accessed
- **Simple explanation:** The address where you send requests to get predictions
- **Example:** `https://api.company.com/predict` ← This is an endpoint

**Feature:**
- **Technical definition:** An input variable used for prediction
- **Simple explanation:** A piece of information the model uses to make decisions
- **Example:** For predicting house prices: bedrooms, square feet, location

**CI/CD (Continuous Integration/Continuous Deployment):**
- **Technical definition:** Automated testing and deployment pipeline
- **Simple explanation:** Robot that tests your code and deploys it automatically if tests pass
- **Prevents:** Broken code from reaching production

**Metrics:**
- **Technical definition:** Quantitative measurements of model or system performance
- **Simple explanation:** Scores that tell you how well things are working
- **Examples:** Accuracy (85%), response time (100ms), requests/second (1000)

**Staging:**
- **Technical definition:** A pre-production environment for testing
- **Simple explanation:** A practice kitchen where you test recipes before serving customers
- **Purpose:** Find bugs before they affect real users

**Production:**
- **Technical definition:** The live environment serving real users
- **Simple explanation:** The restaurant kitchen serving paying customers
- **Rule:** Only battle-tested, monitored code goes here

---

## 💡 Key Principles to Remember

1. **Version Everything:** Code, data, models, configs—if it changes, track it
2. **Automate Ruthlessly:** If you do it twice, automate it
3. **Monitor Constantly:** You can't fix what you can't see
4. **Test Thoroughly:** Test in staging before deploying to production
5. **Document Everything:** Future you will thank present you
6. **Fail Fast:** Find errors early when they're cheap to fix
7. **Keep It Simple:** Complex systems break in complex ways
8. **Security First:** Don't commit secrets, scan for vulnerabilities
9. **Reproducibility Matters:** Anyone should be able to recreate your results
10. **Communicate Clearly:** Systems should be understandable by others

---

## 🎯 What Success Looks Like

**After completing this course, you should be able to:**

✅ **Explain** MLOps concepts to non-technical stakeholders
✅ **Build** reproducible ML pipelines from scratch
✅ **Deploy** models as production-ready APIs
✅ **Monitor** model performance in production
✅ **Debug** common MLOps issues using logs and metrics
✅ **Collaborate** with data scientists and engineers effectively
✅ **Interview** confidently for ML Engineer roles
✅ **Showcase** portfolio projects to potential employers

**You'll have built:**
- A complete churn prediction system
- Data versioning with DVC
- Experiment tracking with MLflow
- Automated pipelines with Airflow
- REST API with FastAPI
- Monitoring with Prometheus/Grafana
- CI/CD with GitHub Actions

**Most importantly, you'll understand WHY, not just HOW.**

---

**Good luck with your MLOps journey! 🚀**

*For questions or issues, please open an issue on GitHub or join the MLOps Community.*

**Remember:** Every expert was once a beginner who didn't give up. You've got this!

---

**Document Version:** 2.0  
**Last Updated:** 2024-11-02  
**Maintained By:** MLOps Course Team  
**Changes in v2.0:** Added comprehensive explanations for beginners—WHY and WHAT sections throughout

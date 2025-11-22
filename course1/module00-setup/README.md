# Module 00: Setup and Overview

## 🎯 Learning Objectives

By the end of this module, you will:
- ✅ Have a working MLOps development environment
- ✅ Understand the course structure and philosophy
- ✅ Know the tools we'll be using
- ✅ Be ready to start Module 01

## ⏱️ Duration

30 minutes

## 📋 Prerequisites

- Basic Python knowledge (functions, loops, classes)
- Familiarity with command line
- Basic understanding of machine learning concepts
- A computer with 8GB+ RAM

## 🛠️ Required Software

### 1. Python 3.11 or higher

**Check if installed:**
```bash
python --version
# or
python3 --version
```

**Install if needed:**
- macOS: `brew install python@3.11`
- Ubuntu: `sudo apt install python3.11`
- Windows: Download from [python.org](https://www.python.org/downloads/)

### 2. Docker Desktop

**Check if installed:**
```bash
docker --version
docker compose version
```

**Install if needed:**
Download from [docker.com](https://www.docker.com/products/docker-desktop/)

### 3. Git

**Check if installed:**
```bash
git --version
```

**Install if needed:**
- macOS: `brew install git`
- Ubuntu: `sudo apt install git`
- Windows: Download from [git-scm.com](https://git-scm.com/)

### 4. Visual Studio Code (Recommended)

Download from [code.visualstudio.com](https://code.visualstudio.com/)

**Recommended Extensions:**
- Python
- Docker
- GitLens
- YAML

## 📥 Course Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Dhananjaiah/mlops.git

# Navigate to course1
cd mlops/course1

# Verify you're in the right place
ls -la
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Verify activation
which python
# Should show path to .venv/bin/python
```

### Step 3: Install Base Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install course dependencies
pip install -r requirements.txt

# Verify installations
pip list
```

### Step 4: Verify Setup

Run the verification script:

```bash
cd module00-setup/code
python verify_setup.py
```

You should see:
```
✅ Python version: OK
✅ Docker: OK
✅ Git: OK
✅ All dependencies: OK
✅ Setup complete!
```

## 📚 Course Overview

### What is MLOps?

**MLOps = Machine Learning Operations**

It's the set of practices that combines:
- Machine Learning
- DevOps
- Data Engineering

**Goal:** Deploy and maintain ML models in production reliably and efficiently.

### Why MLOps?

Without MLOps:
- ❌ "Works on my machine" problems
- ❌ Can't reproduce model results
- ❌ Models break in production silently
- ❌ No systematic way to improve
- ❌ Slow deployment cycles

With MLOps:
- ✅ Reproducible experiments
- ✅ Automated pipelines
- ✅ Monitored production systems
- ✅ Fast, safe deployments
- ✅ Continuous improvement

### Course Philosophy

**Commands First, Theory Second**

1. **Do it** - Run the code
2. **See results** - Observe what happens
3. **Understand why** - Learn the concepts
4. **Practice more** - Build muscle memory

### Tools We'll Use

| Tool | Purpose | When |
|------|---------|------|
| **Python** | Programming language | Throughout |
| **Git** | Version control | Throughout |
| **Docker** | Containerization | Module 02+ |
| **DVC** | Data version control | Module 03 |
| **MLflow** | Experiment tracking | Module 04 |
| **Airflow** | Pipeline orchestration | Module 05 |
| **FastAPI** | API serving | Module 08 |
| **Prometheus** | Monitoring | Later modules |
| **Grafana** | Visualization | Later modules |

## 🎯 Learning Path

### Week 1-2: Foundations
- Module 00: Setup ← **You are here**
- Module 01: MLOps Foundations
- Module 02: Environment & Packaging
- Module 03: Data Versioning
- Module 04: Experiment Tracking

### Week 3-4: Automation
- Module 05: Pipelines & Orchestration
- Module 06: Model Training
- Module 07: Model Registry
- Module 08: Serving & APIs

### Week 5-6: Production (Advanced)
- Module 09: Batch & Streaming
- Module 10: CI/CD
- Module 11: Monitoring
- Module 12: Drift Detection
- Module 13: Security & Compliance
- Module 14: Review & Best Practices

## 📖 How to Use Each Module

Each module follows this structure:

1. **Read README.md** - Overview and objectives
2. **Read transcript.md** - Detailed explanation
3. **Run code examples** - Hands-on practice
4. **Complete exercises** - Test understanding
5. **Check solutions** - Compare approaches

## 💡 Study Tips

### Do's ✅
- Follow modules sequentially
- Type code yourself (don't copy-paste)
- Experiment and break things
- Take notes and ask questions
- Practice regularly (2-3 hours/day)

### Don'ts ❌
- Skip modules
- Just read without coding
- Give up on errors
- Rush through
- Work when tired

## 🆘 Getting Help

### If Stuck

1. **Check transcript** - Look for explanations
2. **Read error messages** - They tell you what's wrong
3. **Search online** - Google the error
4. **Check discussions** - Someone may have asked
5. **Ask for help** - Open an issue

### Common Issues

See `TROUBLESHOOTING.md` in this module for solutions to common setup problems.

## ✅ Checklist

Before moving to Module 01, ensure:

- [ ] Python 3.11+ installed and working
- [ ] Docker Desktop installed and running
- [ ] Git installed and configured
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Verification script passes
- [ ] Understand course structure
- [ ] Read the transcript

## 🎓 What's Next?

Once your setup is verified:

1. Read the complete [transcript](transcript.md) for this module
2. Explore the [code examples](code/)
3. Move to [Module 01: MLOps Foundations](../module01-foundations/README.md)

## 📚 Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

**Questions?** Check the [FAQ](FAQ.md) or open an issue.

**Ready?** Let's move to the [transcript](transcript.md)!

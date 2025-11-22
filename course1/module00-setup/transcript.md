# Module 00: Setup and Overview - Complete Transcript

## Introduction

Welcome to the MLOps course! This is Module 00, where we'll set up your development environment and give you an overview of what you'll learn.

Think of this module as preparing your kitchen before cooking. You need the right tools, ingredients, and workspace before you can create something amazing.

## Part 1: Understanding MLOps (10 minutes)

### What is MLOps?

Let me start with a story. Imagine you're a data scientist who just built an amazing machine learning model. It works perfectly on your laptop - 95% accuracy! You're excited. You show it to your manager, and they say, "Great! Let's use it in production."

Now what? 

- How do you make it available to other systems?
- What if your teammate can't run it on their computer?
- How do you know if it's still working next month?
- What happens when the data changes?
- How do you update it without breaking everything?

This is where MLOps comes in.

**MLOps is like having a professional kitchen for your ML models:**

- **Recipe book** (code versioning) - So you can recreate dishes
- **Ingredient tracking** (data versioning) - Know what went into each dish
- **Quality control** (testing) - Ensure consistent results
- **Automated prep** (pipelines) - Speed up repetitive tasks
- **Delivery system** (APIs) - Get food to customers
- **Health monitoring** (observability) - Catch problems early
- **Continuous improvement** (feedback loops) - Get better over time

### Why Should You Care?

**Without MLOps:**
```
Data Scientist trains model → Sends notebook to engineer → 
Engineer can't run it → Back and forth for weeks → 
Finally deployed → Breaks after 2 weeks → No one knows why →
Start over
```

**With MLOps:**
```
Data Scientist trains model → Pushes to registry → 
Automated tests pass → Auto-deployed to staging → 
Tests pass → Auto-deployed to production → 
Monitoring catches issues → Auto-alerts → Auto-rollback if needed
```

See the difference? MLOps transforms ML from a one-time science project into a reliable engineering system.

## Part 2: The Problem MLOps Solves (10 minutes)

### Real-World Scenario

Let's say you work for a bank. You built a fraud detection model. Here's what happens without MLOps:

**Month 1:**
- You train model on your laptop
- It works great: 92% accuracy
- You save it as `model_final_v3_really_final.pkl`

**Month 2:**
- Your colleague asks: "Which data did you use?"
- You: "Um... I think it was the March data? Or was it April?"
- Colleague: "Can't reproduce your results"

**Month 3:**
- Model is finally in production
- Accuracy drops to 75%
- No one noticed for 3 weeks
- Bank lost money on missed fraud

**Month 4:**
- You want to retrain the model
- Can't find the original code
- Can't find the original data
- Have to start from scratch

This is the **reality for many teams** without MLOps.

### With MLOps

Same scenario, but with MLOps:

**Month 1:**
- Train model
- DVC tracks exact data version
- MLflow logs all parameters and metrics
- Git tracks code changes
- Model registered with metadata

**Month 2:**
- Colleague asks about data
- You share DVC link: "Here's the exact dataset"
- They reproduce your results in 5 minutes

**Month 3:**
- Model deployed via automated pipeline
- Monitoring detects accuracy drop immediately
- Alert sent automatically
- You investigate and find data drift
- Retrain with new data

**Month 4:**
- Automated retraining pipeline runs weekly
- Model stays accurate
- You work on improving features, not firefighting

This is the **power of MLOps**.

## Part 3: Course Structure (5 minutes)

### The Journey

Think of this course as building a house:

1. **Foundation** (Modules 00-02)
   - Set up tools
   - Learn basic concepts
   - Understand the "why"

2. **Framework** (Modules 03-05)
   - Version your data
   - Track experiments
   - Build pipelines

3. **Interior** (Modules 06-08)
   - Train models systematically
   - Manage model lifecycle
   - Serve predictions

4. **Utilities** (Modules 09-14)
   - Monitoring
   - Security
   - Optimization
   - Best practices

### Learning Philosophy

We follow a **"commands first, theory second"** approach:

1. **DO**: Run the command
2. **SEE**: Observe the result
3. **UNDERSTAND**: Learn why it works
4. **PRACTICE**: Do it again differently

**Example:**
```bash
# DO: Run this command
dvc add data/customers.csv

# SEE: A .dvc file is created
# UNDERSTAND: DVC tracks large files outside Git
# PRACTICE: Try with your own data
```

This is the opposite of traditional teaching:
- ❌ Traditional: 2 hours of theory → 10 minutes of practice
- ✅ Our way: 10 minutes of doing → Understanding while doing

### Tools Overview

Let's preview the tools you'll master:

**Git** - Like Microsoft Word's "Track Changes" but for code
- Tracks every change you make
- Lets you go back in time
- Enables collaboration

**Docker** - Like a shipping container for software
- Packages your code with its environment
- Runs the same everywhere
- Eliminates "works on my machine"

**DVC** - Like Git, but for data
- Tracks large data files
- Stores them efficiently
- Enables data versioning

**MLflow** - Like a lab notebook for experiments
- Logs every experiment automatically
- Compares different models
- Stores trained models

**Airflow** - Like a factory assembly line
- Automates workflows
- Schedules tasks
- Handles failures gracefully

**FastAPI** - Like a waiter for your model
- Serves predictions via API
- Handles requests efficiently
- Auto-generates documentation

## Part 4: Environment Setup (15 minutes)

### Why Proper Setup Matters

Imagine you're a carpenter. Would you start a project without checking if you have:
- A working saw?
- The right nails?
- A level surface to work on?

No! Same with MLOps. A proper setup prevents hours of frustration later.

### Step-by-Step Setup

#### 1. Check Python Version

```bash
python --version
```

**What you're doing:** Checking if Python is installed and what version.

**Why it matters:** 
- We need Python 3.11+ for modern features
- Older versions miss important capabilities
- Newer versions ensure compatibility

**If it shows < 3.11:** Install Python from python.org

**Example output:**
```
Python 3.11.5
```

#### 2. Check Docker

```bash
docker --version
docker compose version
```

**What you're doing:** Verifying Docker is installed and running.

**Why it matters:**
- Docker packages our applications
- Makes them run consistently everywhere
- Essential for production deployments

**If Docker isn't running:** Start Docker Desktop

**Example output:**
```
Docker version 24.0.6
Docker Compose version v2.21.0
```

#### 3. Clone Repository

```bash
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops/course1
```

**What you're doing:** Downloading all course materials to your computer.

**Why it matters:**
- Gets you all code examples
- Gets you all exercises
- Gets you all documentation

**What just happened:**
- Git downloaded the repository
- You now have a `mlops/course1` folder
- Inside are all modules and materials

#### 4. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**What you're doing:** Creating an isolated Python environment.

**Why it matters:**

Without virtual environments:
```
Project A needs package v1.0
Project B needs package v2.0
They conflict! 💥
```

With virtual environments:
```
Project A: Its own environment with v1.0
Project B: Its own environment with v2.0
No conflicts! ✅
```

**How to tell it worked:**
Your terminal prompt should change:
```
(.venv) user@computer:~/mlops/course1$
```

The `(.venv)` indicates the environment is active.

#### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**What you're doing:** Installing all required Python packages.

**Why it matters:**
- Installs MLflow, DVC, FastAPI, etc.
- Ensures exact versions (reproducibility)
- All examples will work

**What's in requirements.txt:**
```
mlflow==2.8.0          # Experiment tracking
dvc==3.30.0            # Data versioning
fastapi==0.104.1       # API framework
scikit-learn==1.3.0    # ML library
pandas==2.1.0          # Data manipulation
...
```

**This may take 2-3 minutes.** Getting coffee is acceptable. ☕

#### 6. Verify Setup

```bash
cd module00-setup/code
python verify_setup.py
```

**What you're doing:** Running a script that checks everything is correct.

**Why it matters:**
- Catches issues early
- Confirms you're ready to start
- Saves debugging time later

**Expected output:**
```
🔍 Checking Python version...
✅ Python 3.11.5 - OK

🔍 Checking Docker...
✅ Docker is running

🔍 Checking dependencies...
✅ mlflow: 2.8.0
✅ dvc: 3.30.0
✅ fastapi: 0.104.1
✅ scikit-learn: 1.3.0

🎉 All checks passed! You're ready to start learning.
```

**If you see errors:** Check the troubleshooting section below.

## Part 5: Understanding the Course Structure (5 minutes)

### How Each Module Works

Every module follows the same pattern. Once you know it, you can navigate easily.

```
module-name/
├── README.md          ← Start here: Overview and objectives
├── transcript.md      ← Read second: Detailed explanations
├── code/              ← Run third: Working examples
│   ├── 01_example.py
│   ├── 02_example.py
│   └── ...
├── exercises/         ← Complete fourth: Practice problems
│   ├── exercise01.md
│   └── ...
└── solutions/         ← Check last: Solution code
    ├── exercise01.py
    └── ...
```

### Your Learning Flow

For each module:

1. **Read README.md** (5 min)
   - Understand what you'll learn
   - See the big picture
   - Know the objectives

2. **Read transcript.md** (20-30 min)
   - Detailed explanations
   - Understand concepts deeply
   - See examples and analogies

3. **Run code examples** (30-60 min)
   - Type the code yourself
   - Observe results
   - Experiment and modify

4. **Complete exercises** (30-60 min)
   - Test your understanding
   - Apply what you learned
   - Build confidence

5. **Check solutions** (10-15 min)
   - Compare approaches
   - Learn alternative methods
   - Identify gaps

**Total time per module:** 2-3 hours

## Part 6: Success Tips (5 minutes)

### How to Succeed in This Course

**Do's ✅**

1. **Code Along**
   - Don't just read
   - Type every example
   - Muscle memory matters

2. **Experiment**
   - Change values
   - Break things
   - Fix them
   - Learn by doing

3. **Take Notes**
   - Write down insights
   - Document errors you fix
   - Track your progress

4. **Practice Daily**
   - 30 minutes daily > 4 hours once a week
   - Consistency beats intensity
   - Small wins compound

5. **Ask Questions**
   - No question is stupid
   - Others likely have the same question
   - Asking shows you're engaged

**Don'ts ❌**

1. **Don't Skip Modules**
   - Each builds on previous
   - Gaps will compound
   - Trust the sequence

2. **Don't Copy-Paste**
   - You learn by typing
   - Typing helps remember
   - You'll miss details

3. **Don't Give Up on Errors**
   - Errors are learning opportunities
   - Debugging builds skill
   - Every expert has seen these errors

4. **Don't Rush**
   - Understanding > Speed
   - Quality > Quantity
   - Take your time

5. **Don't Study Tired**
   - Tired = Poor retention
   - Take breaks
   - Fresh mind learns better

### When You Get Stuck

Follow this process:

1. **Read the error message carefully**
   - It usually tells you what's wrong
   - Google the exact error message

2. **Check the transcript**
   - Look for that specific topic
   - Read the explanation again

3. **Review the code**
   - Compare with the example
   - Look for typos
   - Check indentation

4. **Search online**
   - Stack Overflow
   - GitHub issues
   - Documentation

5. **Ask for help**
   - GitHub discussions
   - Course Slack (if available)
   - Open an issue

## Part 7: What's Next (5 minutes)

### Immediate Next Steps

Now that your setup is complete:

1. **Explore the code folder**
   ```bash
   cd module00-setup/code
   ls -la
   ```

2. **Run the example scripts**
   ```bash
   python 01_hello_mlops.py
   python 02_check_tools.py
   ```

3. **Read the exercises**
   ```bash
   cd ../exercises
   cat exercise01.md
   ```

4. **Move to Module 01**
   ```bash
   cd ../../module01-foundations
   cat README.md
   ```

### What You've Accomplished

Congratulations! You've:
- ✅ Installed all required software
- ✅ Set up your development environment
- ✅ Understood the course structure
- ✅ Learned the learning philosophy
- ✅ Seen the big picture of MLOps

### Looking Ahead

In the next modules, you'll:
- **Module 01**: Understand MLOps foundations
- **Module 02**: Master environments and Docker
- **Module 03**: Version data with DVC
- **Module 04**: Track experiments with MLflow
- **Module 05**: Build pipelines with Airflow

Each module builds on this foundation. You're ready!

## Summary

Let's recap what we covered:

**MLOps transforms ML from:**
- Science experiments → Engineering systems
- "Works on my machine" → Works everywhere
- Manual processes → Automated pipelines
- Hope → Confidence

**You now have:**
- A working development environment
- Understanding of the course structure
- A roadmap for learning
- The tools to succeed

**Remember:**
- Take it one module at a time
- Practice daily
- Experiment fearlessly
- Ask questions
- Enjoy the journey!

## Troubleshooting Common Issues

### Issue: Python version too old

**Error:**
```
Python 3.8.10
```

**Solution:**
Install Python 3.11+ from python.org or use your package manager.

### Issue: Virtual environment won't activate

**Error:**
```bash
source .venv/bin/activate
# No change in prompt
```

**Solution:**
```bash
# Try with full path
source /full/path/to/.venv/bin/activate

# Or recreate it
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
```

### Issue: pip install fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Try again
pip install -r requirements.txt

# If still fails, install one by one
pip install mlflow
pip install dvc
# etc.
```

### Issue: Docker not running

**Error:**
```
Cannot connect to the Docker daemon
```

**Solution:**
- Open Docker Desktop
- Wait for it to start (Docker icon should be active)
- Try command again

## Additional Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Docker Get Started](https://docs.docker.com/get-started/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [MLOps Community](https://mlops.community/)

---

**You're all set! Head to Module 01: [MLOps Foundations](../module01-foundations/README.md)**

**Questions? Open an issue or discussion on GitHub.**

**Happy learning! 🚀**

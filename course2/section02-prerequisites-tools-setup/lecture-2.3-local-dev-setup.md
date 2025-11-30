# Lecture 2.3 – Setting Up Local Dev Environment

---

## Time to Set Up

Alright, let's get your hands dirty. In this lecture, we'll set up everything you need to follow along with the course.

By the end, you'll have:
- Python installed and working
- Git configured
- Docker running
- A code editor ready
- All the key tools accessible

Let's go step by step.

---

## Step 1: Install Python

We need Python 3.9 or higher.

### Check If You Already Have Python

Open a terminal and run:

```bash
python --version
# or
python3 --version
```

If you see `Python 3.9.x` or higher, you're good. Skip to Step 2.

### Installing Python

**On macOS:**

Option A – Using Homebrew (recommended):
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

Option B – Download from python.org:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11.x
3. Run the installer

**On Windows:**

1. Go to https://www.python.org/downloads/
2. Download Python 3.11.x
3. **Important**: Check "Add Python to PATH" during installation
4. Run the installer

**On Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### Verify Installation

```bash
python3 --version
# Should show Python 3.9+ 

pip3 --version
# Should show pip version
```

---

## Step 2: Install Git

### Check If You Already Have Git

```bash
git --version
```

If you see a version number, you're good. Skip to Step 3.

### Installing Git

**On macOS:**

Git comes with Xcode Command Line Tools:
```bash
xcode-select --install
```

Or via Homebrew:
```bash
brew install git
```

**On Windows:**

1. Go to https://git-scm.com/download/win
2. Download and run the installer
3. Use default options (or customize if you know what you're doing)

**On Linux:**

```bash
sudo apt install git
```

### Configure Git

Set your name and email (these appear in your commits):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Verify:
```bash
git config --list
```

---

## Step 3: Install Docker

Docker lets us run containers. This is essential for MLOps.

### Installing Docker Desktop

**On macOS and Windows:**

1. Go to https://www.docker.com/products/docker-desktop
2. Download Docker Desktop
3. Run the installer
4. Follow the setup wizard
5. Start Docker Desktop

**On Linux:**

Follow the official guide: https://docs.docker.com/engine/install/

For Ubuntu:
```bash
# Add Docker's official GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Run Docker without sudo
sudo usermod -aG docker $USER
# Log out and log back in for this to take effect
```

### Verify Docker Installation

```bash
docker --version
# Should show Docker version

docker run hello-world
# Should download and run a test container
```

If you see "Hello from Docker!", you're good!

---

## Step 4: Install a Code Editor

You can use any editor, but I recommend VS Code.

### Installing VS Code

1. Go to https://code.visualstudio.com/
2. Download for your OS
3. Install

### Recommended Extensions

Once VS Code is installed, install these extensions (Ctrl+Shift+X or Cmd+Shift+X):

- **Python** (Microsoft) – Python language support
- **Docker** (Microsoft) – Docker support
- **GitLens** – Enhanced Git features
- **YAML** – YAML syntax support
- **Remote - Containers** – Work inside containers

---

## Step 5: Create a Project Directory

Let's create a home for your course work.

```bash
# Navigate to where you want the project
cd ~  # or wherever you prefer

# Create the course directory
mkdir mlops-course
cd mlops-course

# Verify
pwd
# Should show /Users/yourname/mlops-course or similar
```

---

## Step 6: Set Up a Virtual Environment

Virtual environments isolate your Python packages per project.

```bash
# Make sure you're in the project directory
cd ~/mlops-course

# Create a virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your prompt should now show (venv)
```

### Verify Virtual Environment

```bash
which python
# Should show .../mlops-course/venv/bin/python

pip list
# Should show only a few packages (pip, setuptools)
```

### Deactivating (When You're Done)

```bash
deactivate
# Prompt returns to normal
```

**Remember**: Always activate your virtual environment before working on the project!

---

## Step 7: Install Core Python Packages

With your virtual environment activated:

```bash
# Upgrade pip
pip install --upgrade pip

# Install core packages
pip install pandas numpy scikit-learn

# Install MLOps tools
pip install mlflow dvc fastapi uvicorn

# Install development tools
pip install pytest black flake8

# Save your dependencies
pip freeze > requirements.txt
```

### Verify Installations

```bash
python -c "import pandas; print(pandas.__version__)"
python -c "import sklearn; print(sklearn.__version__)"
python -c "import mlflow; print(mlflow.__version__)"
```

---

## Step 8: Initialize Git Repository

```bash
# Make sure you're in the project directory
cd ~/mlops-course

# Initialize Git
git init

# Create a .gitignore file
cat > .gitignore << 'EOF'
# Virtual environment
venv/
.venv/

# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
dist/
build/

# IDE
.vscode/
.idea/

# Data
*.csv
*.parquet
data/

# Models
*.pkl
*.joblib
models/

# MLflow
mlruns/

# DVC
.dvc/cache/

# Environment
.env
*.env

# OS
.DS_Store
Thumbs.db
EOF

# Make first commit
git add .gitignore
git commit -m "Initial commit with .gitignore"
```

---

## Step 9: Test Everything Works

Let's create a quick test script to verify everything is working.

Create a file called `test_setup.py`:

```python
#!/usr/bin/env python3
"""Test script to verify MLOps environment setup."""

import sys

def test_python_version():
    """Check Python version."""
    version = sys.version_info
    assert version.major == 3 and version.minor >= 9, \
        f"Python 3.9+ required, got {version.major}.{version.minor}"
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")

def test_core_packages():
    """Check core data science packages."""
    import pandas
    import numpy
    import sklearn
    print(f"✓ pandas {pandas.__version__}")
    print(f"✓ numpy {numpy.__version__}")
    print(f"✓ scikit-learn {sklearn.__version__}")

def test_mlops_packages():
    """Check MLOps packages."""
    import mlflow
    import dvc
    import fastapi
    print(f"✓ mlflow {mlflow.__version__}")
    print(f"✓ dvc {dvc.__version__}")
    print(f"✓ fastapi {fastapi.__version__}")

def test_dev_tools():
    """Check development tools."""
    import pytest
    import black
    print(f"✓ pytest {pytest.__version__}")
    print(f"✓ black {black.__version__}")

def main():
    """Run all tests."""
    print("\n🔍 Checking MLOps Environment Setup...\n")
    
    try:
        test_python_version()
        test_core_packages()
        test_mlops_packages()
        test_dev_tools()
        
        print("\n✅ All checks passed! Your environment is ready.\n")
        return 0
    except Exception as e:
        print(f"\n❌ Setup check failed: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Run it:

```bash
python test_setup.py
```

You should see all checkmarks. If anything fails, go back and install the missing component.

---

## Step 10: Test Docker

Let's make sure Docker works with a Python container:

```bash
# Run a Python container
docker run --rm python:3.11-slim python -c "print('Docker + Python works!')"
```

You should see "Docker + Python works!"

---

## Troubleshooting Common Issues

### "python: command not found"

- Try `python3` instead of `python`
- On Windows, check that Python was added to PATH
- Try closing and reopening your terminal

### "pip: command not found"

- Try `pip3` instead of `pip`
- Try `python -m pip` instead of `pip`

### "docker: command not found"

- Make sure Docker Desktop is installed and running
- On Linux, you might need to add your user to the docker group

### "Permission denied" on Linux/Docker

- Run: `sudo usermod -aG docker $USER`
- Log out and log back in

### Virtual environment issues

- Delete the venv folder and recreate it
- Make sure you're using Python 3.9+

---

## What You've Set Up

Let's recap:

| Tool | Purpose | Verification |
|------|---------|--------------|
| Python 3.9+ | Programming | `python --version` |
| Git | Version control | `git --version` |
| Docker | Containers | `docker run hello-world` |
| VS Code | Editor | Opens without error |
| Virtual env | Isolation | `which python` shows venv |
| Core packages | Data science | `test_setup.py` passes |

---

## Recap

You now have:
- Python 3.9+ installed
- Git configured with your identity
- Docker running
- VS Code (or your preferred editor)
- A project directory with virtual environment
- Core Python packages installed
- Everything verified working

---

## What's Next

Now that your environment is ready, let's look at how to structure an MLOps project properly.

In the next lecture, we'll design the folder structure for our course project.

---

**Next Lecture**: [2.4 – Project Structure for an MLOps Course Project](lecture-2.4-project-structure.md)

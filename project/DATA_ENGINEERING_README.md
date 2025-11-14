# Data Engineering for Beginners - Quick Start Guide

**👋 Welcome DevOps Engineers!**

This guide is specifically designed for you - someone who knows Docker, Kubernetes, and CI/CD, but has never worked with data science or machine learning.

## 🎯 What You'll Learn

By following this guide, you'll understand:
- **What data engineers do** and why it matters for MLOps
- **How to work with data** using Python and pandas
- **How to prepare data** for machine learning models
- **The basics of training models** without the complex math
- **How this fits into** the DevOps workflow you already know

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
# Navigate to the project directory
cd /home/runner/work/mlops/mlops/project

# Create a virtual environment (isolates dependencies)
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required libraries
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### Step 2: Generate Sample Data

```bash
# Create sample customer data (10,000 records)
python scripts/00_generate_sample_data.py
```

**What this does:** Creates a CSV file with fake customer data including messiness like real data (missing values, outliers, duplicates).

### Step 3: Run the Complete Pipeline

```bash
# Run the entire data engineering pipeline
python scripts/run_data_pipeline.py
```

**What this does:**
1. ✅ Loads and explores data
2. ✅ Cleans messy data
3. ✅ Creates useful features
4. ✅ Prepares data for ML
5. ✅ Trains a churn prediction model
6. ✅ Evaluates performance

**Time:** ~2 minutes

### Step 4: Check the Results

```bash
# View the visualizations created
ls -lh outputs/

# Files created:
# - 01_eda_overview.png - Data exploration visualizations
# - 02_confusion_matrix.png - Model performance matrix
# - 03_feature_importance.png - Which features matter most
# - experiment_results.json - Performance metrics
```

## 📚 Learning Path

### Option 1: Interactive Learning (Recommended)

**Use Jupyter Notebook** for hands-on, step-by-step learning:

```bash
# Start Jupyter
jupyter notebook

# Open: notebooks/data_engineering_tutorial.ipynb
# Follow along with code examples and exercises
```

**Why Jupyter?**
- Run code cell-by-cell
- See immediate results
- Easy to experiment
- Like a REPL for data science

### Option 2: Read the Full Guide

**Read the comprehensive module:**

```bash
# Open in your favorite editor
code course/00.5-data-engineering-for-beginners.md

# Or read on GitHub
# https://github.com/Dhananjaiah/mlops/blob/main/course/00.5-data-engineering-for-beginners.md
```

**What's in it:**
- Detailed explanations of every concept
- Side-by-side code with comments
- DevOps analogies for everything
- Common mistakes and how to avoid them
- Exercises to practice

## 🛠️ Tools You'll Use (The Toolkit)

### pandas - Your Excel in Code
```python
import pandas as pd
df = pd.read_csv('data.csv')  # Load data
df.head()                      # View first rows
df.describe()                  # Get statistics
```

**Think of it as:** `jq` for CSV/JSON, but way more powerful

### numpy - Math at Scale
```python
import numpy as np
mean = np.mean(data)     # Calculate average
std = np.std(data)       # Calculate standard deviation
```

**Think of it as:** Batch operations like `xargs` but for numbers

### scikit-learn - ML Made Easy
```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)    # Train
predictions = model.predict(X_test)  # Predict
```

**Think of it as:** Pre-built, tested libraries (like nginx vs writing your own server)

### matplotlib/seaborn - Visualizations
```python
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.show()
```

**Think of it as:** Grafana for data exploration

## 🎓 Key Concepts Explained

### 1. Features = Input Columns
In DevOps terms: Like environment variables for your model
- `age`, `income`, `login_count` are all features
- The model uses these to make predictions

### 2. Target = What You're Predicting
In DevOps terms: Like the exit code of a script (0=success, 1=failure)
- In churn prediction: 0=customer stays, 1=customer leaves

### 3. Training = Teaching the Model
In DevOps terms: Like fine-tuning autoscaling rules based on past traffic
- Show the model examples with answers
- It learns patterns from the data

### 4. Test Set = Staging Environment
In DevOps terms: Like testing in staging before prod
- Never train on test data
- Test set simulates unseen data

### 5. Metrics = SLIs/SLOs
In DevOps terms: Like measuring latency, uptime, error rate
- Accuracy = % correct predictions
- Precision = quality of predictions
- Recall = coverage of predictions

## 📁 File Structure

```
project/
├── data/
│   ├── raw/                    # Original data (like source code)
│   │   └── customers.csv
│   ├── processed/              # Cleaned data (like compiled code)
│   │   ├── customers_cleaned.csv
│   │   └── customers_with_features.csv
│   ├── train/                  # Training data
│   └── test/                   # Test data
├── models/                     # Trained models (like Docker images)
│   ├── churn_model.pkl
│   ├── scaler.pkl
│   └── imputer.pkl
├── outputs/                    # Results (like logs/metrics)
│   ├── 01_eda_overview.png
│   ├── 02_confusion_matrix.png
│   ├── 03_feature_importance.png
│   └── experiment_results.json
├── scripts/                    # Automation scripts
│   ├── 00_generate_sample_data.py
│   └── run_data_pipeline.py
└── notebooks/                  # Interactive tutorials
    └── data_engineering_tutorial.ipynb
```

## 🔄 The Data Pipeline (Like CI/CD)

```
┌─────────────┐
│ Raw Data    │  ← Like source code in Git
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Exploration │  ← Like code review
│ (EDA)       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Cleaning    │  ← Like linting/formatting
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Feature     │  ← Like preprocessing/compilation
│ Engineering │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Split       │  ← Like dev/staging/prod
│ Train/Test  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Train Model │  ← Like building a container
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Evaluate    │  ← Like integration tests
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Deploy      │  ← Like pushing to production
└─────────────┘
```

## 🎯 Common Questions

### "Why do I need to learn this?"
As MLOps becomes more important, DevOps engineers are expected to understand the ML workflow. This helps you:
- Package ML applications correctly
- Debug data pipeline issues
- Understand what data scientists need
- Build better infrastructure for ML

### "Isn't this just for data scientists?"
No! Modern MLOps requires collaboration. You need to understand:
- What data scientists produce (models, datasets)
- What they need (compute, storage, versioning)
- How to operationalize their work (APIs, batch jobs, monitoring)

### "This looks complicated!"
It's actually simpler than it looks! We're just:
1. Loading data (like reading a config file)
2. Cleaning it (like validating inputs)
3. Creating features (like calculating metrics)
4. Training a model (like fine-tuning parameters)
5. Deploying it (what you already do!)

### "Do I need to understand the math?"
No! You don't need to understand the math behind algorithms, just like you don't need to understand TCP/IP implementation to use Docker networking. You need to:
- Know what tools to use
- Understand inputs and outputs
- Interpret results
- Debug issues

## 🚀 Next Steps

After completing this guide:

1. ✅ **Understand the basics** - You now know what data engineers do
2. ✅ **Move to Module 01** - [MLOps Foundations](../course/01-mlops-foundations.md)
3. ✅ **Learn data versioning** - Module 03 (DVC)
4. ✅ **Track experiments** - Module 04 (MLflow)
5. ✅ **Build pipelines** - Module 05 (Airflow)

## 💡 Tips for DevOps Engineers

### Think in Analogies
- **Data versioning (DVC)** = Git for datasets
- **Experiment tracking (MLflow)** = Version control for models
- **Feature engineering** = ETL pipeline
- **Model training** = Building a container
- **Model deployment** = Releasing to production

### Use Your Existing Skills
- **Docker** - Package models as containers
- **Kubernetes** - Deploy models at scale
- **CI/CD** - Automate training and deployment
- **Monitoring** - Track model performance
- **Logging** - Debug data pipeline issues

### Start Simple
1. Get one model working locally
2. Containerize it
3. Deploy to staging
4. Add monitoring
5. Automate with CI/CD

## 📚 Resources

### Documentation
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/)
- [NumPy Basics](https://numpy.org/doc/stable/user/basics.html)

### Practice Datasets
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php)
- [AWS Open Data](https://registry.opendata.aws/)

### Free Courses
- [DataCamp: Intro to Python for Data Science](https://www.datacamp.com/)
- [Google's ML Crash Course](https://developers.google.com/machine-learning/crash-course)
- [Fast.ai Practical Deep Learning](https://course.fast.ai/)

## 🤝 Need Help?

- **Issues**: [GitHub Issues](https://github.com/Dhananjaiah/mlops/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Dhananjaiah/mlops/discussions)
- **Slack**: MLOps Community

## ✅ Self-Check

Before moving to the next module, make sure you can:

- [ ] Load a CSV file with pandas
- [ ] Check for missing values and outliers
- [ ] Create a new feature from existing columns
- [ ] Split data into train and test sets
- [ ] Scale features using StandardScaler
- [ ] Train a simple classifier
- [ ] Evaluate model with accuracy, precision, recall

If you checked all boxes → **You're ready for MLOps!** 🎉

---

**Happy Learning! 🚀**

[← Back to Main README](../README.md) | [Next: Module 01 - MLOps Foundations →](../course/01-mlops-foundations.md)

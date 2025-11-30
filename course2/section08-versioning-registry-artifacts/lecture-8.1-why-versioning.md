# Lecture 8.1 – Why Versioning Matters (Data + Code + Model Together)

## Human Transcript

Welcome to Section 8. Today we're going to talk about versioning. And I know, versioning sounds boring. But trust me, this is one of those things that separates amateur ML projects from production-grade systems.

Let me tell you a story. I was working with a team that had a model in production. It was working great. Then one day, the model's predictions started looking weird. Accuracy dropped. Customers were complaining. The team went into panic mode.

They asked: "What changed?" But nobody knew. Had the code changed? Maybe. Had the data changed? Probably. Had the model been retrained? Someone thought so. But there was no way to know for sure because nothing was versioned properly.

They spent three days debugging. Three days of senior engineers' time wasted. And in the end, the problem was a data pipeline that had started including a new column that confused the model. If they had proper versioning, they would have found this in minutes.

So what do we mean by versioning? In traditional software, you version your code with Git. Commit hash tells you exactly what code was running. But in ML, code is only part of the equation. You also have data and models. And all three need to be versioned together.

Think about it this way. Your model is a function of:
- The training code (how you train)
- The training data (what you train on)
- The hyperparameters (settings you chose)
- Random seeds (for reproducibility)

If any of these change, your model changes. So you need to track all of them.

Let's break this down.

Code versioning. This one you probably already know. Git is the standard. Every change you make to your code is tracked. You can see exactly what changed, when, and who changed it. You can roll back to any previous version. You can compare versions.

```bash
# See what code was running last week
git checkout abc123

# Compare two versions
git diff abc123 def456

# See who changed what
git blame train.py
```

Data versioning. This is where it gets tricky. Data is often big. Too big for Git. And data changes in different ways than code. You might add new records. You might fix errors in existing records. You might get new features.

Tools for data versioning include:
- DVC (Data Version Control) - works like Git but for data
- Delta Lake - versioned data lake format
- LakeFS - Git-like interface for data lakes
- Custom solutions using S3 versioning or timestamps

With DVC, for example:

```bash
# Track a data file
dvc add data/customers.csv

# Commit the reference (not the data itself)
git add data/customers.csv.dvc
git commit -m "Add customer data v1"

# Later, see what data was used for a specific commit
git checkout abc123
dvc checkout
```

Model versioning. Models are the output of training. They're binary files, often large. And you need to track:
- The model file itself
- What code was used to train it
- What data was used to train it
- The metrics it achieved
- The hyperparameters used

Tools include:
- MLflow Model Registry
- SageMaker Model Registry
- Weights & Biases
- Neptune.ai
- Custom solutions

Here's why all three need to be connected. Imagine this scenario:

You have model v1 in production. It was trained with code commit abc123 and data version d1. Everything is fine.

You retrain with new data (version d2). The model performs better in testing. You deploy it as v2.

A week later, you notice issues. You want to compare v2 to v1. What changed?

Without versioning: You have no idea. You're guessing.

With proper versioning: You can see that v1 used data d1 and v2 used data d2. You can compare the data versions. You can see exactly what rows were added or changed. You find the problem.

Here's how you might structure this in practice:

```python
# training/train.py
import mlflow
import git
import hashlib

def get_code_version():
    """Get current git commit hash."""
    repo = git.Repo(search_parent_directories=True)
    return repo.head.object.hexsha

def get_data_hash(filepath):
    """Get hash of data file for versioning."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def train_model(data_path, hyperparams):
    mlflow.start_run()
    
    # Log versions
    mlflow.log_param("code_version", get_code_version())
    mlflow.log_param("data_hash", get_data_hash(data_path))
    mlflow.log_param("data_path", data_path)
    
    # Log hyperparameters
    for key, value in hyperparams.items():
        mlflow.log_param(key, value)
    
    # Train...
    model = do_training(data_path, hyperparams)
    
    # Log metrics
    mlflow.log_metric("accuracy", model.accuracy)
    mlflow.log_metric("f1_score", model.f1)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    mlflow.end_run()
```

Now every training run is connected to a specific code version and data version. You can always trace back.

Another important concept: reproducibility. If you have versions of everything, you should be able to reproduce any previous result. Given code v1, data v1, and the same random seed, you should get the exact same model.

This is harder than it sounds. Some things that can break reproducibility:
- Different Python versions
- Different library versions
- Different hardware (GPU vs CPU)
- Non-deterministic operations in libraries
- Time-based features

To maximize reproducibility:

```python
# Set all random seeds
import random
import numpy as np
import tensorflow as tf

def set_seeds(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    # For PyTorch: torch.manual_seed(seed)

# Log environment
import pkg_resources
installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
mlflow.log_dict(installed, "environment.json")

# Log system info
import platform
mlflow.log_param("python_version", platform.python_version())
mlflow.log_param("platform", platform.platform())
```

One more thing: version naming conventions. Use clear, consistent naming:

For models:
- `churn_model_v1.0.0` - semantic versioning
- `churn_model_20231215_abc123` - timestamp + commit hash
- `churn_model_exp42_run7` - experiment tracking

For data:
- `customers_2023Q4.parquet` - time-based
- `customers_v3.csv` - simple versioning
- Reference by hash: `customers_abc123def456`

The key is that you can always answer: "What was running in production on date X?" You should be able to say: "Model version 1.2.3, trained on data version d_2023_10_15, with code commit abc123."

That's the foundation of traceable ML systems. In the next lectures, we'll dive deeper into specific tools and techniques for versioning data, code, and models.

Any questions so far? Let's keep going.

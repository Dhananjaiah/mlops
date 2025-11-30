# Lecture 7.1 – Turning Training Code into a Re-usable Python Package

## Human Transcript

Hey everyone, welcome to Section 7 where we're going to talk about model packaging. This is where we take all that experimental code you've been writing and turn it into something that can actually be deployed and used in production.

So let me start with a question. How many of you have written a machine learning model that works perfectly on your laptop but then when you try to share it with someone else or run it on a server, everything breaks? If you're nodding your head right now, you're not alone. This is probably the most common problem I see when people try to move from experimentation to production.

The issue is that most people write their training code as a single script or a Jupyter notebook. And that's fine for experimentation. But when you need to actually deploy this thing, you need something more structured. You need a Python package.

Now, what do I mean by a Python package? At its simplest, it's just a way of organizing your code so that it can be installed and imported just like any other library you use. You know how you write `import pandas as pd` or `import sklearn`? Your model code should work the same way. Someone should be able to write `import my_churn_model` and then call functions from it.

Let me show you what this looks like in practice. Right now, your code probably looks something like this. You've got a file called `train.py` and it has everything in it. Data loading, preprocessing, feature engineering, model training, evaluation, saving. It's all in one big file, maybe 500 lines long, and it works, but it's a nightmare to maintain.

What we want to do is restructure this into a proper package. Here's the basic structure we're going to build:

```
churn_model/
├── pyproject.toml
├── README.md
├── src/
│   └── churn_model/
│       ├── __init__.py
│       ├── config.py
│       ├── data/
│       │   ├── __init__.py
│       │   └── loader.py
│       ├── features/
│       │   ├── __init__.py
│       │   └── engineering.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── train.py
│       │   └── predict.py
│       └── utils/
│           ├── __init__.py
│           └── validation.py
├── tests/
│   ├── __init__.py
│   └── test_model.py
└── data/
    └── sample_data.csv
```

Let's break this down. The top level has your `pyproject.toml`, which is the modern way to configure Python packages. You might have seen `setup.py` files in older projects, but `pyproject.toml` is the new standard. Then we have a `src` directory that contains the actual package code.

Inside the `src/churn_model` directory, we have several subdirectories. The `data` directory handles loading and preprocessing. The `features` directory handles feature engineering. The `models` directory handles training and prediction. And `utils` has helper functions.

Now, why do we structure it this way? A few reasons.

First, separation of concerns. Each piece of code has one job. The data loader loads data. The feature engineering code creates features. The training code trains models. When something breaks, you know exactly where to look.

Second, testability. With this structure, you can write unit tests for each component. You can test your feature engineering code without having to train a whole model. You can test your prediction code with a mock model. This makes debugging so much easier.

Third, reusability. Once you have this structure, you can use the same components in different projects. Maybe you have another project that needs similar feature engineering. Just import the module and use it.

Let me show you what the `pyproject.toml` looks like:

```toml
[project]
name = "churn-model"
version = "1.0.0"
description = "Customer churn prediction model"
requires-python = ">=3.8"
dependencies = [
    "pandas>=1.3.0",
    "scikit-learn>=1.0.0",
    "numpy>=1.21.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

This file tells Python how to build and install your package. The `dependencies` section lists what libraries your package needs. The `optional-dependencies` section lists things you only need for development, like testing tools.

Now let me show you a simple example of how the code inside this structure might look. Here's what the `loader.py` file might contain:

```python
# src/churn_model/data/loader.py
import pandas as pd
from pathlib import Path

def load_raw_data(file_path: str) -> pd.DataFrame:
    """Load raw customer data from CSV file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    df = pd.read_csv(path)
    
    # Basic validation
    required_columns = ['customer_id', 'tenure', 'monthly_charges', 'churned']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return df

def split_features_target(df: pd.DataFrame, target_col: str = 'churned'):
    """Split dataframe into features and target."""
    y = df[target_col]
    X = df.drop(columns=[target_col])
    return X, y
```

See how this is clean and focused? It just does data loading and validation. Nothing else. And it has type hints so anyone reading it knows what to expect.

Here's what the feature engineering might look like:

```python
# src/churn_model/features/engineering.py
import pandas as pd
import numpy as np

def create_tenure_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create features based on customer tenure."""
    df = df.copy()
    df['tenure_months'] = df['tenure']
    df['tenure_years'] = df['tenure'] / 12
    df['is_new_customer'] = (df['tenure'] < 6).astype(int)
    df['is_loyal_customer'] = (df['tenure'] > 36).astype(int)
    return df

def create_charge_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create features based on charges."""
    df = df.copy()
    df['avg_monthly_charge'] = df['monthly_charges']
    df['total_charges'] = df['monthly_charges'] * df['tenure_months']
    df['charge_per_tenure'] = df['monthly_charges'] / (df['tenure_months'] + 1)
    return df

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Run all feature engineering steps."""
    df = create_tenure_features(df)
    df = create_charge_features(df)
    return df
```

Again, clean and focused. Each function does one thing. And there's a main function that chains them together.

Now, how do you install this package? Once you have this structure, you can install it in development mode by running:

```bash
pip install -e .
```

The `-e` flag means "editable" mode. Changes you make to the code are immediately reflected without reinstalling. This is super useful during development.

After installation, you can use your package like this:

```python
from churn_model.data.loader import load_raw_data
from churn_model.features.engineering import prepare_features
from churn_model.models.train import train_model

# Load data
df = load_raw_data('data/customers.csv')

# Engineer features
df = prepare_features(df)

# Train model
model = train_model(df)
```

See how clean that is? Anyone can read this code and understand what's happening. And if there's a bug, they know exactly which module to look at.

Now, some tips for organizing your package:

One, keep your dependencies minimal. Every dependency is something that can break or have security issues. Only include what you really need.

Two, version your package properly. Use semantic versioning. Major dot minor dot patch. When you make a breaking change, bump the major version.

Three, write a good README. Explain how to install the package, how to use it, and give some examples.

Four, include type hints. They make your code self-documenting and help catch bugs before they happen.

Five, write tests. We'll cover this more later, but having tests for each module gives you confidence that your code works.

The transformation from script to package might seem like a lot of work at first. But trust me, it pays off enormously when you need to deploy, debug, or share your code. The extra hour you spend setting this up saves you tens of hours later.

In the next lecture, we're going to look at the most important function in your package: the `predict()` function. This is what actually makes predictions in production, and there are some specific things we need to get right to make it work reliably.

Any questions so far? Great, let's move on.

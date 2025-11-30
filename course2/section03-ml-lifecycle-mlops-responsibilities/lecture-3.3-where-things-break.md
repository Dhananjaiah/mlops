# Lecture 3.3 – Where Things Break in Real Life (Why "Just a Notebook" Fails)

---

## The Notebook Problem

I love Jupyter notebooks. They're great for exploration, visualization, and sharing ideas.

But notebooks in production? That's where things break.

Let me tell you about the disasters I've seen.

---

## Story 1: The Disappearing Model

A data scientist built a churn prediction model. It was beautiful. Clear visualizations. Nice accuracy metrics. The stakeholders loved the presentation.

"Great! Deploy it!"

The data scientist went to deploy... and realized:

- The notebook had cells executed out of order
- Some variables were defined in cells he deleted
- When he ran the notebook from top to bottom, it crashed
- He couldn't reproduce the results that impressed the stakeholders

The model that got approved didn't actually exist in a reproducible form.

---

## Story 2: The 4 AM Disaster

A model went to production. It was a Python notebook converted to a script.

At 4 AM, the on-call engineer got paged. The model was failing.

She opened the script. It was 3,000 lines long. A converted notebook with no structure, no functions, no error handling. Variables like `df2`, `df_final`, `df_final_v2`.

She had no idea where to even start debugging.

Four hours later, she found the bug: a column name had changed in the source data. A one-line fix. But finding it took four hours.

---

## Story 3: The "It Worked Yesterday"

A model ran daily. Monday: fine. Tuesday: fine. Wednesday: crashed.

The team investigated. Nothing in the code changed.

After a full day of debugging, they found it: a library had auto-updated. `pandas==2.0.0` had different behavior than `pandas==1.5.0`.

The notebook never specified versions. `pip install pandas` had grabbed the latest.

---

## Why Notebooks Fail in Production

Let me break down the specific problems:

### 1. Hidden State

Notebooks have hidden state. You can:
- Execute cells out of order
- Delete cells that defined variables
- Have variables from failed cells still in memory

Result: "Works in my notebook" ≠ "Works when run fresh"

### 2. No Structure

Notebooks encourage linear, script-like code:
- All code in one file
- No functions (or poorly defined functions)
- No separation of concerns

Result: 3,000-line notebooks that no one can maintain.

### 3. No Versioning (for Data)

Notebooks track code (sort of), but not data:
- Which dataset was used?
- Did it change since last run?
- Can we reproduce the exact training data?

Result: "The model worked with the old data" 🤷

### 4. No Dependency Management

Notebooks rarely specify:
- Python version
- Package versions
- System dependencies

Result: "Works on my machine, breaks everywhere else."

### 5. No Testing

Notebooks don't naturally support testing:
- No unit tests
- No integration tests
- No validation checks

Result: Bugs discovered in production, not development.

### 6. Hard to Review

Code review for notebooks is painful:
- JSON format (diffs are ugly)
- Output cells clutter the review
- No clear function boundaries

Result: Poor code review → more bugs.

### 7. Hard to Deploy

Notebooks aren't designed for production:
- Can't easily run on a schedule
- No clean entry point
- Mixed exploration and production code

Result: "Let me just convert this to a script..."

---

## The Conversion Problem

"I'll just convert the notebook to a Python script."

This is better than running the notebook, but you often end up with:

```python
# train.py (converted from notebook)

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Cell 1: Load data
df = pd.read_csv('data.csv')

# Cell 2: Some exploration I did
# print(df.head())  # commented out

# Cell 3: Clean data
df = df.dropna()
df2 = df[df['value'] > 0]

# Cell 4: Tried something, didn't work
# df2 = df2.drop_duplicates()

# Cell 5: Features
df_final = df2.copy()
df_final['feature1'] = df_final['a'] / df_final['b']

# Cell 6: More features
df_final_v2 = df_final.copy()
df_final_v2['feature2'] = df_final_v2['c'].apply(lambda x: 'high' if x > 10 else 'low')

# Cell 7: Train
X = df_final_v2[['feature1', 'feature2']]  # Wait, feature2 is categorical...
y = df_final_v2['target']
model = RandomForestClassifier()
model.fit(X, y)

# Cell 8: Save
import pickle
pickle.dump(model, open('model.pkl', 'wb'))
```

Problems:
- No functions
- Dead code (commented experiments)
- Confusing variable names
- No error handling
- Hardcoded paths
- No logging
- No documentation

---

## What Good Production Code Looks Like

Compare the above to proper production code:

```python
# src/models/train.py

"""Training pipeline for churn prediction model."""

import logging
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import mlflow

from src.data.load import load_training_data
from src.features.build import create_features
from src.models.evaluate import evaluate_model
from src.utils.config import load_config

logger = logging.getLogger(__name__)


def train_model(config_path: str = "configs/config.yaml") -> str:
    """
    Train the churn prediction model.
    
    Args:
        config_path: Path to configuration file.
        
    Returns:
        MLflow run ID for the trained model.
    """
    config = load_config(config_path)
    
    logger.info("Loading training data...")
    df = load_training_data(config["data"]["path"])
    
    logger.info("Creating features...")
    X, y = create_features(df, config["features"])
    
    logger.info("Training model...")
    model = RandomForestClassifier(**config["model"]["params"])
    model.fit(X, y)
    
    logger.info("Evaluating model...")
    metrics = evaluate_model(model, X, y)
    
    logger.info("Logging to MLflow...")
    with mlflow.start_run() as run:
        mlflow.log_params(config["model"]["params"])
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")
        
    logger.info(f"Training complete. Run ID: {run.info.run_id}")
    return run.info.run_id


if __name__ == "__main__":
    train_model()
```

Better:
- Clear function with docstring
- Configuration externalized
- Logging for visibility
- Error handling possible
- Testable components
- MLflow tracking
- Clean entry point

---

## The Gap Between Exploration and Production

Here's the reality:

```
Exploration                     Production
──────────────────────────────────────────────────
Quick and dirty                 Clean and maintainable
Try many things fast            Do one thing reliably
Interactive                     Automated
One person                      Many people
Works once                      Works every time
Notebooks                       Scripts/modules
```

You need BOTH. But they're different:

- **Exploration** → Notebooks, experimentation, quick iteration
- **Production** → Scripts, packages, automation, reliability

The mistake is treating exploration code as production code.

---

## The MLOps Solution

MLOps provides the bridge:

### 1. Structure for Production Code

```
src/
├── data/          # Data loading/processing
├── features/      # Feature engineering
├── models/        # Training/inference
└── utils/         # Utilities
```

### 2. Experiment Tracking

MLflow (or similar) captures:
- What parameters were used
- What data was used
- What results were achieved
- The actual model artifact

### 3. Version Control

- Git for code
- DVC for data
- MLflow for models

### 4. Environment Management

```
pyproject.toml or requirements.txt
Python 3.11.6
pandas==2.1.0
scikit-learn==1.3.2
...
```

### 5. Testing

```python
def test_create_features():
    """Test feature creation."""
    df = pd.DataFrame({'a': [1, 2], 'b': [2, 4]})
    result = create_features(df)
    assert 'ratio' in result.columns
    assert result['ratio'].iloc[0] == 0.5
```

### 6. CI/CD

Automated pipeline that:
- Runs tests
- Checks code quality
- Builds containers
- Deploys models

---

## The Transition Process

How do you go from notebook to production?

### Step 1: Explore in Notebook

- Do your exploration
- Try things quickly
- Visualize and understand

### Step 2: Identify Production Code

Ask: "What needs to run repeatedly and reliably?"

Usually:
- Data loading
- Feature engineering
- Model training
- Model inference

### Step 3: Extract and Refactor

Move code from notebook to modules:
- Create functions
- Add parameters
- Add error handling
- Add logging
- Add type hints

### Step 4: Add Tests

Write tests for the extracted code:
- Unit tests for functions
- Integration tests for pipelines

### Step 5: Track with MLflow

Add experiment tracking:
- Log parameters
- Log metrics
- Log artifacts

### Step 6: Create Pipeline

Automate the execution:
- Entry point script
- Configuration file
- Scheduling (if needed)

---

## Recap

Notebooks fail in production because:
- Hidden state
- No structure
- No versioning
- No dependencies
- No testing
- Hard to review
- Hard to deploy

The solution:
- Keep notebooks for exploration
- Move production code to scripts/modules
- Add structure, testing, tracking
- Use proper MLOps practices

The gap between exploration and production is where most ML projects fail. MLOps bridges that gap.

---

## What's Next

Now let's compare MLOps to DevOps. They're related, but what makes MLOps different?

---

**Next Lecture**: [3.4 – MLOps vs DevOps: Same, Similar, Different?](lecture-3.4-mlops-vs-devops.md)

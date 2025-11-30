# Lecture 6.2 – Structuring Experiments (Folders, Scripts, Configs)

---

## From Chaos to Order

In the last lecture, we saw why notebooks fail. Now let's build something better.

A well-structured experiment setup lets you:
- Run experiments reproducibly
- Compare results easily
- Know exactly what produced what
- Collaborate with others

---

## The Ideal Structure

```
experiments/
├── configs/
│   ├── base.yaml           # Default configuration
│   ├── experiment_001.yaml # Override for experiment 1
│   └── experiment_002.yaml # Override for experiment 2
├── src/
│   ├── __init__.py
│   ├── data.py             # Data loading
│   ├── features.py         # Feature engineering
│   ├── model.py            # Model training
│   └── evaluate.py         # Evaluation
├── scripts/
│   └── train.py            # Main entry point
├── notebooks/
│   └── exploration.ipynb   # For exploration only
└── outputs/
    ├── experiment_001/
    │   ├── model.pkl
    │   └── metrics.json
    └── experiment_002/
        ├── model.pkl
        └── metrics.json
```

---

## Configuration-Driven Experiments

The key insight: **Separate configuration from code.**

### Base Configuration

```yaml
# configs/base.yaml
data:
  path: data/processed/features.parquet
  test_size: 0.2
  random_state: 42

features:
  numerical:
    - days_as_customer
    - events_per_day
    - seat_count
  categorical:
    - plan_type

model:
  type: random_forest
  params:
    n_estimators: 100
    max_depth: 10
    random_state: 42

training:
  cv_folds: 5

output:
  dir: outputs/
```

### Experiment Override

```yaml
# configs/experiment_001.yaml
# Try more trees and deeper
model:
  params:
    n_estimators: 200
    max_depth: 15
```

### Load Configuration

```python
# src/config.py
import yaml
from pathlib import Path

def load_config(base_path: str, override_path: str = None) -> dict:
    with open(base_path) as f:
        config = yaml.safe_load(f)
    
    if override_path:
        with open(override_path) as f:
            override = yaml.safe_load(f)
        config = deep_merge(config, override)
    
    return config

def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
```

---

## Modular Code Structure

### Data Module

```python
# src/data.py
import pandas as pd
from typing import Tuple

def load_data(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)

def split_data(
    df: pd.DataFrame, 
    test_size: float, 
    random_state: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    from sklearn.model_selection import train_test_split
    return train_test_split(df, test_size=test_size, random_state=random_state)
```

### Features Module

```python
# src/features.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def prepare_features(
    df: pd.DataFrame,
    numerical_cols: list,
    categorical_cols: list
) -> Tuple[pd.DataFrame, dict]:
    preprocessors = {}
    
    # Numerical
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    preprocessors['scaler'] = scaler
    
    # Categorical
    df_encoded = pd.get_dummies(df, columns=categorical_cols)
    
    return df_encoded, preprocessors
```

### Model Module

```python
# src/model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

def get_model(model_type: str, params: dict):
    models = {
        'random_forest': RandomForestClassifier,
        'logistic_regression': LogisticRegression,
    }
    return models[model_type](**params)

def train_model(model, X, y):
    model.fit(X, y)
    return model
```

### Evaluate Module

```python
# src/evaluate.py
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

def evaluate_model(model, X, y) -> dict:
    predictions = model.predict(X)
    probas = model.predict_proba(X)[:, 1]
    
    return {
        'accuracy': accuracy_score(y, predictions),
        'precision': precision_score(y, predictions),
        'recall': recall_score(y, predictions),
        'auc': roc_auc_score(y, probas),
    }
```

---

## Main Training Script

```python
# scripts/train.py
import argparse
import json
from pathlib import Path

from src.config import load_config
from src.data import load_data, split_data
from src.features import prepare_features
from src.model import get_model, train_model
from src.evaluate import evaluate_model

def main(config_path: str, experiment_name: str):
    # Load config
    config = load_config('configs/base.yaml', config_path)
    
    # Create output directory
    output_dir = Path(config['output']['dir']) / experiment_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load and split data
    df = load_data(config['data']['path'])
    train_df, test_df = split_data(df, config['data']['test_size'], config['data']['random_state'])
    
    # Prepare features
    X_train, preprocessors = prepare_features(
        train_df, 
        config['features']['numerical'],
        config['features']['categorical']
    )
    y_train = train_df['churned']
    
    X_test, _ = prepare_features(test_df, config['features']['numerical'], config['features']['categorical'])
    y_test = test_df['churned']
    
    # Train model
    model = get_model(config['model']['type'], config['model']['params'])
    model = train_model(model, X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    print(f"Metrics: {metrics}")
    
    # Save outputs
    with open(output_dir / 'config.yaml', 'w') as f:
        yaml.dump(config, f)
    with open(output_dir / 'metrics.json', 'w') as f:
        json.dump(metrics, f)
    joblib.dump(model, output_dir / 'model.pkl')
    
    return metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/base.yaml')
    parser.add_argument('--name', required=True, help='Experiment name')
    args = parser.parse_args()
    
    main(args.config, args.name)
```

---

## Running Experiments

```bash
# Run base experiment
python scripts/train.py --name baseline

# Run with override config
python scripts/train.py --config configs/experiment_001.yaml --name exp001

# Run with command-line overrides (using Hydra)
python scripts/train.py --name exp002 model.params.n_estimators=500
```

---

## Benefits of This Structure

1. **Reproducibility**: Config files capture exact settings
2. **Comparison**: Easy to compare experiment configs
3. **Modularity**: Test each module independently
4. **Scalability**: Add new experiments without changing code
5. **Collaboration**: Team members can run same experiments

---

## Recap

Structure experiments with:
- **Configs**: Separate configuration from code
- **Modules**: Split code by responsibility
- **Scripts**: Clean entry points
- **Outputs**: Organized results

Next: How to track all these experiments systematically.

---

**Next Lecture**: [6.3 – Experiment Tracking Concepts (Runs, Params, Metrics, Artifacts)](lecture-6.3-tracking-concepts.md)

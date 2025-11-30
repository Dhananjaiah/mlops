# Lecture 5.4 – Feature Engineering Overview (Not Deep ML, Just Enough to Operate)

---

## What Are Features?

Features are the inputs to your ML model—the signals it uses to make predictions.

Raw data is rarely usable as-is. Feature engineering transforms raw data into useful model inputs.

As an MLOps engineer, you don't need to be a feature engineering expert. But you need to understand:
- What features are
- Common feature types
- How feature pipelines work
- How to operationalize feature engineering

---

## From Raw Data to Features

Example transformation:

```
Raw Data:
┌────────────┬─────────────┬────────────┬───────────┐
│ customer_id│ signup_date │ plan       │ last_login│
├────────────┼─────────────┼────────────┼───────────┤
│ 123        │ 2023-06-15  │ pro        │ 2024-01-10│
│ 456        │ 2024-01-01  │ basic      │ 2024-01-14│
└────────────┴─────────────┴────────────┴───────────┘

Engineered Features:
┌────────────┬───────────────┬──────────┬───────────────────┐
│ customer_id│ days_as_cust  │ is_pro   │ days_since_login  │
├────────────┼───────────────┼──────────┼───────────────────┤
│ 123        │ 214           │ 1        │ 5                 │
│ 456        │ 14            │ 0        │ 1                 │
└────────────┴───────────────┴──────────┴───────────────────┘
```

The raw dates and categories become numeric values the model can use.

---

## Common Feature Types

### Numerical Features

Already numbers, but may need transformation:

**Raw numerical**:
```python
df['amount']  # Use as-is
```

**Scaled numerical** (normalize to 0-1 or standard scale):
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['amount_scaled'] = scaler.fit_transform(df[['amount']])
```

**Log-transformed** (for skewed distributions):
```python
df['amount_log'] = np.log1p(df['amount'])  # log(1+x) handles zeros
```

### Categorical Features

Text categories need encoding:

**One-hot encoding** (creates binary columns):
```python
df = pd.get_dummies(df, columns=['plan_type'])
# Creates: plan_type_basic, plan_type_pro, plan_type_enterprise
```

**Label encoding** (integer mapping):
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['plan_type_encoded'] = le.fit_transform(df['plan_type'])
# basic=0, pro=1, enterprise=2
```

**Target encoding** (average target per category):
```python
# Higher risk encoding for categories with more churners
mean_by_plan = df.groupby('plan_type')['churned'].mean()
df['plan_type_target_encoded'] = df['plan_type'].map(mean_by_plan)
```

### Datetime Features

Extract useful signals from timestamps:

```python
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Age features
df['days_as_customer'] = (pd.Timestamp.now() - df['signup_date']).dt.days
df['months_as_customer'] = df['days_as_customer'] / 30

# Temporal features
df['signup_month'] = df['signup_date'].dt.month
df['signup_dayofweek'] = df['signup_date'].dt.dayofweek
df['is_weekend_signup'] = df['signup_dayofweek'].isin([5, 6]).astype(int)

# Recency
df['days_since_last_login'] = (pd.Timestamp.now() - df['last_login']).dt.days
```

### Aggregation Features

Summarize related records:

```python
# Usage aggregations
usage_features = usage_df.groupby('customer_id').agg({
    'events': ['count', 'sum', 'mean'],
    'session_duration': ['sum', 'mean', 'max'],
    'distinct_features_used': 'nunique',
}).reset_index()

# Flatten column names
usage_features.columns = ['customer_id', 'event_count', 'total_events', 'avg_events',
                          'total_duration', 'avg_duration', 'max_duration', 'features_used']
```

### Ratio/Interaction Features

Combine features:

```python
# Ratios
df['events_per_day'] = df['total_events'] / df['days_as_customer']
df['support_to_usage_ratio'] = df['support_tickets'] / (df['total_events'] + 1)

# Interactions
df['is_new_and_inactive'] = ((df['days_as_customer'] < 30) & 
                              (df['days_since_login'] > 7)).astype(int)
```

### Window Features

Rolling calculations:

```python
# Sort by date first
df = df.sort_values(['customer_id', 'date'])

# Rolling features
df['events_7d_rolling'] = df.groupby('customer_id')['events'].transform(
    lambda x: x.rolling(7, min_periods=1).sum()
)

df['events_trend'] = df.groupby('customer_id')['events'].transform(
    lambda x: x.diff()  # Change from previous day
)
```

---

## Feature Engineering Pipeline

A typical pipeline:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Raw Data   │───►│   Clean &   │───►│  Engineer   │───►│  Feature    │
│             │    │  Validate   │    │  Features   │    │   Store     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Example Pipeline Code

```python
# src/features/build_features.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def build_customer_features(customers_df, usage_df, support_df):
    """Build features for churn prediction."""
    
    # Start with customer base
    features = customers_df[['customer_id']].copy()
    
    # --- Customer features ---
    features['days_as_customer'] = (
        pd.Timestamp.now() - pd.to_datetime(customers_df['signup_date'])
    ).dt.days
    
    features['is_enterprise'] = (customers_df['plan_type'] == 'enterprise').astype(int)
    features['is_pro'] = (customers_df['plan_type'] == 'pro').astype(int)
    features['seat_count'] = customers_df['seat_count']
    
    # --- Usage features ---
    usage_agg = usage_df.groupby('customer_id').agg({
        'events': ['count', 'sum', 'mean'],
        'session_duration': ['sum', 'mean'],
    }).reset_index()
    usage_agg.columns = ['customer_id', 'login_count', 'total_events', 
                         'avg_events', 'total_duration', 'avg_duration']
    
    features = features.merge(usage_agg, on='customer_id', how='left')
    
    # --- Support features ---
    support_agg = support_df.groupby('customer_id').agg({
        'ticket_id': 'count',
        'resolution_hours': 'mean',
        'satisfaction_score': 'mean',
    }).reset_index()
    support_agg.columns = ['customer_id', 'ticket_count', 
                           'avg_resolution_time', 'avg_satisfaction']
    
    features = features.merge(support_agg, on='customer_id', how='left')
    
    # --- Derived features ---
    features['events_per_seat'] = features['total_events'] / features['seat_count']
    features['tickets_per_month'] = (
        features['ticket_count'] / (features['days_as_customer'] / 30 + 1)
    )
    
    # Fill missing values
    features = features.fillna(0)
    
    return features
```

---

## MLOps Considerations for Features

### Reproducibility

**Problem**: Features computed at training time vs serving time might differ.

**Solution**: 
- Same code for training and serving
- Feature store for consistency
- Version your feature code

### Feature Skew

**Training-Serving Skew**: Features computed differently in training vs serving.

Example:
- Training: `days_since_last_login` computed at training time
- Serving: `days_since_last_login` computed at prediction time

If the gap is big, the model sees different data.

**Solution**: Feature stores that serve same features for training and inference.

### Feature Versioning

Track what features a model was trained on:

```python
# Log features with model
mlflow.log_param("feature_version", "v1.2")
mlflow.log_artifact("feature_config.yaml")
```

### Feature Documentation

Document your features:

```yaml
# features/customer_features.yaml
features:
  days_as_customer:
    description: Days since customer signed up
    type: numerical
    source: customers.signup_date
    computation: (now - signup_date).days
    
  events_per_day:
    description: Average daily events
    type: numerical
    source: usage_logs
    computation: total_events / days_as_customer
```

---

## Features for Our Churn Project

| Feature | Type | Source | Description |
|---------|------|--------|-------------|
| days_as_customer | numerical | customers | Customer tenure |
| seat_count | numerical | customers | Number of seats |
| is_enterprise | binary | customers | Enterprise plan flag |
| login_count_30d | numerical | usage | Logins in last 30 days |
| events_per_day | numerical | usage | Daily event rate |
| days_since_last_login | numerical | usage | Recency |
| ticket_count_30d | numerical | support | Recent tickets |
| avg_satisfaction | numerical | support | Avg CSAT score |
| payment_failures_90d | numerical | billing | Recent failures |

---

## Recap

Feature engineering transforms raw data into model inputs.

**Common feature types**:
- Numerical (raw, scaled, transformed)
- Categorical (one-hot, label, target encoding)
- Datetime (age, recency, temporal)
- Aggregations (count, sum, mean)
- Derived (ratios, interactions)

**MLOps considerations**:
- Reproducibility (same code for training/serving)
- Feature skew (avoid training-serving differences)
- Versioning (track what model used)
- Documentation (know what each feature means)

---

## What's Next

Now let's talk about feature stores—a key MLOps component for managing features at scale.

---

**Next Lecture**: [5.5 – Storing Data & Features for Re-use (Intro to Feature Stores)](lecture-5.5-feature-stores.md)

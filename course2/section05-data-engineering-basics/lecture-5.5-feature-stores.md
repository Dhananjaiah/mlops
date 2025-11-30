# Lecture 5.5 – Storing Data & Features for Re-use (Intro to Feature Stores)

---

## The Feature Reuse Problem

Let me describe a common scenario:

Team A builds a churn prediction model. They create 50 features.
Team B builds a cross-sell model. They create 40 features.

Turns out, 30 of those features are the same: `days_as_customer`, `total_events`, `support_tickets`, etc.

But Team A and Team B computed them differently. Slightly different SQL. Slightly different time windows. Their models can't share features reliably.

This is the feature reuse problem. Feature stores solve it.

---

## What Is a Feature Store?

A feature store is a centralized repository for storing, managing, and serving ML features.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FEATURE STORE                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                      Feature Registry                          │     │
│  │  - Feature definitions                                         │     │
│  │  - Documentation                                               │     │
│  │  - Ownership                                                   │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ┌─────────────────────────┐    ┌─────────────────────────┐            │
│  │    Offline Store        │    │     Online Store        │            │
│  │  (Training Data)        │    │   (Serving Data)        │            │
│  │                         │    │                         │            │
│  │  - Historical features  │    │  - Latest features      │            │
│  │  - Batch retrieval      │    │  - Low latency          │            │
│  │  - Parquet/BigQuery     │    │  - Redis/DynamoDB       │            │
│  └─────────────────────────┘    └─────────────────────────┘            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                 │                              │
                 ▼                              ▼
           Model Training                Online Prediction
```

---

## Why Feature Stores?

### 1. Feature Reuse

Define a feature once, use it everywhere:
- Churn model uses `events_per_day`
- Cross-sell model uses same `events_per_day`
- Guaranteed to be computed the same way

### 2. Training-Serving Consistency

Same feature values for training and serving:
- No training-serving skew
- Consistent model behavior

### 3. Point-in-Time Correctness

For training, you need features as they were at prediction time, not current values.

Example: Predicting if customer X will churn next month.
- Wrong: Use today's features (includes future information)
- Right: Use features as they were when prediction was made

Feature stores handle this with timestamps.

### 4. Feature Discovery

Find existing features before creating new ones:
- Search by name, description, owner
- See feature statistics
- Understand lineage

---

## Feature Store Components

### Feature Registry

Metadata about features:

```yaml
# Example feature definition
name: events_per_day
description: Average daily events over last 30 days
entity: customer
value_type: FLOAT
owner: ml-team@company.com
tags:
  - engagement
  - activity
source:
  table: usage_logs
  computation: |
    SELECT customer_id, 
           SUM(events) / 30.0 as events_per_day
    FROM usage_logs
    WHERE event_date >= CURRENT_DATE - 30
    GROUP BY customer_id
```

### Offline Store

For training data retrieval:
- Historical feature values
- High throughput (batch reads)
- Usually: Data warehouse, Parquet files

```python
# Get training data with historical features
training_df = feature_store.get_historical_features(
    entity_df=customer_entity_df,  # customer_id, timestamp
    feature_refs=[
        "customer_features:days_as_customer",
        "usage_features:events_per_day",
        "support_features:ticket_count",
    ]
)
```

### Online Store

For real-time serving:
- Latest feature values
- Low latency (milliseconds)
- Usually: Redis, DynamoDB, Bigtable

```python
# Get features for online prediction
features = feature_store.get_online_features(
    entity_rows=[{"customer_id": "123"}],
    feature_refs=[
        "customer_features:days_as_customer",
        "usage_features:events_per_day",
    ]
)
```

---

## Feature Store Options

### Open Source

**Feast** (Most popular):
```python
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Define feature view
from feast import Entity, Feature, FeatureView, ValueType

customer = Entity(name="customer", value_type=ValueType.STRING)

customer_features = FeatureView(
    name="customer_features",
    entities=["customer"],
    features=[
        Feature(name="days_as_customer", dtype=ValueType.INT64),
        Feature(name="seat_count", dtype=ValueType.INT64),
    ],
    online=True,
    source=BigQuerySource(table_ref="project.dataset.customer_features"),
)

# Retrieve features
features = store.get_online_features(
    features=["customer_features:days_as_customer"],
    entity_rows=[{"customer": "123"}]
).to_dict()
```

**Other options**: Hopsworks, Butterfree

### Managed Services

**AWS SageMaker Feature Store**:
```python
import sagemaker
from sagemaker.feature_store.feature_group import FeatureGroup

feature_group = FeatureGroup(
    name="customer-features",
    sagemaker_session=sagemaker.Session()
)

# Ingest features
feature_group.ingest(data_frame=features_df, max_workers=3)

# Read features
feature_group.athena_query().run(
    query_string="SELECT * FROM customer_features WHERE customer_id = '123'"
)
```

**Google Vertex AI Feature Store**:
```python
from google.cloud import aiplatform

feature_store = aiplatform.Featurestore(
    featurestore_name="my-feature-store"
)

# Read features
entity_type = feature_store.get_entity_type("customer")
features = entity_type.read(entity_ids=["123"])
```

**Databricks Feature Store**:
```python
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

# Create feature table
fs.create_table(
    name="customer_features",
    primary_keys=["customer_id"],
    df=features_df
)

# Read features
features = fs.read_table(name="customer_features")
```

---

## Do You Need a Feature Store?

### You Probably DON'T Need One If:

- Single model or few models
- Batch predictions only
- Small team
- Simple features

### You Probably DO Need One If:

- Many models sharing features
- Real-time predictions requiring features
- Large team with feature reuse needs
- Training-serving consistency critical

### Our Project Approach

For our churn prediction project, we'll use a simple approach:
- Store features in a feature table (data warehouse)
- Version with DVC
- No full feature store (would be overkill)

But you'll learn the concepts so you can implement one when needed.

---

## Simple Feature Storage (Without Feature Store)

For small projects, a simple approach:

```
features/
├── customer_features/
│   ├── feature_spec.yaml      # Feature definitions
│   └── data/
│       └── customer_features.parquet
│
└── pipelines/
    └── build_features.py      # Feature pipeline
```

**Feature spec**:
```yaml
# feature_spec.yaml
features:
  - name: days_as_customer
    type: int
    description: Days since signup
  - name: events_per_day
    type: float
    description: Average daily events
entity: customer_id
update_frequency: daily
owner: ml-team
```

**Simple feature retrieval**:
```python
def get_training_features(customer_ids, feature_date):
    """Get features for training."""
    features_df = pd.read_parquet('features/customer_features/data/')
    
    # Filter to requested customers and date
    features_df = features_df[
        (features_df['customer_id'].isin(customer_ids)) &
        (features_df['feature_date'] == feature_date)
    ]
    
    return features_df
```

---

## Best Practices

### 1. Document Everything

```yaml
name: events_per_day
description: |
  Average number of events per day over the last 30 days.
  Computed from usage_logs table.
  Null for customers with less than 1 day tenure (filled with 0).
unit: events/day
range: [0, inf]
null_handling: fill_zero
```

### 2. Version Your Features

When feature definitions change, version them:
- `events_per_day_v1`: 30-day window
- `events_per_day_v2`: 7-day window

Models should reference specific versions.

### 3. Monitor Feature Quality

Track:
- Feature freshness
- Null rates
- Distribution changes
- Outliers

### 4. Separate Compute from Storage

Feature computation and storage are separate concerns:
- Compute: Feature engineering pipeline
- Storage: Feature store/table

---

## For Our Churn Project

We'll implement:

1. **Feature table** in data warehouse
2. **Feature pipeline** (daily update)
3. **Feature spec** documentation
4. **DVC versioning** for feature snapshots

No full feature store—we'll keep it simple.

```python
# Our feature storage approach
def save_features(features_df, date):
    """Save features with date partitioning."""
    path = f"data/features/customer_features/date={date}/features.parquet"
    features_df.to_parquet(path)
    
def load_features(date):
    """Load features for a specific date."""
    path = f"data/features/customer_features/date={date}/features.parquet"
    return pd.read_parquet(path)
```

---

## Recap

Feature stores solve:
- Feature reuse across models
- Training-serving consistency
- Point-in-time correctness
- Feature discovery

Components:
- Feature registry (metadata)
- Offline store (training)
- Online store (serving)

Options: Feast (open source), SageMaker/Vertex AI/Databricks (managed)

Start simple, add complexity when needed.

---

## What's Next

Let's clarify where Data Engineering ends and MLOps begins—the responsibility boundary.

---

**Next Lecture**: [5.6 – Where Data Engineer Ends and MLOps Starts (Responsibility Boundaries)](lecture-5.6-responsibility-boundaries.md)

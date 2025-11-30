# Lecture 5.1 – Data Types & Storage (DB, Data Lake, CSV, Parquet)

---

## Data Is Everything

In ML, your model is only as good as your data.

But before we can use data, we need to understand how it's stored, what formats exist, and when to use each one.

This lecture gives you the data engineering foundation you need for MLOps.

---

## Data Types in ML Projects

Let's categorize the data you'll encounter:

### Structured Data

Data organized in rows and columns with a defined schema.

**Examples**:
- Customer records
- Transaction logs
- Sensor readings with timestamps

**Characteristics**:
- Fixed schema (column names and types)
- Easy to query (SQL)
- Fits in tables

**Storage**: Databases, data warehouses, CSV, Parquet

### Semi-Structured Data

Data with some organization but flexible schema.

**Examples**:
- JSON logs
- XML configuration files
- Event payloads

**Characteristics**:
- Nested structures
- Schema can vary between records
- More flexible than structured

**Storage**: JSON files, document databases (MongoDB), data lakes

### Unstructured Data

Data without predefined structure.

**Examples**:
- Text documents
- Images
- Audio/video files

**Characteristics**:
- No fixed schema
- Requires processing to extract features
- Large file sizes

**Storage**: Object storage (S3, GCS), file systems

---

## Storage Systems

### Relational Databases (OLTP)

**What they are**: Traditional databases for transactional operations.

**Examples**: PostgreSQL, MySQL, SQL Server

**Use when**:
- Need ACID transactions
- Real-time reads/writes
- Consistent, normalized data

**For ML**: Often the source of truth for customer data, transactions.

```sql
-- Example: Query customer data
SELECT customer_id, signup_date, plan_type
FROM customers
WHERE is_active = true;
```

### Data Warehouses (OLAP)

**What they are**: Databases optimized for analytics and querying large datasets.

**Examples**: Snowflake, BigQuery, Redshift, Databricks

**Use when**:
- Running analytical queries
- Aggregating large datasets
- Business intelligence

**For ML**: Where you often find clean, aggregated training data.

```sql
-- Example: Aggregate usage data
SELECT 
    customer_id,
    DATE_TRUNC('week', event_date) as week,
    COUNT(*) as events
FROM usage_logs
GROUP BY 1, 2;
```

### Data Lakes

**What they are**: Large-scale storage for raw data in various formats.

**Examples**: S3 + Athena, Azure Data Lake, GCS + BigQuery

**Use when**:
- Storing raw, unprocessed data
- Schema-on-read (define schema when querying)
- Diverse data types

**For ML**: Store raw logs, images, large datasets.

### Object Storage

**What it is**: Blob storage for files of any type.

**Examples**: Amazon S3, Google Cloud Storage, Azure Blob

**Use for**:
- Model artifacts
- Training data snapshots
- Logs and exports

```bash
# Example: Upload model to S3
aws s3 cp model.pkl s3://my-bucket/models/v1.0.0/model.pkl
```

---

## File Formats

### CSV (Comma-Separated Values)

**What it is**: Simple text file with values separated by commas.

**Pros**:
- Human readable
- Universal support
- Easy to create

**Cons**:
- No schema enforcement
- No compression
- Slow for large files
- Type inference issues

**Use when**: Small datasets, data exchange, quick exports.

```python
import pandas as pd
df = pd.read_csv('data.csv')
df.to_csv('output.csv', index=False)
```

### Parquet

**What it is**: Columnar storage format optimized for analytics.

**Pros**:
- Compressed (much smaller than CSV)
- Schema embedded
- Fast column reads
- Type preservation

**Cons**:
- Not human readable
- Requires library to read

**Use when**: Large datasets, production ML pipelines, data lakes.

```python
import pandas as pd
df = pd.read_parquet('data.parquet')
df.to_parquet('output.parquet', index=False)
```

### Size Comparison

```
Same dataset:
- CSV:     1,000 MB
- Parquet:   150 MB (85% smaller!)

Read time (pandas):
- CSV:     45 seconds
- Parquet:  8 seconds
```

### JSON / JSON Lines

**What it is**: Text format for nested/semi-structured data.

**Pros**:
- Handles nested structures
- Human readable
- Flexible schema

**Cons**:
- Verbose
- No compression
- Slower to parse

**Use when**: Event logs, API responses, configuration.

```python
import pandas as pd
df = pd.read_json('data.json', lines=True)  # JSON Lines format
```

### Avro

**What it is**: Row-based format with schema, often used with Kafka.

**Use when**: Streaming data, schema evolution needed.

### ORC

**What it is**: Columnar format optimized for Hive/Hadoop.

**Use when**: Hadoop ecosystem, very large datasets.

---

## Format Comparison

| Format | Structure | Compression | Schema | Best For |
|--------|-----------|-------------|--------|----------|
| CSV | Row | None | No | Small data, sharing |
| Parquet | Column | Yes | Yes | Analytics, ML |
| JSON | Flexible | None | No | Nested data, logs |
| Avro | Row | Yes | Yes | Streaming |
| ORC | Column | Yes | Yes | Hadoop |

---

## Storage for ML

Here's how I organize ML project data:

```
data/
├── raw/                    # Raw, immutable data
│   ├── customers/          # Parquet files
│   ├── usage/              # Parquet files
│   └── support/            # Parquet files
│
├── processed/              # Cleaned data
│   └── 2024-01-15/         # Date-partitioned
│       └── customers.parquet
│
├── features/               # Feature-engineered data
│   └── customer_features.parquet
│
└── training/               # Training datasets
    ├── train.parquet
    └── test.parquet
```

### Storage Recommendations

| Data Type | Format | Location |
|-----------|--------|----------|
| Raw source data | Parquet | Data lake |
| Processed data | Parquet | Data lake |
| Features | Parquet | Feature store / Data lake |
| Training data | Parquet | Versioned (DVC) |
| Model artifacts | pickle/joblib/ONNX | Model registry |

---

## Reading Data in Python

### From Databases

```python
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL
engine = create_engine('postgresql://user:pass@host:5432/db')
df = pd.read_sql('SELECT * FROM customers', engine)

# BigQuery
df = pd.read_gbq('SELECT * FROM dataset.customers', project_id='my-project')
```

### From Files

```python
import pandas as pd

# CSV
df = pd.read_csv('data.csv')

# Parquet
df = pd.read_parquet('data.parquet')

# Multiple Parquet files
df = pd.read_parquet('data/*.parquet')  # with pyarrow

# JSON Lines
df = pd.read_json('data.jsonl', lines=True)
```

### From Object Storage

```python
import pandas as pd

# S3 (requires s3fs)
df = pd.read_parquet('s3://my-bucket/data/file.parquet')

# GCS (requires gcsfs)
df = pd.read_parquet('gs://my-bucket/data/file.parquet')
```

---

## Data Partitioning

For large datasets, partition by date or key:

```
data/
└── events/
    ├── year=2024/
    │   ├── month=01/
    │   │   ├── day=01/
    │   │   │   └── data.parquet
    │   │   └── day=02/
    │   │       └── data.parquet
    │   └── month=02/
    │       └── ...
    └── year=2023/
        └── ...
```

**Benefits**:
- Query only relevant partitions
- Faster processing
- Easier data management

```python
# Read only January 2024
df = pd.read_parquet('s3://bucket/events/year=2024/month=01/')
```

---

## For Our Churn Project

We'll use:

| Data | Format | Storage |
|------|--------|---------|
| Customer data | Parquet | Data warehouse |
| Usage logs | Parquet | Data warehouse |
| Support tickets | Parquet | Data warehouse |
| Billing data | Parquet | Data warehouse |
| Feature dataset | Parquet | Local + DVC |
| Training data | Parquet | Local + DVC |
| Model artifacts | pickle | MLflow registry |

---

## Recap

Key takeaways:

**Data types**: Structured, semi-structured, unstructured

**Storage systems**:
- Databases (OLTP) for transactions
- Data warehouses (OLAP) for analytics
- Data lakes for raw storage
- Object storage for files

**File formats**:
- CSV for simple, small data
- Parquet for everything else (compressed, typed, fast)
- JSON for nested/flexible data

**Best practice**: Use Parquet for ML pipelines.

---

## What's Next

Now let's look at how data gets from source systems into our ML pipeline.

---

**Next Lecture**: [5.2 – Data Ingestion Patterns (Batch, Streaming, APIs)](lecture-5.2-data-ingestion-patterns.md)

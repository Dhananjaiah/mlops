# Lecture 5.2 – Data Ingestion Patterns (Batch, Streaming, APIs)

---

## Getting Data Into Your Pipeline

Data doesn't magically appear in your ML pipeline. It needs to be ingested—collected from source systems and loaded into your data store.

Let's explore the three main ingestion patterns.

---

## The Three Patterns

### 1. Batch Ingestion

Process data in large chunks on a schedule.

```
Source → [Wait for schedule] → Extract all new data → Load
              │
              └── Daily, hourly, etc.
```

### 2. Streaming Ingestion

Process data continuously as it arrives.

```
Source → Event stream → Process immediately → Load
              │
              └── Real-time, milliseconds
```

### 3. API-Based Ingestion

Pull data from APIs on demand.

```
Source API → Request data → Transform → Load
              │
              └── On-demand or scheduled
```

---

## Batch Ingestion

### When to Use

- Historical data processing
- Daily/weekly reports
- ML training data preparation
- When real-time isn't needed

### How It Works

```
┌─────────────┐                     ┌─────────────┐
│   Source    │    Schedule         │   Target    │
│  Database   │───────────────────►│ Data Lake   │
└─────────────┘    (e.g., daily)    └─────────────┘
      │                                    │
      │         ┌─────────────┐           │
      └────────►│   Extract   │───────────┘
                │ Transform   │
                │   Load      │
                └─────────────┘
```

### Patterns

**Full Extract**: Copy entire table every time.
```python
# Full extract - simple but inefficient for large tables
df = pd.read_sql("SELECT * FROM customers", engine)
df.to_parquet(f"data/customers/{date}.parquet")
```

**Incremental Extract**: Only get new/changed records.
```python
# Incremental - efficient, needs watermark
last_run = get_last_watermark()
df = pd.read_sql(f"""
    SELECT * FROM customers 
    WHERE updated_at > '{last_run}'
""", engine)
save_watermark(datetime.now())
```

**Change Data Capture (CDC)**: Capture database changes.
```python
# CDC captures INSERT, UPDATE, DELETE operations
# Usually done with tools like Debezium
```

### Tools

- **Apache Airflow**: Workflow orchestration
- **dbt**: SQL transformations
- **Spark**: Large-scale processing
- **Custom Python scripts**: Simple pipelines

### Example: Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_customers():
    df = pd.read_sql("SELECT * FROM customers", engine)
    df.to_parquet(f"/data/raw/customers/{datetime.now().date()}.parquet")

def transform_customers():
    df = pd.read_parquet(f"/data/raw/customers/*.parquet")
    df_clean = clean_data(df)
    df_clean.to_parquet(f"/data/processed/customers.parquet")

with DAG('customer_ingestion', schedule_interval='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_customers)
    transform = PythonOperator(task_id='transform', python_callable=transform_customers)
    extract >> transform
```

---

## Streaming Ingestion

### When to Use

- Real-time predictions
- Event-driven systems
- Low-latency requirements
- Continuous data flow

### How It Works

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Source    │───►│   Message   │───►│   Stream    │───►│   Target    │
│   Events    │    │   Broker    │    │  Processor  │    │   Store     │
└─────────────┘    │  (Kafka)    │    │  (Flink)    │    └─────────────┘
                   └─────────────┘    └─────────────┘
```

### Key Concepts

**Producer**: Sends events to the stream
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event = {'user_id': 123, 'action': 'login', 'timestamp': '2024-01-15T10:30:00'}
producer.send('user-events', event)
```

**Consumer**: Reads events from the stream
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    process_event(event)
```

### Tools

- **Apache Kafka**: Message broker
- **Apache Flink**: Stream processing
- **Apache Spark Streaming**: Micro-batch streaming
- **AWS Kinesis**: Managed streaming
- **Google Pub/Sub**: Managed messaging

### For ML: Usually Convert to Batch

Even with streaming sources, ML training is usually batch:

```
Real-time events → Kafka → [Aggregate] → Daily batch → Training data
```

Streaming ingestion feeds real-time serving:

```
Real-time events → Kafka → Feature computation → Online prediction
```

---

## API-Based Ingestion

### When to Use

- Third-party data (SaaS tools)
- No direct database access
- On-demand data pulls
- External data enrichment

### How It Works

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   API       │───►│   Client    │───►│   Target    │
│  Endpoint   │    │   (Python)  │    │   Store     │
└─────────────┘    └─────────────┘    └─────────────┘
      │
      └── REST, GraphQL, etc.
```

### Example: REST API

```python
import requests
import pandas as pd

def fetch_support_tickets(api_key, start_date, end_date):
    """Fetch tickets from Zendesk API."""
    url = "https://company.zendesk.com/api/v2/tickets.json"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"start_time": start_date.timestamp()}
    
    all_tickets = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_tickets.extend(data['tickets'])
        url = data.get('next_page')  # Pagination
    
    return pd.DataFrame(all_tickets)

# Usage
tickets = fetch_support_tickets(API_KEY, start_date, end_date)
tickets.to_parquet('data/raw/support/tickets.parquet')
```

### API Considerations

- **Rate Limits**: Don't exceed allowed requests
- **Pagination**: Handle large result sets
- **Authentication**: Secure API keys
- **Error Handling**: Retry on failures
- **Idempotency**: Handle duplicate pulls

### Tools

- **Python requests**: HTTP calls
- **Airflow HTTP operators**: Scheduled API calls
- **Fivetran / Airbyte**: Managed API connectors
- **Singer**: Open-source ETL

---

## Comparison

| Aspect | Batch | Streaming | API |
|--------|-------|-----------|-----|
| Latency | Hours/days | Seconds/minutes | On-demand |
| Volume | Large | Continuous | Variable |
| Complexity | Low | High | Medium |
| Use case | Training data | Real-time features | External data |
| Tools | Airflow, Spark | Kafka, Flink | requests, Fivetran |

---

## For Our Churn Project

We'll use:

| Data Source | Pattern | Frequency | Tool |
|-------------|---------|-----------|------|
| Customer DB | Batch (CDC) | Daily | Airflow |
| Usage logs | Batch (aggregate) | Daily | Airflow |
| Support tickets | API | Daily | Airflow + Python |
| Billing data | API | Daily | Airflow + Python |

### Our Ingestion Pipeline

```python
# airflow/dags/data_ingestion.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def extract_customers(**context):
    """Extract customer data from PostgreSQL."""
    from src.data.extract import extract_customers_incremental
    extract_customers_incremental(context['ds'])

def extract_usage(**context):
    """Extract usage data from data warehouse."""
    from src.data.extract import extract_usage_daily
    extract_usage_daily(context['ds'])

def extract_support(**context):
    """Extract support tickets from Zendesk API."""
    from src.data.extract import extract_support_tickets
    extract_support_tickets(context['ds'])

def extract_billing(**context):
    """Extract billing data from Stripe API."""
    from src.data.extract import extract_billing_data
    extract_billing_data(context['ds'])

with DAG(
    'data_ingestion',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    customers = PythonOperator(task_id='extract_customers', python_callable=extract_customers)
    usage = PythonOperator(task_id='extract_usage', python_callable=extract_usage)
    support = PythonOperator(task_id='extract_support', python_callable=extract_support)
    billing = PythonOperator(task_id='extract_billing', python_callable=extract_billing)
    
    # All run in parallel
    [customers, usage, support, billing]
```

---

## Recap

Three ingestion patterns:

1. **Batch**: Scheduled, large volumes, most common for ML
2. **Streaming**: Real-time, continuous, for online features
3. **API**: External data, on-demand, for SaaS integrations

For ML training: Batch is usually sufficient.
For real-time serving: May need streaming features.

Our project: Daily batch ingestion for all sources.

---

## What's Next

Now let's talk about ensuring data quality before it enters your ML pipeline.

---

**Next Lecture**: [5.3 – Data Quality & Validation (Basic Checks MLOps Must Enforce)](lecture-5.3-data-quality-validation.md)

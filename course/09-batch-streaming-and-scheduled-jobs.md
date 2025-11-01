# Module 09: Batch, Streaming & Scheduled Jobs

## 🎯 Goals

- Implement **batch scoring** for large datasets
- Build **streaming inference** with Kafka
- Schedule **recurring jobs** with Airflow cron
- Optimize **batch performance** (parallelization, batching)
- Handle **late-arriving data** and reprocessing
- Monitor **job execution** and failures

---

## 📖 Key Terms

- **Batch inference**: Scoring large datasets offline (e.g., nightly scoring of all customers)
- **Streaming inference**: Real-time predictions on event streams (Kafka, Kinesis)
- **Scheduled jobs**: Recurring tasks (daily model retraining, weekly reports)
- **Backfill**: Reprocessing historical data with new model/logic
- **Idempotency**: Running job multiple times produces same result (critical for retries)
- **Watermark**: Timestamp tracking progress in streaming (handles late data)

---

## 🔧 Commands First: Batch Scoring Script

```bash
# Create batch scoring script
cat > src/batch_score.py << 'EOF'
import mlflow.sklearn
import pandas as pd
import sys
from datetime import datetime

def batch_score(input_path, output_path, model_uri):
    """Score large dataset in batches"""
    
    # Load model
    model = mlflow.sklearn.load_model(model_uri)
    
    # Read data in chunks (for large files)
    chunk_size = 10000
    results = []
    
    for chunk in pd.read_csv(input_path, chunksize=chunk_size):
        X = chunk[['age', 'tenure', 'monthly_charges']]
        predictions = model.predict(X)
        
        chunk['prediction'] = predictions
        chunk['scored_at'] = datetime.now()
        results.append(chunk)
    
    # Combine and save
    df_scored = pd.concat(results, ignore_index=True)
    df_scored.to_csv(output_path, index=False)
    
    print(f"Scored {len(df_scored)} rows, saved to {output_path}")

if __name__ == "__main__":
    batch_score(
        input_path=sys.argv[1],
        output_path=sys.argv[2],
        model_uri="models:/ChurnPredictor/Production"
    )
EOF

# Run batch scoring
python src/batch_score.py data/customers.csv data/customers_scored.csv
```

**Why**: Chunked reading handles large files. Batch scoring is cost-effective for non-real-time needs.

---

## ⏰ Schedule with Airflow

```bash
# Create Airflow DAG for daily batch scoring
cat > ~/airflow/dags/batch_scoring_daily.py << 'EOF'
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_batch_scoring',
    default_args=default_args,
    description='Daily batch scoring of customer churn',
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False,
) as dag:
    
    extract_data = BashOperator(
        task_id='extract_customers',
        bash_command='python src/extract_data.py {{ ds }}',  # ds = execution date
    )
    
    score_batch = BashOperator(
        task_id='score_batch',
        bash_command='python src/batch_score.py data/customers_{{ ds }}.csv data/scored_{{ ds }}.csv',
    )
    
    upload_results = BashOperator(
        task_id='upload_to_s3',
        bash_command='aws s3 cp data/scored_{{ ds }}.csv s3://${BUCKET}/scored/',
    )
    
    extract_data >> score_batch >> upload_results
EOF
```

**Why**: Airflow cron schedules recurring jobs. `{{ ds }}` templating enables date-based file naming.

---

## 🌊 Streaming Inference with Kafka

```bash
# Install kafka-python
pip install kafka-python

# Create Kafka consumer for streaming inference
cat > src/streaming_consumer.py << 'EOF'
from kafka import KafkaConsumer, KafkaProducer
import mlflow.sklearn
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model
model = mlflow.sklearn.load_model("models:/ChurnPredictor/Production")

# Kafka setup
consumer = KafkaConsumer(
    'customer-events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='churn-predictor-group'
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

logger.info("Streaming consumer started")

for message in consumer:
    try:
        event = message.value
        
        # Extract features
        features = [[
            event['age'],
            event['tenure'],
            event['monthly_charges']
        ]]
        
        # Predict
        prediction = model.predict(features)[0]
        
        # Produce result
        result = {
            'customer_id': event['customer_id'],
            'prediction': int(prediction),
            'timestamp': event['timestamp']
        }
        producer.send('churn-predictions', value=result)
        
        logger.info(f"Predicted customer {event['customer_id']}: {prediction}")
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
EOF

# Run consumer (in background or container)
python src/streaming_consumer.py &
```

**Why**: Streaming enables real-time predictions on live events. Kafka provides durability and reprocessing.

---

## 🚀 Parallel Batch Processing

```bash
# Install dask for parallel processing
pip install dask[complete]

cat > src/batch_score_parallel.py << 'EOF'
import mlflow.sklearn
import dask.dataframe as dd
from datetime import datetime

def score_partition(df_partition, model_uri):
    """Score a single partition"""
    model = mlflow.sklearn.load_model(model_uri)
    X = df_partition[['age', 'tenure', 'monthly_charges']]
    df_partition['prediction'] = model.predict(X)
    df_partition['scored_at'] = datetime.now()
    return df_partition

# Read with Dask (parallel)
ddf = dd.read_csv('data/customers_large.csv')

# Score in parallel across partitions
model_uri = "models:/ChurnPredictor/Production"
ddf_scored = ddf.map_partitions(score_partition, model_uri=model_uri)

# Save
ddf_scored.to_csv('data/scored_parallel/*.csv', index=False)
print("Parallel batch scoring complete")
EOF
```

**Why**: Dask parallelizes across CPU cores. Scales to datasets larger than RAM.

---

## 🔄 Backfill Historical Data

```bash
# Create backfill script
cat > src/backfill.py << 'EOF'
import sys
from datetime import datetime, timedelta
import subprocess

def backfill(start_date, end_date):
    """Reprocess historical data"""
    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        print(f"Processing {date_str}...")
        
        # Run batch scoring for this date
        subprocess.run([
            'python', 'src/batch_score.py',
            f'data/customers_{date_str}.csv',
            f'data/scored_{date_str}.csv'
        ])
        
        current += timedelta(days=1)

if __name__ == "__main__":
    backfill(sys.argv[1], sys.argv[2])
EOF

# Backfill last 7 days
python src/backfill.py 2024-01-01 2024-01-07
```

**Why**: Backfill reprocesses data with new model. Ensures consistent predictions across time.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Create batch scoring job and schedule with Airflow.

1. **Create batch script**:
```bash
mkdir -p ~/mlops-lab-09 && cd ~/mlops-lab-09
# Copy batch_score.py from above
```

2. **Test locally**:
```bash
# Create sample data
cat > customers.csv << 'EOF'
customer_id,age,tenure,monthly_charges
1,34,12,65.5
2,45,24,89.0
EOF

python batch_score.py customers.csv scored.csv
cat scored.csv  # Should have predictions
```

3. **Create Airflow DAG**:
```bash
# Copy batch_scoring_daily.py to ~/airflow/dags/
```

4. **Trigger manually**:
```bash
airflow dags trigger daily_batch_scoring
```

**Expected output**: Batch job scores all rows, Airflow shows successful run.

---

## ❓ Quiz (5 Questions)

1. **When to use batch vs streaming inference?**
   - Answer: Batch for non-real-time, large datasets (nightly scoring). Streaming for real-time events (fraud detection).

2. **What is idempotency and why does it matter?**
   - Answer: Same input produces same output. Critical for safe retries after failures.

3. **How does Kafka enable reprocessing?**
   - Answer: Kafka retains events. Consumers can rewind offset to reprocess historical data.

4. **What is a backfill?**
   - Answer: Reprocessing historical data with new model or logic to ensure consistency.

5. **Why use Dask for batch scoring?**
   - Answer: Parallelizes across cores, handles datasets larger than RAM, speeds up processing.

---

## ⚠️ Common Mistakes

1. **Loading model per row** → Extremely slow.  
   *Fix*: Load once, predict in batches of 1000+ rows.

2. **Not handling failures** → Partial results, duplicates.  
   *Fix*: Make jobs idempotent, use Airflow retries, checkpoint progress.

3. **No monitoring** → Silent failures.  
   *Fix*: Log row counts, alert on job failures, track SLA.

4. **Streaming without error handling** → Consumer crashes on bad event.  
   *Fix*: Wrap in try/except, send bad events to dead-letter queue.

5. **Not versioning scored data** → Can't audit or debug.  
   *Fix*: Include model_version and scored_at timestamp in output.

---

## 🛠️ Troubleshooting

**Issue**: "Batch job OOM (Out Of Memory)"  
→ **Root cause**: Loading entire dataset at once.  
→ **Fix**: Use chunked reading (pandas chunksize) or Dask for parallel processing.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Batch job OOM"

**Issue**: "Kafka consumer lag increasing"  
→ **Root cause**: Predictions slower than event rate.  
→ **Fix*: Add more consumer instances (same group_id), optimize model inference, batch predictions.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Kafka consumer lag"

---

## 📚 Key Takeaways

- **Batch scoring** for offline, large-scale predictions (use chunking/Dask)
- **Streaming** for real-time inference on events (Kafka, Kinesis)
- **Schedule jobs** with Airflow cron expressions
- **Idempotency** enables safe retries after failures
- **Backfill** reprocesses historical data with new models
- **Monitor** job execution, lag, throughput

---

## 🚀 Next Steps

- **Module 10**: CI/CD pipelines for automated deployments
- **Module 11**: Observability and monitoring
- **Hands-on**: Build batch scoring pipeline for Churn Predictor

---

**[← Module 08](08-serving-and-apis.md)** | **[Next: Module 10 →](10-ci-cd-and-environments.md)**

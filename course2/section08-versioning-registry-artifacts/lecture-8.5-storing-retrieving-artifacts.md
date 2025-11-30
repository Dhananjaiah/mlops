# Lecture 8.5 – Storing and Retrieving Artifacts in Pipelines

## Human Transcript

Alright, let's talk about artifacts. In ML pipelines, you have lots of things moving around: datasets, processed data, trained models, evaluation reports, plots, logs. These are all artifacts. And managing them properly is crucial for reproducibility and debugging.

What's an artifact? It's any file or object that's produced or consumed by your pipeline. Some common examples:

Input artifacts:
- Raw data files
- Configuration files
- Pre-trained models for transfer learning

Intermediate artifacts:
- Processed and cleaned data
- Feature matrices
- Train/test splits

Output artifacts:
- Trained models
- Evaluation metrics
- Plots and visualizations
- Predictions

The challenge is: how do you store these, retrieve them, and track what was used where?

Let me show you different approaches.

Local filesystem. The simplest approach. Everything in a folder structure:

```
project/
├── data/
│   ├── raw/
│   │   └── customers.csv
│   ├── processed/
│   │   └── customers_clean.parquet
│   └── features/
│       └── feature_matrix.parquet
├── models/
│   └── churn_model_v1.joblib
├── reports/
│   └── evaluation_report.html
└── logs/
    └── training_2023-10-15.log
```

This works for experimentation, but has problems:
- No versioning
- Hard to share
- Easy to overwrite
- Doesn't scale

Cloud storage. Store artifacts in S3, GCS, or Azure Blob:

```python
import boto3
import joblib
from pathlib import Path

def save_artifact(artifact, s3_path, bucket='ml-artifacts'):
    """Save an artifact to S3."""
    s3 = boto3.client('s3')
    
    # Save locally first
    local_path = f"/tmp/{Path(s3_path).name}"
    joblib.dump(artifact, local_path)
    
    # Upload to S3
    s3.upload_file(local_path, bucket, s3_path)
    
    return f"s3://{bucket}/{s3_path}"

def load_artifact(s3_path, bucket='ml-artifacts'):
    """Load an artifact from S3."""
    s3 = boto3.client('s3')
    
    local_path = f"/tmp/{Path(s3_path).name}"
    s3.download_file(bucket, s3_path, local_path)
    
    return joblib.load(local_path)

# Usage
model_path = save_artifact(model, "models/churn/v1/model.joblib")
model = load_artifact("models/churn/v1/model.joblib")
```

MLflow artifacts. MLflow has built-in artifact management:

```python
import mlflow

with mlflow.start_run():
    # Log individual files
    mlflow.log_artifact("data/processed.csv")
    
    # Log entire directories
    mlflow.log_artifacts("plots/", artifact_path="visualizations")
    
    # Log the model (special handling)
    mlflow.sklearn.log_model(model, "model")
    
    # Log metrics file
    with open("metrics.json", "w") as f:
        json.dump(metrics, f)
    mlflow.log_artifact("metrics.json")

# Later, retrieve artifacts
run = mlflow.get_run(run_id)
artifact_uri = run.info.artifact_uri  # e.g., "s3://bucket/mlflow/123/"

# Download artifacts
mlflow.artifacts.download_artifacts(
    run_id=run_id,
    artifact_path="model",
    dst_path="./downloaded_model"
)
```

Now let's talk about artifact management in pipelines. When you have a pipeline with multiple steps, you need to pass artifacts between them.

With Airflow:

```python
from airflow.decorators import task, dag

@dag(schedule_interval="@daily")
def ml_pipeline():
    
    @task
    def extract_data():
        data = load_from_database()
        # Save to shared location
        data.to_parquet("s3://bucket/pipeline/data/raw.parquet")
        return "s3://bucket/pipeline/data/raw.parquet"
    
    @task
    def process_data(raw_path):
        data = pd.read_parquet(raw_path)
        processed = clean_and_transform(data)
        processed_path = "s3://bucket/pipeline/data/processed.parquet"
        processed.to_parquet(processed_path)
        return processed_path
    
    @task
    def train_model(processed_path):
        data = pd.read_parquet(processed_path)
        model = train(data)
        model_path = "s3://bucket/pipeline/models/model.joblib"
        joblib.dump(model, model_path)
        return model_path
    
    raw = extract_data()
    processed = process_data(raw)
    model = train_model(processed)

ml_pipeline()
```

With Prefect:

```python
from prefect import task, flow

@task
def process_data(data_path: str) -> str:
    data = pd.read_parquet(data_path)
    processed = clean_and_transform(data)
    output_path = "s3://bucket/processed.parquet"
    processed.to_parquet(output_path)
    return output_path

@task
def train_model(data_path: str) -> str:
    data = pd.read_parquet(data_path)
    model = train(data)
    model_path = "s3://bucket/model.joblib"
    save_artifact(model, model_path)
    return model_path

@flow
def ml_pipeline():
    raw_path = "s3://bucket/raw.parquet"
    processed_path = process_data(raw_path)
    model_path = train_model(processed_path)
    return model_path
```

Best practices for artifact management:

Use consistent naming. Include version or timestamp:
```
s3://bucket/artifacts/
├── churn-model/
│   ├── v1.0.0/
│   │   ├── model.joblib
│   │   ├── metadata.json
│   │   └── metrics.json
│   └── v1.0.1/
│       └── ...
├── features/
│   ├── 2023-10-15/
│   │   └── feature_matrix.parquet
│   └── 2023-10-16/
│       └── feature_matrix.parquet
```

Include metadata. Every artifact should have associated metadata:

```python
def save_artifact_with_metadata(artifact, path, metadata):
    # Save the artifact
    joblib.dump(artifact, f"{path}/artifact.joblib")
    
    # Save metadata
    metadata_dict = {
        "created_at": datetime.now().isoformat(),
        "git_commit": get_git_commit(),
        "python_version": sys.version,
        "dependencies": get_installed_packages(),
        **metadata
    }
    with open(f"{path}/metadata.json", "w") as f:
        json.dump(metadata_dict, f)
```

Use checksums. Verify artifacts weren't corrupted:

```python
import hashlib

def compute_checksum(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def save_with_checksum(data, path):
    joblib.dump(data, path)
    checksum = compute_checksum(path)
    with open(f"{path}.sha256", 'w') as f:
        f.write(checksum)

def load_with_checksum(path):
    expected = open(f"{path}.sha256").read().strip()
    actual = compute_checksum(path)
    if expected != actual:
        raise ValueError(f"Checksum mismatch for {path}")
    return joblib.load(path)
```

Set retention policies. Don't keep artifacts forever. Define policies:

```python
def cleanup_old_artifacts(bucket, prefix, keep_days=30):
    s3 = boto3.client('s3')
    cutoff = datetime.now() - timedelta(days=keep_days)
    
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in objects.get('Contents', []):
        if obj['LastModified'] < cutoff:
            s3.delete_object(Bucket=bucket, Key=obj['Key'])
```

Track lineage. Know where each artifact came from:

```python
# In your training script
lineage = {
    "artifact_type": "model",
    "created_from": {
        "data_path": data_path,
        "data_checksum": compute_checksum(data_path),
        "code_commit": get_git_commit(),
        "training_run_id": mlflow.active_run().info.run_id
    }
}
save_artifact_with_metadata(model, model_path, lineage)
```

Handle large artifacts. For very large files, consider:
- Multipart uploads
- Compression
- Streaming instead of loading into memory

```python
def upload_large_file(filepath, bucket, key, chunk_size=50*1024*1024):
    """Upload large file using multipart upload."""
    s3 = boto3.client('s3')
    
    upload = s3.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = upload['UploadId']
    
    parts = []
    with open(filepath, 'rb') as f:
        part_number = 1
        while chunk := f.read(chunk_size):
            part = s3.upload_part(
                Bucket=bucket,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk
            )
            parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
            part_number += 1
    
    s3.complete_multipart_upload(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
```

Alright, that's artifact management. The key points: store artifacts in a shared, versioned location; include metadata with everything; track lineage between artifacts; and have cleanup policies to manage storage costs.

In the final lecture of this section, we'll talk about governance: who can do what with models and data.

Questions? Let's wrap up this section.

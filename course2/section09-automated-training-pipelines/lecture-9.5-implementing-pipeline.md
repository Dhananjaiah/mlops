# Lecture 9.5 – Implementing the Training Pipeline (Example with One Tool)

## Human Transcript

Alright, let's implement the pipeline we designed. I'm going to use Prefect because it's easy to understand and you can run it locally without complex setup. The concepts transfer to any other tool.

First, let's set up our environment:

```bash
pip install prefect pandas scikit-learn xgboost mlflow
```

Now let's create our pipeline. I'm going to build a complete, runnable example:

```python
# pipelines/training_pipeline.py
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import mlflow
from mlflow.tracking import MlflowClient
import joblib
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure MLflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("churn-prediction")


@task(retries=3, retry_delay_seconds=60)
def extract_data(execution_date: str) -> str:
    """
    Extract customer data for training.
    
    In a real scenario, this would query a database or API.
    For this example, we'll generate synthetic data.
    """
    logger.info(f"Extracting data for {execution_date}")
    
    # Generate synthetic customer data
    np.random.seed(42)
    n_samples = 5000
    
    data = {
        'customer_id': [f'CUST{i:05d}' for i in range(n_samples)],
        'tenure_months': np.random.randint(1, 72, n_samples),
        'monthly_charges': np.random.uniform(20, 100, n_samples),
        'total_charges': np.random.uniform(100, 5000, n_samples),
        'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'payment_method': np.random.choice(['Bank transfer', 'Credit card', 'Electronic check'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable with some logic
    churn_probability = (
        0.3 * (df['contract_type'] == 'Month-to-month').astype(float) +
        0.2 * (df['tenure_months'] < 12).astype(float) +
        0.2 * (df['monthly_charges'] > 70).astype(float) +
        np.random.uniform(0, 0.3, n_samples)
    )
    df['churned'] = (churn_probability > 0.5).astype(int)
    
    # Save to file
    output_dir = Path(f"data/raw/{execution_date}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / "customers.parquet")
    df.to_parquet(output_path)
    
    logger.info(f"Extracted {len(df)} records to {output_path}")
    return output_path


@task(retries=2)
def validate_data(data_path: str) -> dict:
    """Validate data quality before processing."""
    logger.info(f"Validating data from {data_path}")
    
    df = pd.read_parquet(data_path)
    
    validations = {
        "row_count": len(df),
        "null_rate": float(df.isnull().mean().mean()),
        "churn_rate": float(df['churned'].mean()),
        "duplicate_rate": float(df.duplicated(subset=['customer_id']).mean()),
        "data_path": data_path
    }
    
    # Quality gates
    issues = []
    
    if validations["row_count"] < 100:
        issues.append(f"Too few records: {validations['row_count']}")
    
    if validations["null_rate"] > 0.1:
        issues.append(f"Too many nulls: {validations['null_rate']:.1%}")
    
    if validations["duplicate_rate"] > 0.01:
        issues.append(f"Too many duplicates: {validations['duplicate_rate']:.1%}")
    
    if validations["churn_rate"] < 0.05 or validations["churn_rate"] > 0.95:
        issues.append(f"Unusual churn rate: {validations['churn_rate']:.1%}")
    
    if issues:
        raise ValueError(f"Data validation failed: {'; '.join(issues)}")
    
    logger.info(f"Data validation passed: {validations}")
    return validations


@task
def transform_and_engineer_features(validation_result: dict) -> dict:
    """Transform data and create features."""
    data_path = validation_result['data_path']
    logger.info(f"Transforming data from {data_path}")
    
    df = pd.read_parquet(data_path)
    
    # Handle missing values
    df['total_charges'] = df['total_charges'].fillna(0)
    
    # Create derived features
    df['avg_monthly'] = df['total_charges'] / (df['tenure_months'] + 1)
    df['is_new_customer'] = (df['tenure_months'] < 6).astype(int)
    df['is_high_value'] = (df['monthly_charges'] > 70).astype(int)
    
    # Encode categoricals
    df = pd.get_dummies(df, columns=['contract_type', 'payment_method'])
    
    # Define feature columns
    feature_columns = [
        'tenure_months', 'monthly_charges', 'total_charges', 'avg_monthly',
        'is_new_customer', 'is_high_value',
        'contract_type_Month-to-month', 'contract_type_One year', 
        'contract_type_Two year', 'payment_method_Bank transfer',
        'payment_method_Credit card', 'payment_method_Electronic check'
    ]
    
    # Ensure all columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Split data
    X = df[feature_columns]
    y = df['churned']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Save feature matrices
    output_dir = Path(data_path).parent.parent / "features"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / "feature_data.joblib")
    
    joblib.dump({
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test,
        'feature_columns': feature_columns
    }, output_path)
    
    logger.info(f"Created {len(feature_columns)} features, saved to {output_path}")
    
    return {
        "feature_path": output_path,
        "n_features": len(feature_columns),
        "n_train": len(X_train),
        "n_test": len(X_test)
    }


@task
def train_model(feature_data: dict) -> dict:
    """Train the churn prediction model."""
    logger.info("Training model...")
    
    data = joblib.load(feature_data['feature_path'])
    
    with mlflow.start_run() as run:
        # Log parameters
        params = {
            "n_estimators": 100,
            "max_depth": 5,
            "learning_rate": 0.1,
            "random_state": 42
        }
        
        for key, value in params.items():
            mlflow.log_param(key, value)
        
        mlflow.log_param("n_features", feature_data['n_features'])
        mlflow.log_param("n_train_samples", feature_data['n_train'])
        
        # Train model
        model = XGBClassifier(**params)
        model.fit(data['X_train'], data['y_train'])
        
        # Log model
        mlflow.xgboost.log_model(model, "model")
        
        logger.info(f"Model trained, run_id: {run.info.run_id}")
        
        return {
            "run_id": run.info.run_id,
            "model_uri": f"runs:/{run.info.run_id}/model",
            "feature_path": feature_data['feature_path']
        }


@task
def evaluate_model(model_info: dict) -> dict:
    """Evaluate model performance."""
    logger.info("Evaluating model...")
    
    # Load model and data
    model = mlflow.xgboost.load_model(model_info['model_uri'])
    data = joblib.load(model_info['feature_path'])
    
    # Predictions
    y_pred = model.predict(data['X_test'])
    y_proba = model.predict_proba(data['X_test'])[:, 1]
    
    # Calculate metrics
    metrics = {
        "accuracy": float(accuracy_score(data['y_test'], y_pred)),
        "precision": float(precision_score(data['y_test'], y_pred)),
        "recall": float(recall_score(data['y_test'], y_pred)),
        "f1": float(f1_score(data['y_test'], y_pred)),
        "auc_roc": float(roc_auc_score(data['y_test'], y_proba))
    }
    
    # Log metrics to MLflow
    with mlflow.start_run(run_id=model_info['run_id']):
        for name, value in metrics.items():
            mlflow.log_metric(name, value)
    
    logger.info(f"Model metrics: {metrics}")
    
    return {
        **model_info,
        "metrics": metrics
    }


@task
def compare_and_register(eval_results: dict) -> dict:
    """Compare with production and register if better."""
    logger.info("Comparing with production model...")
    
    client = MlflowClient()
    
    # Check if model exists
    try:
        prod_versions = client.get_latest_versions("churn-model", stages=["Production"])
    except mlflow.exceptions.MlflowException:
        prod_versions = []
    
    should_register = False
    reason = ""
    
    if not prod_versions:
        should_register = True
        reason = "No production model exists"
    else:
        # Get production model metrics
        prod_run = client.get_run(prod_versions[0].run_id)
        prod_f1 = prod_run.data.metrics.get("f1", 0)
        new_f1 = eval_results['metrics']['f1']
        
        improvement = (new_f1 - prod_f1) / prod_f1 if prod_f1 > 0 else float('inf')
        
        if improvement > 0.01:  # More than 1% improvement
            should_register = True
            reason = f"F1 improved by {improvement:.2%} ({prod_f1:.4f} -> {new_f1:.4f})"
        else:
            reason = f"F1 did not improve enough ({improvement:.2%})"
    
    if should_register:
        # Register the model
        try:
            model_version = mlflow.register_model(
                eval_results['model_uri'],
                "churn-model"
            )
            version = model_version.version
            logger.info(f"Registered model version {version}")
        except Exception as e:
            logger.error(f"Failed to register model: {e}")
            version = None
            should_register = False
            reason = f"Registration failed: {e}"
    else:
        version = None
    
    return {
        "registered": should_register,
        "version": version,
        "reason": reason,
        "metrics": eval_results['metrics']
    }


@task
def notify_results(result: dict) -> None:
    """Send notification about pipeline results."""
    if result['registered']:
        message = f"""
        ✅ New churn model registered!
        
        Version: {result['version']}
        Reason: {result['reason']}
        
        Metrics:
        - Accuracy: {result['metrics']['accuracy']:.4f}
        - Precision: {result['metrics']['precision']:.4f}
        - Recall: {result['metrics']['recall']:.4f}
        - F1 Score: {result['metrics']['f1']:.4f}
        - AUC-ROC: {result['metrics']['auc_roc']:.4f}
        """
    else:
        message = f"""
        ℹ️ Training completed, no new model registered.
        
        Reason: {result['reason']}
        
        New Model Metrics:
        - F1 Score: {result['metrics']['f1']:.4f}
        - AUC-ROC: {result['metrics']['auc_roc']:.4f}
        """
    
    logger.info(message)
    
    # In production, you would send to Slack, email, etc.
    # send_slack_notification(channel="#ml-alerts", message=message)
    # send_email(to="ml-team@company.com", subject="Churn Model Training", body=message)


@flow(name="churn-model-training", log_prints=True)
def training_pipeline(execution_date: str = None):
    """
    Main training pipeline for churn prediction model.
    
    Args:
        execution_date: Date string (YYYY-MM-DD) for the training run.
                       Defaults to today.
    """
    if execution_date is None:
        execution_date = datetime.now().strftime("%Y-%m-%d")
    
    logger.info(f"Starting training pipeline for {execution_date}")
    
    # Execute pipeline steps
    data_path = extract_data(execution_date)
    validation = validate_data(data_path)
    features = transform_and_engineer_features(validation)
    model_info = train_model(features)
    evaluation = evaluate_model(model_info)
    registration = compare_and_register(evaluation)
    notify_results(registration)
    
    return registration


if __name__ == "__main__":
    # Run the pipeline
    result = training_pipeline()
    print(f"\nPipeline completed. Result: {result}")
```

To run this pipeline:

```bash
python pipelines/training_pipeline.py
```

You'll see output like:

```
INFO: Starting training pipeline for 2023-10-15
INFO: Extracting data for 2023-10-15
INFO: Extracted 5000 records to data/raw/2023-10-15/customers.parquet
INFO: Validating data from data/raw/2023-10-15/customers.parquet
INFO: Data validation passed: {'row_count': 5000, 'null_rate': 0.0, ...}
INFO: Transforming data from data/raw/2023-10-15/customers.parquet
INFO: Created 12 features, saved to data/features/feature_data.joblib
INFO: Training model...
INFO: Model trained, run_id: abc123def456
INFO: Evaluating model...
INFO: Model metrics: {'accuracy': 0.83, 'f1': 0.79, ...}
INFO: Comparing with production model...
INFO: Registered model version 1

✅ New churn model registered!
Version: 1
Reason: No production model exists
```

To schedule this with Prefect:

```python
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(
    flow=training_pipeline,
    name="daily-churn-training",
    schedule=CronSchedule(cron="0 6 * * *"),  # Daily at 6 AM
    work_queue_name="ml-training"
)

deployment.apply()
```

Now the pipeline will run automatically every day at 6 AM.

That's a complete, working implementation. In the next lecture, we'll talk about handling scheduling, retries, and failures.

Questions?

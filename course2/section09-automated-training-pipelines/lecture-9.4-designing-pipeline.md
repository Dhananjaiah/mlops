# Lecture 9.4 – Designing a Training Pipeline for Our Project (Diagram)

## Human Transcript

Alright, let's get practical. We're going to design a complete training pipeline for our churn prediction project. I'm going to walk you through the thinking process, show you the architecture, and explain why each piece exists.

Remember our project? We're predicting customer churn. We have customer data coming from our database, and we want to retrain our model regularly to keep it fresh.

Let's start with the requirements:

1. The pipeline should run daily
2. It should use the latest customer data
3. It should only deploy a new model if it's better than the current one
4. It should notify the team of results
5. It should be fully automated, no human intervention needed
6. Everything should be logged for debugging and auditing

Here's the high-level architecture:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Training Pipeline                             │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Extract   │────▶│   Validate   │────▶│  Transform   │
│     Data     │     │     Data     │     │    Data      │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                     ┌───────────────────────────┘
                     │
                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Feature    │────▶│    Train     │────▶│   Evaluate   │
│ Engineering  │     │    Model     │     │    Model     │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                     ┌───────────────────────────┘
                     │
                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Compare    │────▶│   Register   │────▶│   Notify     │
│  with Prod   │     │    Model     │     │    Team      │
└──────────────┘     └──────────────┘     └──────────────┘
```

Let me walk through each step:

Extract Data. This step pulls the latest customer data from our source systems.

```python
@task
def extract_data(execution_date: str) -> str:
    """Extract customer data for training."""
    query = f"""
    SELECT 
        customer_id,
        signup_date,
        tenure_months,
        monthly_charges,
        total_charges,
        contract_type,
        payment_method,
        churned
    FROM customers
    WHERE snapshot_date = '{execution_date}'
    """
    
    df = pd.read_sql(query, connection)
    
    output_path = f"s3://ml-data/churn/raw/{execution_date}/customers.parquet"
    df.to_parquet(output_path)
    
    log.info(f"Extracted {len(df)} records to {output_path}")
    return output_path
```

Validate Data. Before we do anything with the data, we check it's valid.

```python
@task
def validate_data(data_path: str) -> dict:
    """Validate data quality before processing."""
    df = pd.read_parquet(data_path)
    
    validations = {
        "row_count": len(df),
        "null_rate": df.isnull().mean().mean(),
        "target_distribution": df['churned'].value_counts(normalize=True).to_dict(),
        "duplicate_rate": df.duplicated(subset=['customer_id']).mean()
    }
    
    # Quality gates
    if validations["row_count"] < 1000:
        raise ValueError(f"Too few records: {validations['row_count']}")
    
    if validations["null_rate"] > 0.1:
        raise ValueError(f"Too many nulls: {validations['null_rate']:.1%}")
    
    if validations["duplicate_rate"] > 0.01:
        raise ValueError(f"Too many duplicates: {validations['duplicate_rate']:.1%}")
    
    log.info(f"Data validation passed: {validations}")
    return validations
```

Transform Data. Clean and prepare the data for modeling.

```python
@task
def transform_data(data_path: str) -> str:
    """Transform raw data into modeling-ready format."""
    df = pd.read_parquet(data_path)
    
    # Handle missing values
    df['total_charges'] = df['total_charges'].fillna(0)
    
    # Encode categoricals
    df = pd.get_dummies(df, columns=['contract_type', 'payment_method'])
    
    # Create derived features
    df['avg_monthly'] = df['total_charges'] / (df['tenure_months'] + 1)
    
    # Split
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['churned'])
    
    train_path = data_path.replace('raw', 'processed').replace('.parquet', '_train.parquet')
    test_path = data_path.replace('raw', 'processed').replace('.parquet', '_test.parquet')
    
    train_df.to_parquet(train_path)
    test_df.to_parquet(test_path)
    
    return {"train_path": train_path, "test_path": test_path}
```

Feature Engineering. Create features for the model.

```python
@task
def engineer_features(data_paths: dict) -> dict:
    """Create model features."""
    train_df = pd.read_parquet(data_paths['train_path'])
    test_df = pd.read_parquet(data_paths['test_path'])
    
    feature_columns = [
        'tenure_months', 'monthly_charges', 'total_charges', 'avg_monthly',
        'contract_type_Month-to-month', 'contract_type_One year', 
        'contract_type_Two year', 'payment_method_Bank transfer',
        'payment_method_Credit card', 'payment_method_Electronic check'
    ]
    
    X_train = train_df[feature_columns]
    y_train = train_df['churned']
    X_test = test_df[feature_columns]
    y_test = test_df['churned']
    
    # Save feature matrices
    feature_path = data_paths['train_path'].replace('processed', 'features')
    
    joblib.dump({
        'X_train': X_train, 'y_train': y_train,
        'X_test': X_test, 'y_test': y_test,
        'feature_columns': feature_columns
    }, feature_path)
    
    return {"feature_path": feature_path, "n_features": len(feature_columns)}
```

Train Model. The core training step.

```python
@task
def train_model(feature_data: dict) -> dict:
    """Train the churn prediction model."""
    import mlflow
    
    data = joblib.load(feature_data['feature_path'])
    
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param("n_features", feature_data['n_features'])
        mlflow.log_param("n_train_samples", len(data['X_train']))
        
        # Train model
        model = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        model.fit(data['X_train'], data['y_train'])
        
        # Log model
        mlflow.xgboost.log_model(model, "model")
        
        return {
            "run_id": run.info.run_id,
            "model_uri": f"runs:/{run.info.run_id}/model"
        }
```

Evaluate Model. Measure how good the model is.

```python
@task
def evaluate_model(model_info: dict, feature_data: dict) -> dict:
    """Evaluate model performance."""
    import mlflow
    
    # Load model and data
    model = mlflow.xgboost.load_model(model_info['model_uri'])
    data = joblib.load(feature_data['feature_path'])
    
    # Predictions
    y_pred = model.predict(data['X_test'])
    y_proba = model.predict_proba(data['X_test'])[:, 1]
    
    # Metrics
    metrics = {
        "accuracy": accuracy_score(data['y_test'], y_pred),
        "precision": precision_score(data['y_test'], y_pred),
        "recall": recall_score(data['y_test'], y_pred),
        "f1": f1_score(data['y_test'], y_pred),
        "auc_roc": roc_auc_score(data['y_test'], y_proba)
    }
    
    # Log to MLflow
    with mlflow.start_run(run_id=model_info['run_id']):
        for name, value in metrics.items():
            mlflow.log_metric(name, value)
    
    log.info(f"Model metrics: {metrics}")
    return {**model_info, "metrics": metrics}
```

Compare with Production. Only deploy if we're better than the current model.

```python
@task
def compare_with_production(eval_results: dict) -> dict:
    """Compare new model with production model."""
    # Get current production model metrics
    client = MlflowClient()
    prod_versions = client.get_latest_versions("churn-model", stages=["Production"])
    
    if not prod_versions:
        # No production model yet, proceed
        return {**eval_results, "should_deploy": True, "reason": "No production model"}
    
    prod_run = client.get_run(prod_versions[0].run_id)
    prod_f1 = prod_run.data.metrics.get("f1", 0)
    
    new_f1 = eval_results['metrics']['f1']
    improvement = (new_f1 - prod_f1) / prod_f1 if prod_f1 > 0 else float('inf')
    
    # Deploy if at least 1% improvement
    should_deploy = improvement > 0.01
    
    return {
        **eval_results,
        "should_deploy": should_deploy,
        "prod_f1": prod_f1,
        "improvement": improvement,
        "reason": f"F1 improvement: {improvement:.2%}"
    }
```

Register Model. If approved, register in the model registry.

```python
@task
def register_model(comparison: dict) -> dict:
    """Register model if it should be deployed."""
    if not comparison['should_deploy']:
        log.info(f"Skipping registration: {comparison['reason']}")
        return {"registered": False, "reason": comparison['reason']}
    
    # Register the model
    model_version = mlflow.register_model(
        comparison['model_uri'],
        "churn-model"
    )
    
    # Transition to staging first
    client = MlflowClient()
    client.transition_model_version_stage(
        name="churn-model",
        version=model_version.version,
        stage="Staging"
    )
    
    log.info(f"Registered model version {model_version.version} to Staging")
    return {
        "registered": True,
        "version": model_version.version,
        "metrics": comparison['metrics']
    }
```

Notify Team. Send results to the team.

```python
@task
def notify_team(result: dict):
    """Send notification about pipeline results."""
    if result['registered']:
        message = f"""
        ✅ New churn model registered!
        
        Version: {result['version']}
        F1 Score: {result['metrics']['f1']:.4f}
        AUC-ROC: {result['metrics']['auc_roc']:.4f}
        
        Model is now in Staging. Please review and promote to Production.
        """
    else:
        message = f"""
        ℹ️ Training completed, no new model registered.
        
        Reason: {result['reason']}
        """
    
    send_slack_notification(channel="#ml-alerts", message=message)
    send_email(to="ml-team@company.com", subject="Churn Model Training", body=message)
```

Now let's put it all together:

```python
@dag(
    schedule_interval="0 6 * * *",  # Daily at 6 AM
    start_date=datetime(2023, 1, 1),
    catchup=False
)
def churn_model_training():
    # Extract
    data_path = extract_data()
    
    # Validate
    validation = validate_data(data_path)
    
    # Transform
    processed = transform_data(data_path)
    
    # Feature engineering
    features = engineer_features(processed)
    
    # Train
    model = train_model(features)
    
    # Evaluate
    evaluation = evaluate_model(model, features)
    
    # Compare
    comparison = compare_with_production(evaluation)
    
    # Register
    registration = register_model(comparison)
    
    # Notify
    notify_team(registration)
```

That's our complete pipeline. In the next lecture, we'll actually implement this with a real tool.

Questions before we dive into implementation?

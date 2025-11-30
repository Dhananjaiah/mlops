# Lecture 9.7 – Where MLOps Sits vs Data Engineers in Orchestration

## Human Transcript

Let me close out this section by addressing something that causes a lot of confusion in organizations: who owns what when it comes to pipelines and orchestration?

In many companies, you'll have data engineers, ML engineers, MLOps engineers, and sometimes platform engineers. They all work with pipelines. So who does what?

Let me paint a picture of the typical data flow in an organization:

```
Raw Data Sources → Data Pipelines → Feature Store → ML Training → Model Serving
                   ↑                               ↑              ↑
              Data Engineers                  ML Engineers    MLOps Engineers
```

Data Engineers. They're responsible for:
- Getting data from source systems into the data platform
- Building and maintaining data pipelines (ETL/ELT)
- Ensuring data quality and freshness
- Managing data infrastructure (warehouses, lakes, streaming)

Their pipelines look like:

```python
# Data Engineering Pipeline
@dag(schedule="@hourly")
def customer_data_pipeline():
    # Extract from source systems
    raw_transactions = extract_from_postgres()
    raw_clickstream = extract_from_kafka()
    raw_crm = extract_from_salesforce_api()
    
    # Transform and clean
    clean_transactions = transform_transactions(raw_transactions)
    clean_clickstream = transform_clickstream(raw_clickstream)
    clean_crm = transform_crm(raw_crm)
    
    # Load to data warehouse
    load_to_warehouse([clean_transactions, clean_clickstream, clean_crm])
    
    # Update data catalog
    update_catalog()
```

ML Engineers. They're responsible for:
- Designing and training ML models
- Feature engineering
- Model experimentation
- Working with data scientists on productionizing models

Their pipelines look like:

```python
# ML Engineering Pipeline
@flow
def model_training_flow():
    # Feature engineering
    features = create_features(raw_data)
    
    # Experiment with different models
    model_a = train_xgboost(features)
    model_b = train_lightgbm(features)
    model_c = train_neural_net(features)
    
    # Evaluate and select best
    best_model = evaluate_and_select([model_a, model_b, model_c])
    
    # Register for deployment
    register_model(best_model)
```

MLOps Engineers. They're responsible for:
- Deploying models to production
- Monitoring model performance
- Managing model lifecycle
- CI/CD for ML systems
- Infrastructure for ML (training clusters, serving infrastructure)

Their pipelines look like:

```python
# MLOps Pipeline
@dag(schedule="@daily")
def model_deployment_pipeline():
    # Get latest approved model
    model = get_approved_model_from_registry()
    
    # Build and test container
    container = build_serving_container(model)
    run_integration_tests(container)
    
    # Deploy with canary
    deploy_canary(container, traffic_percent=10)
    
    # Monitor and validate
    metrics = monitor_canary(duration_hours=2)
    
    # Full deployment if successful
    if validate_metrics(metrics):
        deploy_full(container)
    else:
        rollback()
```

Where do the boundaries lie?

The handoff between Data Engineering and ML typically happens at the feature store or clean data layer:

```
Data Engineering Domain        │  ML Domain
                               │
Source Systems                 │  Feature Store
    ↓                         │      ↓
Raw Data Layer                 │  Training Data
    ↓                         │      ↓
Cleaned Data Layer ──────────────→ Model Training
    ↓                         │      ↓
Data Warehouse                 │  Model Registry
```

Data Engineers say: "Here's clean, reliable data in the feature store, updated hourly."

ML Engineers say: "We'll use that data to train models and register them here."

The handoff between ML Engineering and MLOps typically happens at the model registry:

```
ML Engineering Domain          │  MLOps Domain
                               │
Experiments                    │  Model Registry
    ↓                         │      ↓
Model Development              │  Staging Deployment
    ↓                         │      ↓
Model Registration ──────────────→ Production Deployment
                               │      ↓
                               │  Monitoring
```

ML Engineers say: "Here's a trained model in the registry with these metrics."

MLOps Engineers say: "We'll deploy it, monitor it, and let you know if it degrades."

Shared responsibilities. Some things are shared:

Feature pipelines. These might be owned by:
- Data Engineers (if they're simple transformations)
- ML Engineers (if they require ML expertise)
- A dedicated Feature Platform team (in larger orgs)

```python
# Feature Pipeline - Could be DE or ML
@dag(schedule="@hourly")
def feature_pipeline():
    # Get clean data (from DE)
    clean_data = get_from_warehouse()
    
    # Create ML features (ML expertise needed)
    features = compute_features(clean_data)
    
    # Store in feature store (infrastructure)
    write_to_feature_store(features)
```

Training pipelines. Often a collaboration:
- Infrastructure: MLOps
- Pipeline logic: ML Engineers
- Data dependencies: Data Engineers

Orchestrator ownership. Who owns the orchestration platform itself?

In some organizations: Data Engineering. They run Airflow, everyone uses it.

In others: Platform/MLOps team. They provide a self-service platform.

In others: Each team runs their own (not recommended at scale).

My recommendation: Have a platform team (could be called MLOps Platform, Data Platform, or just Platform) that owns the orchestration infrastructure. Teams self-serve on top of it.

```
┌────────────────────────────────────────────────────────┐
│                Platform Team Owns                       │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Airflow / Prefect Cluster           │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│    Data Engineers      ML Engineers     MLOps Engineers│
│    deploy their        deploy their     deploy their   │
│    DAGs here           flows here       pipelines here │
└────────────────────────────────────────────────────────┘
```

Communication patterns. When things span teams, communication is key:

SLAs and contracts:

```python
# Data Engineering provides this guarantee
DATA_SLA = {
    "table": "clean_customers",
    "freshness": "1 hour",
    "availability": "99.9%",
    "schema_version": "2.3.0"
}

# ML team depends on it
@task
def get_training_data():
    # Check SLA before proceeding
    freshness = check_data_freshness("clean_customers")
    if freshness > timedelta(hours=2):
        raise DataSLAViolation("Data is too stale")
    return load_data("clean_customers")
```

Event-based handoffs:

```python
# Data Engineering publishes
publish_event("data.customers.updated", {
    "timestamp": datetime.now(),
    "record_count": 1000000
})

# ML Pipeline subscribes
@flow(triggers=[EventTrigger("data.customers.updated")])
def training_triggered_by_data_update(event):
    logger.info(f"New data available: {event['record_count']} records")
    train_model()
```

Shared monitoring:

```python
# Everyone reports to the same dashboard
emit_metric("pipeline.duration", duration, tags={
    "pipeline": "customer_features",
    "owner": "data_engineering"
})

emit_metric("pipeline.duration", duration, tags={
    "pipeline": "churn_training",
    "owner": "ml_engineering"
})
```

The bottom line:

1. Data Engineers own getting data ready
2. ML Engineers own building models
3. MLOps owns deploying and monitoring models
4. Everyone uses shared infrastructure
5. Clear contracts and communication at handoff points

This isn't always clean-cut. Many organizations have hybrid roles. The important thing is that someone owns each piece and teams communicate at boundaries.

This wraps up Section 9 on automated training pipelines. You now understand why we need pipelines, how to build them, what tools to use, and how different teams work together.

In the next section, we'll talk about CI/CD for ML systems - how to automatically test, build, and deploy your ML code and models.

See you there!

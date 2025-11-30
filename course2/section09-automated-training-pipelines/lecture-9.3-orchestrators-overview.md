# Lecture 9.3 – Overview of Common Orchestrators (Airflow, Prefect, Kubeflow, Tekton, etc.)

## Human Transcript

Now that you understand the building blocks, let's look at the tools. There are many orchestration tools out there, and honestly, it can be overwhelming. So let me give you a clear picture of the landscape and when to use what.

Let me start with the major players.

Apache Airflow. This is the most widely used orchestrator in data and ML. It's been around since 2014 and has a huge community.

Pros:
- Mature and battle-tested
- Huge ecosystem of operators and plugins
- Great for scheduled batch jobs
- Excellent monitoring UI
- Strong community support

Cons:
- Complex to set up and manage
- DAGs are defined in Python files that get parsed, which can be slow
- Not great for dynamic workflows
- Heavy for simple use cases

Best for: Scheduled data pipelines, batch ML training, enterprise environments with existing Airflow installations.

```python
# Airflow DAG example
from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(
    "ml_training_pipeline",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily"
) as dag:
    
    @task
    def extract():
        return "data/raw.csv"
    
    @task
    def transform(path):
        return "data/processed.csv"
    
    @task
    def train(path):
        return "models/model.pkl"
    
    raw = extract()
    processed = transform(raw)
    model = train(processed)
```

Prefect. A newer alternative to Airflow. Designed to fix some of Airflow's pain points.

Pros:
- Modern Python-native API
- Easier local development
- Better handling of dynamic workflows
- Cloud-hosted option available
- Simpler to get started

Cons:
- Smaller community than Airflow
- Less mature
- Some features require Prefect Cloud

Best for: Modern ML teams, dynamic workflows, teams that value developer experience.

```python
# Prefect flow example
from prefect import flow, task

@task
def extract():
    return "data/raw.csv"

@task
def transform(path):
    return "data/processed.csv"

@task
def train(path):
    return "models/model.pkl"

@flow
def ml_pipeline():
    raw = extract()
    processed = transform(raw)
    model = train(processed)
    return model

# Run locally
ml_pipeline()
```

Kubeflow Pipelines. Built specifically for ML on Kubernetes. Deeply integrated with the Kubernetes ecosystem.

Pros:
- Native Kubernetes integration
- ML-specific features (experiments, runs, metrics)
- Component reusability
- Supports GPU workloads natively
- Integration with other Kubeflow components

Cons:
- Requires Kubernetes
- Steeper learning curve
- Complex setup
- Overkill for simple pipelines

Best for: Teams already on Kubernetes, large-scale ML training, GPU-intensive workloads.

```python
# Kubeflow Pipelines example
from kfp import dsl

@dsl.component
def train_model(data_path: str) -> str:
    # Training logic
    return "model.pkl"

@dsl.pipeline(name="ml-training")
def ml_pipeline(data_path: str):
    train_task = train_model(data_path=data_path)

# Compile and run
from kfp import compiler
compiler.Compiler().compile(ml_pipeline, 'pipeline.yaml')
```

Dagster. Another modern alternative, with a focus on data assets and software-defined assets.

Pros:
- Asset-centric view (think "what" not "how")
- Great local development
- Strong typing and testing
- Beautiful UI
- Good for both data engineering and ML

Cons:
- Different paradigm, takes adjustment
- Smaller community
- Less enterprise adoption so far

Best for: Teams that think in terms of data assets, modern data platforms, teams valuing strong software engineering practices.

```python
# Dagster example
from dagster import asset, Definitions

@asset
def raw_data():
    return load_raw_data()

@asset
def processed_data(raw_data):
    return clean(raw_data)

@asset
def trained_model(processed_data):
    return train(processed_data)

defs = Definitions(assets=[raw_data, processed_data, trained_model])
```

Argo Workflows. Kubernetes-native workflow engine. More general-purpose than Kubeflow.

Pros:
- Kubernetes native
- Very flexible
- Good for mixed workloads (not just ML)
- YAML-based definitions

Cons:
- Requires Kubernetes
- Less ML-specific features
- YAML can get verbose

Best for: Kubernetes environments, teams needing general-purpose workflows beyond just ML.

Tekton. CI/CD-focused but can be used for ML pipelines. Also Kubernetes-native.

Pros:
- Strong CI/CD integration
- Kubernetes native
- Reusable tasks
- Good for MLOps CI/CD

Cons:
- More focused on CI/CD than data/ML
- Less ML-specific features

Best for: Teams wanting to unify CI/CD and ML pipelines on Kubernetes.

Now let me help you choose.

For beginners or small teams:
- Start with Prefect. It's the easiest to learn and you can run locally.
- Or use simple scripts with a scheduler like cron for very basic needs.

For enterprise data platforms:
- Airflow is the safe choice. It's proven and widely understood.
- Dagster if you're starting fresh and want modern practices.

For Kubernetes-native environments:
- Kubeflow Pipelines if ML is your focus.
- Argo Workflows for general-purpose needs.
- Tekton if CI/CD integration is critical.

For rapid iteration and experimentation:
- Prefect or Dagster. Both have great local development experiences.

For existing infrastructure:
- If you already have Airflow, use it. Don't add another tool.
- If you're on Kubernetes, lean toward Kubeflow or Argo.

Here's a comparison table:

| Feature          | Airflow | Prefect | Kubeflow | Dagster |
|------------------|---------|---------|----------|---------|
| Learning Curve   | Medium  | Low     | High     | Medium  |
| Local Dev        | Poor    | Great   | Poor     | Great   |
| Scheduling       | Great   | Good    | Good     | Good    |
| Kubernetes       | Plugin  | Native  | Native   | Plugin  |
| ML-specific      | Low     | Medium  | High     | Medium  |
| Enterprise Ready | High    | Medium  | Medium   | Medium  |
| Community Size   | Huge    | Growing | Large    | Growing |

My personal recommendation? Start with Prefect if you're learning. It's the most beginner-friendly and you can always migrate later. If your company already uses Airflow, learn Airflow. The concepts transfer between tools.

In the next lecture, we'll design an actual training pipeline for our project.

Questions? Let's move on.

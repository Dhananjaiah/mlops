# Lecture 9.2 – Pipeline Building Blocks (Tasks / Steps / DAGs)

## Human Transcript

Alright, now that you understand why we need pipelines, let's look at the building blocks. Every pipeline framework has similar concepts, just with different names. Once you understand these concepts, you can work with any tool.

The three core concepts are: Tasks, Dependencies, and DAGs.

Tasks. A task is a single unit of work. It's like a function that does one thing. Examples:
- Download data from a database
- Clean and preprocess data
- Train a model
- Evaluate model performance
- Send a notification

Each task should be:
- Self-contained: it has clear inputs and outputs
- Atomic: it either completes fully or fails
- Idempotent: running it multiple times with the same inputs gives the same result

Let me show you what a task looks like:

```python
# A simple task
def download_data(date: str, output_path: str) -> str:
    """Download data for a specific date."""
    query = f"SELECT * FROM customers WHERE date = '{date}'"
    df = execute_query(query)
    df.to_parquet(output_path)
    return output_path

# In Airflow, you'd wrap it
from airflow.decorators import task

@task
def download_data(date: str, output_path: str) -> str:
    query = f"SELECT * FROM customers WHERE date = '{date}'"
    df = execute_query(query)
    df.to_parquet(output_path)
    return output_path
```

Dependencies. Tasks don't run in isolation. They have dependencies. Task B needs the output of Task A. Task C needs outputs from both A and B.

```python
# Task B depends on Task A
@task
def clean_data(raw_data_path: str) -> str:
    """Clean the raw data."""
    df = pd.read_parquet(raw_data_path)  # Uses output from download_data
    df_clean = clean(df)
    output_path = "data/clean.parquet"
    df_clean.to_parquet(output_path)
    return output_path

# Usage: The dependency is implicit in the function call
raw_path = download_data("2023-10-15", "data/raw.parquet")
clean_path = clean_data(raw_path)  # Depends on raw_path
```

Or you can make it explicit:

```python
# Explicit dependency definition
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG("my_pipeline"):
    task_a = PythonOperator(task_id="download", python_callable=download_data)
    task_b = PythonOperator(task_id="clean", python_callable=clean_data)
    task_c = PythonOperator(task_id="train", python_callable=train_model)
    
    task_a >> task_b >> task_c  # A -> B -> C
```

DAGs. A DAG is a Directed Acyclic Graph. Fancy term, simple concept.

Directed: dependencies have a direction. A comes before B.
Acyclic: no circular dependencies. A can't depend on B if B depends on A.
Graph: tasks are nodes, dependencies are edges.

Here's a visual:

```
     ┌─────────────┐
     │ download_   │
     │    data     │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │   clean_    │
     │    data     │
     └──────┬──────┘
            │
     ┌──────┴──────┐
     │             │
┌────▼────┐ ┌──────▼─────┐
│ train_  │ │  compute_  │
│ model   │ │  features  │
└────┬────┘ └──────┬─────┘
     │             │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  evaluate   │
     │   model     │
     └─────────────┘
```

In this DAG:
- `download_data` has no dependencies (starting point)
- `clean_data` depends on `download_data`
- `train_model` and `compute_features` both depend on `clean_data` (they can run in parallel!)
- `evaluate` depends on both `train_model` and `compute_features`

Here's how you define this:

```python
# Airflow style
download >> clean >> [train, features] >> evaluate

# Prefect style
with Flow("my_flow") as flow:
    data = download_data()
    clean = clean_data(data)
    model = train_model(clean)
    feats = compute_features(clean)
    result = evaluate(model, feats)
```

Let me explain each part in more detail.

Inputs and outputs. Each task can have inputs and outputs. Outputs of one task become inputs of the next.

```python
@task
def prepare_data() -> dict:
    """Returns metadata about prepared data."""
    df = load_and_prepare()
    return {
        "path": "data/prepared.parquet",
        "row_count": len(df),
        "columns": list(df.columns)
    }

@task
def train_model(data_info: dict) -> str:
    """Uses the data info from previous task."""
    df = pd.read_parquet(data_info["path"])
    print(f"Training on {data_info['row_count']} rows")
    model = fit_model(df)
    return "models/model.pkl"
```

Parameters. Pipelines often need parameters that change between runs:

```python
# Define pipeline with parameters
@dag(
    params={
        "training_date": Param(default="2023-10-15", type="string"),
        "model_type": Param(default="xgboost", type="string"),
        "test_size": Param(default=0.2, type="number")
    }
)
def training_pipeline():
    # Access parameters
    @task
    def prepare_data(**context):
        date = context["params"]["training_date"]
        return load_data_for_date(date)
    
    @task
    def train(data_path, **context):
        model_type = context["params"]["model_type"]
        test_size = context["params"]["test_size"]
        return train_model(data_path, model_type, test_size)
```

Branching. Sometimes you need different paths based on conditions:

```python
@task.branch
def check_data_quality(metrics: dict) -> str:
    """Decide which path to take based on data quality."""
    if metrics["missing_rate"] > 0.1:
        return "handle_missing_data"  # Go to this task
    else:
        return "proceed_to_training"  # Go to this task

# In the DAG
check = check_data_quality(quality_metrics)
handle_missing = handle_missing_data()
proceed = proceed_to_training()

check >> [handle_missing, proceed]  # Branch based on check result
```

Joining. After parallel tasks, you often need to join results:

```python
@task
def combine_results(model_metrics: dict, feature_importance: dict) -> dict:
    """Combine results from parallel tasks."""
    return {
        **model_metrics,
        "feature_importance": feature_importance
    }

# Parallel tasks converge
evaluate = evaluate_model(model)
importance = compute_importance(model)
combined = combine_results(evaluate, importance)
```

Task groups. For complex pipelines, you can group related tasks:

```python
from airflow.utils.task_group import TaskGroup

with DAG("complex_pipeline"):
    with TaskGroup("data_preparation") as prep_group:
        download = download_data()
        clean = clean_data(download)
        validate = validate_data(clean)
    
    with TaskGroup("model_training") as train_group:
        train = train_model()
        tune = tune_hyperparameters()
        select_best = select_best_model()
    
    with TaskGroup("deployment") as deploy_group:
        test = run_tests()
        deploy = deploy_model()
    
    prep_group >> train_group >> deploy_group
```

These building blocks are universal. Whether you use Airflow, Prefect, Kubeflow Pipelines, or something else, you'll work with tasks, dependencies, and DAGs.

In the next lecture, we'll look at specific orchestration tools and when to use each.

Questions? Let's keep going.

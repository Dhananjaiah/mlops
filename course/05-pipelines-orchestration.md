# Module 05: Pipelines & Orchestration

## 🎯 Goals

- Build **DAGs (Directed Acyclic Graphs)** for ML workflows
- Orchestrate with **Apache Airflow** (local executor → Kubernetes)
- Use **Kubeflow Pipelines** for cloud-native workflows
- Implement **caching** and **retries** for reliability
- Schedule **training** and **batch inference** jobs
- Monitor **pipeline execution** and debug failures

---

## 📖 Key Terms

- **DAG (Directed Acyclic Graph)**: Workflow definition with tasks and dependencies
- **Operator**: Task type in Airflow (PythonOperator, BashOperator, KubernetesPodOperator)
- **Executor**: Backend running tasks (LocalExecutor, CeleryExecutor, KubernetesExecutor)
- **XCom**: Cross-communication mechanism for passing data between tasks in Airflow
- **Kubeflow Pipelines (KFP)**: Cloud-native ML orchestration on Kubernetes
- **Component**: Reusable pipeline step in KFP (containerized task)
- **Idempotency**: Running a task multiple times produces same result (critical for retries)

---

## 🎓 Lessons with Transcript

### What We're Doing in This Module

**Welcome to Pipelines & Orchestration!** This is where we automate ML workflows. Instead of manually running scripts in order, we define pipelines that handle dependencies, retries, and scheduling automatically.

### Lesson 1: Why Manual Workflows Don't Scale

**Transcript:**
"When you start in ML, you run scripts manually: 'First I run download_data.py, then preprocess.py, then train.py.' This works for learning, but it's a nightmare in production. What if download fails? You have to remember where you left off. What if you want to run this every day? You set up cron jobs that don't handle failures. What if preprocessing succeeds but training fails? You have to manually check each step. Orchestration tools like Airflow solve this by defining workflows as DAGs - directed acyclic graphs. You declare 'training depends on preprocessing, which depends on download.' Airflow handles execution order, retries, monitoring, and scheduling. You focus on the logic, not the plumbing."

**What you're learning:** Why automated orchestration is essential for production ML workflows.

### Lesson 2: DAGs - Declaring Dependencies as Code

**Transcript:**
"A DAG is a graph where tasks point to their dependencies. 'Download data' has no dependencies, so it runs first. 'Preprocess' depends on download, so it waits. 'Train' and 'Validate' both depend on preprocess, so they run in parallel after preprocessing completes. This is declarative programming - you say what depends on what, and Airflow figures out the execution order. If a task fails, only its downstream dependencies are blocked; unrelated tasks continue. If you need to rerun just training, Airflow knows preprocessing is already done. This makes complex workflows manageable."

**What you're learning:** How DAG-based orchestration handles complex dependencies and partial reruns.

### Lesson 3: Operators - Task Types in Airflow

**Transcript:**
"Airflow has different operators for different task types. PythonOperator runs Python functions - good for lightweight tasks like data validation. BashOperator runs shell commands - useful for invoking CLIs like DVC or MLflow. KubernetesPodOperator spins up containers - perfect for heavy training jobs that need GPUs. You choose the operator based on your task requirements. A data download might use BashOperator to run `dvc pull`. Training might use KubernetesPodOperator to launch a containerized job with GPU access. This flexibility lets you mix and match execution environments within one pipeline."

**What you're learning:** How different Airflow operators suit different task types and resource requirements.

### Lesson 4: Idempotency - Safe Retries

**Transcript:**
"Idempotency means running a task multiple times produces the same result. This is crucial for orchestration because tasks fail - networks hiccup, APIs time out, resources get exhausted. If your download task fails halfway through, can you safely rerun it? If it overwrites partial files correctly, yes - it's idempotent. If it appends to existing files, no - rerunning creates duplicate data. Airflow assumes tasks are idempotent so it can safely retry them. Design your tasks to either succeed completely or fail completely, with no partial states. Use atomic operations, write to temporary locations then move, and check for completion markers."

**What you're learning:** Why idempotency is critical for reliable, retryable pipelines.

### Lesson 5: Kubeflow Pipelines - Cloud-Native Alternative

**Transcript:**
"While Airflow is general-purpose, Kubeflow Pipelines is built specifically for ML on Kubernetes. Every task runs in its own container, giving you complete isolation and reproducibility. KFP has built-in support for ML-specific features like hyperparameter tuning and model serving. The trade-off is that it requires Kubernetes, while Airflow can run anywhere. For cloud-native ML stacks, KFP integrates beautifully with Kubernetes autoscaling and GPU scheduling. For hybrid or on-prem setups, Airflow offers more flexibility. Choose based on your infrastructure and team expertise."

**What you're learning:** When to use Airflow vs Kubeflow Pipelines based on your infrastructure.

### Key Definition - What We're Doing Overall

**In this module, we're automating ML workflows with orchestration.** We're defining pipelines as DAGs that declare task dependencies. We're using operators to match tasks to appropriate execution environments. We're designing idempotent tasks that can be safely retried. And we're choosing orchestration tools - Airflow for flexibility, Kubeflow for Kubernetes-native ML.

**By the end of this lesson, you should understand:** How to write Airflow DAGs with task dependencies, how to choose appropriate operators for different tasks, how to make tasks idempotent for safe retries, and when to use Airflow vs Kubeflow Pipelines. Orchestration transforms manual scripts into automated, monitored, resilient workflows that run reliably in production.

---

## 🔧 Commands First: Install Airflow Locally

```bash
# Install Airflow with constraints (avoid dependency conflicts)
export AIRFLOW_VERSION=2.8.0
export PYTHON_VERSION=3.11
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Initialize database (SQLite by default)
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@mlops.dev \
  --password admin

# Start webserver and scheduler
airflow webserver --port 8080 &
airflow scheduler &

# Open UI at http://localhost:8080 (admin/admin)
```

**Why**: Airflow orchestrates complex workflows with dependencies, retries, and scheduling. Webserver provides UI, scheduler triggers tasks.

---

## 📋 Create First DAG (Training Pipeline)

```bash
# Create DAG directory
mkdir -p ~/airflow/dags

# Create training DAG
cat > ~/airflow/dags/train_model.py << 'EOF'
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import mlflow
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

def load_data(**context):
    """Load and split data"""
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Push to XCom for next tasks
    context['ti'].xcom_push(key='X_train', value=X_train.tolist())
    context['ti'].xcom_push(key='X_test', value=X_test.tolist())
    context['ti'].xcom_push(key='y_train', value=y_train.tolist())
    context['ti'].xcom_push(key='y_test', value=y_test.tolist())
    print(f"Loaded {len(X_train)} training samples")

def train_model(**context):
    """Train model and log to MLflow"""
    import numpy as np
    
    # Pull from XCom
    X_train = np.array(context['ti'].xcom_pull(key='X_train'))
    y_train = np.array(context['ti'].xcom_pull(key='y_train'))
    
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("airflow-iris")
    
    with mlflow.start_run():
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        
        mlflow.log_param("n_estimators", 100)
        mlflow.sklearn.log_model(clf, "model")
        
        # Store run_id for evaluation
        run_id = mlflow.active_run().info.run_id
        context['ti'].xcom_push(key='run_id', value=run_id)
        print(f"Model trained, run_id: {run_id}")

def evaluate_model(**context):
    """Evaluate model"""
    import numpy as np
    
    X_test = np.array(context['ti'].xcom_pull(key='X_test'))
    y_test = np.array(context['ti'].xcom_pull(key='y_test'))
    run_id = context['ti'].xcom_pull(key='run_id')
    
    mlflow.set_tracking_uri("http://localhost:5000")
    
    # Load model from MLflow
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)
    
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    # Log metric
    with mlflow.start_run(run_id=run_id):
        mlflow.log_metric("test_accuracy", accuracy)
    
    print(f"Test accuracy: {accuracy:.3f}")

# Define DAG
with DAG(
    'train_iris_model',
    default_args=default_args,
    description='Train Iris classifier with MLflow',
    schedule_interval='@daily',  # Run daily
    catchup=False,
) as dag:
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
    )
    
    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True,
    )
    
    evaluate_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
        provide_context=True,
    )
    
    # Define dependencies
    load_task >> train_task >> evaluate_task
EOF

# Trigger DAG manually
airflow dags trigger train_iris_model

# Monitor in UI or CLI
airflow dags list
airflow tasks list train_iris_model
```

**Why**: DAG defines workflow as code. Airflow handles scheduling, retries, logging. XCom passes data between tasks.

---

## ✅ Verify Airflow DAG

```bash
# Check DAG is loaded
airflow dags list | grep train_iris_model

# Test individual task
airflow tasks test train_iris_model load_data 2024-01-01

# Check run status
airflow dags list-runs -d train_iris_model

# View logs
airflow tasks logs train_iris_model train_model <execution_date>
```

---

## 🚀 Advanced: Kubernetes Executor

```bash
# Install Kubernetes provider
pip install apache-airflow-providers-cncf-kubernetes

# Configure airflow.cfg for K8s executor
cat >> ~/airflow/airflow.cfg << 'EOF'
[core]
executor = KubernetesExecutor

[kubernetes]
namespace = airflow
in_cluster = False
kube_config_path = ~/.kube/config
worker_container_repository = apache/airflow
worker_container_tag = 2.8.0-python3.11
EOF

# Create DAG with KubernetesPodOperator
cat > ~/airflow/dags/train_k8s.py << 'EOF'
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    'train_on_k8s',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    
    train_task = KubernetesPodOperator(
        task_id='train_model_k8s',
        name='train-model-pod',
        namespace='mlops',
        image='ghcr.io/mlops-course/mlops-train:latest',
        cmds=['python', 'src/train.py'],
        get_logs=True,
    )
EOF
```

**Why**: KubernetesPodOperator runs each task in isolated K8s pod. Scales horizontally, better resource isolation.

---

## ☁️ Kubeflow Pipelines (Alternative to Airflow)

```bash
# Install KFP SDK
pip install kfp

# Create pipeline
cat > kfp_train_pipeline.py << 'EOF'
import kfp
from kfp import dsl

@dsl.component(base_image='python:3.11')
def load_data_component(dataset_path: str) -> dict:
    """Load data and return paths"""
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    import pickle
    
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save to files
    with open('/tmp/X_train.pkl', 'wb') as f:
        pickle.dump(X_train, f)
    with open('/tmp/y_train.pkl', 'wb') as f:
        pickle.dump(y_train, f)
    
    return {'X_train': '/tmp/X_train.pkl', 'y_train': '/tmp/y_train.pkl'}

@dsl.component(base_image='python:3.11', packages_to_install=['scikit-learn', 'mlflow'])
def train_component(data_paths: dict) -> str:
    """Train model"""
    import pickle
    import mlflow
    from sklearn.ensemble import RandomForestClassifier
    
    with open(data_paths['X_train'], 'rb') as f:
        X_train = pickle.load(f)
    with open(data_paths['y_train'], 'rb') as f:
        y_train = pickle.load(f)
    
    mlflow.set_tracking_uri("http://mlflow.mlops.svc.cluster.local:5000")
    mlflow.set_experiment("kfp-iris")
    
    with mlflow.start_run():
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        mlflow.sklearn.log_model(clf, "model")
        return mlflow.active_run().info.run_id

@dsl.pipeline(name='Iris Training Pipeline')
def train_pipeline():
    """Full training pipeline"""
    load_task = load_data_component(dataset_path='iris')
    train_task = train_component(data_paths=load_task.output)

# Compile pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(train_pipeline, 'iris_pipeline.yaml')
    print("Pipeline compiled to iris_pipeline.yaml")
EOF

# Compile
python kfp_train_pipeline.py

# Upload to KFP (if cluster available)
# kfp_client = kfp.Client(host='http://localhost:8080')
# kfp_client.create_run_from_pipeline_package('iris_pipeline.yaml')
```

**Why**: KFP is cloud-native (K8s only), better for large-scale. Components are containerized. Better artifact passing via volumes.

---

## 🔄 Caching and Retries

```bash
# Airflow DAG with caching
cat > ~/airflow/dags/cached_pipeline.py << 'EOF'
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import hashlib

def expensive_preprocessing(**context):
    """Simulate expensive preprocessing"""
    import time
    # Check cache
    cache_key = hashlib.md5(b"data_v1").hexdigest()
    cache_path = f"/tmp/cache_{cache_key}.pkl"
    
    import os
    if os.path.exists(cache_path):
        print("Using cached result")
        with open(cache_path, 'rb') as f:
            import pickle
            result = pickle.load(f)
    else:
        print("Running preprocessing...")
        time.sleep(5)  # Simulate work
        result = {"features": [1, 2, 3, 4]}
        
        # Cache result
        with open(cache_path, 'wb') as f:
            import pickle
            pickle.dump(result, f)
    
    context['ti'].xcom_push(key='preprocessed', value=result)

with DAG(
    'cached_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    
    preprocess = PythonOperator(
        task_id='preprocess',
        python_callable=expensive_preprocessing,
        provide_context=True,
        retries=3,  # Retry 3 times on failure
    )
EOF
```

**Why**: Caching avoids re-running expensive tasks. Retries handle transient failures (network, OOM).

---

## 🧪 Mini-Lab (10 min)

**Goal**: Create a simple Airflow DAG for data → train → evaluate.

1. **Start Airflow**:
```bash
cd ~/mlops-lab-05
airflow db init
airflow users create --username admin --password admin --firstname A --lastname B --role Admin --email a@b.c
airflow webserver --port 8080 &
airflow scheduler &
```

2. **Create DAG**:
```bash
mkdir -p ~/airflow/dags
cat > ~/airflow/dags/simple_pipeline.py << 'EOF'
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'simple_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    
    task1 = BashOperator(task_id='print_date', bash_command='date')
    task2 = BashOperator(task_id='print_hello', bash_command='echo "Hello MLOps"')
    
    task1 >> task2  # task1 runs before task2
EOF
```

3. **Trigger and monitor**:
```bash
airflow dags trigger simple_pipeline
sleep 5
airflow dags list-runs -d simple_pipeline
# Open http://localhost:8080 to view graph
```

**Expected output**: DAG runs, tasks succeed, logs show date and "Hello MLOps".

---

## ❓ Quiz (5 Questions)

1. **What is a DAG in Airflow?**
   - Answer: Directed Acyclic Graph—a workflow with tasks and dependencies, no cycles.

2. **What is XCom used for?**
   - Answer: Passing small data (metadata, paths, IDs) between Airflow tasks.

3. **Why use KubernetesPodOperator over PythonOperator?**
   - Answer: Isolation (each task in separate pod), better scaling, resource limits per task.

4. **What is idempotency and why does it matter?**
   - Answer: Running a task multiple times produces same result. Critical for safe retries.

5. **When to use Kubeflow Pipelines vs Airflow?**
   - Answer: KFP for K8s-only, ML-focused, artifact passing. Airflow for general workflows, multi-cloud, legacy systems.

---

## ⚠️ Common Mistakes

1. **Passing large data via XCom** → Database bloat, slow tasks.  
   *Fix*: Store data in S3/GCS, pass only paths via XCom.

2. **Not setting retries** → One transient failure kills entire pipeline.  
   *Fix*: Set `retries=2` and `retry_delay` in default_args.

3. **Non-idempotent tasks** → Retries create duplicates or corrupt data.  
   *Fix*: Use unique IDs, check-before-insert, or upsert patterns.

4. **Too many dependencies in one DAG** → Hard to debug, long run times.  
   *Fix*: Split into multiple DAGs, use ExternalTaskSensor for inter-DAG deps.

5. **Ignoring task failure alerts** → Silent production breakage.  
   *Fix*: Configure email/Slack alerts on failure.

---

## 🛠️ Troubleshooting

**Issue**: "Airflow webserver won't start"  
→ **Root cause**: Port 8080 in use or database not initialized.  
→ **Fix**: `lsof -i :8080` to find process, kill it, or use different port. Run `airflow db init`.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Airflow webserver fails"

**Issue**: "DAG not showing in UI"  
→ **Root cause**: Python syntax error or not in dags/ folder.  
→ **Fix**: Check `airflow dags list` for errors, verify path in airflow.cfg `dags_folder`.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Airflow DAG not loaded"

---

## 📚 Key Takeaways

- **Airflow** orchestrates workflows with scheduling, retries, monitoring
- **DAGs** define tasks and dependencies as Python code
- **XCom** passes metadata between tasks (not large data)
- **KubernetesPodOperator** runs tasks in isolated pods (better scaling)
- **Kubeflow Pipelines** is K8s-native alternative (better for cloud ML)
- Always design **idempotent** tasks for safe retries

---

## 🚀 Next Steps

- **Module 06**: Systematic model training, evaluation, and selection
- **Module 07**: Model registry and governance with MLflow Registry
- **Hands-on**: Build Churn Predictor training pipeline in Airflow

---

**[← Module 04](04-experiment-tracking-and-reproducibility.md)** | **[Next: Module 06 →](06-model-training-eval-and-selection.md)**

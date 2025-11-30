# Lecture 9.6 – Scheduling, Retries & Failure Handling

## Human Transcript

Alright, we have a working pipeline. But in the real world, things go wrong. Networks fail. Databases time out. Data sources go down. A good pipeline handles these gracefully.

Let's talk about three critical aspects: scheduling, retries, and failure handling.

Scheduling. When should your pipeline run?

The most common pattern is cron scheduling. Cron expressions let you specify exactly when:

```python
# Cron format: minute hour day-of-month month day-of-week

"0 6 * * *"     # Daily at 6:00 AM
"0 */4 * * *"   # Every 4 hours
"30 8 * * 1"    # Every Monday at 8:30 AM
"0 2 1 * *"     # First day of each month at 2 AM
"0 6 * * 1-5"   # Weekdays at 6 AM
```

In Prefect:

```python
from prefect.server.schemas.schedules import CronSchedule, IntervalSchedule

# Cron schedule
cron_schedule = CronSchedule(
    cron="0 6 * * *",
    timezone="America/New_York"
)

# Interval schedule (every 6 hours)
interval_schedule = IntervalSchedule(interval=timedelta(hours=6))
```

In Airflow:

```python
from airflow import DAG

with DAG(
    "my_pipeline",
    schedule_interval="0 6 * * *",  # Cron expression
    # Or use preset
    # schedule_interval="@daily",    # Same as "0 0 * * *"
    # schedule_interval="@hourly",   # Same as "0 * * * *"
    # schedule_interval="@weekly",   # Same as "0 0 * * 0"
    start_date=datetime(2023, 1, 1),
    catchup=False  # Don't run for past dates
) as dag:
    pass
```

Event-driven scheduling. Sometimes you want to run when something happens:

```python
# Prefect - trigger on file arrival
from prefect import flow
from prefect.events import DeploymentEventTrigger

# This would be configured in deployment
trigger = DeploymentEventTrigger(
    expect=["s3://bucket/data/new_file_arrived"]
)
```

Hybrid approach. Run on schedule, but also allow manual triggers:

```python
# The pipeline can be run manually
training_pipeline()  # Direct call

# Or scheduled
deployment = Deployment.build_from_flow(
    flow=training_pipeline,
    schedule=CronSchedule(cron="0 6 * * *")
)
```

Retries. Things fail. The question is: what do you do about it?

Transient failures. Network timeouts, temporary unavailability. These often succeed if you just try again.

```python
from prefect import task

@task(
    retries=3,                    # Retry up to 3 times
    retry_delay_seconds=60,       # Wait 60 seconds between retries
)
def fetch_data_from_api():
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()
```

Exponential backoff. For rate-limited APIs or overloaded systems, waiting longer each time helps:

```python
from prefect import task
from prefect.tasks import exponential_backoff

@task(
    retries=5,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    # Delays: 10s, 20s, 40s, 80s, 160s
)
def call_rate_limited_api():
    return api_call()
```

In Airflow:

```python
from airflow.decorators import task
from datetime import timedelta

@task(
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    max_retry_delay=timedelta(minutes=30)
)
def flaky_task():
    pass
```

When NOT to retry. Not all failures should be retried:

```python
@task(retries=3)
def process_data(data_path):
    # Don't retry validation errors - they won't fix themselves
    if not validate_data(data_path):
        raise ValueError("Invalid data - manual intervention needed")
    
    # Do retry network errors
    try:
        result = upload_to_s3(data_path)
    except ConnectionError:
        raise  # Will be retried
    
    return result
```

Custom retry logic:

```python
from prefect import task

def should_retry(task, task_run, state):
    """Custom function to decide whether to retry."""
    exception = state.result()
    
    # Retry network errors
    if isinstance(exception, (ConnectionError, TimeoutError)):
        return True
    
    # Don't retry data errors
    if isinstance(exception, ValueError):
        return False
    
    # Default: retry
    return True

@task(
    retries=3,
    retry_condition_fn=should_retry
)
def smart_task():
    pass
```

Failure Handling. What happens when a task fails permanently?

Immediate notification:

```python
from prefect import task, flow
from prefect.states import Failed

def on_failure(task, task_run, state):
    """Called when a task fails."""
    send_alert(
        channel="#ml-alerts",
        message=f"Task {task.name} failed: {state.message}"
    )

@task(on_failure=[on_failure])
def critical_task():
    pass
```

Pipeline-level failure handling:

```python
@flow(on_failure=[notify_on_pipeline_failure])
def training_pipeline():
    try:
        data = extract_data()
        model = train_model(data)
    except Exception as e:
        # Log the error
        logger.error(f"Pipeline failed: {e}")
        
        # Save partial state for debugging
        save_debug_state(locals())
        
        # Re-raise to mark pipeline as failed
        raise

def notify_on_pipeline_failure(flow, flow_run, state):
    """Send detailed failure notification."""
    send_email(
        to="ml-team@company.com",
        subject=f"Pipeline Failed: {flow.name}",
        body=f"""
        Pipeline: {flow.name}
        Run ID: {flow_run.id}
        Error: {state.message}
        
        Logs: https://prefect.company.com/runs/{flow_run.id}
        """
    )
```

Graceful degradation. Sometimes you can continue with partial results:

```python
@flow
def training_pipeline():
    # Try to get new data
    try:
        new_data = extract_new_data()
    except DataSourceError:
        logger.warning("New data unavailable, using cached data")
        new_data = load_cached_data()
    
    # Continue with whatever data we have
    model = train_model(new_data)
    return model
```

Cleanup on failure:

```python
@task
def train_with_cleanup(data_path):
    temp_files = []
    
    try:
        # Create temporary files
        temp_file = create_temp_file()
        temp_files.append(temp_file)
        
        # Do training
        model = do_training(data_path, temp_file)
        
        return model
    
    finally:
        # Always cleanup, even on failure
        for f in temp_files:
            try:
                os.remove(f)
            except OSError:
                pass
```

Dead letter queues. For batch processing, save failed items for later:

```python
@task
def process_batch(items):
    results = []
    failed_items = []
    
    for item in items:
        try:
            result = process_item(item)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {item}: {e}")
            failed_items.append({
                "item": item,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    # Save failed items for manual review
    if failed_items:
        save_to_dead_letter_queue(failed_items)
        logger.warning(f"{len(failed_items)} items failed, saved to DLQ")
    
    return results
```

Timeouts. Tasks shouldn't run forever:

```python
from prefect import task

@task(timeout_seconds=3600)  # 1 hour timeout
def long_running_training():
    """Will be killed if it takes more than 1 hour."""
    model = train_large_model()
    return model
```

In Airflow:

```python
from airflow.decorators import task

@task(execution_timeout=timedelta(hours=1))
def long_running_task():
    pass
```

Here's a complete example putting it all together:

```python
from prefect import flow, task
from prefect.tasks import exponential_backoff

@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=10),
    timeout_seconds=300,
    on_failure=[send_slack_alert]
)
def extract_data():
    """Robust data extraction."""
    return fetch_from_database()

@task(
    retries=1,  # Only retry once - if data is bad, it's bad
    timeout_seconds=3600,
    on_failure=[save_debug_info, send_slack_alert]
)
def train_model(data):
    """Training with failure handling."""
    return do_training(data)

@flow(
    on_failure=[send_pipeline_failure_email],
    timeout_seconds=7200  # 2 hour total timeout
)
def robust_training_pipeline():
    data = extract_data()
    model = train_model(data)
    return model
```

The key principles:
- Retry transient failures, don't retry permanent ones
- Always have timeouts
- Always notify on failures
- Clean up after yourself
- Save state for debugging

In the next lecture, we'll discuss where MLOps fits versus data engineering in the orchestration world.

Questions?

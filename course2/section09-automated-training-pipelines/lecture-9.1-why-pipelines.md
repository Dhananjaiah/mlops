# Lecture 9.1 – Why We Need Pipelines (Not Manual "Run This Script")

## Human Transcript

Welcome to Section 9. We're going to talk about automated training pipelines and orchestration. This is where your ML system starts to become a real system instead of a collection of scripts.

Let me start with a scenario I've seen too many times. A data scientist has a notebook that trains a model. When it's time to retrain, they manually:
1. Download the latest data
2. Run some cleaning scripts
3. Open the notebook
4. Click "Run All"
5. Wait an hour
6. Check if it worked
7. Manually copy the model file to somewhere
8. Update some documentation

What's wrong with this picture? Everything.

First, it requires a human. Someone has to remember to do it. Someone has to be available. Someone has to not make mistakes. And humans are bad at all three.

Second, it's not reproducible. Did you run the scripts in the right order? Did you use the right parameters? Was your environment correct? Who knows.

Third, it doesn't scale. What if you need to train 10 models? 100? What if you need to retrain every day?

Fourth, it's error-prone. Manual steps mean manual errors. Forgot to download the latest data? Ran the wrong cleaning script? Wrong model version uploaded?

Fifth, there's no audit trail. What happened? When? Who did it? If something goes wrong, good luck figuring out why.

This is why we need pipelines. A pipeline is a sequence of steps that run automatically, in order, with proper error handling and logging.

Let me show you the difference. Here's the manual approach:

```
# Manual workflow (in a doc somewhere)
1. SSH to server
2. cd /home/data/projects/churn
3. python download_data.py
4. python clean_data.py
5. python train_model.py
6. python evaluate_model.py
7. If metrics look good, run: python deploy_model.py
8. Send Slack message to team
```

And here's what a pipeline looks like:

```python
# training_pipeline.py (pseudocode)
from pipeline_framework import Pipeline, Step

pipeline = Pipeline("churn-model-training")

@pipeline.step
def download_data():
    # Downloads latest data from source
    return data_path

@pipeline.step(depends_on=["download_data"])
def clean_data(data_path):
    # Cleans and validates data
    return cleaned_data_path

@pipeline.step(depends_on=["clean_data"])
def train_model(cleaned_data_path):
    # Trains the model
    return model_path

@pipeline.step(depends_on=["train_model"])
def evaluate_model(model_path):
    # Evaluates model performance
    return metrics

@pipeline.step(depends_on=["evaluate_model"])
def check_quality_gate(metrics):
    # Automatic decision: is the model good enough?
    if metrics['f1'] < 0.80:
        raise QualityGateError("Model doesn't meet quality threshold")
    return True

@pipeline.step(depends_on=["check_quality_gate"])
def register_model(model_path):
    # Register in model registry
    return model_version

@pipeline.step(depends_on=["register_model"])
def notify_team(model_version):
    # Send Slack notification
    send_slack(f"New model v{model_version} registered")

# Run the pipeline
pipeline.run()
```

See the difference? Every step is explicit. Dependencies are clear. The pipeline runs automatically. If any step fails, you know exactly where and why.

What does a pipeline give you?

Automation. The pipeline runs without human intervention. Schedule it to run daily, weekly, or triggered by events.

Reproducibility. The same pipeline with the same inputs produces the same outputs. Every time.

Reliability. If a step fails, the pipeline stops and alerts you. No silent failures.

Logging. Every step logs what it did, how long it took, what inputs it used.

Retry logic. If a step fails due to a transient error, retry automatically.

Parallelization. Independent steps can run in parallel, speeding things up.

Version control. The pipeline itself is code. You can version it, review changes, roll back.

Let me show you what pipeline execution looks like:

```
[2023-10-15 08:00:00] Pipeline started: churn-model-training
[2023-10-15 08:00:01] Step: download_data - STARTED
[2023-10-15 08:05:23] Step: download_data - COMPLETED (5m 22s)
[2023-10-15 08:05:24] Step: clean_data - STARTED
[2023-10-15 08:12:45] Step: clean_data - COMPLETED (7m 21s)
[2023-10-15 08:12:46] Step: train_model - STARTED
[2023-10-15 08:52:12] Step: train_model - COMPLETED (39m 26s)
[2023-10-15 08:52:13] Step: evaluate_model - STARTED
[2023-10-15 08:53:45] Step: evaluate_model - COMPLETED (1m 32s)
[2023-10-15 08:53:46] Step: check_quality_gate - STARTED
[2023-10-15 08:53:46] Step: check_quality_gate - COMPLETED (0s)
[2023-10-15 08:53:47] Step: register_model - STARTED
[2023-10-15 08:53:52] Step: register_model - COMPLETED (5s)
[2023-10-15 08:53:53] Step: notify_team - STARTED
[2023-10-15 08:53:54] Step: notify_team - COMPLETED (1s)
[2023-10-15 08:53:54] Pipeline completed: churn-model-training (53m 54s)
```

You can see exactly what happened. If something failed, you'd see which step and why.

Now, when do you need a pipeline?

You definitely need one if:
- You're training models more than occasionally
- Multiple people are involved in the process
- The process has more than 2-3 steps
- You need to audit what happened
- You're going to production

You might get away without one if:
- You're just experimenting
- It's a one-time analysis
- You're the only person who will ever touch this

But honestly, even for experiments, having a simple pipeline makes life easier. The habits you build now will help when you scale up.

Here's a key mindset shift. Stop thinking "I'll run this script." Start thinking "The system will run this pipeline."

You're not the operator. You're the engineer who builds the system. The system operates itself.

In the next lectures, we'll dive into the building blocks of pipelines and look at specific tools you can use to build them.

Any questions? Let's continue.

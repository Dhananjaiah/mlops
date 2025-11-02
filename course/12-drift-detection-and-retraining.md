# Module 12: Drift Detection & Retraining

## 🎯 Goals

- Detect **data drift** (input distribution changes)
- Monitor **concept drift** (target relationship changes)
- Track **prediction drift** (output distribution changes)
- Set up **automated alerts** on drift
- Trigger **retraining pipelines** automatically
- Evaluate **retraining effectiveness**

---

## 📖 Key Terms

- **Data drift**: Changes in input feature distributions over time
- **Concept drift**: Changes in relationship between features and target
- **Prediction drift**: Changes in model output distribution
- **Evidently**: Open-source drift detection library
- **Baseline**: Reference dataset for comparison (e.g., training data)
- **Retraining trigger**: Automated workflow started on drift detection

---

## 🎓 Lessons with Transcript

### What We're Doing in This Module

**Welcome to Drift Detection & Retraining!** This is where we handle the reality that models degrade over time. We're learning to detect when the world has changed and automatically trigger retraining to maintain model quality.

### Lesson 1: Why Models Degrade - The Three Types of Drift

**Transcript:**
"Unlike traditional software, ML models degrade even if the code is perfect. Three types of drift cause this. Data drift - your input feature distributions change. You trained on users aged 30-40, now your users are 20-30. Concept drift - the relationship between inputs and outputs changes. What predicted churn last year doesn't predict it this year because customer behavior evolved. Prediction drift - your model's outputs shift. You used to predict 20% churn, now it's 30%. Each type requires different responses. Data drift might just need retraining. Concept drift might need new features or algorithms. Detecting drift early prevents model failure."

**What you're learning:** The three types of drift and why models degrade in production.

### Lesson 2: Data Drift Detection with Statistical Tests

**Transcript:**
"Data drift means your feature distributions changed. Evidently detects this using statistical tests. For continuous features, it uses the Kolmogorov-Smirnov test - comparing the distribution of your production data to your training data. For categorical features, it uses chi-squared tests. If the test returns a low p-value, distributions are significantly different - that's drift. Evidently generates reports showing which features drifted and how much. You might find that 'age' distribution shifted from mean 35 to mean 28. This insight helps you decide if retraining is needed."

**What you're learning:** How statistical tests identify changes in feature distributions.

### Lesson 3: Concept Drift - Detecting Degraded Performance

**Transcript:**
"Data drift doesn't always hurt performance. Maybe age distribution shifted but your model still works fine. Concept drift is different - it directly degrades accuracy. The problem is you often can't measure it in real-time because you don't have ground truth labels immediately. A churn prediction made today won't be validated for months. The workaround is proxy metrics. If your model's confidence scores drop, that suggests concept drift. If prediction distributions change dramatically, that's suspicious. You also monitor delayed labels - when you eventually learn who actually churned, compare to predictions. Concept drift detection is harder than data drift but more important."

**What you're learning:** How to detect performance degradation when ground truth labels are delayed.

### Lesson 4: Automated Retraining Pipelines

**Transcript:**
"Detecting drift is only useful if you act on it. Automated retraining means when drift is detected, your system triggers a training pipeline automatically. Evidently generates drift reports. Your monitoring system checks if drift exceeds thresholds. If yes, it triggers an Airflow DAG that pulls the latest data with DVC, trains a new model, evaluates it, and if it's better, registers it for deployment. This happens without human intervention. The key is making the entire training process reliable and tested, so automated runs are safe. You might still have human approval before production deployment."

**What you're learning:** How to build automated retraining workflows triggered by drift detection.

### Lesson 5: Retraining Strategies - Scheduled vs Triggered

**Transcript:**
"There are two retraining philosophies. Scheduled retraining happens on a cadence - weekly, monthly - regardless of drift. It's simple and ensures models never get too stale. Triggered retraining only happens when drift is detected. It's more efficient - you don't retrain unnecessarily - but requires robust drift detection. Most production systems use a hybrid: scheduled retraining as a backstop (at least monthly), plus triggered retraining for significant drift. This ensures models are always reasonably fresh while responding quickly to major distribution shifts. For each model, you choose based on how quickly data changes and how critical freshness is."

**What you're learning:** When to use scheduled vs drift-triggered retraining strategies.

### Key Definition - What We're Doing Overall

**In this module, we're building proactive model maintenance.** We're implementing drift detection that monitors for data, concept, and prediction drift. We're using Evidently to statistically measure distribution changes. We're building automated retraining pipelines that trigger when drift exceeds thresholds. And we're choosing retraining strategies - scheduled, triggered, or hybrid - based on our use case.

**By the end of this lesson, you should understand:** The three types of drift and how each manifests, how to use Evidently to detect drift with statistical tests, how to build automated retraining workflows triggered by drift, and when to use scheduled vs triggered retraining. Drift detection and retraining transform static models into adaptive systems that maintain quality over time - it's what makes ML systems sustainable.

---

## 🔧 Commands First: Drift Detection with Evidently

```bash
# Install Evidently
pip install evidently

# Create drift detection script
cat > src/detect_drift.py << 'EOF'
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.test_suite import TestSuite
from evidently.tests import TestColumnDrift
import sys

def detect_drift(reference_path, current_path, output_html="drift_report.html"):
    """Detect data and target drift"""
    
    # Load data
    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)
    
    # Generate report
    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset()
    ])
    
    report.run(reference_data=reference, current_data=current)
    report.save_html(output_html)
    
    # Test suite for automated checks
    test_suite = TestSuite(tests=[
        TestColumnDrift(column_name='age', stattest='ks'),
        TestColumnDrift(column_name='tenure', stattest='ks'),
        TestColumnDrift(column_name='monthly_charges', stattest='ks'),
    ])
    
    test_suite.run(reference_data=reference, current_data=current)
    
    # Check if any tests failed
    result = test_suite.as_dict()
    has_drift = any(test['status'] == 'FAIL' for test in result['tests'])
    
    print(f"Drift detected: {has_drift}")
    print(f"Report saved to {output_html}")
    
    return has_drift

if __name__ == "__main__":
    has_drift = detect_drift(sys.argv[1], sys.argv[2])
    sys.exit(1 if has_drift else 0)  # Exit 1 if drift detected
EOF

# Run drift detection
python src/detect_drift.py data/train_baseline.csv data/current_week.csv
```

**Why**: Evidently quantifies drift with statistical tests. Automated tests enable CI/CD integration.

---

## 📊 Monitor Drift Over Time

```bash
# Create continuous drift monitoring
cat > src/drift_monitoring.py << 'EOF'
import pandas as pd
from evidently.metrics import ColumnDriftMetric
from evidently.report import Report
import mlflow
from datetime import datetime, timedelta

def monitor_drift_daily():
    """Run drift detection daily and log to MLflow"""
    
    # Load baseline (training data)
    baseline = pd.read_csv("data/train_baseline.csv")
    
    # Load yesterday's production data
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    current = pd.read_csv(f"data/production_{yesterday}.csv")
    
    # Calculate drift for each feature
    mlflow.set_experiment("drift-monitoring")
    
    with mlflow.start_run(run_name=f"drift_{yesterday}"):
        mlflow.log_param("date", yesterday)
        
        for col in ['age', 'tenure', 'monthly_charges']:
            report = Report(metrics=[ColumnDriftMetric(column_name=col)])
            report.run(reference_data=baseline, current_data=current)
            
            result = report.as_dict()
            drift_score = result['metrics'][0]['result']['drift_score']
            drift_detected = result['metrics'][0]['result']['drift_detected']
            
            mlflow.log_metric(f"{col}_drift_score", drift_score)
            mlflow.log_metric(f"{col}_drift_detected", 1 if drift_detected else 0)
            
            print(f"{col}: drift_score={drift_score:.3f}, drift={drift_detected}")

if __name__ == "__main__":
    monitor_drift_daily()
EOF

# Schedule with Airflow (see Module 05)
```

**Why**: Continuous monitoring tracks drift over time. MLflow logs enable alerting and trend analysis.

---

## 🚨 Alert on Drift

```bash
# Prometheus alert rule for drift
cat >> alerts.yml << 'EOF'
  - alert: DataDrift
    expr: avg(drift_detected) > 0.5
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Data drift detected"
      description: "{{ $value }} features show drift"
  
  - alert: PredictionDrift
    expr: stddev(prediction_confidence) > 0.2
    for: 30m
    labels:
      severity: warning
    annotations:
      summary: "Prediction confidence variance increased"
      description: "Model uncertainty is rising"
EOF

# Alertmanager configuration
cat > alertmanager.yml << 'EOF'
route:
  receiver: 'ml-team'
  routes:
    - match:
        alertname: DataDrift
      receiver: 'ml-team-urgent'

receivers:
  - name: 'ml-team'
    email_configs:
      - to: 'mlops@company.com'
  
  - name: 'ml-team-urgent'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/XXX'
        channel: '#mlops-alerts'
EOF
```

**Why**: Alerts notify team when drift exceeds thresholds. Quick response prevents model degradation.

---

## 🔄 Automated Retraining Pipeline

```bash
# Create Airflow DAG for retraining
cat > ~/airflow/dags/retrain_on_drift.py << 'EOF'
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import subprocess

def check_drift(**context):
    """Check if retraining is needed"""
    result = subprocess.run(
        ['python', 'src/detect_drift.py', 'data/baseline.csv', 'data/current.csv'],
        capture_output=True
    )
    
    if result.returncode == 1:  # Drift detected
        return 'retrain_model'
    else:
        return 'skip_retrain'

with DAG(
    'retrain_on_drift',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    check = BranchPythonOperator(
        task_id='check_drift',
        python_callable=check_drift,
        provide_context=True,
    )
    
    retrain = BashOperator(
        task_id='retrain_model',
        bash_command='python src/train.py --auto-retrain',
    )
    
    evaluate = BashOperator(
        task_id='evaluate_model',
        bash_command='python src/evaluate.py',
    )
    
    promote = BashOperator(
        task_id='promote_to_staging',
        bash_command='python src/register_model.py --stage Staging',
    )
    
    skip = BashOperator(
        task_id='skip_retrain',
        bash_command='echo "No drift detected, skipping retrain"',
    )
    
    check >> [retrain, skip]
    retrain >> evaluate >> promote
EOF
```

**Why**: Automated retraining keeps models fresh. Branching logic retrains only when needed (saves compute).

---

## 📈 Evaluate Retraining Impact

```bash
# Compare old vs new model
cat > src/compare_models.py << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

def compare_models(old_version, new_version, test_data_path):
    """Compare old and new model performance"""
    
    client = MlflowClient()
    
    # Load models
    old_model_uri = f"models:/ChurnPredictor/{old_version}"
    new_model_uri = f"models:/ChurnPredictor/{new_version}"
    
    old_model = mlflow.sklearn.load_model(old_model_uri)
    new_model = mlflow.sklearn.load_model(new_model_uri)
    
    # Load test data
    df = pd.read_csv(test_data_path)
    X = df[['age', 'tenure', 'monthly_charges']]
    y = df['churn']
    
    # Evaluate both
    from sklearn.metrics import accuracy_score, f1_score
    
    old_acc = accuracy_score(y, old_model.predict(X))
    new_acc = accuracy_score(y, new_model.predict(X))
    
    old_f1 = f1_score(y, old_model.predict(X))
    new_f1 = f1_score(y, new_model.predict(X))
    
    print(f"Old model (v{old_version}): accuracy={old_acc:.3f}, f1={old_f1:.3f}")
    print(f"New model (v{new_version}): accuracy={new_acc:.3f}, f1={new_f1:.3f}")
    
    # Decision
    if new_acc > old_acc:
        print("✅ New model is better, recommend promotion to Production")
        return True
    else:
        print("❌ New model is worse, recommend keeping old model")
        return False

if __name__ == "__main__":
    compare_models("1", "2", "data/test_current.csv")
EOF
```

**Why**: Always validate new models before deploying. Prevent regressions from automated retraining.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Detect drift and trigger retraining.

1. **Create baseline and drifted data**:
```bash
mkdir -p ~/mlops-lab-12 && cd ~/mlops-lab-12

# Baseline data
cat > baseline.csv << 'EOF'
age,tenure,monthly_charges,churn
34,12,65.5,0
45,24,89.0,0
23,3,45.2,1
EOF

# Drifted data (higher ages)
cat > current.csv << 'EOF'
age,tenure,monthly_charges,churn
54,12,65.5,0
65,24,89.0,0
43,3,45.2,1
EOF
```

2. **Run drift detection**:
```bash
python detect_drift.py baseline.csv current.csv
# Should exit with code 1 (drift detected)
# Open drift_report.html in browser
```

3. **View report**:
```bash
# drift_report.html shows:
# - Drift detected for 'age' column
# - Statistical tests and visualizations
```

**Expected output**: Drift detected, report shows age distribution shift.

---

## ❓ Quiz (5 Questions)

1. **What is data drift?**
   - Answer: Changes in input feature distributions over time.

2. **What is concept drift?**
   - Answer: Changes in relationship between features and target (model assumptions invalid).

3. **When should you retrain?**
   - Answer: On detected drift, scheduled intervals, or significant performance degradation.

4. **Why not retrain on every drift alert?**
   - Answer: Expensive, may not improve model, need validation to prevent regressions.

5. **What is a baseline in drift detection?**
   - Answer: Reference dataset (usually training data) for comparison with current data.

---

## ⚠️ Common Mistakes

1. **Not setting baseline** → No reference for drift comparison.  
   *Fix*: Save training data statistics as baseline.

2. **Retraining without validation** → Deploy worse models.  
   *Fix*: Always evaluate new model vs old before promoting.

3. **Ignoring concept drift** → Model performance drops even with stable data distribution.  
   *Fix*: Monitor prediction accuracy, not just feature distributions.

4. **Alert fatigue from minor drift** → Team ignores alerts.  
   *Fix*: Set appropriate thresholds, alert only on significant drift.

5. **No retraining automation** → Models degrade until manual intervention.  
   *Fix*: Automate retraining pipeline triggered by drift.

---

## 🛠️ Troubleshooting

**Issue**: "Constant drift alerts for stable data"  
→ **Root cause**: Thresholds too sensitive or baseline mismatch.  
→ **Fix**: Adjust drift thresholds, update baseline, use rolling window baseline.  
→ **See**: `/troubleshooting/triage-matrix.md` row "False drift alerts"

**Issue**: "Retraining doesn't improve model"  
→ **Root cause**: Insufficient new data, same features, or concept hasn't changed.  
→ **Fix**: Collect more data, add features, check if retraining is actually needed.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Retraining no improvement"

---

## 📚 Key Takeaways

- **Drift monitoring** detects data, concept, and prediction drift
- **Evidently** provides statistical tests and visualizations
- **Automated alerts** notify team when drift exceeds thresholds
- **Retraining pipelines** trigger automatically on drift
- **Always validate** new models before deployment
- **Track retraining effectiveness** to optimize triggers

---

## 🚀 Next Steps

- **Module 13**: Security, compliance, and cost optimization
- **Module 14**: Comprehensive review tying all modules together
- **Hands-on**: Implement drift monitoring and automated retraining for Churn Predictor

---

**[← Module 11](11-observability-and-monitoring.md)** | **[Next: Module 13 →](13-security-compliance-and-cost.md)**

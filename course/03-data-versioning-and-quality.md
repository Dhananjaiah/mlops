# Module 03: Data Versioning & Quality

## 🎯 Goals

- Version datasets with **DVC** (Data Version Control)
- Configure **remote storage** (S3, MinIO, GCS, or local)
- Track data **lineage** and metadata
- Validate data quality with **Great Expectations** or **Evidently**
- Detect **schema drift** and data anomalies
- Automate **data pipelines** with DVC pipelines

---

## 📖 Key Terms

- **DVC (Data Version Control)**: Git-like versioning for data and models (stores pointers in git, data in remote)
- **Remote storage**: External location for large files (S3, GCS, Azure Blob, MinIO, or network drive)
- **Data lineage**: Traceable path from raw data → processed → features → model
- **Schema drift**: Changes in data structure (column types, missing fields, new categories)
- **Data drift**: Changes in statistical properties (mean, distribution, ranges)
- **Great Expectations**: Data validation framework with expectations (rules) on datasets
- **Evidently**: Open-source tool for data/model drift detection and visualization

---

## 🔧 Commands First: Install and Initialize DVC

```bash
# Install DVC with S3 support
pip install 'dvc[s3]'  # or [gs] for GCS, [azure] for Azure

# For local/MinIO
pip install 'dvc[s3]'

# Initialize DVC in git repo
cd ~/mlops-demo
dvc init

# Check created files
git status
# Should show .dvc/, .dvcignore

# Commit DVC setup
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

**Why**: DVC stores large files externally and tracks pointers (.dvc files) in git. This keeps git fast while versioning data.

---

## 📦 Add Data to DVC

```bash
# Create sample dataset
mkdir -p data/raw
cat > data/raw/customers.csv << 'EOF'
customer_id,age,tenure,monthly_charges,churn
1,34,12,65.5,0
2,45,24,89.0,0
3,23,3,45.2,1
4,56,36,120.0,0
5,29,6,55.0,1
EOF

# Add to DVC (not git)
dvc add data/raw/customers.csv

# Check generated files
ls data/raw/
# customers.csv (actual data)
# customers.csv.dvc (pointer file)

# Git tracks only the .dvc file
git add data/raw/customers.csv.dvc data/raw/.gitignore
git commit -m "Add customers dataset (v1)"

# DVC automatically adds data/ to .gitignore
cat data/raw/.gitignore
# Should contain: /customers.csv
```

**Why**: `dvc add` creates a `.dvc` file with MD5 hash and metadata. Git tracks the small .dvc file, not the large data.

---

## ☁️ Configure Remote Storage (Local for Lab)

```bash
# Option 1: Local remote (for testing)
mkdir -p /tmp/dvc-remote
dvc remote add -d local /tmp/dvc-remote

# Option 2: MinIO (S3-compatible, local)
dvc remote add -d minio s3://mlops-artifacts
dvc remote modify minio endpointurl http://localhost:9000
dvc remote modify minio access_key_id minioadmin
dvc remote modify minio secret_access_key minioadmin

# Option 3: AWS S3 (production)
dvc remote add -d s3 s3://${BUCKET}/dvc-store
# Uses AWS credentials from ~/.aws/credentials or IAM role

# Check config
dvc remote list
# Should show configured remote

# Save config to git
git add .dvc/config
git commit -m "Configure DVC remote"
```

**Why**: Remotes store actual data. Team members pull data from shared remote instead of passing files around.

---

## ⬆️ Push and Pull Data

```bash
# Push data to remote
dvc push

# Verify (for local remote)
ls /tmp/dvc-remote/
# Should see hashed files

# Simulate teammate: Remove local data
rm data/raw/customers.csv

# Pull from remote
dvc pull

# Verify
ls data/raw/customers.csv
# Data is back!
```

**Why**: `dvc push` uploads to remote, `dvc pull` downloads. Like git push/pull but for data.

---

## ✅ Verify DVC Setup

```bash
# Check DVC status
dvc status
# Should show "Data and pipelines are up to date"

# Check remote
dvc remote list
# Should show configured remote

# Verify data tracked
dvc list . data/raw/
# Should show customers.csv

# Check git doesn't have large files
git --no-pager log --all --pretty=format: --name-only --diff-filter=A | \
  sort -u | xargs -I {} sh -c 'du -h "{}" 2>/dev/null' | \
  awk '$1 ~ /M$|G$/'
# Should be empty (no large files in git)
```

---

## 🧪 Data Pipelines with DVC

```bash
# Create preprocessing script
cat > src/preprocess.py << 'EOF'
import pandas as pd
import sys

def preprocess(input_path, output_path):
    df = pd.read_csv(input_path)
    # Simple preprocessing
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 50, 100], labels=['young', 'mid', 'senior'])
    df.to_csv(output_path, index=False)
    print(f"Processed {len(df)} rows")

if __name__ == "__main__":
    preprocess(sys.argv[1], sys.argv[2])
EOF

# Create DVC pipeline
dvc stage add -n preprocess \
  -d src/preprocess.py \
  -d data/raw/customers.csv \
  -o data/processed/customers_processed.csv \
  python src/preprocess.py data/raw/customers.csv data/processed/customers_processed.csv

# Run pipeline
dvc repro

# Check outputs
cat data/processed/customers_processed.csv
# Should have age_group column

# Commit pipeline
git add dvc.yaml dvc.lock
git commit -m "Add preprocessing pipeline"
```

**Why**: DVC pipelines track dependencies (input data, code) and outputs. `dvc repro` reruns only changed stages (like Makefile).

---

## 📊 Data Quality with Great Expectations

```bash
# Install
pip install great_expectations

# Initialize
great_expectations init

# Create expectation suite
great_expectations suite new customers_suite

# Edit expectation suite (great_expectations/expectations/customers_suite.json)
cat > great_expectations/expectations/customers_suite.json << 'EOF'
{
  "expectation_suite_name": "customers_suite",
  "expectations": [
    {
      "expectation_type": "expect_table_columns_to_match_ordered_list",
      "kwargs": {
        "column_list": ["customer_id", "age", "tenure", "monthly_charges", "churn"]
      }
    },
    {
      "expectation_type": "expect_column_values_to_be_between",
      "kwargs": {
        "column": "age",
        "min_value": 18,
        "max_value": 100
      }
    },
    {
      "expectation_type": "expect_column_values_to_be_in_set",
      "kwargs": {
        "column": "churn",
        "value_set": [0, 1]
      }
    }
  ]
}
EOF

# Run validation
great_expectations checkpoint new customers_checkpoint
great_expectations checkpoint run customers_checkpoint
```

**Why**: Great Expectations validates data against expectations. Fails pipeline if data is corrupt or drifted.

---

## 📈 Data Drift Detection with Evidently

```bash
# Install
pip install evidently

# Create drift detection script
cat > src/check_drift.py << 'EOF'
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Reference data (baseline)
reference = pd.read_csv("data/raw/customers.csv")

# Current data (new batch)
current = pd.read_csv("data/raw/customers_new.csv")

# Generate report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)
report.save_html("reports/drift_report.html")

print("Drift report saved to reports/drift_report.html")
EOF

# Create new batch with drift
cat > data/raw/customers_new.csv << 'EOF'
customer_id,age,tenure,monthly_charges,churn
6,70,48,150.0,0
7,72,52,160.0,0
8,68,44,145.0,1
EOF

# Run drift detection
mkdir -p reports
python src/check_drift.py

# View report
# Open reports/drift_report.html in browser
```

**Why**: Evidently detects statistical drift (distribution changes). Use in monitoring pipelines to trigger retraining.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Version a dataset, create a preprocessing pipeline, and validate quality.

1. **Setup**:
```bash
mkdir -p ~/mlops-lab-03 && cd ~/mlops-lab-03
git init
dvc init
git add .dvc .dvcignore && git commit -m "Init DVC"
```

2. **Add data**:
```bash
mkdir -p data/raw
echo -e "id,value\n1,10\n2,20\n3,30" > data/raw/input.csv
dvc add data/raw/input.csv
git add data/raw/input.csv.dvc data/raw/.gitignore
git commit -m "Add input data"
```

3. **Configure local remote**:
```bash
mkdir -p /tmp/lab03-remote
dvc remote add -d local /tmp/lab03-remote
git add .dvc/config && git commit -m "Add remote"
dvc push
```

4. **Create pipeline**:
```bash
mkdir -p src
cat > src/transform.py << 'EOF'
import sys
with open(sys.argv[1]) as f:
    lines = f.readlines()
with open(sys.argv[2], 'w') as f:
    f.write(lines[0])  # header
    for line in lines[1:]:
        parts = line.strip().split(',')
        f.write(f"{parts[0]},{int(parts[1]) * 2}\n")
EOF

dvc stage add -n transform \
  -d src/transform.py \
  -d data/raw/input.csv \
  -o data/processed/output.csv \
  python src/transform.py data/raw/input.csv data/processed/output.csv

dvc repro
cat data/processed/output.csv
# Should show: id,value\n1,20\n2,40\n3,60
```

5. **Commit**:
```bash
git add dvc.yaml dvc.lock data/processed/.gitignore
git commit -m "Add transform pipeline"
```

**Expected output**: Pipeline runs, output.csv has doubled values, all tracked by DVC.

---

## ❓ Quiz (5 Questions)

1. **What files does DVC track in git?**
   - Answer: .dvc pointer files (e.g., data.csv.dvc), dvc.yaml, dvc.lock. Actual data stays in remote.

2. **What is the difference between data drift and schema drift?**
   - Answer: Schema drift = structure changes (columns, types). Data drift = statistical changes (distributions, means).

3. **Why use DVC pipelines instead of shell scripts?**
   - Answer: DVC tracks dependencies and caches results. Reruns only changed stages (incremental builds).

4. **What does Great Expectations validate?**
   - Answer: Data quality rules (schemas, ranges, uniqueness, distributions) against expectations.

5. **When should you retrain a model?**
   - Answer: On detected data/concept drift, scheduled intervals, or significant performance degradation.

---

## ⚠️ Common Mistakes

1. **Committing data to git instead of DVC** → Repo bloat.  
   *Fix*: Always use `dvc add`, never `git add` for large files.

2. **Not configuring DVC remote** → Can't share data with team.  
   *Fix*: Set remote with `dvc remote add`, push regularly.

3. **Skipping data validation** → Bad data breaks training silently.  
   *Fix*: Add Great Expectations checks in pipelines.

4. **Not versioning preprocessing code** → Can't reproduce features.  
   *Fix*: Track preprocessing scripts in git and DVC pipelines.

5. **Ignoring drift alerts** → Model degrades over time.  
   *Fix*: Monitor with Evidently, automate retraining triggers.

---

## 🛠️ Troubleshooting

**Issue**: "dvc push fails with 403 Forbidden"  
→ **Root cause**: Missing S3/MinIO credentials or wrong permissions.  
→ **Fix**: Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` or configure `dvc remote modify` credentials.  
→ **See**: `/troubleshooting/triage-matrix.md` row "DVC remote access denied"

**Issue**: "dvc repro says 'Stage is cached', but output is wrong"  
→ **Root cause**: Stale cache, dependencies not tracked correctly.  
→ **Fix**: `dvc repro --force` to ignore cache, or add missing `-d` dependencies.  
→ **See**: `/troubleshooting/triage-matrix.md` row "DVC pipeline not rerunning"

---

## 📚 Key Takeaways

- **DVC** versions data/models in external remotes, tracks small .dvc pointers in git
- **DVC pipelines** make preprocessing reproducible and incremental (like Makefile for data)
- **Great Expectations** validates data quality (schema, ranges, distributions)
- **Evidently** detects data drift (statistical changes) for monitoring
- Always **version both data and preprocessing code** for full reproducibility
- **Automate validation** in pipelines to catch bad data early

---

## 🚀 Next Steps

- **Module 04**: Track experiments with MLflow (params, metrics, artifacts, models)
- **Module 05**: Orchestrate multi-stage pipelines with Airflow/Kubeflow
- **Hands-on**: Add DVC tracking to Churn Predictor datasets in `/project/data/`

---

**[← Module 02](02-env-and-packaging.md)** | **[Next: Module 04 →](04-experiment-tracking-and-reproducibility.md)**

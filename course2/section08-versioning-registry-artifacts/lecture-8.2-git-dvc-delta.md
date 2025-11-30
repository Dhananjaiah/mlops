# Lecture 8.2 – Git for Code, DVC/Delta/etc. for Data (Concepts)

## Human Transcript

Alright, let's dive deeper into how we actually version data. We've established that Git handles code versioning really well. But data is a different beast. And in this lecture, I'm going to show you the main approaches and tools.

First, why can't we just use Git for data?

Git stores the complete history of your repository. Every version of every file. For code, this works great because text files compress well and changes are usually small. But for data? Imagine you have a 10 GB dataset. You make a small change, adding a few rows. Git stores the entire 10 GB again as a new version. Your repository balloons to 20 GB. Do this a few times and you're in trouble.

There are also practical issues. Git repositories are meant to be cloned. Every developer gets a full copy. You don't want every developer downloading 50 GB of historical data just to run a script.

So we need different approaches for data. Let me walk you through the main ones.

DVC, Data Version Control. This is probably the most popular tool. DVC works alongside Git. Here's the key insight: Git tracks metadata files that describe your data, while the actual data lives elsewhere.

Let me show you how it works:

```bash
# Initialize DVC in your Git repo
dvc init

# Add a data file to DVC tracking
dvc add data/customers.csv
```

This creates two things:
1. `data/customers.csv.dvc` - a small file containing metadata and a hash
2. `.gitignore` entry - so Git ignores the actual data file

```bash
# The .dvc file looks like this:
cat data/customers.csv.dvc
```
```yaml
outs:
- md5: d41d8cd98f00b204e9800998ecf8427e
  size: 1048576
  path: customers.csv
```

Now you commit the `.dvc` file to Git:

```bash
git add data/customers.csv.dvc
git commit -m "Add customer data v1"
```

Where does the actual data go? DVC has remote storage, similar to Git remote. You can use S3, Google Cloud Storage, Azure Blob, or even a local folder:

```bash
# Configure remote storage
dvc remote add -d myremote s3://my-bucket/dvc-storage

# Push data to remote
dvc push
```

When someone clones your repo, they get the `.dvc` files. To get the actual data:

```bash
git clone your-repo
cd your-repo
dvc pull  # Downloads the data files
```

The beautiful thing is versioning. If you update your data:

```bash
# Modify data somehow
python scripts/add_new_customers.py

# Track the change
dvc add data/customers.csv
git add data/customers.csv.dvc
git commit -m "Add customer data v2"
dvc push
```

Now Git has two commits, each pointing to a different version of the data. You can switch between them:

```bash
git checkout HEAD~1  # Go to previous commit
dvc checkout         # Get the data for that commit
```

DVC also supports pipelines. You can define data processing steps:

```yaml
# dvc.yaml
stages:
  process_data:
    cmd: python scripts/process.py
    deps:
      - scripts/process.py
      - data/raw/customers.csv
    outs:
      - data/processed/customers_clean.csv
  
  train_model:
    cmd: python scripts/train.py
    deps:
      - scripts/train.py
      - data/processed/customers_clean.csv
    outs:
      - models/churn_model.pkl
    metrics:
      - metrics/results.json:
          cache: false
```

Run the pipeline:
```bash
dvc repro  # Runs only stages whose inputs changed
```

Now let's talk about Delta Lake. This is a different approach. Delta Lake is a storage format that adds ACID transactions and versioning to data lakes.

With Delta Lake, your data lives as Parquet files, but with a transaction log that tracks every change:

```python
# Write data in Delta format
from delta import DeltaTable
import pandas as pd

df = pd.read_csv("customers.csv")

# Write as Delta table
df.write.format("delta").save("/data/customers_delta")

# Later, update some rows
spark.sql("""
UPDATE delta.`/data/customers_delta`
SET status = 'churned'
WHERE last_active < '2023-01-01'
""")
```

Delta Lake keeps history automatically. You can query any previous version:

```python
# Query current version
df_current = spark.read.format("delta").load("/data/customers_delta")

# Query version 5
df_v5 = spark.read.format("delta").option("versionAsOf", 5).load("/data/customers_delta")

# Query as of a timestamp
df_historical = spark.read.format("delta") \
    .option("timestampAsOf", "2023-10-15") \
    .load("/data/customers_delta")
```

You can also roll back:
```python
# Restore to version 5
deltaTable = DeltaTable.forPath(spark, "/data/customers_delta")
deltaTable.restoreToVersion(5)
```

Delta Lake is great when:
- You're already using Spark
- You have large datasets that change incrementally
- You need ACID transactions
- You want time travel queries built in

LakeFS is another option. It provides a Git-like interface for your data lake. You can have branches, commits, and merges for your data:

```bash
# Create a branch
lakectl branch create lakefs://repo/experiment-1 --source lakefs://repo/main

# Make changes to data in the branch
# ... upload new files, delete files, etc.

# Commit changes
lakectl commit lakefs://repo/experiment-1 -m "Added new features"

# Merge back to main
lakectl merge lakefs://repo/experiment-1 lakefs://repo/main
```

This is powerful for experimentation. You can create a data branch, try processing it differently, and if it works, merge back.

Let me also mention cloud-native options:

S3 versioning. AWS S3 can keep multiple versions of objects. Simple to use but limited:
```bash
aws s3api put-object --bucket my-bucket --key data/customers.csv --body customers.csv
# S3 automatically keeps the previous version
```

BigQuery snapshots. If you're using BigQuery, you can create table snapshots and query historical data:
```sql
SELECT * FROM `project.dataset.table`
FOR SYSTEM_TIME AS OF TIMESTAMP('2023-10-15 12:00:00')
```

How do you choose? Here's my recommendation:

Use DVC if:
- Your data is files (CSV, Parquet, images, etc.)
- You're already using Git
- You want to integrate data versioning with code versioning
- You have a small to medium team

Use Delta Lake if:
- You're using Spark
- Your data is in a data lake
- You need ACID transactions
- You have complex data pipelines with lots of updates

Use LakeFS if:
- You want Git-like branching for data
- You need to experiment with different data versions
- You're managing a data platform

Use cloud-native options if:
- Your needs are simple
- You're already deep in one cloud ecosystem

The key thing is: pick something. Any versioning is better than no versioning. The worst situation is having a model in production and not knowing what data it was trained on.

In the next lecture, we'll look at model registries, which is where we store and version our trained models.

Questions? Let's move on.

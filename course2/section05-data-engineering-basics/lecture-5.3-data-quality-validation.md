# Lecture 5.3 – Data Quality & Validation (Basic Checks MLOps Must Enforce)

---

## Garbage In, Garbage Out

You've heard it before: if you put bad data into a model, you get bad predictions out.

Data quality is MLOps's first line of defense. In this lecture, you'll learn what to check and how to automate those checks.

---

## Why Data Quality Matters

Real stories:

**Story 1**: A model's accuracy dropped from 85% to 60%. Investigation took two weeks. Cause: A decimal point moved in one feature. `$1000.00` became `$100000`.

**Story 2**: A batch scoring job ran but produced garbage predictions. Cause: The source table was empty. No one checked.

**Story 3**: A retraining run incorporated test data into training. Cause: No validation that datasets were disjoint. Model appeared perfect (100% accuracy!), failed completely in production.

Data quality checks would have caught all of these immediately.

---

## Types of Data Quality Checks

### 1. Schema Validation

**Question**: Does the data have the expected structure?

Checks:
- Expected columns exist
- Column types are correct
- No unexpected columns

```python
def validate_schema(df, expected_schema):
    """Validate dataframe matches expected schema."""
    errors = []
    
    # Check required columns
    for col, dtype in expected_schema.items():
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
        elif str(df[col].dtype) != dtype:
            errors.append(f"Wrong type for {col}: expected {dtype}, got {df[col].dtype}")
    
    if errors:
        raise SchemaValidationError(errors)
```

### 2. Completeness Checks

**Question**: Is the data complete?

Checks:
- Required columns have no nulls
- Tables have expected row counts
- All expected partitions exist

```python
def check_completeness(df, required_columns):
    """Check for missing values in required columns."""
    for col in required_columns:
        null_count = df[col].isnull().sum()
        null_pct = null_count / len(df) * 100
        
        if null_pct > 0:
            logger.warning(f"{col} has {null_pct:.2f}% nulls")
        if null_pct > 5:  # Threshold
            raise DataQualityError(f"{col} exceeds null threshold: {null_pct:.2f}%")
```

### 3. Range/Domain Validation

**Question**: Are values within expected bounds?

Checks:
- Numerical ranges (age > 0 and < 150)
- Categorical values in allowed set
- Dates within expected range

```python
def check_ranges(df):
    """Validate values are in expected ranges."""
    validations = [
        ('age', lambda x: (x >= 0) & (x <= 120)),
        ('amount', lambda x: x >= 0),
        ('date', lambda x: x <= pd.Timestamp.now()),
    ]
    
    for col, check in validations:
        if col in df.columns:
            invalid = ~check(df[col])
            if invalid.sum() > 0:
                raise DataQualityError(f"{col} has {invalid.sum()} out-of-range values")
```

### 4. Uniqueness Checks

**Question**: Are IDs actually unique?

Checks:
- Primary keys are unique
- No duplicate rows

```python
def check_uniqueness(df, key_columns):
    """Check for duplicate records."""
    duplicates = df.duplicated(subset=key_columns, keep=False)
    if duplicates.sum() > 0:
        raise DataQualityError(f"Found {duplicates.sum()} duplicate rows")
```

### 5. Freshness Checks

**Question**: Is the data recent enough?

Checks:
- Latest timestamp within expected range
- Data not stale

```python
def check_freshness(df, date_column, max_age_hours=24):
    """Check if data is fresh enough."""
    latest = df[date_column].max()
    age_hours = (pd.Timestamp.now() - latest).total_seconds() / 3600
    
    if age_hours > max_age_hours:
        raise DataQualityError(f"Data is {age_hours:.1f} hours old (max: {max_age_hours})")
```

### 6. Referential Integrity

**Question**: Do foreign keys reference valid records?

Checks:
- All customer_ids exist in customer table
- No orphaned records

```python
def check_referential_integrity(df, ref_df, key_column):
    """Check foreign key references are valid."""
    valid_keys = set(ref_df[key_column])
    invalid_keys = set(df[key_column]) - valid_keys
    
    if invalid_keys:
        raise DataQualityError(f"Found {len(invalid_keys)} invalid {key_column} references")
```

### 7. Statistical Checks

**Question**: Does the data distribution look normal?

Checks:
- Mean/median within expected range
- Standard deviation not extreme
- Distribution hasn't shifted dramatically

```python
def check_statistics(df, column, expected_mean, tolerance=0.2):
    """Check statistical properties."""
    actual_mean = df[column].mean()
    deviation = abs(actual_mean - expected_mean) / expected_mean
    
    if deviation > tolerance:
        raise DataQualityError(
            f"{column} mean {actual_mean:.2f} deviates {deviation:.0%} from expected {expected_mean:.2f}"
        )
```

---

## Great Expectations

Great Expectations is a popular library for data validation:

```python
import great_expectations as ge

# Load data as Great Expectations dataframe
df = ge.read_csv("data/customers.csv")

# Define expectations
df.expect_column_to_exist("customer_id")
df.expect_column_values_to_not_be_null("customer_id")
df.expect_column_values_to_be_unique("customer_id")
df.expect_column_values_to_be_between("age", min_value=0, max_value=120)
df.expect_column_values_to_be_in_set("plan_type", ["basic", "pro", "enterprise"])

# Run validation
results = df.validate()

if not results["success"]:
    for result in results["results"]:
        if not result["success"]:
            print(f"FAILED: {result['expectation_config']['expectation_type']}")
```

### Creating an Expectation Suite

```python
from great_expectations.core import ExpectationSuite, ExpectationConfiguration

suite = ExpectationSuite("customer_data_suite")

suite.add_expectation(ExpectationConfiguration(
    expectation_type="expect_column_to_exist",
    kwargs={"column": "customer_id"}
))

suite.add_expectation(ExpectationConfiguration(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={"column": "customer_id"}
))

# Save suite
context.save_expectation_suite(suite)
```

---

## Data Validation in Pipelines

Where to add validation:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Extract   │───►│  VALIDATE   │───►│  Transform  │───►│    Load     │
└─────────────┘    │   (here!)   │    └─────────────┘    └─────────────┘
                   └─────────────┘
                         │
                   Fail fast if
                   data is bad
```

### Airflow Example with Validation

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator

def extract_data(**context):
    df = extract_from_source()
    df.to_parquet('/tmp/raw_data.parquet')

def validate_data(**context):
    df = pd.read_parquet('/tmp/raw_data.parquet')
    
    # Run all checks
    check_schema(df, EXPECTED_SCHEMA)
    check_completeness(df, REQUIRED_COLUMNS)
    check_ranges(df)
    check_freshness(df, 'updated_at')
    
    # If we get here, all checks passed
    return True

def handle_validation_failure(**context):
    """Alert team about data quality issues."""
    send_slack_alert("Data validation failed! Check logs.")
    raise AirflowException("Data validation failed")

def transform_data(**context):
    df = pd.read_parquet('/tmp/raw_data.parquet')
    df_transformed = transform(df)
    df_transformed.to_parquet('/tmp/transformed_data.parquet')

with DAG('data_pipeline_with_validation') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    validate = PythonOperator(task_id='validate', python_callable=validate_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    
    extract >> validate >> transform
```

---

## Validation for ML Specifically

### Training Data Validation

```python
def validate_training_data(train_df, test_df, target_column):
    """Validate training/test data for ML."""
    
    # Check for data leakage
    train_ids = set(train_df['id'])
    test_ids = set(test_df['id'])
    overlap = train_ids & test_ids
    if overlap:
        raise DataQualityError(f"Data leakage: {len(overlap)} IDs in both train and test")
    
    # Check class balance
    class_counts = train_df[target_column].value_counts(normalize=True)
    if class_counts.min() < 0.01:
        logger.warning(f"Severe class imbalance: {class_counts.to_dict()}")
    
    # Check feature coverage
    for col in train_df.columns:
        if train_df[col].nunique() == 1:
            raise DataQualityError(f"Column {col} has only one value")
```

### Feature Validation

```python
def validate_features(features_df, feature_spec):
    """Validate feature values."""
    for feature_name, spec in feature_spec.items():
        col = features_df[feature_name]
        
        # Check for infinite values
        if col.isin([np.inf, -np.inf]).any():
            raise DataQualityError(f"{feature_name} contains infinite values")
        
        # Check for extreme outliers
        if spec.get('check_outliers', True):
            z_scores = (col - col.mean()) / col.std()
            extreme = (z_scores.abs() > 10).sum()
            if extreme > 0:
                logger.warning(f"{feature_name} has {extreme} extreme outliers")
```

---

## What to Do When Validation Fails

### Option 1: Stop the Pipeline

Most conservative. Nothing proceeds if data is bad.

```python
if not validation_passed:
    raise PipelineException("Validation failed, stopping pipeline")
```

### Option 2: Alert and Continue (with Caution)

For non-critical issues.

```python
if null_percentage > 1:
    send_alert(f"Warning: {null_percentage}% nulls in {column}")
    # Continue anyway, but team is aware
```

### Option 3: Auto-Remediation

Fix known issues automatically.

```python
# Fill missing values with defaults
df['industry'] = df['industry'].fillna('unknown')

# Remove out-of-range values
df = df[df['age'].between(0, 120)]

# Log what was fixed
logger.info(f"Auto-remediated {fixed_count} records")
```

### Best Practice: Tiered Approach

```python
def validate_with_tiers(df):
    """Tiered validation: Critical, Warning, Info."""
    
    # CRITICAL: Stop pipeline
    if df.empty:
        raise CriticalDataError("DataFrame is empty!")
    if 'customer_id' not in df.columns:
        raise CriticalDataError("Missing customer_id column!")
    
    # WARNING: Alert but continue
    null_pct = df['industry'].isnull().mean()
    if null_pct > 0.1:
        send_alert(f"Warning: industry has {null_pct:.1%} nulls")
    
    # INFO: Log for monitoring
    logger.info(f"Processed {len(df)} records")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
```

---

## For Our Churn Project

Key validations we'll implement:

| Check | Type | Action if Failed |
|-------|------|------------------|
| customer_id not null | Critical | Stop pipeline |
| customer_id unique | Critical | Stop pipeline |
| Expected columns exist | Critical | Stop pipeline |
| Row count > 1000 | Critical | Stop pipeline |
| Data freshness < 24h | Warning | Alert team |
| Null rate < 5% per column | Warning | Alert team |
| No future dates | Critical | Stop pipeline |

---

## Recap

Data quality checks to implement:

1. **Schema**: Expected columns and types
2. **Completeness**: No unexpected nulls
3. **Range**: Values within bounds
4. **Uniqueness**: No duplicates where expected
5. **Freshness**: Data is recent enough
6. **Referential integrity**: Foreign keys valid
7. **Statistics**: Distribution looks reasonable

Use Great Expectations for comprehensive validation.

Tiered approach: Critical (stop), Warning (alert), Info (log).

---

## What's Next

Now let's talk about feature engineering—transforming raw data into inputs your model can use.

---

**Next Lecture**: [5.4 – Feature Engineering Overview (Not Deep ML, Just Enough to Operate)](lecture-5.4-feature-engineering.md)

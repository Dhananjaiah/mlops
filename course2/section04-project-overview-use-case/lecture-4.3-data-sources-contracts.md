# Lecture 4.3 – Data Sources & Data Contracts (Who Owns the Data?)

---

## Data Is the Foundation

You can have the best model architecture in the world. If your data is wrong, your model is wrong.

In this lecture, we'll map out where our data comes from and establish contracts with the teams who own it.

---

## Our Data Sources

For churn prediction, we need data from multiple sources:

### 1. Customer Database

**What it contains**:
- Customer ID
- Company name
- Signup date
- Plan type (Basic, Pro, Enterprise)
- Number of seats
- Account manager assigned
- Industry/vertical

**Owner**: Product Engineering team

**Update frequency**: Real-time (transactional)

**Access method**: PostgreSQL database

### 2. Usage Logs

**What it contains**:
- Customer ID
- Timestamp
- Action (login, create_project, invite_user, etc.)
- Duration
- Features used

**Owner**: Data Engineering team

**Update frequency**: Streaming (via Kafka) → Daily aggregates

**Access method**: Data warehouse (BigQuery/Snowflake)

### 3. Support Tickets

**What it contains**:
- Customer ID
- Ticket ID
- Created date
- Category (bug, feature_request, how_to, billing)
- Priority
- Resolution time
- Satisfaction score

**Owner**: Customer Support team

**Update frequency**: Real-time (Zendesk)

**Access method**: Zendesk API → Data warehouse

### 4. Billing Data

**What it contains**:
- Customer ID
- Invoice date
- Amount
- Payment status
- Payment failures
- Plan changes

**Owner**: Finance team

**Update frequency**: Daily

**Access method**: Stripe API → Data warehouse

### 5. Churn Labels (Historical)

**What it contains**:
- Customer ID
- Churn date (if churned)
- Churn reason (if captured)

**Owner**: Customer Success team

**Update frequency**: Monthly reconciliation

**Access method**: CRM (Salesforce) → Data warehouse

---

## Data Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Customer   │     │   Usage     │     │   Support   │
│     DB      │     │    Logs     │     │   Tickets   │
│ (PostgreSQL)│     │  (Kafka)    │     │ (Zendesk)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│                   ETL Pipelines                       │
│                    (Airflow)                          │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│                  Data Warehouse                       │
│               (BigQuery/Snowflake)                    │
├──────────────────────────────────────────────────────┤
│  raw.customers    │  raw.usage    │  raw.support     │
│  raw.billing      │  raw.churn_labels               │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│               Feature Engineering                     │
│                 (dbt / Spark)                         │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│                  Feature Store                        │
│           (features.customer_features)               │
└──────────────────────────────────────────────────────┘
                           │
                           ▼
                    ML Training / Serving
```

---

## Data Contracts

A data contract is an agreement between the data producer and consumer about:
- What data will be provided
- In what format
- At what quality
- On what schedule

### Why Data Contracts Matter

Without contracts:
- Data format changes without warning → pipeline breaks
- Data quality drops → model performance drops
- Schedule changes → predictions delayed
- Schema changes → code fails

With contracts:
- Changes are communicated in advance
- Quality expectations are clear
- Both sides know their responsibilities

---

## Example Data Contract

Here's a contract for the customer data:

```yaml
# data_contracts/customer_data.yaml

contract_name: customer_data
version: "1.0"
owner: Product Engineering
consumers:
  - Data Engineering
  - ML Team

description: >
  Core customer information from the product database.
  Used for churn prediction and customer analytics.

schema:
  type: object
  properties:
    customer_id:
      type: string
      format: uuid
      description: Unique customer identifier
      nullable: false
    
    company_name:
      type: string
      description: Company name
      nullable: false
      pii: true  # Personally identifiable information
    
    signup_date:
      type: string
      format: date
      description: Date customer signed up
      nullable: false
    
    plan_type:
      type: string
      enum: [basic, pro, enterprise]
      description: Current subscription plan
      nullable: false
    
    seat_count:
      type: integer
      minimum: 1
      description: Number of licensed seats
      nullable: false
    
    industry:
      type: string
      description: Customer's industry vertical
      nullable: true
    
    is_active:
      type: boolean
      description: Whether customer is currently active
      nullable: false

quality:
  completeness:
    customer_id: 100%
    company_name: 100%
    signup_date: 100%
    plan_type: 100%
    seat_count: 100%
    industry: 85%  # Some customers don't provide this
    is_active: 100%
  
  freshness:
    max_delay: 1 hour
  
  uniqueness:
    customer_id: true

delivery:
  format: parquet
  location: gs://data-warehouse/raw/customers/
  partitioning: daily
  schedule: continuous (CDC)
  retention: 3 years

sla:
  availability: 99.9%
  support_contact: data-eng@techflow.com
  change_notification: 2 weeks advance notice

testing:
  - name: not_null_customer_id
    type: not_null
    column: customer_id
  
  - name: valid_plan_type
    type: accepted_values
    column: plan_type
    values: [basic, pro, enterprise]
  
  - name: positive_seats
    type: custom
    sql: SELECT COUNT(*) FROM customers WHERE seat_count <= 0
    threshold: 0
```

---

## Contracts for All Sources

We need contracts for each data source:

### Customer Data Contract

| Field | Type | Nullable | Quality |
|-------|------|----------|---------|
| customer_id | UUID | No | 100% complete |
| company_name | String | No | 100% complete |
| signup_date | Date | No | 100% complete |
| plan_type | Enum | No | 100% complete |
| seat_count | Integer | No | 100% complete |

### Usage Data Contract

| Field | Type | Nullable | Quality |
|-------|------|----------|---------|
| customer_id | UUID | No | 100% complete |
| event_date | Date | No | 100% complete |
| event_type | String | No | 100% complete |
| event_count | Integer | No | 100% complete |
| daily_active_users | Integer | No | 95% complete |

### Support Data Contract

| Field | Type | Nullable | Quality |
|-------|------|----------|---------|
| customer_id | UUID | No | 100% complete |
| ticket_date | Date | No | 100% complete |
| category | Enum | No | 100% complete |
| priority | Enum | No | 100% complete |
| resolution_hours | Float | Yes | 90% complete |

### Billing Data Contract

| Field | Type | Nullable | Quality |
|-------|------|----------|---------|
| customer_id | UUID | No | 100% complete |
| invoice_date | Date | No | 100% complete |
| amount | Decimal | No | 100% complete |
| payment_status | Enum | No | 100% complete |
| failures_count | Integer | No | 100% complete |

---

## Data Ownership Matrix

Who's responsible for what?

| Data | Owner | Quality | Pipeline | Consumer |
|------|-------|---------|----------|----------|
| Customer | Product Eng | Product Eng | Data Eng | ML Team |
| Usage | Backend | Backend | Data Eng | ML Team |
| Support | CS Ops | CS Ops | Data Eng | ML Team |
| Billing | Finance | Finance | Data Eng | ML Team |
| Features | ML Team | ML Team | ML Team | ML Team |
| Predictions | ML Team | ML Team | ML Team | CS Team |

---

## Handling Data Issues

What happens when data doesn't meet the contract?

### Issue: Missing Data

```python
# Example: Handle missing industry
def fill_missing_industry(df):
    """Fill missing industry with 'unknown'."""
    df['industry'] = df['industry'].fillna('unknown')
    return df
```

### Issue: Late Data

```python
# Example: Fail gracefully if data is stale
def check_data_freshness(df, max_age_hours=24):
    """Check if data is fresh enough."""
    latest = df['updated_at'].max()
    age_hours = (datetime.now() - latest).total_seconds() / 3600
    
    if age_hours > max_age_hours:
        logger.warning(f"Data is {age_hours:.1f} hours old")
        if age_hours > max_age_hours * 2:
            raise DataFreshnessError(f"Data too stale: {age_hours:.1f} hours")
    
    return True
```

### Issue: Schema Change

```python
# Example: Validate schema before processing
EXPECTED_COLUMNS = ['customer_id', 'signup_date', 'plan_type', 'seat_count']

def validate_schema(df):
    """Validate dataframe has expected columns."""
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise SchemaError(f"Missing columns: {missing}")
    return True
```

---

## Working with Data Teams

Tips for successful collaboration:

### 1. Start with a Conversation

Don't just send requirements. Meet with the data owners:
- Explain what you're building
- Understand their constraints
- Agree on what's realistic

### 2. Document Everything

Write down the agreement:
- Schema
- Quality expectations
- Schedule
- Change process

### 3. Build Validation

Automate checks in your pipeline:
```python
# Run at start of every training pipeline
validate_customer_data(customer_df)
validate_usage_data(usage_df)
validate_support_data(support_df)
```

### 4. Create Feedback Loops

Let data teams know about issues:
- Automated alerts on quality drops
- Regular data quality reports
- Quarterly review meetings

### 5. Plan for Changes

Data will change. Plan for it:
- Version your schemas
- Make code adaptable
- Have rollback plans

---

## Recap

Data sources for our churn prediction:
- **Customer DB**: Core customer info
- **Usage logs**: Product engagement
- **Support tickets**: Customer issues
- **Billing data**: Payment health
- **Churn labels**: Training targets

Data contracts define:
- Schema and types
- Quality expectations
- Delivery schedule
- Change notification process

Key principles:
- Clear ownership
- Documented contracts
- Automated validation
- Collaborative relationships

---

## What's Next

Now let's design the high-level architecture that ties all these components together.

---

**Next Lecture**: [4.4 – High-Level Architecture for Our Project (Big Diagram)](lecture-4.4-project-architecture.md)

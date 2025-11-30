# Lecture 3.5 – Online vs Batch ML Systems (Where Your Work Fits)

---

## Two Ways to Serve Predictions

When you deploy an ML model, there are two main patterns:

1. **Online (Real-time)**: Model responds to individual requests as they come
2. **Batch (Offline)**: Model processes large volumes of data periodically

Understanding the difference is crucial because it affects every decision you make: infrastructure, latency requirements, scaling, and cost.

---

## Online (Real-Time) Serving

### What It Is

The model is deployed as a service. When a request comes in, the model makes a prediction and returns it immediately.

```
User Action → Request → Model → Prediction → Response
     ↓                                           ↓
  "Add to cart"                        "Show recommendation"
  
Latency: milliseconds
```

### Examples

- **Fraud detection**: Evaluate a transaction as it happens
- **Recommendation**: Show products when user opens the page
- **Search ranking**: Order search results in real-time
- **Content moderation**: Flag inappropriate content on upload
- **Chatbots**: Respond to user messages instantly

### Characteristics

| Aspect | Online Serving |
|--------|----------------|
| Latency | Milliseconds (10-200ms typical) |
| Volume | High throughput, one prediction at a time |
| Data | Features computed in real-time or fetched from cache |
| Infrastructure | Always-on service (API) |
| Scaling | Horizontal (more instances for more load) |
| Cost | Continuous compute costs |

### Architecture

```
                    ┌──────────────┐
                    │   Load       │
                    │   Balancer   │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌───────────┐    ┌───────────┐    ┌───────────┐
   │  Model    │    │  Model    │    │  Model    │
   │ Instance 1│    │ Instance 2│    │ Instance 3│
   └───────────┘    └───────────┘    └───────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                    ┌──────────────┐
                    │   Feature    │
                    │    Store     │
                    └──────────────┘
```

### Challenges

1. **Latency constraints**: Must respond fast
2. **Feature computation**: Features need to be available instantly
3. **High availability**: Service must always be up
4. **Scaling**: Must handle traffic spikes
5. **Cost**: Always-on infrastructure

---

## Batch Serving

### What It Is

The model runs on a schedule, processing large amounts of data at once. Results are stored and used later.

```
Scheduler triggers → Load all data → Model predicts all → Store results
        ↓                                                      ↓
    "Every night"                                    "Results in database"
  
Latency: hours (acceptable because results are pre-computed)
```

### Examples

- **Churn prediction**: Score all customers weekly
- **Lead scoring**: Rank all leads nightly
- **Propensity modeling**: Calculate purchase likelihood daily
- **Risk scoring**: Evaluate loan portfolios monthly
- **Report generation**: Summarize trends weekly

### Characteristics

| Aspect | Batch Serving |
|--------|---------------|
| Latency | Hours to days (OK because pre-computed) |
| Volume | Large volumes at once |
| Data | Full dataset access |
| Infrastructure | Scheduled job (spin up, run, spin down) |
| Scaling | Vertical (bigger machine) or parallel |
| Cost | Pay only when running |

### Architecture

```
┌──────────────┐
│   Scheduler  │  (Airflow, cron, etc.)
└──────┬───────┘
       │ Triggers nightly
       ▼
┌──────────────┐      ┌──────────────┐
│   Load Data  │ ───► │   Run Model  │
│ from Source  │      │  (bulk)      │
└──────────────┘      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │Store Results │
                      │ to Database  │
                      └──────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │  App reads   │
                      │  from DB     │
                      └──────────────┘
```

### Challenges

1. **Data freshness**: Results are only as fresh as the last run
2. **Processing time**: Large datasets take time
3. **Failure recovery**: If batch fails, what happens?
4. **Storage**: Need to store all predictions
5. **Scheduling**: Coordinate with data availability

---

## Comparing the Two

| Factor | Online | Batch |
|--------|--------|-------|
| When predictions made | On request | On schedule |
| Latency requirement | Milliseconds | Hours OK |
| Infrastructure | Always running | Run periodically |
| Scaling | More instances | Bigger machine |
| Feature computation | Real-time | Pre-computed |
| Cost model | Continuous | Periodic |
| Use case | Real-time decisions | Pre-computed scores |

---

## When to Use Which

### Use Online When:

✓ Decision must be made immediately
✓ Context changes with each request
✓ Can't pre-compute (too many combinations)
✓ Freshness is critical

Examples:
- Fraud detection at checkout (can't wait)
- Search results (depends on query)
- Chat response (immediate interaction)

### Use Batch When:

✓ Predictions can be pre-computed
✓ Results don't change rapidly
✓ Processing large volumes
✓ Cost matters (don't need always-on)

Examples:
- Churn scores (customers don't change hourly)
- Lead scoring (updated daily is fine)
- Report generation (periodic is OK)

### Decision Framework

```
                    Is real-time decision required?
                              │
              ┌───────────────┴───────────────┐
              │ Yes                           │ No
              ▼                               ▼
        Use Online                  Can results be pre-computed?
                                              │
                              ┌───────────────┴───────────────┐
                              │ Yes                           │ No
                              ▼                               ▼
                         Use Batch                    Consider Near-Real-Time
```

---

## The Hybrid: Near-Real-Time

Sometimes you need something in between:

### Near-Real-Time (Micro-Batch)

- Process data in small batches frequently
- More fresh than batch, less costly than online
- Example: Process events every 5 minutes

```
Events arrive → Buffer (5 min) → Batch process → Store
                                                   ↓
                                           Results available
                                         (slight delay, not instant)
```

Use cases:
- Dashboard metrics
- Anomaly detection on logs
- Aggregated analytics

---

## Churn Prediction: Which Pattern?

For our course project, which should we use?

**Analysis**:
- Customers don't churn instantly—it's a gradual process
- Weekly scoring is sufficient for intervention
- Processing thousands of customers at once
- Cost efficiency matters

**Decision**: Batch serving

**How it will work**:
1. Every Sunday night: Run batch job
2. Load all customer features
3. Score all customers
4. Store predictions in database
5. Monday morning: Marketing team reviews high-risk customers

We'll also build an online API for demonstration, but batch is the primary use case.

---

## Infrastructure Differences

### Online Infrastructure

```yaml
# Kubernetes deployment for online serving
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-model-api
spec:
  replicas: 3  # Multiple instances for availability
  template:
    spec:
      containers:
      - name: model-api
        image: churn-model:v1
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
        ports:
        - containerPort: 8000
---
# Service to load balance
apiVersion: v1
kind: Service
metadata:
  name: churn-model-api
spec:
  selector:
    app: churn-model-api
  ports:
  - port: 80
    targetPort: 8000
```

### Batch Infrastructure

```yaml
# Kubernetes job for batch serving
apiVersion: batch/v1
kind: Job
metadata:
  name: churn-batch-scoring
spec:
  template:
    spec:
      containers:
      - name: batch-scorer
        image: churn-batch:v1
        resources:
          requests:
            memory: "4Gi"  # More memory for batch
            cpu: "2000m"
        env:
        - name: INPUT_PATH
          value: "s3://bucket/customers.parquet"
        - name: OUTPUT_PATH
          value: "s3://bucket/predictions/"
      restartPolicy: Never
  backoffLimit: 3
```

---

## Cost Comparison

Let's do some rough math:

### Online Serving (24/7)

```
3 instances × $0.10/hour × 24 hours × 30 days = $216/month

Plus:
- Load balancer: ~$20/month
- Feature store: ~$50/month
- Monitoring: ~$30/month

Total: ~$316/month
```

### Batch Serving (Weekly)

```
1 large instance × $0.50/hour × 2 hours × 4 weeks = $4/month

Plus:
- Scheduler (shared): ~$5/month
- Storage: ~$10/month

Total: ~$19/month
```

Batch is dramatically cheaper when it fits your use case.

---

## Recap

Two main serving patterns:

**Online (Real-Time)**:
- Predictions on demand
- Millisecond latency
- Always-on infrastructure
- Higher cost
- Use when: Immediate decisions required

**Batch (Offline)**:
- Predictions on schedule
- Pre-computed results
- Run periodically
- Lower cost
- Use when: Can pre-compute, freshness less critical

**Near-Real-Time**: Micro-batching as middle ground

For churn prediction: Batch is the right choice.

---

## What's Next

Now let's look at what MLOps is responsible for at each stage of the ML lifecycle. This will clarify your role.

---

**Next Lecture**: [3.6 – MLOps Responsibilities in Each Lifecycle Stage](lecture-3.6-mlops-responsibilities.md)

# Lecture 4.1 – Defining Our Use Case (Customer Churn / Loan Default / Sales Forecast)

---

## Time to Build Something Real

We've covered the theory. Now let's apply it.

Throughout the rest of this course, we'll build a complete MLOps system. Not a toy example—a real system you could deploy in a company.

Let's define our project.

---

## The Use Case: Customer Churn Prediction

### What Is Churn?

Churn is when customers stop using your product or service.

- For a subscription business: cancel their subscription
- For an app: stop logging in
- For a bank: close their account
- For e-commerce: stop purchasing

Churn is expensive. Acquiring a new customer costs 5-25x more than retaining an existing one.

### Why Churn Prediction?

If we can predict who's about to churn, we can intervene:
- Offer a discount
- Have customer success reach out
- Address their concerns
- Improve their experience

A good churn model pays for itself many times over.

---

## Our Scenario

**Company**: TechFlow (fictional B2B SaaS company)

**Product**: Project management software (think: simplified Jira)

**Business model**: Monthly subscriptions ($50/month per seat)

**The problem**: 6% monthly churn rate

**The math**:
- 10,000 customers
- 6% churn = 600 customers lost per month
- $50/seat × average 5 seats = $250/customer
- $250 × 600 = $150,000 lost revenue per month

**The goal**: Reduce churn by identifying at-risk customers early

---

## Defining the ML Problem

Let's apply our framing from Lecture 3.1.

### Step 1: Business Outcome

**What does success look like?**

- Reduce monthly churn from 6% to 5%
- Retain 100 additional customers per month
- Save ~$25,000/month in revenue
- ROI: Worth investing in this project

### Step 2: The Decision

**What action will be taken?**

When we identify a high-risk customer:
1. Customer Success team reviews the account
2. They reach out with personalized engagement
3. Offer retention incentives if appropriate
4. Address specific concerns

**Without prediction**: React to customers after they request cancellation (too late)
**With prediction**: Proactively engage before they decide to leave

### Step 3: The Prediction Target

**What exactly should the model predict?**

> "Predict the probability that a customer will churn in the next 30 days"

Why 30 days?
- Enough time to intervene
- Recent enough to be actionable
- Matches our customer success workflow

**Output**: Probability score (0 to 1)
**Threshold**: Flag customers with probability > 0.7

### Step 4: Timeline

**When do we need predictions?**

- **Frequency**: Weekly (every Monday morning)
- **Volume**: ~10,000 customers scored
- **Latency**: Batch processing OK (not real-time)
- **Freshness**: Last week's data is acceptable

### Step 5: Success Metrics

**Model metrics**:
- Precision ≥ 80%: When we say someone will churn, we're right 80% of the time
- Recall ≥ 70%: We catch 70% of actual churners
- Why these numbers? Balance between catching churners and not overwhelming Customer Success

**Business metrics**:
- Reduce churn rate by 1 percentage point (from 6% to 5%)
- ROI positive within 3 months

---

## Problem Definition Document

Let's formalize this:

```markdown
# ML Problem Definition: Customer Churn Prediction

## Overview
Build a model to predict which customers are likely to churn in the next 30 days,
enabling proactive retention efforts.

## Business Context
- Company: TechFlow (B2B SaaS)
- Problem: High churn rate (6% monthly)
- Impact: $150,000/month in lost revenue
- Current approach: Reactive (respond after cancellation request)
- Desired approach: Proactive (identify at-risk customers early)

## Prediction Task
- **Type**: Binary classification
- **Target**: Churn within 30 days (yes/no)
- **Output**: Probability score (0-1)
- **Threshold**: 0.7 (flag as high risk)

## Operational Requirements
- **Frequency**: Weekly batch scoring (Monday mornings)
- **Volume**: ~10,000 customers per batch
- **Latency**: Overnight processing acceptable
- **SLA**: Predictions available by 8 AM Monday

## Success Criteria

### Model Metrics
| Metric | Threshold | Notes |
|--------|-----------|-------|
| Precision | ≥ 80% | Minimize false positives |
| Recall | ≥ 70% | Catch most churners |
| AUC-ROC | ≥ 0.85 | Overall discrimination |

### Business Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Churn reduction | 1 percentage point | Compare pre/post |
| Retained customers | 100/month | Track saves |
| ROI | Positive in 3 months | Revenue saved vs. cost |

## Stakeholders
- **Owner**: VP of Customer Success
- **Users**: Customer Success team (5 people)
- **Technical**: Data Science + MLOps + Data Engineering

## Constraints
- Must be explainable (CSMs need to understand why)
- Cannot use PII in predictions (privacy compliance)
- Budget: 2 Data Scientists, 1 MLOps engineer, 3 months
```

---

## Alternative Use Cases

While we'll focus on churn, here are other use cases that follow similar patterns:

### Loan Default Prediction

```
Business: Bank
Problem: Some borrowers default on loans
Prediction: Probability of default in next 90 days
Decision: Adjust credit limits, increase monitoring
```

### Sales Forecasting

```
Business: Retail
Problem: Need to plan inventory
Prediction: Units sold per product per store per day
Decision: Order inventory, plan promotions
```

### Lead Scoring

```
Business: B2B Sales
Problem: Too many leads, limited sales capacity
Prediction: Probability of conversion
Decision: Prioritize sales outreach
```

All these follow the same MLOps patterns we'll learn.

---

## Why This Use Case Is Good for Learning

The churn prediction project is ideal because:

1. **Realistic complexity**: Real data challenges, real business constraints
2. **Covers all MLOps**: Data pipelines, training, serving, monitoring
3. **Batch serving**: Most common pattern, easier to start with
4. **Clear ROI**: Easy to measure business impact
5. **Well-documented**: Many resources and examples available
6. **Transferable skills**: Patterns apply to many other use cases

---

## What We'll Build

Here's the system we'll build:

```
┌────────────────────────────────────────────────────────────────────┐
│                    Customer Churn Prediction System                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Data Layer                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │  Customer   │    │   Usage     │    │   Support   │            │
│  │    DB       │───►│    Logs     │───►│   Tickets   │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│         │                  │                  │                    │
│         └──────────────────┴──────────────────┘                    │
│                            │                                        │
│                            ▼                                        │
│  Feature Engineering       ┌─────────────────┐                     │
│                            │  Feature Store  │                     │
│                            └────────┬────────┘                     │
│                                     │                               │
│  Training Pipeline                  ▼                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │   Train     │───►│   MLflow    │───►│   Model     │            │
│  │   Model     │    │  Tracking   │    │  Registry   │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│                                               │                     │
│  Serving                                      ▼                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │   Batch     │◄───│   Load      │◄───│   Model     │            │
│  │   Scoring   │    │   Model     │    │  Artifact   │            │
│  └──────┬──────┘    └─────────────┘    └─────────────┘            │
│         │                                                          │
│         ▼                                                          │
│  ┌─────────────┐    ┌─────────────┐                               │
│  │ Predictions │───►│  Dashboard  │                               │
│  │    DB       │    │  (Grafana)  │                               │
│  └─────────────┘    └─────────────┘                               │
│                                                                     │
│  Monitoring                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │   Drift     │    │   Model     │    │   Alerts    │            │
│  │ Detection   │───►│  Metrics    │───►│  (Slack)    │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Recap

Our use case: **Customer Churn Prediction for TechFlow**

- **Problem**: High churn rate costing $150K/month
- **Prediction**: Probability of churn in next 30 days
- **Decision**: Proactive customer success outreach
- **Serving**: Weekly batch scoring
- **Success**: Reduce churn by 1 percentage point

This is a realistic, complete use case that covers all MLOps concepts.

---

## What's Next

Now let's define the business requirements and success metrics in more detail.

---

**Next Lecture**: [4.2 – Business Requirements & Success Metrics (How Will We Know It Works?)](lecture-4.2-business-requirements.md)

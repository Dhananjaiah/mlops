# Lecture 4.2 – Business Requirements & Success Metrics (How Will We Know It Works?)

---

## Why Requirements Matter

I've seen projects fail not because the model was bad, but because no one agreed on what "good" meant.

Data scientist says: "The model has 92% accuracy!"
Business says: "But our churn rate didn't improve..."
Everyone's confused.

Let's avoid this by defining clear requirements upfront.

---

## Types of Requirements

We need to capture three types:

1. **Business requirements**: What business outcome do we need?
2. **Functional requirements**: What should the system do?
3. **Non-functional requirements**: How should the system behave?

---

## Business Requirements

### Primary Goal

> Reduce customer churn rate from 6% to 5% monthly.

This is the north star. Everything we do serves this goal.

### Secondary Goals

1. **Enable proactive retention**: Give Customer Success team actionable insights
2. **Prioritize efforts**: Focus on highest-risk customers first
3. **Measure intervention effectiveness**: Track which save attempts work

### Business Constraints

1. **Budget**: 3 months of development, 2 DS + 1 MLOps engineer
2. **Timeline**: MVP in production within 2 months
3. **Resources**: Customer Success team can handle 200 outreach calls/week max

### Stakeholder Needs

| Stakeholder | Need |
|-------------|------|
| VP Customer Success | Dashboard showing at-risk customers |
| Customer Success Managers | Weekly list of customers to contact |
| Finance | ROI report showing revenue saved |
| Data Science | Model performance metrics |
| Engineering | Integration with CRM system |

---

## Functional Requirements

What the system must DO.

### Core Functionality

| ID | Requirement |
|----|-------------|
| FR-1 | System SHALL generate churn probability for all active customers weekly |
| FR-2 | System SHALL classify customers as High Risk (>70%), Medium (40-70%), Low (<40%) |
| FR-3 | System SHALL provide top 200 highest-risk customers to CS team |
| FR-4 | System SHALL explain key factors for each prediction |
| FR-5 | System SHALL track prediction history for each customer |

### Data Requirements

| ID | Requirement |
|----|-------------|
| FR-6 | System SHALL use customer data from the past 90 days |
| FR-7 | System SHALL include usage, support, and billing data |
| FR-8 | System SHALL handle missing data gracefully |
| FR-9 | System SHALL process new customers (< 30 days) separately |

### Output Requirements

| ID | Requirement |
|----|-------------|
| FR-10 | System SHALL write predictions to CS dashboard by 8 AM Monday |
| FR-11 | System SHALL include risk score, risk tier, and top 3 factors |
| FR-12 | System SHALL flag data quality issues |

---

## Non-Functional Requirements

How the system must BEHAVE.

### Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Batch processing time | < 2 hours for 10,000 customers |
| NFR-2 | Model latency (if online) | < 100ms per prediction |
| NFR-3 | Throughput (if online) | 100 requests/second |

### Reliability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-4 | System availability | 99.5% uptime |
| NFR-5 | Data freshness | Predictions based on data < 7 days old |
| NFR-6 | Recovery time | < 4 hours after failure |

### Scalability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-7 | Customer growth | Handle 100K customers without re-architecture |
| NFR-8 | Feature growth | Support 100+ features |

### Security

| ID | Requirement |
|----|-------------|
| NFR-9 | No PII in model features |
| NFR-10 | Access control on predictions |
| NFR-11 | Audit logging for all predictions |

### Maintainability

| ID | Requirement |
|----|-------------|
| NFR-12 | Model retraining within 4 hours |
| NFR-13 | Rollback capability within 30 minutes |
| NFR-14 | Documentation for all components |

---

## Success Metrics

How do we know the project succeeded?

### Model Performance Metrics

| Metric | Definition | Target | Why |
|--------|------------|--------|-----|
| Precision | TP / (TP + FP) | ≥ 80% | Don't waste CS time on non-churners |
| Recall | TP / (TP + FN) | ≥ 70% | Catch most actual churners |
| AUC-ROC | Area under ROC curve | ≥ 0.85 | Overall discrimination ability |
| F1 Score | Harmonic mean of P and R | ≥ 75% | Balanced measure |

### Operational Metrics

| Metric | Definition | Target | Why |
|--------|------------|--------|-----|
| Processing time | Time to score all customers | < 2 hours | Meet Monday deadline |
| Success rate | % of runs completing | > 99% | Reliable operations |
| Data quality | % of valid input records | > 95% | Trustworthy predictions |

### Business Metrics

| Metric | Definition | Target | Timeline |
|--------|------------|--------|----------|
| Churn rate | % customers leaving per month | 5% (down from 6%) | 3 months post-launch |
| Save rate | % of flagged customers retained | > 30% | Monthly |
| Revenue saved | $ from retained customers | $25,000/month | Monthly |
| ROI | Revenue saved / project cost | > 200% | 6 months |

---

## Measurement Plan

How will we actually measure these?

### Model Metrics

```python
# Tracked automatically in MLflow
- Log precision, recall, AUC after each training run
- Compare against baseline model
- Alert if metrics drop below threshold
```

### Operational Metrics

```python
# Tracked via monitoring (Prometheus/Grafana)
- Pipeline duration (histogram)
- Success/failure counts (counter)
- Data quality scores (gauge)
```

### Business Metrics

This is trickier. We need to:

1. **Track predictions**: Log every prediction with timestamp
2. **Track outcomes**: Did the customer actually churn? (30 days later)
3. **Track interventions**: Did CS contact them? What was the result?

```sql
-- Example: Calculate actual vs predicted
SELECT 
    date_predicted,
    COUNT(*) as total_flagged,
    SUM(CASE WHEN actually_churned = 0 THEN 1 ELSE 0 END) as saved,
    SUM(CASE WHEN cs_contacted = 1 THEN 1 ELSE 0 END) as contacted
FROM predictions p
JOIN outcomes o ON p.customer_id = o.customer_id
WHERE risk_tier = 'HIGH'
GROUP BY date_predicted;
```

### A/B Testing (Optional)

For rigorous measurement:
- Randomly split high-risk customers
- Group A: CS outreach (treatment)
- Group B: No special outreach (control)
- Compare churn rates

This proves the model + intervention works, not just the model.

---

## Baseline Comparison

What are we comparing against?

### Current State (Baseline)

- **No prediction model**: CS reacts to cancellation requests
- **Churn rate**: 6% monthly
- **Save rate**: 10% (only catch customers actively complaining)

### Simple Baseline Model

- **Rule-based**: Flag customers with no login in 14 days
- **Precision**: ~50% (lots of false positives)
- **Recall**: ~40% (misses many churners)

### Our Target

- **ML model**: Predict based on multiple signals
- **Precision**: ≥ 80%
- **Recall**: ≥ 70%
- **Churn rate improvement**: 1 percentage point

---

## Success Criteria Summary

| Category | Metric | Target | Measurement |
|----------|--------|--------|-------------|
| Model | Precision | ≥ 80% | MLflow |
| Model | Recall | ≥ 70% | MLflow |
| Model | AUC | ≥ 0.85 | MLflow |
| Operations | Processing time | < 2 hours | Prometheus |
| Operations | Success rate | > 99% | Prometheus |
| Business | Churn reduction | 1 point | Monthly report |
| Business | ROI | > 200% | Quarterly review |

---

## Go/No-Go Criteria

Before deploying to production, we need:

### Must Have (Blockers)

- [ ] Model precision ≥ 80%
- [ ] Model recall ≥ 70%
- [ ] Processing completes in < 2 hours
- [ ] Integration with CS dashboard working
- [ ] No PII in predictions
- [ ] Stakeholder sign-off

### Should Have

- [ ] Explainability for predictions
- [ ] Monitoring dashboard
- [ ] Alerting configured
- [ ] Documentation complete

### Nice to Have

- [ ] A/B testing framework
- [ ] Automated retraining
- [ ] Advanced explainability (SHAP values)

---

## Recap

Clear requirements prevent project failure:

**Business requirements**:
- Reduce churn from 6% to 5%
- Enable proactive retention
- ROI positive in 3 months

**Functional requirements**:
- Weekly batch scoring
- Risk tiers (high/medium/low)
- Explainable predictions

**Non-functional requirements**:
- < 2 hours processing
- 99.5% availability
- Secure and auditable

**Success metrics**:
- Model: Precision ≥ 80%, Recall ≥ 70%
- Operations: 99% success rate
- Business: 1 point churn reduction

---

## What's Next

Now let's talk about where the data comes from and establish data contracts.

---

**Next Lecture**: [4.3 – Data Sources & Data Contracts (Who Owns the Data?)](lecture-4.3-data-sources-contracts.md)

# Lecture 4.6 – What We Will Automate vs What Will Stay Manual

---

## Automation Philosophy

Not everything should be automated. 

The goal isn't to automate everything—it's to automate the right things.

In this lecture, we'll decide what to automate in our churn prediction system and what intentionally stays manual.

---

## The Automation Spectrum

Think of automation as a spectrum:

```
Fully Manual          Partially Automated          Fully Automated
     │                        │                          │
     ▼                        ▼                          ▼
Run script by hand   Trigger with one command    Runs without humans
Human makes decisions   Human approves automated    No human in the loop
Error-prone               Safer, faster              Risky if unchecked
```

Different components belong at different points.

---

## Our Automation Decisions

Let's go through each component:

### Data Ingestion

**Decision: Fully Automated ✓**

```
┌────────────────────────────────────────────────────────┐
│  Daily Data Ingestion (Automated)                      │
│                                                        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│  │ Extract │───►│Validate │───►│  Load   │           │
│  │  Data   │    │  Data   │    │   DW    │           │
│  └─────────┘    └─────────┘    └─────────┘           │
│                                                        │
│  Trigger: Schedule (daily at 2 AM)                    │
│  Human: None (alerts on failure)                      │
└────────────────────────────────────────────────────────┘
```

**Why automate?**
- Runs daily, same steps
- No decisions required
- Failure handling defined

**What stays manual?**
- Schema changes (requires code update)
- New data source onboarding
- Debugging failures

### Data Validation

**Decision: Fully Automated ✓**

```
Automated checks:
- Schema validation
- Null checks
- Range checks
- Freshness checks
- Row count checks

If fail:
- Alert team
- Don't proceed with training
- Log issue for review
```

**Why automate?**
- Same checks every time
- Fast feedback
- Consistent quality

### Feature Engineering

**Decision: Automated Execution, Manual Design ✓**

```
┌────────────────────────────────────────────────────────┐
│  Feature Pipeline (Automated Execution)               │
│                                                        │
│  MANUAL: Design features                              │
│          │                                             │
│          ▼                                             │
│  AUTOMATED: Execute feature pipeline                  │
│  ┌─────────────────────────────────────────────┐     │
│  │ Raw Data → Transform → Engineer → Store      │     │
│  └─────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────┘
```

**Why mixed?**
- Feature design requires human judgment
- Feature computation should be reproducible
- New features need manual testing first

### Model Training

**Decision: Automated with Human Trigger ◐**

```
┌────────────────────────────────────────────────────────┐
│  Training Pipeline                                     │
│                                                        │
│  TRIGGER:                                              │
│  - Manual: Data scientist initiates                   │
│  - Scheduled: Weekly retrain                          │
│  - Alert: Drift detected                              │
│                                                        │
│  EXECUTION: Fully automated                            │
│  ┌─────────────────────────────────────────────┐     │
│  │ Load Data → Train → Evaluate → Register      │     │
│  └─────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────┘
```

**Why mixed?**
- Training is compute-intensive
- Want control over when it runs
- Automatic retraining can spiral costs

### Model Evaluation

**Decision: Automated Checks, Manual Review ◐**

```
AUTOMATED:
- Run test suite
- Calculate metrics
- Compare to baseline
- Check thresholds
- Generate report

MANUAL:
- Review evaluation report
- Approve/reject for promotion
- Investigate anomalies
```

**Why mixed?**
- Automated checks catch obvious issues
- Human review catches subtle problems
- Approval gate prevents bad models in production

### Model Promotion

**Decision: Human Approval Required ✗**

```
┌────────────────────────────────────────────────────────┐
│  Model Promotion (Manual Approval)                     │
│                                                        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│  │ Staging │───►│ APPROVE │───►│Production│           │
│  │         │    │ (Human) │    │         │           │
│  └─────────┘    └─────────┘    └─────────┘           │
│                                                        │
│  Requires:                                            │
│  - Evaluation report reviewed                         │
│  - Stakeholder sign-off                               │
│  - Change ticket approved                             │
└────────────────────────────────────────────────────────┘
```

**Why manual?**
- High risk decision
- Need accountability
- Regulatory compliance
- Stakeholder visibility

### Batch Scoring

**Decision: Fully Automated ✓**

```
┌────────────────────────────────────────────────────────┐
│  Weekly Scoring (Automated)                            │
│                                                        │
│  Trigger: Sunday 2 AM                                 │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  Load    │─►│  Score   │─►│  Write   │           │
│  │  Model   │  │ All Cust │  │ Results  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                        │
│  No human intervention unless failure                 │
└────────────────────────────────────────────────────────┘
```

**Why automate?**
- Same process every week
- Must complete by Monday
- No decisions needed
- Reliable and predictable

### Monitoring

**Decision: Automated Collection, Manual Response ◐**

```
AUTOMATED:
- Collect metrics (continuous)
- Calculate drift scores (daily)
- Generate dashboards (continuous)
- Send alerts (on threshold)

MANUAL:
- Investigate alerts
- Decide on action
- Trigger retraining if needed
- Update thresholds
```

**Why mixed?**
- Data collection must be continuous
- Response requires human judgment
- False positive alerts need human triage

### Rollback

**Decision: Human Initiated, Automated Execution ◐**

```
┌────────────────────────────────────────────────────────┐
│  Rollback Process                                      │
│                                                        │
│  HUMAN: Decides to rollback                           │
│         │                                              │
│         ▼                                              │
│  AUTOMATED: Execute rollback                          │
│  ┌─────────────────────────────────────────────┐     │
│  │ Stop current → Deploy previous → Verify      │     │
│  └─────────────────────────────────────────────┘     │
│                                                        │
│  Human calls: make rollback MODEL=v1.2.0              │
└────────────────────────────────────────────────────────┘
```

**Why mixed?**
- Rollback is serious decision
- Execution should be fast and reliable
- Human accountable for decision

---

## Automation Summary Table

| Component | Automation Level | Trigger | Human Role |
|-----------|------------------|---------|------------|
| Data ingestion | Full | Schedule | Debug failures |
| Data validation | Full | Auto | Review alerts |
| Feature engineering | Partial | Schedule | Design features |
| Model training | Partial | Manual/Schedule | Initiate, monitor |
| Model evaluation | Partial | Auto | Review, approve |
| Model promotion | Manual | Human | Approve |
| Batch scoring | Full | Schedule | Debug failures |
| Online serving | Full | On-demand | Monitor |
| Monitoring | Partial | Continuous | Respond to alerts |
| Rollback | Partial | Human | Decide to rollback |

---

## What We'll Build

Given these decisions, here's what we're building:

### Automated Pipelines

1. **Data ingestion pipeline** (Airflow DAG)
   - Daily schedule
   - Validation gates
   - Alerting on failure

2. **Feature pipeline** (Airflow DAG)
   - Triggered after ingestion
   - Builds feature table
   - Version controlled

3. **Training pipeline** (Airflow DAG)
   - Manual or scheduled trigger
   - Full MLflow tracking
   - Auto-registration to staging

4. **Scoring pipeline** (Airflow DAG)
   - Weekly schedule
   - Loads production model
   - Writes predictions

### Manual Processes

1. **Model approval workflow**
   - Review in MLflow
   - Sign-off checklist
   - Promotion command

2. **Incident response**
   - Runbook documentation
   - On-call rotation
   - Escalation path

3. **Feature development**
   - Hypothesis
   - Implementation
   - Testing
   - Review

---

## Automation ROI

Let's think about the value:

### High ROI Automation

| Task | Frequency | Time Manual | Time Automated | ROI |
|------|-----------|-------------|----------------|-----|
| Data ingestion | Daily | 30 min | 0 min | Very High |
| Data validation | Daily | 20 min | 0 min | Very High |
| Batch scoring | Weekly | 1 hour | 0 min | High |
| Training execution | Weekly | 2 hours | 10 min | High |

### Lower ROI Automation

| Task | Frequency | Time Manual | Why Not Automate |
|------|-----------|-------------|------------------|
| Feature design | Monthly | 8 hours | Requires creativity |
| Model approval | Weekly | 30 min | Needs accountability |
| Incident response | Rare | Variable | Requires judgment |

---

## When to Revisit

Automation decisions aren't permanent. Revisit when:

- **Volume increases**: Manual can't keep up
- **Frequency increases**: Daily becomes hourly
- **Team grows**: Need standardization
- **Errors happen**: Humans make mistakes
- **Compliance requires**: Audit trail needed

---

## Section 4 Complete! 🎉

You now have a complete picture of our project:

- **Use case**: Customer churn prediction
- **Requirements**: Reduce churn by 1 point
- **Data sources**: Customer, usage, support, billing
- **Architecture**: End-to-end ML system
- **Enterprise fit**: Part of larger ecosystem
- **Automation**: Right balance of auto vs manual

---

**Next Section**: [Section 5 – Data Engineering Basics for MLOps](../section05-data-engineering-basics/lecture-5.1-data-types-storage.md)

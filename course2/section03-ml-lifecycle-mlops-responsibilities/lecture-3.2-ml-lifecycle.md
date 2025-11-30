# Lecture 3.2 – The Classic ML Lifecycle (CRISP-DM Style)

---

## The Map of ML Projects

Before we dive deeper into MLOps, let's understand the overall ML lifecycle.

CRISP-DM (Cross-Industry Standard Process for Data Mining) has been around since the 1990s. It's old, but it's still the best framework for understanding how ML projects flow.

Let me walk you through it with modern examples.

---

## The Six Phases

CRISP-DM has six phases:

```
    ┌─────────────────────────────────────────┐
    │                                         │
    ▼                                         │
┌───────────────┐      ┌───────────────┐      │
│   Business    │ ───► │     Data      │      │
│ Understanding │      │ Understanding │      │
└───────────────┘      └───────────────┘      │
                              │               │
                              ▼               │
                       ┌───────────────┐      │
                       │     Data      │      │
                       │  Preparation  │      │
                       └───────────────┘      │
                              │               │
                              ▼               │
                       ┌───────────────┐      │
                       │   Modeling    │      │
                       └───────────────┘      │
                              │               │
                              ▼               │
                       ┌───────────────┐      │
                       │  Evaluation   │      │
                       └───────────────┘      │
                              │               │
                              ▼               │
                       ┌───────────────┐      │
                       │  Deployment   │──────┘
                       └───────────────┘
                              │
                              ▼
                        Feedback Loop
                      (Back to any phase)
```

Let me explain each phase.

---

## Phase 1: Business Understanding

**What happens**: Understand what problem we're solving and why.

**Key activities**:
- Define business objectives
- Assess the situation (resources, constraints, risks)
- Determine data mining goals
- Produce a project plan

**Deliverables**:
- Problem definition document
- Success criteria
- Project timeline

**Example for Churn**:
```
Objective: Reduce customer churn by 10%
Current state: 5% monthly churn rate, no predictive capability
Success criteria: Identify 70% of churners before they leave
Constraints: Must be ready in 3 months, limited data access
```

**MLOps involvement**: Low. This is mostly business and data science.

---

## Phase 2: Data Understanding

**What happens**: Explore available data and understand its quality.

**Key activities**:
- Collect initial data
- Describe data (volume, types, statistics)
- Explore data (visualizations, patterns)
- Verify data quality

**Deliverables**:
- Data description report
- Data quality report
- Initial insights

**Example for Churn**:
```
Data sources:
- Customer table: 100K customers, demographics, signup date
- Usage logs: 500M events, last 12 months, user actions
- Support tickets: 50K tickets, categories, resolution
- Payment history: All transactions

Quality issues:
- 15% missing email addresses
- Usage logs have duplicate events
- Support ticket categories inconsistent before 2023
```

**MLOps involvement**: Moderate. Setting up data pipelines starts here.

---

## Phase 3: Data Preparation

**What happens**: Transform raw data into features the model can use.

**Key activities**:
- Select relevant data
- Clean data (missing values, outliers, errors)
- Construct new features (feature engineering)
- Integrate data from multiple sources
- Format data for modeling

**Deliverables**:
- Cleaned dataset
- Feature definitions
- Data preparation pipeline

**Example for Churn**:
```
Features created:
- days_since_last_login (usage logs)
- avg_sessions_per_week (usage logs)
- support_tickets_last_30_days (support)
- payment_failures_last_90_days (payments)
- contract_months_remaining (customer)

Cleaning:
- Fill missing emails with 'unknown'
- Remove duplicate usage events
- Standardize ticket categories
```

**MLOps involvement**: High. Data pipelines, feature engineering, data versioning.

---

## Phase 4: Modeling

**What happens**: Build and tune machine learning models.

**Key activities**:
- Select modeling techniques
- Generate test design (train/test split, cross-validation)
- Build models
- Assess models (compare algorithms, tune hyperparameters)

**Deliverables**:
- Trained models
- Model comparison results
- Selected model with parameters

**Example for Churn**:
```
Models tested:
- Logistic Regression: AUC 0.75, interpretable
- Random Forest: AUC 0.82, less interpretable
- XGBoost: AUC 0.84, least interpretable
- Neural Network: AUC 0.83, black box

Selected: XGBoost with early stopping
Hyperparameters: max_depth=6, learning_rate=0.1, n_estimators=200
```

**MLOps involvement**: Moderate. Experiment tracking, compute resources.

---

## Phase 5: Evaluation

**What happens**: Validate that the model meets business requirements.

**Key activities**:
- Evaluate results against business criteria
- Review the process (what worked, what didn't)
- Determine next steps (deploy, iterate, abandon)

**Deliverables**:
- Evaluation results
- Review of process
- Go/no-go decision

**Example for Churn**:
```
Model performance:
- Precision at top 20%: 78% (target: 70%) ✓
- Recall: 72% (target: 70%) ✓
- Business simulation: Would catch 720 of 1000 churners

Stakeholder review:
- Marketing approves targeting strategy
- Legal approves use of features (no PII issues)
- Finance approves intervention budget

Decision: Proceed to deployment
```

**MLOps involvement**: Moderate. Validation pipelines, approval workflows.

---

## Phase 6: Deployment

**What happens**: Put the model into production and maintain it.

**Key activities**:
- Plan deployment
- Plan monitoring and maintenance
- Produce final report
- Review project

**Deliverables**:
- Deployed model
- Monitoring dashboard
- Maintenance plan
- Final documentation

**Example for Churn**:
```
Deployment:
- Model packaged as API
- Batch scoring every Sunday night
- Results written to marketing database

Monitoring:
- Track prediction distribution
- Monitor model accuracy (monthly feedback)
- Alert if predictions shift significantly

Maintenance:
- Retrain monthly with new data
- Review feature importance quarterly
- Major review annually
```

**MLOps involvement**: Very High. This is where MLOps shines.

---

## The Iterative Nature

CRISP-DM is not linear. You'll go back and forth:

- **Evaluation reveals data issues** → Back to Data Preparation
- **Modeling shows need for new features** → Back to Data Understanding
- **Deployment reveals business misalignment** → Back to Business Understanding

This is normal. Plan for iteration.

---

## Time Distribution

Typical time spent on each phase:

| Phase | Time | Notes |
|-------|------|-------|
| Business Understanding | 5-10% | Often underestimated |
| Data Understanding | 15-20% | Exploration takes time |
| Data Preparation | 40-50% | The bulk of the work |
| Modeling | 10-15% | Often overestimated |
| Evaluation | 5-10% | Don't rush this |
| Deployment | 10-20% | Often underestimated |

Yes, 40-50% is data preparation. This is reality.

---

## Modern Additions to CRISP-DM

The original CRISP-DM was from 1996. Here's what we add today:

### Continuous Training

Not just train once—retrain regularly:
- Scheduled retraining (weekly, monthly)
- Trigger-based retraining (when drift detected)

### Monitoring

Not just deploy and forget:
- Model performance monitoring
- Data drift detection
- Concept drift detection

### Automation

Manual steps become pipelines:
- Automated data preparation
- Automated training
- Automated deployment

### Version Control

Track everything:
- Code versions
- Data versions
- Model versions
- Configuration versions

This is what MLOps adds to CRISP-DM.

---

## The ML Lifecycle in Practice

Here's what a real project timeline might look like:

```
Week 1-2: Business Understanding
- Stakeholder interviews
- Define success criteria
- Draft project plan

Week 2-4: Data Understanding
- Access data sources
- Exploratory analysis
- Data quality assessment
- Document findings

Week 4-8: Data Preparation
- Build data pipelines
- Feature engineering
- Create training datasets
- Set up data versioning

Week 8-10: Modeling
- Experiment with algorithms
- Hyperparameter tuning
- Track experiments in MLflow
- Select best model

Week 10-11: Evaluation
- Business validation
- Stakeholder review
- Legal/compliance review
- Go/no-go decision

Week 11-14: Deployment
- Package model
- Build serving infrastructure
- Set up monitoring
- Deploy to production

Week 14+: Operations
- Monitor performance
- Collect feedback
- Retrain as needed
- Iterate on features
```

---

## CRISP-DM vs Agile

"But we're agile! We don't do waterfall!"

CRISP-DM isn't waterfall. It's iterative within each phase and between phases.

You can run CRISP-DM in sprints:
- Sprint 1-2: Business + Data Understanding
- Sprint 3-5: Data Preparation (MVP)
- Sprint 6-7: Modeling (baseline)
- Sprint 8: Evaluation + Early Deployment
- Sprint 9+: Iterate and improve

The phases are a framework, not a straitjacket.

---

## Recap

The ML lifecycle (CRISP-DM) has six phases:

1. **Business Understanding** – What problem are we solving?
2. **Data Understanding** – What data do we have?
3. **Data Preparation** – Make data usable (40-50% of time)
4. **Modeling** – Build and tune models
5. **Evaluation** – Does it meet business needs?
6. **Deployment** – Put it in production

Modern additions:
- Continuous training
- Monitoring
- Automation
- Version control

MLOps is heavily involved in phases 3, 4, and especially 6.

---

## What's Next

Now let's talk about where things go wrong. In the next lecture, we'll discuss why "just a notebook" fails in real life.

---

**Next Lecture**: [3.3 – Where Things Break in Real Life (Why "Just a Notebook" Fails)](lecture-3.3-where-things-break.md)

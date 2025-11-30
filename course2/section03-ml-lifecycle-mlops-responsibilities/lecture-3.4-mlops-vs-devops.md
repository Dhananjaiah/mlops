# Lecture 3.4 – MLOps vs DevOps: Same, Similar, Different?

---

## The DevOps Foundation

If you're coming from a software engineering or DevOps background, you might be thinking:

"MLOps looks a lot like DevOps. What's the difference?"

Great question. Let's explore.

---

## What Is DevOps?

DevOps is a set of practices that combines software development (Dev) and IT operations (Ops).

Key DevOps principles:
- **Automation**: Automate repetitive tasks
- **CI/CD**: Continuous Integration and Continuous Delivery
- **Infrastructure as Code**: Manage infrastructure programmatically
- **Monitoring**: Know what's happening in production
- **Collaboration**: Break down silos between teams

DevOps transformed how we build and deploy software.

---

## What Is MLOps?

MLOps applies DevOps principles to machine learning systems.

But ML has unique challenges that require adaptations.

Let me show you the similarities and differences.

---

## What's the Same

### 1. Version Control

**DevOps**: Version control for code (Git)
**MLOps**: Version control for code (Git)

Same!

### 2. CI/CD

**DevOps**: Automated pipelines to build, test, deploy
**MLOps**: Automated pipelines to build, test, deploy

Same concept, different specifics (we'll get to that).

### 3. Infrastructure as Code

**DevOps**: Define infrastructure in Terraform, CloudFormation
**MLOps**: Define infrastructure in Terraform, CloudFormation

Same!

### 4. Monitoring and Alerting

**DevOps**: Monitor application health, set up alerts
**MLOps**: Monitor application health, set up alerts

Same concept, but MLOps adds more (model monitoring).

### 5. Automation Philosophy

**DevOps**: Automate everything possible
**MLOps**: Automate everything possible

Same philosophy.

---

## What's Different

Here's where ML systems diverge from traditional software.

### 1. What's Being Deployed

**DevOps**: 
- Deploy code
- Code changes → redeploy

**MLOps**: 
- Deploy code AND data AND models
- Code changes → redeploy
- Data changes → maybe retrain
- Model changes → redeploy

In ML, you have **three moving parts**: code, data, and models.

### 2. Testing Complexity

**DevOps Testing**:
```
Given input X, expect output Y.
```
Deterministic. You know exactly what the output should be.

**MLOps Testing**:
```
Given input X, expect output Y... probably... most of the time.
```

ML outputs are probabilistic. A model might give slightly different outputs for similar inputs. Testing is harder:
- Data validation tests
- Model performance tests
- Drift detection tests
- Fairness tests

### 3. Continuous Deployment vs Continuous Training

**DevOps**: 
- Continuous Deployment: Code change → Deploy new version

**MLOps**: 
- Continuous Training: Data changes → Retrain model
- Continuous Deployment: New model → Deploy new version

MLOps adds a training step that doesn't exist in traditional DevOps.

```
Traditional DevOps:
Code → Build → Test → Deploy

MLOps:
Code ─────────────────┐
                      ├─→ Train → Test → Package → Deploy
Data (changing) ──────┘
```

### 4. Model Decay

**DevOps**: 
- Code doesn't get worse over time
- If it worked yesterday, it works today

**MLOps**: 
- Models decay over time
- The world changes, but the model doesn't
- What worked last month might not work this month

This is called **model drift** (or data drift / concept drift).

DevOps doesn't have an equivalent. Your JavaScript doesn't slowly get worse.

### 5. Experimentation

**DevOps**: 
- Feature development follows a defined spec
- A/B testing happens at the product level

**MLOps**: 
- Heavy experimentation phase
- Try 50 different models/configurations
- Track all experiments
- Choose the best one

MLOps requires **experiment tracking**—something DevOps doesn't need.

### 6. Data Versioning

**DevOps**: 
- Git versions code
- Database migrations for schema changes
- Data mostly doesn't change (or changes are migrations)

**MLOps**: 
- Git versions code
- DVC (or similar) versions data
- Training data changes regularly
- Need to track which data trained which model

### 7. Specialized Monitoring

**DevOps Monitoring**:
- Is the server up?
- What's the latency?
- What's the error rate?
- How much CPU/memory?

**MLOps Monitoring** (all of the above, plus):
- Is the model accuracy still good?
- Is the input data distribution changing?
- Is the output distribution changing?
- Are predictions fair across groups?

MLOps monitoring is a superset of DevOps monitoring.

---

## Comparison Table

| Aspect | DevOps | MLOps |
|--------|--------|-------|
| Deploy what | Code | Code + Data + Models |
| Version control | Git (code) | Git (code) + DVC (data) + Registry (models) |
| Testing | Unit, integration, E2E | + Data validation, model validation, drift |
| CD | Code → Deploy | Code/Data → Train → Deploy |
| Decay | No | Yes (model drift) |
| Experimentation | Limited | Heavy (experiment tracking) |
| Monitoring | App metrics | + Model metrics, drift |
| Feedback loop | User feedback | + Model performance data |

---

## The MLOps Additions to DevOps

Think of MLOps as DevOps + ML-specific practices:

```
MLOps = DevOps + {
    Data Versioning,
    Experiment Tracking,
    Model Registry,
    Continuous Training,
    Model Monitoring,
    Drift Detection,
    Feature Stores
}
```

### Data Versioning

Track datasets like you track code:
- Which version of data trained which model?
- Can I reproduce training with the same data?
- What changed between data versions?

### Experiment Tracking

Record every experiment:
- Parameters used
- Metrics achieved
- Artifacts produced
- Data used

### Model Registry

Central repository for models:
- Model versions
- Model stages (staging, production)
- Model metadata
- Model lineage

### Continuous Training

Automatically retrain when:
- New data is available
- Performance drops
- Schedule triggers

### Model Monitoring

Watch models in production:
- Prediction distribution
- Feature distribution
- Performance metrics (if labels available)

### Drift Detection

Alert when distributions change:
- Data drift: inputs changed
- Concept drift: relationship between input and output changed

### Feature Stores

Centralized feature management:
- Consistent features across training and serving
- Feature reuse across models
- Feature versioning

---

## Career Implications

If you know DevOps, you're halfway to MLOps:

**Skills that transfer directly**:
- CI/CD pipelines
- Containerization (Docker)
- Orchestration (Kubernetes)
- Infrastructure as Code
- Monitoring and alerting
- Scripting and automation

**Skills you need to add**:
- Basic ML understanding
- Experiment tracking
- Data versioning
- Model monitoring concepts
- Feature engineering awareness

---

## Tools Comparison

| DevOps Tool | MLOps Equivalent |
|-------------|------------------|
| Git | Git |
| GitHub Actions | GitHub Actions (same!) |
| Terraform | Terraform (same!) |
| Docker | Docker (same!) |
| Kubernetes | Kubernetes (same!) |
| Prometheus | Prometheus + Evidently |
| Grafana | Grafana (same!) |
| Jenkins | Jenkins / Kubeflow Pipelines |
| - | MLflow (experiment tracking) |
| - | DVC (data versioning) |
| - | Feature Store (Feast, Tecton) |

Many tools are the same! MLOps adds specialized ML tools on top.

---

## Working Together

In practice, DevOps and MLOps teams work together:

**DevOps/Platform Team**:
- Manages core infrastructure
- Sets up Kubernetes clusters
- Manages CI/CD platform
- Handles networking and security

**MLOps Team**:
- Builds on DevOps foundation
- Adds ML-specific tooling
- Manages model lifecycle
- Monitors model performance

**Collaboration**:
- MLOps uses infrastructure DevOps provides
- DevOps learns ML-specific requirements
- Shared monitoring and alerting
- Joint incident response

---

## Recap

MLOps vs DevOps:

**Same**:
- Version control (Git)
- CI/CD philosophy
- Infrastructure as Code
- Monitoring and alerting
- Automation mindset

**Different**:
- Deploy code + data + models (not just code)
- Testing is harder (probabilistic)
- Models decay (drift)
- Heavy experimentation
- Data versioning required
- ML-specific monitoring

**MLOps = DevOps + ML-specific practices**

If you know DevOps, you have a strong foundation. Add ML knowledge and ML-specific tools.

---

## What's Next

Now let's talk about the two main types of ML systems: online and batch. Understanding this distinction will help you design the right solution.

---

**Next Lecture**: [3.5 – Online vs Batch ML Systems (Where Your Work Fits)](lecture-3.5-online-vs-batch.md)

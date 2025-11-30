# Lecture 4.5 – Where This Project Fits in a Real Company's Stack

---

## Not Building in Isolation

Our churn prediction system doesn't exist in a vacuum. It's part of a larger technology ecosystem.

Understanding this context helps you:
- Know what to leverage (not reinvent)
- Understand integration points
- Navigate organizational complexity

---

## The Typical Enterprise Data Stack

Here's what a real company's data and ML stack might look like:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENTERPRISE DATA & AI PLATFORM                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  APPLICATIONS                                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │  Web App │ │Mobile App│ │   CRM    │ │   ERP    │ │  Admin   │         │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘         │
│       │            │            │            │            │               │
│  ─────┴────────────┴────────────┴────────────┴────────────┴──────         │
│                               │                                            │
│                               ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        API GATEWAY                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                               │                                            │
│       ┌───────────────────────┼───────────────────────┐                   │
│       ▼                       ▼                       ▼                   │
│  ┌──────────┐          ┌──────────┐          ┌──────────┐                 │
│  │ Product  │          │   ML     │          │ Analytics│                 │
│  │ Services │          │ Services │          │ Services │                 │
│  └──────────┘          └────┬─────┘          └──────────┘                 │
│                             │                                              │
│                             │  ← OUR PROJECT LIVES HERE                    │
│                             │                                              │
│  ┌──────────────────────────┴──────────────────────────────────────────┐  │
│  │                        ML PLATFORM                                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │  │
│  │  │  Feature   │ │   Model    │ │ Experiment │ │   Model    │       │  │
│  │  │   Store    │ │  Registry  │ │  Tracking  │ │  Serving   │       │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                               │                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                        DATA PLATFORM                                  │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │ │
│  │  │    Data    │ │    Data    │ │   Data     │ │   Data     │       │ │
│  │  │   Lake     │ │ Warehouse  │ │  Pipelines │ │  Catalog   │       │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                               │                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                       INFRASTRUCTURE                                  │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │ │
│  │  │ Kubernetes │ │  Database  │ │   Object   │ │ Networking │       │ │
│  │  │  Clusters  │ │  Services  │ │   Storage  │ │  & Security│       │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Teams and Their Domains

Different teams own different parts:

### Platform Engineering / DevOps

**They own**:
- Kubernetes clusters
- CI/CD platform
- Networking and security
- Cloud infrastructure

**We depend on them for**:
- Compute resources
- Deployment targets
- Security policies

### Data Engineering

**They own**:
- Data lake and warehouse
- ETL pipelines
- Data catalog
- Data quality

**We depend on them for**:
- Source data
- Data pipelines
- Feature pipelines (sometimes)

### Data Science

**They own**:
- Model development
- Experimentation
- Algorithm selection

**We collaborate on**:
- Experiment tracking
- Model evaluation
- Feature engineering

### ML Platform Team (if exists)

**They own**:
- Feature store
- Model registry
- Serving infrastructure
- ML tooling

**We either ARE this team** or use what they provide.

### Product Engineering

**They own**:
- Product applications
- APIs
- User interfaces

**We integrate with**:
- CRM systems
- Dashboards
- Product features

---

## Integration Points

Our churn prediction system integrates at these points:

### Upstream (We Consume)

| System | What We Get | Integration |
|--------|-------------|-------------|
| Customer DB | Customer data | Read from replica |
| Event Stream | Usage events | Consume from Kafka |
| Data Warehouse | Aggregated data | SQL queries |
| Support System | Ticket data | API/Data warehouse |
| Billing System | Payment data | API/Data warehouse |

### Downstream (We Produce)

| System | What We Provide | Integration |
|--------|-----------------|-------------|
| CS Dashboard | Predictions | Write to DB |
| CRM | Risk scores | API/Batch update |
| Alerting | Model alerts | Prometheus/Slack |
| Analytics | ML metrics | Data warehouse |

### Lateral (We Collaborate)

| Team | Collaboration |
|------|---------------|
| Data Engineering | Data quality, pipelines |
| Platform | Infrastructure, deployment |
| Security | Compliance, access |
| Product | Requirements, integration |

---

## Shared Services We Use

Typical enterprise shared services:

### Authentication & Authorization

- **OIDC/SAML** for user authentication
- **IAM roles** for service accounts
- **RBAC** for access control

We use: Service accounts for pipeline access, RBAC for model registry.

### Secrets Management

- **HashiCorp Vault** or cloud secret managers
- **Kubernetes secrets** for deployment

We use: Database credentials, API keys, model registry tokens.

### Logging & Monitoring

- **Central logging** (ELK, Splunk, CloudWatch)
- **Metrics platform** (Prometheus, Datadog)
- **Alerting system** (PagerDuty, Opsgenie)

We use: Log ML jobs, metrics, alerts.

### Container Registry

- **Private registry** (ECR, GCR, Harbor)
- **Image scanning**

We use: Store model container images.

### CI/CD Platform

- **Pipeline runners** (GitHub Actions, Jenkins, GitLab)
- **Deployment automation**

We use: Build, test, deploy ML code.

---

## What We Build vs What We Use

### Build Ourselves

| Component | Why |
|-----------|-----|
| Training code | Model-specific logic |
| Feature engineering | Domain-specific |
| Serving code | Custom API needs |
| Monitoring dashboards | ML-specific metrics |
| Pipeline DAGs | Our workflow |

### Use Shared Platform

| Component | Why |
|-----------|-----|
| Kubernetes | Standard infra |
| CI/CD runners | Standard DevOps |
| Data warehouse | Shared data platform |
| Secrets management | Security compliance |
| Logging | Centralized ops |

### Depends on Company Maturity

| Component | Early Stage | Mature |
|-----------|-------------|--------|
| Feature store | Build simple | Use platform |
| Model registry | MLflow self-hosted | Central platform |
| Experiment tracking | MLflow self-hosted | Central platform |
| Serving infrastructure | Custom | Standard platform |

---

## Organizational Patterns

How ML fits in organizations:

### Pattern 1: Centralized ML Platform

```
                    ┌─────────────────────┐
                    │   ML Platform Team  │
                    │  (MLOps + ML Eng)   │
                    └─────────┬───────────┘
                              │ Provides
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Team A   │   │ Team B   │   │ Team C   │
        │(DS + PM) │   │(DS + PM) │   │(DS + PM) │
        └──────────┘   └──────────┘   └──────────┘
```

**Pros**: Consistent tooling, expertise sharing
**Cons**: Can be bottleneck, less context

### Pattern 2: Embedded ML

```
┌─────────────────────────────────────────────────┐
│                   Product Team                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │   DS    │ │  MLOps  │ │   SWE   │           │
│  └─────────┘ └─────────┘ └─────────┘           │
└─────────────────────────────────────────────────┘
```

**Pros**: Close to product, fast iteration
**Cons**: Inconsistent practices, duplicated effort

### Pattern 3: Hybrid

```
┌─────────────────────────────────────────────────┐
│              ML Platform Team                    │
│         (Core infra, standards)                  │
└─────────────────────┬───────────────────────────┘
                      │ Provides + Consults
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Team A     │ │   Team B     │ │   Team C     │
│ (DS + MLOps) │ │ (DS + MLOps) │ │ (DS + MLOps) │
└──────────────┘ └──────────────┘ └──────────────┘
```

**Pros**: Balance consistency and autonomy
**Cons**: Coordination complexity

---

## Where Churn Prediction Fits

In our company (TechFlow):

```
Customer Success Domain
├── Churn Prediction (our project)
├── Customer Health Scoring
├── Upsell Recommendations
└── Support Ticket Routing

Uses ML Platform
├── MLflow (shared)
├── Feature Store (shared)
└── Serving Infrastructure (shared)

Uses Data Platform
├── Data Warehouse (shared)
├── ETL Pipelines (shared)
└── Data Catalog (shared)

Uses Infrastructure
├── Kubernetes (shared)
├── CI/CD (shared)
└── Monitoring (shared)
```

---

## Enterprise Considerations

When working in enterprise:

### Compliance

- **Data privacy**: GDPR, CCPA compliance
- **Audit trails**: Who did what, when
- **Model documentation**: Model cards, bias reports

### Security

- **Least privilege**: Only access what's needed
- **Encryption**: Data at rest and in transit
- **Vulnerability scanning**: Container images, dependencies

### Cost

- **Compute costs**: Training, serving
- **Storage costs**: Data, models, logs
- **Chargeback**: Who pays for ML resources?

### Change Management

- **Approval processes**: Model promotion gates
- **Change windows**: When can we deploy?
- **Rollback procedures**: How to revert?

---

## Recap

Our churn prediction project fits into:

**Enterprise layers**:
- Applications (CS dashboard)
- ML Services (our prediction service)
- ML Platform (shared tooling)
- Data Platform (shared data)
- Infrastructure (shared compute)

**We integrate with**:
- Upstream: Data sources
- Downstream: Consumers
- Lateral: Teams

**We build** domain-specific code, **we use** shared platforms.

Different organizational patterns exist; adapt to yours.

---

## What's Next

Finally, let's define what we'll automate and what we'll keep manual in this project.

---

**Next Lecture**: [4.6 – What We Will Automate vs What Will Stay Manual](lecture-4.6-automation-scope.md)

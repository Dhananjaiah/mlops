# Lecture 1.6 – Who Does What? (Data Engineer, ML Engineer, MLOps, DevOps, SRE, Product)

---

## The Team

Building production ML systems is a team sport. You can't do it alone.

In this lecture, I want to be very specific about who does what. This will help you:

1. Understand your own role better
2. Know who to talk to when you need help
3. Avoid stepping on toes or leaving gaps

Let's meet the team.

---

## The Cast of Characters

Here are the typical roles involved in an ML project:

1. **Product Manager (PM)**
2. **Data Engineer**
3. **Data Scientist**
4. **Machine Learning Engineer**
5. **MLOps Engineer**
6. **DevOps Engineer / SRE**
7. **Software Engineer**

Let me break down each one.

---

## Product Manager (PM)

### What They Do

The PM owns the "why" and the "what."

- Define the problem to solve
- Gather business requirements
- Set success metrics
- Prioritize work
- Communicate with stakeholders

### What They Don't Do

- Write code
- Build models
- Make technical architecture decisions

### How They Interact with MLOps

The PM tells you what success looks like. "We need the model to predict churn with 80% precision." "We need predictions available within 100ms."

You translate these requirements into technical specs.

### Key Deliverables

- Product requirements document (PRD)
- Success metrics definition
- User stories and acceptance criteria

---

## Data Engineer

### What They Do

Data Engineers build the plumbing for data.

- Build and maintain data pipelines
- Manage data infrastructure (warehouses, lakes)
- Ensure data quality
- Transform raw data into usable formats
- Manage data access and security

### What They Don't Do

- Build ML models
- Deploy models to production
- Monitor model performance

### How They Interact with MLOps

Data Engineers are your partners. They provide the data your models need.

- "I need customer purchase history for the last 12 months, updated daily."
- "I need this data in Parquet format in S3."
- "The feature pipeline needs to compute these 20 features."

You work closely with them to define **data contracts**—what data you need, in what format, at what frequency.

### Key Deliverables

- Data pipelines (Airflow DAGs, dbt models)
- Data quality checks
- Feature engineering pipelines
- Data documentation

---

## Data Scientist

### What They Do

Data Scientists create the intelligence.

- Explore and analyze data
- Build and evaluate ML models
- Select algorithms and tune hyperparameters
- Communicate insights to stakeholders
- Run experiments

### What They Don't Do

- Build production infrastructure
- Deploy models (in most orgs)
- Maintain production systems

### How They Interact with MLOps

Data Scientists are your primary customers. They create models; you deploy them.

Your job is to make their life easier:
- Provide tools for experiment tracking
- Set up reproducible training environments
- Give them visibility into how their models perform in production

### Key Deliverables

- Trained models
- Experiment reports
- Model evaluation metrics
- Feature definitions

---

## Machine Learning Engineer

### What They Do

ML Engineers bridge data science and production.

- Optimize models for production (speed, memory)
- Write production-quality training code
- Build feature pipelines
- Implement model serving solutions
- Work on ML infrastructure

### What They Don't Do

- Explore data (usually)
- Define business requirements
- Manage general infrastructure (VMs, networking)

### How They Interact with MLOps

ML Engineers and MLOps Engineers work very closely. In some companies, it's the same role.

The ML Engineer focuses more on:
- Model optimization
- Training pipeline code
- Feature engineering

The MLOps Engineer focuses more on:
- CI/CD
- Deployment infrastructure
- Monitoring
- Automation

### Key Deliverables

- Production-ready model code
- Training pipelines
- Optimized model artifacts
- Model serving implementations

---

## MLOps Engineer

### What They Do

This is us! MLOps Engineers own the operational side of ML.

- Set up CI/CD for ML projects
- Build and maintain deployment pipelines
- Manage model registries
- Set up monitoring and alerting
- Automate retraining
- Ensure reproducibility
- Manage ML infrastructure

### What They Don't Do

- Build models from scratch (though they should understand them)
- Define business requirements
- Write the core product code

### How They Interact with Others

MLOps is the glue:
- **Data Engineers**: "I need this data pipeline to feed into training."
- **Data Scientists**: "I'll deploy your model and monitor it."
- **DevOps**: "I need a Kubernetes cluster for model serving."
- **Software Engineers**: "Here's the API endpoint for predictions."

### Key Deliverables

- CI/CD pipelines for ML
- Model deployment automation
- Monitoring dashboards
- Model registry management
- Infrastructure as code for ML systems

---

## DevOps Engineer / SRE

### What They Do

DevOps/SRE manages the infrastructure and keeps systems reliable.

- Manage cloud infrastructure
- Set up CI/CD (for general software)
- Ensure system reliability
- Handle incidents
- Manage Kubernetes clusters
- Implement security best practices

### What They Don't Do

- Build ML models
- Understand ML-specific concerns (drift, etc.)
- Manage ML-specific tools

### How They Interact with MLOps

DevOps provides the foundation:
- "I need a Kubernetes namespace for the ML services."
- "Can you set up networking so the model API can reach the feature store?"
- "I need help setting up TLS for the model endpoints."

MLOps extends DevOps practices for ML. You'll often adopt their tools and conventions.

### Key Deliverables

- Infrastructure as code (Terraform)
- CI/CD pipelines
- Monitoring infrastructure (Prometheus, Grafana)
- Incident response procedures

---

## Software Engineer

### What They Do

Software Engineers build the applications that use ML.

- Build user-facing applications
- Integrate ML predictions into products
- Implement business logic
- Build APIs and services

### What They Don't Do

- Build ML models
- Manage ML infrastructure
- Monitor model performance

### How They Interact with MLOps

Software Engineers consume what MLOps provides:
- "What's the API endpoint for churn predictions?"
- "What's the expected response format?"
- "What's the latency SLA?"

You need to provide clear documentation and reliable APIs.

### Key Deliverables

- Application code
- Frontend/backend implementations
- Integration with ML services

---

## The Responsibility Matrix

Here's a visual way to think about who owns what:

| Activity | PM | Data Eng | Data Sci | ML Eng | MLOps | DevOps | SW Eng |
|----------|:--:|:--------:|:--------:|:------:|:-----:|:------:|:------:|
| Define requirements | ✓ | | | | | | |
| Build data pipelines | | ✓ | | | | | |
| Explore data | | | ✓ | | | | |
| Build models | | | ✓ | ✓ | | | |
| Track experiments | | | ✓ | ✓ | ✓ | | |
| Optimize models | | | | ✓ | | | |
| Build training pipelines | | | | ✓ | ✓ | | |
| Deploy models | | | | ✓ | ✓ | | |
| Set up CI/CD | | | | | ✓ | ✓ | |
| Monitor models | | | | | ✓ | | |
| Manage infrastructure | | | | | | ✓ | |
| Build applications | | | | | | | ✓ |
| Integrate predictions | | | | | | | ✓ |

Note: This varies by company! Some data scientists deploy their own models. Some DevOps teams handle MLOps. Adapt to your context.

---

## Common Team Structures

Let me describe a few real-world team structures:

### Structure 1: Centralized ML Platform Team

```
┌─────────────────────────────────────┐
│         ML Platform Team            │
│  (MLOps + ML Eng + some DevOps)     │
│                                     │
│  Serves multiple product teams      │
└─────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────┐   ┌───────┐   ┌───────┐
│Team A │   │Team B │   │Team C │
│(DS+PM)│   │(DS+PM)│   │(DS+PM)│
└───────┘   └───────┘   └───────┘
```

**Pros**: Consistent infrastructure, shared expertise
**Cons**: Bottleneck, might not know specific team needs

### Structure 2: Embedded MLOps

```
┌──────────────────────────────────┐
│           Product Team           │
├──────────────────────────────────┤
│  PM + Data Sci + SW Eng + MLOps  │
│  (Everyone on one team)          │
└──────────────────────────────────┘
```

**Pros**: Close collaboration, understands context
**Cons**: Inconsistent practices across teams

### Structure 3: Hybrid

```
┌─────────────────────────────────────┐
│     Central ML Platform Team        │
│   (Core infra, tools, standards)    │
└─────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  Team A   │ │  Team B   │ │  Team C   │
│ (DS + PM  │ │ (DS + PM  │ │ (DS + PM  │
│ + 1 MLOps)│ │ + 1 MLOps)│ │ + 1 MLOps)│
└───────────┘ └───────────┘ └───────────┘
```

**Pros**: Balance of consistency and flexibility
**Cons**: More complex coordination

---

## Handoffs and Communication

Where things often break down:

### The Data Handoff

- **Problem**: Data Engineer builds pipeline, but it doesn't produce what the model needs.
- **Solution**: Clear **data contracts**—documented schemas, quality requirements, SLAs.

### The Model Handoff

- **Problem**: Data Scientist builds model in notebook, MLOps can't deploy it.
- **Solution**: Clear **model interface requirements**—what format, what dependencies, what input/output.

### The Deployment Handoff

- **Problem**: MLOps deploys model, but Software Engineer doesn't know how to use it.
- **Solution**: Clear **API documentation**—endpoints, request/response formats, error codes.

---

## Your Role Might Be Different

Here's the thing: job titles are messy.

You might be called:
- MLOps Engineer
- ML Engineer
- Data Engineer (but doing MLOps work)
- Platform Engineer
- Production ML Engineer
- ML Infrastructure Engineer

The title matters less than the work. Use this lecture to understand the work, not to define rigid boundaries.

---

## Recap

The typical ML team includes:
- **Product Manager**: What and why
- **Data Engineer**: Data pipelines and storage
- **Data Scientist**: Models and experiments
- **ML Engineer**: Production-ready models
- **MLOps Engineer**: Deployment, monitoring, automation
- **DevOps/SRE**: Infrastructure and reliability
- **Software Engineer**: Applications that use ML

Key points:
- Roles overlap—that's normal
- Communication and clear contracts prevent problems
- Team structure varies by company
- Focus on the work, not the title

---

## What's Next

Now that you know who does what, let's look at what we'll cover in this entire course.

In the next lecture, I'll walk through the **agenda**—every section and what you'll learn.

---

**Next Lecture**: [1.7 – Agenda of the Entire Course (What We'll Build Step by Step)](lecture-1.7-course-agenda.md)

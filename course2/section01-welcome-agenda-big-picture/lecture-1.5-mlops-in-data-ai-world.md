# Lecture 1.5 – Where Does MLOps Fit in the Overall Data/AI World?

---

## The Bigger Ecosystem

MLOps doesn't exist in isolation. It's part of a larger ecosystem of data and AI disciplines.

In this lecture, I want to help you understand how MLOps connects to these other fields. This will help you:

1. Know who you'll be working with
2. Understand where your responsibilities start and end
3. See the career paths available to you

Let's map it out.

---

## The Data & AI Landscape

Imagine a company that wants to use data and AI to improve its business. Here are all the disciplines involved:

### 1. Data Engineering

**What they do**: Build the infrastructure to collect, store, and process data.

**Key activities**:
- Build data pipelines
- Manage data warehouses and data lakes
- Ensure data quality and availability
- Transform raw data into usable formats

**Tools**: Apache Spark, Airflow, dbt, Kafka, Snowflake, BigQuery

**Relationship to MLOps**: Data engineers provide the data that ML models use. MLOps teams depend on them for reliable, quality data.

---

### 2. Data Science

**What they do**: Analyze data and build models to extract insights and make predictions.

**Key activities**:
- Explore and analyze data
- Build and evaluate ML models
- Communicate findings to stakeholders
- Run experiments

**Tools**: Python, Jupyter, Pandas, scikit-learn, TensorFlow, PyTorch

**Relationship to MLOps**: Data scientists create the models that MLOps teams deploy. MLOps provides the infrastructure for data scientists to work efficiently and deploy their models.

---

### 3. Machine Learning Engineering

**What they do**: Bridge the gap between data science and production systems.

**Key activities**:
- Optimize models for production (speed, size)
- Build training pipelines
- Implement model serving solutions
- Work on feature engineering at scale

**Tools**: MLflow, Kubeflow, TensorFlow Extended, ONNX, Docker

**Relationship to MLOps**: ML Engineering and MLOps overlap significantly. Some companies combine them into one role. Others separate them, with ML Engineers focusing on the model side and MLOps on the infrastructure side.

---

### 4. MLOps

**What they do**: Build and maintain the systems that deploy, monitor, and manage ML models in production.

**Key activities**:
- Set up CI/CD for ML
- Manage model deployments
- Monitor model performance
- Automate retraining
- Ensure reproducibility

**Tools**: MLflow, Kubeflow, Airflow, Docker, Kubernetes, Prometheus

**Relationship to others**: MLOps is the glue. It connects Data Engineering (data), Data Science (models), DevOps (infrastructure), and the business.

---

### 5. DevOps / SRE

**What they do**: Build and maintain the infrastructure and processes for software delivery.

**Key activities**:
- Manage cloud infrastructure
- Set up CI/CD pipelines
- Ensure system reliability
- Handle incidents

**Tools**: Terraform, Kubernetes, GitHub Actions, Jenkins, Prometheus, Grafana

**Relationship to MLOps**: DevOps provides the foundation that MLOps builds on. Many MLOps practices are borrowed from DevOps, adapted for ML.

---

### 6. Software Engineering

**What they do**: Build the applications and services that use ML models.

**Key activities**:
- Build user-facing applications
- Integrate ML predictions into products
- Handle business logic

**Tools**: Whatever the stack is—Python, Java, Node.js, React, etc.

**Relationship to MLOps**: Software engineers are often the "consumers" of ML models. They call the prediction APIs that MLOps teams deploy and maintain.

---

### 7. AI Engineering / LLMOps (Emerging)

**What they do**: Build applications that use large language models and generative AI.

**Key activities**:
- Integrate LLM APIs (OpenAI, Anthropic, etc.)
- Build RAG (Retrieval Augmented Generation) systems
- Manage prompts and model versions
- Monitor LLM-specific metrics (hallucinations, costs)

**Tools**: LangChain, LlamaIndex, vector databases, LLM APIs

**Relationship to MLOps**: LLMOps is a specialized branch of MLOps. Many principles overlap, but there are unique challenges with LLMs (prompt management, high costs, hallucinations).

---

## The Maturity Journey

Companies typically evolve through stages:

### Stage 1: Ad Hoc Analytics

- Analysts query databases
- One-off analyses in Excel or notebooks
- No data infrastructure

### Stage 2: Basic Data Engineering

- Data warehouse established
- Regular ETL pipelines
- Business intelligence dashboards

### Stage 3: Data Science Exploration

- Data scientists hired
- Models built in notebooks
- Occasional models make it to production (painfully)

### Stage 4: ML in Production

- MLOps practices established
- Models deployed reliably
- Some automation in place

### Stage 5: Mature AI Organization

- Fully automated ML pipelines
- Feature stores
- A/B testing of models
- ML is a core part of the product

Most companies are somewhere between Stage 2 and Stage 4.

---

## The Organization Chart

In a typical company, where does everyone sit?

```
┌─────────────────────────────────────────────────────┐
│                    CTO / VP Engineering             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Platform   │  │     Data     │  │  Product  │ │
│  │  Engineering │  │    & AI      │  │Engineering│ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                 │                │        │
│    ┌────┴────┐      ┌────┴────┐      ┌────┴────┐  │
│    │ DevOps/ │      │  Data   │      │ Software│  │
│    │   SRE   │      │  Eng    │      │   Eng   │  │
│    └─────────┘      └─────────┘      └─────────┘  │
│                     │                             │
│              ┌──────┴──────┐                      │
│              │ Data Science│                      │
│              └─────────────┘                      │
│                     │                             │
│              ┌──────┴──────┐                      │
│              │   ML Eng /  │                      │
│              │   MLOps     │                      │
│              └─────────────┘                      │
└─────────────────────────────────────────────────────┘
```

This varies a lot by company. Some structures:

- **MLOps under Platform Engineering**: Focus on infrastructure
- **MLOps under Data & AI**: Focus on data science support
- **MLOps as a cross-functional team**: Serve multiple teams

There's no "right" structure—it depends on the company's needs.

---

## How Work Flows Between Teams

Let me trace a typical ML project:

1. **Business**: "We want to predict customer churn."
2. **Product**: Defines requirements, success metrics.
3. **Data Engineering**: Builds pipelines to gather customer data.
4. **Data Science**: Explores data, builds and evaluates models.
5. **ML Engineering**: Optimizes model, writes production code.
6. **MLOps**: Sets up deployment pipeline, monitoring, CI/CD.
7. **DevOps/SRE**: Provides infrastructure, handles incidents.
8. **Software Engineering**: Integrates predictions into the app.

In practice, these boundaries are blurry. A data scientist might do some ML engineering. An MLOps person might do some data engineering. That's normal.

---

## Where MLOps Fits: The Summary

MLOps sits at the intersection of:

- **Data Engineering**: MLOps needs data; data engineering provides it
- **Data Science**: MLOps deploys models; data science creates them
- **DevOps**: MLOps uses DevOps practices; adapts them for ML
- **Software Engineering**: MLOps provides APIs; software engineering consumes them

Think of MLOps as the bridge between "the model works on my laptop" and "the model is reliably serving millions of users."

---

## Career Implications

If you're thinking about career paths:

**From DevOps → MLOps**
- You already know infrastructure, CI/CD, Kubernetes
- Learn: ML basics, data pipelines, model concepts
- This is a natural transition

**From Data Science → MLOps**
- You already know models, Python, experiments
- Learn: Infrastructure, deployment, monitoring, software engineering practices
- Great if you want to see your models actually used

**From Data Engineering → MLOps**
- You already know data pipelines, orchestration, data storage
- Learn: ML concepts, model serving, monitoring
- Natural extension of your skills

**From Software Engineering → MLOps**
- You already know software development, APIs, testing
- Learn: ML concepts, data handling, experiment tracking
- Good fit if you're interested in ML

---

## The Rise of AI Engineering

One more thing I want to mention: the field is evolving.

With the rise of LLMs, a new role is emerging: **AI Engineer** or **LLM Engineer**.

This role focuses on:
- Integrating LLM APIs
- Building AI-powered applications
- Prompt engineering
- RAG systems

It overlaps with MLOps but has unique challenges. We won't cover LLMOps deeply in this course, but I wanted you to know it exists.

---

## Recap

- MLOps is part of a larger ecosystem: Data Engineering, Data Science, ML Engineering, DevOps, Software Engineering
- MLOps sits at the intersection of all these disciplines
- Companies evolve from ad-hoc analytics to mature AI organizations
- Organization structures vary, but MLOps typically bridges data/model work with infrastructure
- Career paths into MLOps come from many directions

---

## What's Next

Now that you understand where MLOps fits in the big picture, let's get more specific.

In the next lecture, we'll look at **who does what**—the specific roles and responsibilities of each person involved in an ML project.

---

**Next Lecture**: [1.6 – Who Does What? (Data Engineer, ML Engineer, MLOps, DevOps, SRE, Product)](lecture-1.6-roles-responsibilities.md)

# Lecture 1.2 – What Is MLOps? In One Story, Not a Definition

---

## Let's Skip the Definition

I could start this lecture by saying:

*"MLOps is a set of practices that combines Machine Learning, DevOps, and Data Engineering to deploy and maintain ML systems in production reliably and efficiently."*

But that doesn't really help you understand anything, does it?

Instead, let me tell you a story.

---

## The Story of Two Data Scientists

### Meet Sarah

Sarah is a data scientist at a retail company. Her job is to predict which customers are likely to stop buying from the company—what we call "churn prediction."

She spends three weeks building a model. She cleans the data, engineers features, trains multiple algorithms, and picks the best one. Her model achieves 87% accuracy. Her manager is thrilled.

"Great work, Sarah! Can we use this model to identify risky customers every week?"

Sarah says yes. Here's what happens next:

**Week 1**: Sarah runs her Jupyter notebook manually. Extracts predictions. Sends an Excel file to the marketing team.

**Week 2**: Same thing. Manual run. Excel file.

**Week 3**: Sarah is on vacation. The model doesn't run. Marketing has no predictions.

**Week 4**: Sarah is back. But the data format changed slightly. Her notebook crashes. She spends two days fixing it.

**Week 5**: A new data scientist joins. He wants to understand Sarah's model. The notebook is 2000 lines long. No documentation. He's lost.

**Month 2**: The model accuracy drops to 72%. No one knows why. No one noticed until a customer complained.

**Month 3**: Management wants a new model. Sarah builds one. But now there are two models. Which one is in production? What data did each use? No one is sure.

Sarah is frustrated. She's a good data scientist. But her models keep causing problems instead of solving them.

---

### Meet Alex

Alex is also a data scientist at a different company. Same task: churn prediction.

But Alex's company does MLOps.

Here's how Alex's story goes:

**Week 1**: Alex builds the model. But instead of stopping at the notebook, he packages it into a Python script with clear inputs and outputs.

**Week 2**: The MLOps team helps Alex set up an **automated pipeline**. Every Monday, the pipeline automatically:
1. Pulls fresh data
2. Runs the model
3. Saves predictions to a database
4. Sends alerts if anything goes wrong

**Week 3**: Alex is on vacation. The pipeline runs anyway. Marketing gets their predictions.

**Week 4**: The data format changes. The pipeline detects this (data validation!) and alerts the team. They fix it within hours.

**Week 5**: A new data scientist joins. She looks at the experiment tracking system and sees every model Alex trained, with parameters, metrics, and the exact data used. She's up to speed in a day.

**Month 2**: The monitoring dashboard shows model accuracy dropping. The team is alerted immediately. They investigate and find a data issue upstream. Fixed.

**Month 3**: Alex trains a new model. The old model is marked as "archived" in the model registry. The new one is "production." Everyone knows exactly which model is serving predictions.

Alex is happy. His models actually deliver business value.

---

## So, What Is MLOps?

Now you've seen the difference. Let me explain.

**MLOps is everything you need to take a machine learning model from "works on my laptop" to "runs reliably in production."**

It's the answer to questions like:

- How do I run this model automatically every day?
- How do I know if the model is still working well?
- How do I deploy a new version without breaking things?
- How do I track which data and code produced which model?
- How do I roll back if something goes wrong?

---

## The Three Pillars of MLOps

Think of MLOps as having three pillars:

### 1. Machine Learning

This is what data scientists do: build models. Train algorithms. Tune hyperparameters. Evaluate metrics.

MLOps doesn't replace this. It supports it.

### 2. DevOps

DevOps is about automating software delivery. Build systems. Test systems. Deploy systems. Monitor systems.

MLOps borrows heavily from DevOps, but adapts it for the unique challenges of ML.

### 3. Data Engineering

Data is the lifeblood of ML. Getting data, cleaning data, transforming data, storing data.

MLOps works closely with data engineering to make sure models have the data they need, when they need it.

---

## What's Different About ML?

You might be thinking, "Why do we need MLOps? Can't we just use regular DevOps?"

Good question. Here's what makes ML different:

### Code + Data + Model

In traditional software, you deploy code. That's it.

In ML, you deploy three things:
- **Code**: The training script, the inference function, the API.
- **Data**: The training data, the feature pipelines, the live data.
- **Model**: The trained weights, the serialized artifact.

All three can change. All three need to be versioned. All three can cause bugs.

### Testing Is Harder

In regular software, you write tests: "Given input X, expect output Y."

In ML, the output is probabilistic. A model might give different answers for similar inputs. How do you test that?

### Models Decay

Regular software doesn't get worse over time. If it worked yesterday, it works today.

ML models decay. The world changes. Customer behavior changes. What worked last month might not work this month.

This is called **model drift**, and it's one of the biggest challenges in production ML.

### Experiments Are Messy

Data scientists run hundreds of experiments. Different datasets, different algorithms, different parameters.

Keeping track of all this without proper tooling is a nightmare.

---

## MLOps Is Not a Tool

This is important: **MLOps is not a single tool.**

You'll hear about tools like MLflow, Kubeflow, DVC, Airflow, and dozens of others. They're all part of the MLOps ecosystem.

But MLOps is really a set of **practices**:

- Automate what can be automated
- Version everything
- Test your ML code
- Monitor your models
- Have a clear process for deploying models
- Make it easy to roll back

Tools help you implement these practices. But the practices come first.

---

## The MLOps Maturity Model

Not every team does MLOps the same way. There's a spectrum.

**Level 0 – Manual**
- Models trained manually
- Deployment is "copy this file to the server"
- No monitoring
- This is where Sarah was

**Level 1 – Automated Training**
- Training pipeline is automated
- Models can be retrained on schedule
- Some basic monitoring

**Level 2 – Automated Training + Deployment**
- CI/CD for models
- Automated testing
- Model registry
- This is where most mature teams aim to be

**Level 3 – Fully Automated**
- Automatic retraining when drift is detected
- A/B testing of models
- Sophisticated monitoring
- This is where companies like Google and Netflix are

Most teams are somewhere between Level 0 and Level 2. And that's okay. You don't need to be Google on Day 1.

---

## Why Should You Care?

Here's the deal:

- **If you're a data scientist**: Learning MLOps makes your models actually useful. You'll go from "I built a model" to "I delivered business value."

- **If you're a DevOps engineer**: MLOps is the next frontier. Companies need people who can deploy ML systems.

- **If you're a software engineer**: ML is eating software. Understanding how to build production ML systems is a valuable skill.

- **If you're a manager**: Teams that do MLOps ship faster, break less, and can actually measure the impact of their ML investments.

---

## Recap

Let me summarize:

1. MLOps is about taking models from laptop to production.
2. It combines ML, DevOps, and Data Engineering.
3. ML is different from regular software: code + data + model, harder to test, models decay.
4. MLOps is practices, not a single tool.
5. Teams mature from manual (Level 0) to fully automated (Level 3).

Sarah struggled because she didn't have MLOps.

Alex succeeded because he did.

Which one do you want to be?

---

## What's Next

In the next lecture, we'll dig deeper into **why MLOps matters**. We'll talk about the gap between a "cool model" and actual business value.

Because building a model is just the beginning.

---

**Next Lecture**: [1.3 – Why Do We Need MLOps? (From "Cool Model" → "Business Value")](lecture-1.3-why-mlops.md)

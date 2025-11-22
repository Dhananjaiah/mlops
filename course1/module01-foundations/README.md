# Module 01: MLOps Foundations

## 🎯 Learning Objectives

By the end of this module, you will:
- ✅ Understand the complete ML lifecycle
- ✅ Know the different MLOps roles and responsibilities
- ✅ Understand what artifacts need to be tracked
- ✅ Learn the importance of dev-prod parity
- ✅ See why reproducibility matters

## ⏱️ Duration

1 hour

## 📋 Prerequisites

- Completed Module 00 (Setup)
- Understanding of basic ML concepts
- Familiarity with Python

## 📚 What You'll Learn

### The ML Lifecycle

Traditional software has a simple lifecycle:
```
Code → Build → Test → Deploy → Monitor
```

ML systems are more complex:
```
Data Collection → Data Preparation → Feature Engineering →
Model Training → Model Evaluation → Model Deployment →
Monitoring → Retraining → (Loop back)
```

### Why MLOps?

**The Problem:**
- Data scientists train models on laptops
- Models work in notebooks but fail in production
- No way to reproduce results
- No monitoring of deployed models
- Manual, error-prone processes

**The Solution: MLOps**
- Version everything (code, data, models)
- Automate pipelines
- Monitor continuously
- Enable fast, safe iterations

### Key Concepts

1. **Artifacts**: Everything your ML system produces or uses
   - Data files
   - Trained models
   - Configuration files
   - Metrics and logs
   - Model predictions

2. **Lineage**: The history and relationships between artifacts
   - Which data produced which model?
   - Which code version was used?
   - What were the hyperparameters?

3. **Reproducibility**: Ability to recreate exact results
   - Same code + same data + same environment = same model
   - Essential for debugging and compliance

4. **Dev-Prod Parity**: Development and production should be identical
   - Same Python version
   - Same libraries
   - Same data format
   - Same infrastructure

## 🎓 Key Takeaways

After this module, remember:

1. **ML is different from traditional software**
   - Data is code
   - Models drift over time
   - Need continuous monitoring

2. **Track everything**
   - Code (Git)
   - Data (DVC)
   - Experiments (MLflow)
   - Configurations
   - Metrics

3. **Automate ruthlessly**
   - Manual steps lead to errors
   - Automation enables scale
   - Pipelines ensure consistency

4. **Dev-prod parity prevents surprises**
   - Same environment everywhere
   - Use containers (Docker)
   - Infrastructure as code

## 📖 Module Structure

### 1. Read the Transcript
Start with `transcript.md` for detailed explanations of all concepts.

### 2. Run Code Examples

```bash
cd code/

# Example 1: Basic ML workflow
python 01_ml_workflow.py

# Example 2: Tracking artifacts
python 02_artifact_tracking.py

# Example 3: Reproducibility demo
python 03_reproducibility.py
```

### 3. Complete Exercises

```bash
cd ../exercises/

# Exercise 1: Design an ML system
cat exercise01_system_design.md

# Exercise 2: Identify artifacts
cat exercise02_artifacts.md

# Exercise 3: Ensure reproducibility
cat exercise03_reproducibility.md
```

### 4. Check Solutions

```bash
cd ../solutions/

# Review solution approaches
cat solution01.md
cat solution02.md
cat solution03.md
```

## 🔑 Key Terms

- **MLOps**: Machine Learning Operations - practices for deploying and maintaining ML models
- **Artifact**: Any file or object produced or used by the ML pipeline
- **Lineage**: The history and relationships between artifacts
- **Reproducibility**: Ability to recreate exact results
- **Dev-Prod Parity**: Keeping development and production environments identical
- **Pipeline**: Automated sequence of steps in the ML workflow
- **Model Drift**: Degradation of model performance over time

## 🎯 Success Criteria

You've mastered this module when you can:

- [ ] Explain the ML lifecycle to someone
- [ ] Identify artifacts in an ML system
- [ ] Understand why reproducibility matters
- [ ] Know the difference between dev and prod environments
- [ ] Recognize when models need retraining

## 📚 Additional Resources

- [MLOps: Continuous delivery and automation pipelines (Google)](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [What is MLOps? (AWS)](https://aws.amazon.com/what-is/mlops/)
- [Awesome MLOps (GitHub)](https://github.com/visenger/awesome-mlops)

## 🚀 Next Steps

After completing this module:

1. Review your notes
2. Complete all exercises
3. Move to [Module 02: Environment & Packaging](../module02-environment/README.md)

---

**Questions?** Check the [transcript](transcript.md) or open an issue.

**Ready?** Let's dive into the [complete transcript](transcript.md)!

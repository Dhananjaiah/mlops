# MLOps Course: 0→1→Production (Commands-First)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> A comprehensive, hands-on MLOps course covering the complete journey from development to production. **Commands first, minimal theory, maximum practice.**

---

## 🎯 What You'll Learn

By completing this course, you will:
- ✅ **Version** data, code, and models for full reproducibility
- ✅ **Track experiments** and systematically compare models
- ✅ **Build automated pipelines** for training and deployment
- ✅ **Serve models** via APIs with monitoring and autoscaling
- ✅ **Detect drift** and trigger automated retraining
- ✅ **Deploy with CI/CD** to multiple environments
- ✅ **Monitor production** systems with metrics and alerts
- ✅ **Secure and optimize** ML systems for cost and compliance

---

## 📚 Course Structure

### **Modules** (16 total)
Each module includes: Goals, Key Terms, Commands, Verify steps, Mini-lab, Quiz, Troubleshooting

| # | Module | Topics | Duration |
|---|--------|--------|----------|
| [00](course/00-overview.md) | **Overview** | Course structure, tooling, success criteria | 30 min |
| [00.5](course/00.5-data-engineering-for-beginners.md) | **Data Engineering for Beginners** ⭐ NEW! | For DevOps engineers with no data background | 2 hours |
| [01](course/01-mlops-foundations.md) | **MLOps Foundations** | Lifecycle, roles, artifacts, dev-prod parity | 1 hour |
| [02](course/02-env-and-packaging.md) | **Environment & Packaging** | uv, poetry, Docker, pre-commit | 1.5 hours |
| [03](course/03-data-versioning-and-quality.md) | **Data Versioning & Quality** | DVC, Great Expectations, Evidently | 2 hours |
| [04](course/04-experiment-tracking-and-reproducibility.md) | **Experiment Tracking** | MLflow (experiments, artifacts, models) | 2 hours |
| [05](course/05-pipelines-orchestration.md) | **Pipelines & Orchestration** | Airflow, Kubeflow Pipelines, DAGs | 2.5 hours |
| [06](course/06-model-training-eval-and-selection.md) | **Training, Eval & Selection** | Cross-validation, hyperparameter tuning, bias checks | 2 hours |
| [07](course/07-model-registry-and-governance.md) | **Model Registry & Governance** | MLflow Registry, stage transitions, model cards | 1.5 hours |
| [08](course/08-serving-and-apis.md) | **Serving & APIs** | FastAPI, KServe, BentoML, health checks | 2 hours |
| [09](course/09-batch-streaming-and-scheduled-jobs.md) | **Batch & Streaming** | Batch scoring, Kafka, scheduled jobs | 2 hours |
| [10](course/10-ci-cd-and-environments.md) | **CI/CD & Environments** | GitHub Actions, multi-env, canary deploys | 2.5 hours |
| [11](course/11-observability-and-monitoring.md) | **Observability & Monitoring** | Prometheus, Grafana, OpenTelemetry, SLOs | 2 hours |
| [12](course/12-drift-detection-and-retraining.md) | **Drift Detection & Retraining** | Evidently, automated retraining triggers | 1.5 hours |
| [13](course/13-security-compliance-and-cost.md) | **Security, Compliance & Cost** | CVE scanning, SBOM, PII detection, FinOps | 2 hours |
| [14](course/14-comprehensive-review.md) | **Comprehensive Review** | End-to-end scenario, troubleshooting, career paths | 1.5 hours |

**Total**: ~27 hours of hands-on learning (includes beginner data engineering module)

---

## 🚀 Quick Start

> 💡 **New to this project?** Check out the [**Project Execution Guide**](PROJECT_EXECUTION_GUIDE.md) for detailed step-by-step instructions, role-based paths, and "who does what"!

### **Option 1: Local (Docker Compose)**
```bash
# Clone the repository
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops/project

# Start the stack
docker compose up -d

# Verify services
docker compose ps
curl http://localhost:8000/health  # FastAPI
curl http://localhost:5000         # MLflow
curl http://localhost:9090         # Prometheus
curl http://localhost:3000         # Grafana (admin/admin)

# Train a model
make run-train

# Test the API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[34, 12, 65.5]]}'
```

### **Option 2: Kubernetes (K3d)**
```bash
# Create local K8s cluster
k3d cluster create mlops-cluster --servers 1 --agents 2

# Deploy to K8s
kubectl create namespace mlops
kustomize build project/infra/k8s/overlays/dev | kubectl apply -f -

# Port-forward services
kubectl port-forward -n mlops svc/mlops-api 8000:80 &
kubectl port-forward -n mlops svc/mlflow 5000:5000 &
```

---

## 📂 Repository Structure

```
mlops/
├── course/                      # Course modules (00-14)
│   ├── 00-overview.md
│   ├── 01-mlops-foundations.md
│   ├── ...
│   └── 14-comprehensive-review.md
├── project/                     # Capstone project (Churn Predictor)
│   ├── data/                    # Data (DVC tracked)
│   ├── src/                     # Source code
│   ├── serving/                 # API serving
│   ├── pipelines/               # Airflow/Kubeflow pipelines
│   ├── infra/                   # Infrastructure (Terraform, K8s)
│   ├── tests/                   # Tests
│   ├── scripts/                 # Utility scripts
│   ├── docker-compose.yml       # Local stack
│   ├── Makefile                 # Common commands
│   └── README.md                # Project documentation
├── cheatsheets/                 # Quick reference cards
│   ├── python-env.md
│   ├── dvc-mlflow.md
│   └── docker-k8s.md
├── troubleshooting/             # Triage matrix for common issues
│   └── triage-matrix.md
├── exams/                       # Mock certification exams
│   ├── mock-exam-1.md
│   └── mock-exam-2.md
└── README.md                    # This file
```

---

## 🛠️ Technology Stack

| Category | Tools |
|----------|-------|
| **Python** | uv, poetry, pyproject.toml |
| **Data Versioning** | DVC (S3/MinIO remotes) |
| **Experiment Tracking** | MLflow |
| **Orchestration** | Airflow, Kubeflow Pipelines |
| **Data Quality** | Great Expectations, Evidently |
| **Serving** | FastAPI, KServe, BentoML |
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kubernetes, Kustomize, Helm |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana, OpenTelemetry |
| **Security** | Trivy, Gitleaks, Syft (SBOM) |
| **Infrastructure** | Terraform |

---

## 🎓 Learning Path

### **New to Data Engineering?** Start Here! ⭐
0. Complete [Module 00.5: Data Engineering for Beginners](course/00.5-data-engineering-for-beginners.md)
   - Perfect for DevOps engineers with no data background
   - Learn data gathering, cleaning, feature engineering, and basic ML
   - Hands-on tutorial with sample code
   - [Quick Start Guide](project/DATA_ENGINEERING_README.md)

### **Beginner Track** (Weeks 1-2)
1. Complete modules 00-04 (Overview, Foundations, Environment, Data, Experiments)
2. Work through mini-labs in each module
3. Start the capstone project (Churn Predictor)

### **Intermediate Track** (Weeks 3-4)
4. Complete modules 05-09 (Pipelines, Training, Registry, Serving, Batch)
5. Deploy locally with docker-compose
6. Add monitoring and drift detection

### **Advanced Track** (Weeks 5-6)
7. Complete modules 10-14 (CI/CD, Monitoring, Drift, Security, Review)
8. Deploy to Kubernetes
9. Complete full end-to-end workflow
10. Take mock exams

---

## 📖 Resources

### **📘 Implementation Guide** ⭐ NEW!
- [**Complete Implementation & Teaching Guide**](IMPLEMENTATION_GUIDE.md) - Comprehensive step-by-step runbook for implementing and teaching the entire course (1700+ lines)

### **Cheatsheets**
- [Linux for MLOps/DevOps](cheatsheets/linux.md) ⭐ NEW!
- [Python Environment Management](cheatsheets/python-env.md)
- [DVC + MLflow](cheatsheets/dvc-mlflow.md)
- [Docker & Kubernetes](cheatsheets/docker-k8s.md)

### **Troubleshooting**
- [Triage Matrix](troubleshooting/triage-matrix.md) - Symptom → Fix for common issues

### **Exams**
- [Mock Exam 1](exams/mock-exam-1.md) - 90 minutes, 100 points
- Mock Exam 2 - Coming soon

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Report Issues**: Found a bug or unclear explanation? [Open an issue](https://github.com/Dhananjaiah/mlops/issues)
2. **Improve Content**: Submit PRs to fix typos, add examples, or enhance explanations
3. **Share Your Projects**: Built something cool? Share in Discussions
4. **Add Tools**: Know a better tool? Suggest it or add a module

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 💬 Community

- **Discussions**: [GitHub Discussions](https://github.com/Dhananjaiah/mlops/discussions)
- **Issues**: [Bug Reports & Feature Requests](https://github.com/Dhananjaiah/mlops/issues)
- **Slack**: Join [MLOps Community](https://mlops.community) #course channel
- **Twitter**: Share your progress with #MLOpsCourse

---

## 📜 License

This course is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

This course is built on the shoulders of giants:
- MLOps Community for inspiration
- Open-source maintainers of MLflow, DVC, Evidently, and other tools
- Contributors who've shared feedback and improvements

---

## ⭐ Star This Repo!

If you find this course helpful, please **star the repository** ⭐ and share it with others!

---

## 🎯 Next Steps

1. **🚀 Ready to Execute?**: [Project Execution Guide →](PROJECT_EXECUTION_GUIDE.md) ⭐ NEW! - Clear step-by-step instructions with "who does what"
2. **📖 New to Data?**: [Data Engineering for Beginners →](course/00.5-data-engineering-for-beginners.md) ⭐ NEW!
3. **📖 Complete Implementation Guide**: [Step-by-Step Runbook →](IMPLEMENTATION_GUIDE.md)
4. **Start Learning**: [Module 00 - Overview →](course/00-overview.md)
5. **Quick Start**: [Capstone Project README →](project/README.md)
6. **Get Help**: [Troubleshooting Matrix →](troubleshooting/triage-matrix.md)

**Let's build production ML systems together! 🚀**

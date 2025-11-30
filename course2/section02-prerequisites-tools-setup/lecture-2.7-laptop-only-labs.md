# Lecture 2.7 – How to Follow Labs if You Only Have a Laptop

---

## No Cloud? No Problem!

Here's some good news: you don't need cloud accounts to follow this course.

I've designed everything to work on a regular laptop. Whether you have a MacBook Air, a Windows laptop, or a Linux desktop—you can do all the labs.

Let me show you how.

---

## What You'll Use Instead of Cloud

### Instead of Cloud VMs → Docker

Cloud VMs are just Linux machines. Docker gives you the same thing locally.

```bash
# Instead of SSH-ing into a cloud VM:
docker run -it ubuntu:22.04 bash

# You're now in a Linux environment!
```

### Instead of Kubernetes Cluster → K3d/Kind

K3d and Kind create Kubernetes clusters inside Docker.

```bash
# Install k3d
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Create a local cluster
k3d cluster create mlops-local --servers 1 --agents 2

# Now you have Kubernetes!
kubectl get nodes
```

### Instead of S3/GCS → MinIO

MinIO is S3-compatible storage that runs locally.

```bash
# Run MinIO with Docker
docker run -d \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"

# Access MinIO console at http://localhost:9001
```

### Instead of Cloud Databases → Docker Containers

PostgreSQL:
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgres:15
```

Redis:
```bash
docker run -d --name redis -p 6379:6379 redis:7
```

---

## The Local Development Stack

Here's what we'll run locally with Docker Compose:

```yaml
# docker-compose.yml
version: '3.8'

services:
  # MLflow for experiment tracking
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.8.0
    ports:
      - "5000:5000"
    command: mlflow server --host 0.0.0.0
    
  # PostgreSQL for databases
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
      
  # MinIO for S3-like storage
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    
  # Prometheus for metrics
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  # Grafana for dashboards
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
```

Start everything:
```bash
docker compose up -d
```

Now you have:
- MLflow: http://localhost:5000
- MinIO: http://localhost:9001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

---

## Minimum System Requirements

Here's what you actually need:

### Minimum
- **RAM**: 8 GB (16 GB recommended)
- **CPU**: 4 cores
- **Storage**: 50 GB free
- **OS**: macOS, Windows 10+, or Linux

### Recommended
- **RAM**: 16 GB
- **CPU**: 8 cores
- **Storage**: 100 GB free SSD

### If You're Low on Resources

Run services one at a time instead of all together:

```bash
# Just run what you need
docker compose up mlflow -d
# ... do mlflow labs ...
docker compose down

docker compose up prometheus grafana -d
# ... do monitoring labs ...
docker compose down
```

---

## Laptop-Friendly Configurations

### Reduce Docker Memory

By default, Docker might use too much RAM. Limit it:

**Docker Desktop Settings**:
- Resources → Memory: 4-6 GB is enough
- Resources → CPUs: 4 cores
- Resources → Disk: 50 GB

### Use Lighter Images

```dockerfile
# Instead of:
FROM python:3.11

# Use:
FROM python:3.11-slim

# Even lighter:
FROM python:3.11-alpine
```

### Smaller Datasets

For labs, we'll use small datasets:
- 10,000 rows instead of 10 million
- Sampled data for testing
- Synthetic data when real data is too big

---

## Alternative: Cloud Free Tiers

If you want cloud experience but free:

### GitHub Codespaces (Free Tier)
- 60 hours/month free
- Full dev environment in browser
- VS Code in the cloud

To use:
1. Fork the course repo
2. Click "Code" → "Codespaces" → "Create"
3. Full environment ready!

### Google Colab
- Free Jupyter notebooks
- Good for experimentation
- Limited for full MLOps workflows

### AWS Free Tier
- 12 months of free EC2 (t2.micro)
- Free S3 (5 GB)
- Free Lambda invocations

### GCP Free Tier
- $300 credit for new accounts
- Always free Compute Engine (e2-micro)
- Free Cloud Storage (5 GB)

---

## Setting Up for Offline Work

Want to work without internet? Prepare ahead:

### Pre-pull Docker Images

```bash
# Pull all images you'll need
docker pull python:3.11-slim
docker pull postgres:15
docker pull redis:7
docker pull minio/minio
docker pull prom/prometheus
docker pull grafana/grafana
docker pull ghcr.io/mlflow/mlflow:v2.8.0
```

### Pre-download Python Packages

```bash
# Download packages for offline use
pip download -d ./packages -r requirements.txt

# Install offline
pip install --no-index --find-links=./packages -r requirements.txt
```

### Pre-download Datasets

```bash
# Download course datasets
python scripts/download_data.py

# They'll be in data/raw/
```

---

## Troubleshooting Common Laptop Issues

### "Docker is using too much memory"

1. Limit Docker resources in settings
2. Stop containers you're not using: `docker compose down`
3. Prune unused images: `docker system prune`

### "My laptop is too slow"

1. Run fewer services at once
2. Use smaller datasets
3. Close other applications
4. Consider using GitHub Codespaces

### "Out of disk space"

```bash
# Clean up Docker
docker system prune -a  # removes all unused images

# Clean up Python
pip cache purge

# Clean up DVC cache
rm -rf .dvc/cache
```

### "Services won't start"

```bash
# Check what's using ports
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
docker run -p 5001:5000 ...
```

---

## The Laptop-Friendly Learning Path

Here's how I recommend working through the course:

### Phase 1: Core Skills (Local Only)
- Sections 1-6
- Use Python, Git, Docker locally
- Run MLflow in Docker
- Small datasets

### Phase 2: Production Skills (Docker Compose)
- Sections 7-10
- Full local stack
- API serving, CI/CD, monitoring

### Phase 3: Infrastructure (Optional K8s)
- Sections 11-13
- Use K3d for local Kubernetes
- Or skip K8s details

### Phase 4: Capstone
- Sections 14-15
- Full project on local or free cloud tier

---

## Quick Setup Commands

Here's your copy-paste setup:

```bash
# 1. Create project directory
mkdir -p ~/mlops-course
cd ~/mlops-course

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip

# 3. Install packages
pip install pandas numpy scikit-learn mlflow dvc fastapi uvicorn pytest black

# 4. Verify Docker
docker --version
docker run hello-world

# 5. Start local MLflow
docker run -d -p 5000:5000 --name mlflow ghcr.io/mlflow/mlflow:v2.8.0 \
    mlflow server --host 0.0.0.0

# 6. Verify MLflow
curl http://localhost:5000/health
# Or open http://localhost:5000 in browser

# You're ready!
```

---

## Recap

You don't need cloud resources for this course:

- **Docker** replaces cloud VMs
- **K3d** replaces Kubernetes clusters
- **MinIO** replaces S3
- **Local Postgres/Redis** replaces managed databases
- **Docker Compose** ties it all together

Minimum requirements:
- 8 GB RAM, 4 cores, 50 GB disk

If you're resource-constrained:
- Run services one at a time
- Use smaller datasets
- Consider GitHub Codespaces (free tier)

---

## Section 2 Complete! 🎉

Congratulations on finishing Section 2!

**You now have**:
- Python environment set up
- Git configured
- Docker running
- Project structure created
- All packages installed
- Local development strategy

---

**Next Section**: [Section 3 – Understanding the ML Lifecycle & MLOps Responsibilities](../section03-ml-lifecycle-mlops-responsibilities/lecture-3.1-framing-problems.md)

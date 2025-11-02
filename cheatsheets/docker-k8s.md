# Docker & Kubernetes Cheatsheet for MLOps

## Docker Basics

### Build & Run
```bash
# Build image
docker build -t my-ml-api:latest .
docker build -f Dockerfile.train -t ml-train:v1 .

# Run container
docker run -d -p 8000:8000 --name api my-ml-api:latest
docker run --rm -it ml-train:v1  # Interactive, auto-remove

# Run with environment variables
docker run -e MLFLOW_URI=http://mlflow:5000 my-ml-api:latest

# Run with volume mount
docker run -v $(pwd)/data:/app/data my-ml-api:latest

# Run with GPU
docker run --gpus all nvidia/cuda:11.8-base nvidia-smi
```

### Container Management
```bash
# List containers
docker ps            # Running
docker ps -a         # All

# Stop/start
docker stop api
docker start api
docker restart api

# Remove
docker rm api        # Remove container
docker rmi my-ml-api:latest  # Remove image

# Logs
docker logs api
docker logs -f api --tail=100  # Follow, last 100 lines

# Execute command
docker exec -it api /bin/bash
docker exec api python -c "import torch; print(torch.cuda.is_available())"

# Stats
docker stats api
```

### Images
```bash
# List images
docker images

# Pull/push
docker pull python:3.11-slim
docker push ghcr.io/user/my-ml-api:latest

# Tag
docker tag my-ml-api:latest ghcr.io/user/my-ml-api:v1.0

# Inspect
docker inspect my-ml-api:latest

# History
docker history my-ml-api:latest
```

### Dockerfile Best Practices
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
WORKDIR /app
COPY . .
CMD ["python", "app.py"]

# .dockerignore
__pycache__/
*.pyc
.git/
.venv/
*.md
tests/
```

---

## Docker Compose

### Basic Commands
```bash
# Start services
docker compose up          # Foreground
docker compose up -d       # Detached

# Stop
docker compose down        # Remove containers
docker compose down -v     # Remove volumes too

# Logs
docker compose logs
docker compose logs -f mlflow

# Restart
docker compose restart mlflow

# Status
docker compose ps

# Execute command
docker compose exec mlflow bash
```

### docker-compose.yml Example
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: mlops
      POSTGRES_PASSWORD: mlops
      POSTGRES_DB: mlflow
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mlops"]
      interval: 10s
      timeout: 5s
      retries: 5

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    command: >
      mlflow server
      --backend-store-uri postgresql://mlops:mlops@db:5432/mlflow
      --default-artifact-root /mlflow/artifacts
      --host 0.0.0.0
      --port 5000
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/mlflow
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      MLFLOW_TRACKING_URI: http://mlflow:5000
    depends_on:
      - mlflow
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
  mlflow_data:
```

---

## Kubernetes Basics

### Cluster Management
```bash
# Context
kubectl config get-contexts
kubectl config use-context my-cluster
kubectl config current-context

# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl top nodes
```

### Namespaces
```bash
# List namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace mlops

# Set default namespace
kubectl config set-context --current --namespace=mlops

# Delete namespace
kubectl delete namespace mlops
```

### Pods
```bash
# List pods
kubectl get pods
kubectl get pods -n mlops
kubectl get pods --all-namespaces

# Describe pod
kubectl describe pod my-pod

# Logs
kubectl logs my-pod
kubectl logs -f my-pod --tail=100
kubectl logs my-pod -c container-name  # Specific container

# Execute command
kubectl exec -it my-pod -- /bin/bash
kubectl exec my-pod -- python -c "import torch; print(torch.cuda.is_available())"

# Port forward
kubectl port-forward pod/my-pod 8000:8000

# Delete pod
kubectl delete pod my-pod
```

### Deployments
```bash
# List deployments
kubectl get deployments

# Create deployment
kubectl create deployment mlops-api --image=ghcr.io/user/mlops-api:latest

# Scale
kubectl scale deployment mlops-api --replicas=3

# Rollout
kubectl rollout status deployment/mlops-api
kubectl rollout history deployment/mlops-api
kubectl rollout undo deployment/mlops-api

# Update image
kubectl set image deployment/mlops-api mlops-api=ghcr.io/user/mlops-api:v2

# Describe
kubectl describe deployment mlops-api

# Delete
kubectl delete deployment mlops-api
```

### Services
```bash
# List services
kubectl get svc

# Expose deployment
kubectl expose deployment mlops-api --port=80 --target-port=8000 --type=LoadBalancer

# Port forward service
kubectl port-forward svc/mlops-api 8000:80

# Delete service
kubectl delete svc mlops-api
```

### ConfigMaps & Secrets
```bash
# ConfigMap
kubectl create configmap app-config --from-file=config.yaml
kubectl get configmap app-config -o yaml

# Secret
kubectl create secret generic api-secrets --from-literal=api-key=abc123
kubectl get secret api-secrets -o yaml

# Delete
kubectl delete configmap app-config
kubectl delete secret api-secrets
```

---

## Kubernetes Manifests

### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-api
  namespace: mlops
  labels:
    app: mlops-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mlops-api
  template:
    metadata:
      labels:
        app: mlops-api
    spec:
      containers:
      - name: api
        image: ghcr.io/user/mlops-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow:5000"
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: api-key
        resources:
          requests:
            cpu: "100m"
            memory: "256Mi"
          limits:
            cpu: "1"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Service YAML
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mlops-api
  namespace: mlops
spec:
  selector:
    app: mlops-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mlops-api-hpa
  namespace: mlops
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mlops-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Apply Manifests
```bash
# Apply single file
kubectl apply -f deployment.yaml

# Apply directory
kubectl apply -f k8s/

# Apply with Kustomize
kubectl apply -k k8s/overlays/dev/

# Dry run
kubectl apply -f deployment.yaml --dry-run=client -o yaml

# Delete
kubectl delete -f deployment.yaml
```

---

## Kustomize

### Structure
```
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patch-replicas.yaml
    └── prod/
        ├── kustomization.yaml
        └── patch-replicas.yaml
```

### base/kustomization.yaml
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

commonLabels:
  app: mlops-api
```

### overlays/dev/kustomization.yaml
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: mlops-dev

resources:
  - ../../base

replicas:
  - name: mlops-api
    count: 1

images:
  - name: ghcr.io/user/mlops-api
    newTag: dev-latest
```

### overlays/prod/kustomization.yaml
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: mlops-prod

resources:
  - ../../base

replicas:
  - name: mlops-api
    count: 5

images:
  - name: ghcr.io/user/mlops-api
    newTag: v1.0.0
```

### Build and Apply
```bash
# Build kustomization
kustomize build k8s/overlays/dev/

# Apply
kubectl apply -k k8s/overlays/dev/
kubectl apply -k k8s/overlays/prod/
```

---

## Helm (Package Manager)

### Install Helm
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Commands
```bash
# Add repo
helm repo add stable https://charts.helm.sh/stable
helm repo update

# Search
helm search repo mlflow

# Install chart
helm install my-mlflow stable/mlflow -n mlops

# List releases
helm list -n mlops

# Upgrade
helm upgrade my-mlflow stable/mlflow -n mlops --set replicas=3

# Rollback
helm rollback my-mlflow 1

# Uninstall
helm uninstall my-mlflow -n mlops
```

---

## Troubleshooting

### Pod not starting
```bash
# Check status
kubectl get pods
kubectl describe pod my-pod

# Common issues:
# - ImagePullBackOff: Wrong image name or no access
# - CrashLoopBackOff: App crashes on startup
# - Pending: Insufficient resources

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check logs
kubectl logs my-pod --previous  # Previous crashed container
```

### Service not accessible
```bash
# Check service
kubectl get svc
kubectl describe svc my-service

# Check endpoints
kubectl get endpoints my-service

# Port forward for testing
kubectl port-forward svc/my-service 8000:80
curl http://localhost:8000/health
```

### Resource issues
```bash
# Check node resources
kubectl top nodes
kubectl describe node my-node

# Check pod resources
kubectl top pods
kubectl describe pod my-pod
```

---

## Quick Reference

| Task | Docker | Kubernetes |
|------|--------|------------|
| Run | `docker run` | `kubectl run` |
| List | `docker ps` | `kubectl get pods` |
| Logs | `docker logs` | `kubectl logs` |
| Exec | `docker exec` | `kubectl exec` |
| Stop | `docker stop` | `kubectl delete pod` |
| Scale | N/A | `kubectl scale` |

---

## Resources

- [Docker docs](https://docs.docker.com/)
- [Kubernetes docs](https://kubernetes.io/docs/)
- [Kustomize](https://kustomize.io/)
- [Helm](https://helm.sh/)

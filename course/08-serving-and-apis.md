# Module 08: Serving & APIs

## 🎯 Goals

- Serve models via **FastAPI** REST endpoints
- Deploy with **Docker** and horizontal scaling
- Use **KServe** for Kubernetes-native serving
- Implement **health checks** and **readiness probes**
- Add **request validation** and error handling
- Monitor **API metrics** (latency, throughput)

---

## 📖 Key Terms

- **Model serving**: Exposing models via API for real-time predictions
- **FastAPI**: Modern Python web framework for building APIs (async, auto-docs)
- **KServe**: Kubernetes-native model serving framework (autoscaling, canary, A/B)
- **BentoML**: Model serving framework with built-in model management
- **Health check**: Endpoint to verify service is alive (/health)
- **Readiness probe**: Check if service is ready to accept traffic
- **Request validation**: Pydantic models for type-safe input/output

---

## 🔧 Commands First: FastAPI Model Server

```bash
# Create FastAPI serving script
cat > src/api.py << 'EOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import mlflow.sklearn
import numpy as np
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ML Model API", version="1.0.0")

# Load model at startup
MODEL_URI = "models:/ChurnPredictor/Production"
model = None

@app.on_event("startup")
async def load_model():
    global model
    try:
        mlflow.set_tracking_uri("http://mlflow:5000")
        model = mlflow.sklearn.load_model(MODEL_URI)
        logger.info(f"Model loaded from {MODEL_URI}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

# Request/Response models
class PredictionRequest(BaseModel):
    features: List[List[float]] = Field(..., example=[[5.1, 3.5, 1.4, 0.2]])
    
    class Config:
        schema_extra = {
            "example": {
                "features": [[5.1, 3.5, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]
            }
        }

class PredictionResponse(BaseModel):
    predictions: List[int]
    model_version: str = "1.0"

# Health endpoints
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    """Readiness check"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready", "model": MODEL_URI}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make predictions"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        X = np.array(request.features)
        predictions = model.predict(X).tolist()
        
        logger.info(f"Predicted {len(predictions)} samples")
        return PredictionResponse(predictions=predictions, model_version="1.0")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Metadata endpoint
@app.get("/model/info")
async def model_info():
    """Get model metadata"""
    return {
        "model_uri": MODEL_URI,
        "framework": "scikit-learn",
        "model_type": "RandomForestClassifier"
    }
EOF

# Run locally
pip install fastapi uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --reload &

# Test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}'

# View auto-generated docs
# Open http://localhost:8000/docs
```

**Why**: FastAPI provides async performance, automatic OpenAPI docs, type validation with Pydantic.

---

## 🐳 Dockerize API

```bash
# Create Dockerfile for serving
cat > Dockerfile.api << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-serve.txt .
RUN pip install --no-cache-dir -r requirements-serve.txt

# Copy API code
COPY src/api.py .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run with uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create requirements
cat > requirements-serve.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
mlflow==2.9.2
scikit-learn==1.3.2
numpy==1.26.2
EOF

# Build
docker build -f Dockerfile.api -t mlops-api:latest .

# Run
docker run -d -p 8000:8000 \
  -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 \
  --name mlops-api \
  mlops-api:latest

# Test
curl http://localhost:8000/health
```

**Why**: Docker ensures consistent environment. Health check enables orchestrator monitoring.

---

## ☸️ Deploy to Kubernetes with KServe

```bash
# Install KServe (assuming K8s cluster exists)
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/kserve.yaml

# Create InferenceService
cat > kserve-inference.yaml << 'EOF'
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: churn-predictor
  namespace: mlops
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "s3://mlops-artifacts/models/churn-predictor"
      resources:
        limits:
          cpu: "1"
          memory: "2Gi"
        requests:
          cpu: "100m"
          memory: "512Mi"
    minReplicas: 1
    maxReplicas: 5
    scaleTarget: 80  # Target 80% CPU utilization
EOF

kubectl apply -f kserve-inference.yaml

# Get endpoint
kubectl get inferenceservice churn-predictor -n mlops
```

**Why**: KServe provides autoscaling, canary deployments, A/B testing out-of-the-box on K8s.

---

## 📊 Add Metrics and Monitoring

```bash
# Enhanced API with Prometheus metrics
pip install prometheus-fastapi-instrumentator

cat > src/api_with_metrics.py << 'EOF'
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import mlflow.sklearn
import time
from prometheus_client import Counter, Histogram

app = FastAPI()

# Custom metrics
prediction_counter = Counter('predictions_total', 'Total predictions made')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')

# Enable built-in metrics
Instrumentator().instrument(app).expose(app)

@app.post("/predict")
async def predict(request: dict):
    start = time.time()
    
    # Load and predict (simplified)
    result = {"prediction": [1]}
    
    # Record metrics
    prediction_counter.inc()
    prediction_latency.observe(time.time() - start)
    
    return result

# Metrics endpoint at /metrics
EOF

# Prometheus scrape config
cat > prometheus.yml << 'EOF'
scrape_configs:
  - job_name: 'mlops-api'
    static_configs:
      - targets: ['mlops-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
EOF
```

**Why**: Prometheus metrics enable monitoring latency, throughput, errors in Grafana.

---

## 🧪 Load Testing

```bash
# Install locust for load testing
pip install locust

cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class ModelAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict(self):
        self.client.post("/predict", json={
            "features": [[5.1, 3.5, 1.4, 0.2]]
        })
    
    @task(3)  # 3x more frequent
    def health_check(self):
        self.client.get("/health")
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10
# Open http://localhost:8089 for UI
```

**Why**: Load testing finds performance bottlenecks, validates scaling behavior.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Deploy FastAPI model server and test.

1. **Create API**:
```bash
mkdir -p ~/mlops-lab-08 && cd ~/mlops-lab-08
# Copy api.py from above
```

2. **Run locally**:
```bash
uvicorn api:app --reload &
```

3. **Test endpoints**:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}'
```

4. **Dockerize**:
```bash
docker build -t lab08-api:latest .
docker run -p 8000:8000 lab08-api:latest
```

**Expected output**: API serves predictions, Swagger UI accessible, Docker container runs.

---

## ❓ Quiz (5 Questions)

1. **Why use FastAPI over Flask?**
   - Answer: Async support, automatic API docs (OpenAPI/Swagger), type validation with Pydantic, better performance.

2. **What is a health check?**
   - Answer: Endpoint (/health) that returns OK if service is alive, used by orchestrators for monitoring.

3. **What does KServe provide over basic K8s deployment?**
   - Answer: Autoscaling, canary deployments, A/B testing, request/response logging, model versioning.

4. **Why add Prometheus metrics to API?**
   - Answer: Monitor latency, throughput, errors; alert on anomalies; visualize in Grafana.

5. **What is the difference between health and readiness probes?**
   - Answer: Health = is service alive? Readiness = is service ready to accept traffic (model loaded)?

---

## ⚠️ Common Mistakes

1. **Loading model on every request** → High latency.  
   *Fix*: Load model once at startup.

2. **No input validation** → Crashes on bad data.  
   *Fix*: Use Pydantic models for request validation.

3. **Synchronous API** → Low throughput under load.  
   *Fix*: Use FastAPI async endpoints for I/O operations.

4. **No health checks** → K8s can't detect unhealthy pods.  
   *Fix*: Implement /health and /ready endpoints.

5. **Single replica in production** → No redundancy.  
   *Fix*: Deploy multiple replicas with load balancer.

---

## 🛠️ Troubleshooting

**Issue**: "API returns 503 Service Unavailable"  
→ **Root cause**: Model failed to load at startup.  
→ **Fix**: Check MLflow connectivity, verify model exists in registry, check logs.  
→ **See**: `/troubleshooting/triage-matrix.md` row "API 503 errors"

**Issue**: "High latency (>1 second per prediction)"  
→ **Root cause**: Model too large, loading on each request, or no batching.  
→ **Fix**: Load model once, enable batching, optimize model (quantization, pruning).  
→ **See**: `/troubleshooting/triage-matrix.md` row "High API latency"

---

## 📚 Key Takeaways

- **FastAPI** provides async performance + auto-docs + type validation
- **Load model once** at startup, not per request
- **Health/readiness checks** enable orchestrator monitoring
- **Pydantic** validates requests, prevents runtime errors
- **KServe** adds autoscaling, canary, A/B testing on K8s
- **Prometheus metrics** enable monitoring and alerting

---

## 🚀 Next Steps

- **Module 09**: Batch and streaming inference
- **Module 10**: CI/CD pipelines for automated deployment
- **Hands-on**: Deploy Churn Predictor API to K8s with autoscaling

---

**[← Module 07](07-model-registry-and-governance.md)** | **[Next: Module 09 →](09-batch-streaming-and-scheduled-jobs.md)**

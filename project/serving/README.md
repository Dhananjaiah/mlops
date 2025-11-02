# Serving Directory

This directory contains the serving configuration and deployment files for the ML model API.

## Files

- **Dockerfile.api**: Docker configuration for building the FastAPI serving container
- **kserve-inference.yaml**: Kubernetes InferenceService configuration for KServe deployment

## Usage

### Docker Build

```bash
# Build the API image
docker build -f serving/Dockerfile.api -t mlops-api:latest .

# Run the API container
docker run -d -p 8000:8000 \
  -e MLFLOW_TRACKING_URI=http://mlflow:5000 \
  -e MLFLOW_S3_ENDPOINT_URL=http://minio:9000 \
  -e AWS_ACCESS_KEY_ID=minioadmin \
  -e AWS_SECRET_ACCESS_KEY=minioadmin \
  --name mlops-api \
  mlops-api:latest
```

### Docker Compose

```bash
# Start all services including the API
docker compose up -d

# Check API status
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Kubernetes with KServe

```bash
# Deploy the InferenceService
kubectl apply -f serving/kserve-inference.yaml

# Check status
kubectl get inferenceservice churn-predictor -n mlops
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /ready` - Readiness probe
- `POST /predict` - Make predictions
- `GET /model/info` - Get model metadata
- `GET /docs` - Interactive API documentation (Swagger UI)

# Module 11: Observability & Monitoring

## 🎯 Goals

- Monitor **infrastructure metrics** (CPU, memory, network)
- Track **application metrics** (latency, throughput, errors)
- Log **ML-specific metrics** (predictions, confidence, drift)
- Build **Grafana dashboards** for visualization
- Set up **alerts** for anomalies and SLO violations
- Use **distributed tracing** (OpenTelemetry) for debugging

---

## 📖 Key Terms

- **Observability**: Ability to understand system internal state from external outputs
- **Metrics**: Time-series numerical data (counters, gauges, histograms)
- **Prometheus**: Time-series database and monitoring system
- **Grafana**: Visualization and dashboarding platform
- **SLI/SLO/SLA**: Service Level Indicator/Objective/Agreement (metrics, targets, contracts)
- **RED method**: Rate, Errors, Duration (key API metrics)
- **Golden signals**: Latency, traffic, errors, saturation

---

## 🔧 Commands First: Prometheus Setup

```bash
# Install Prometheus (Docker)
docker run -d -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Prometheus config
cat > prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'mlops-api'
    static_configs:
      - targets: ['mlops-api:8000']
    metrics_path: '/metrics'
  
  - job_name: 'mlflow'
    static_configs:
      - targets: ['mlflow:5000']
  
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

rule_files:
  - 'alerts.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
EOF

# Open http://localhost:9090
```

**Why**: Prometheus scrapes metrics from services. Centralized monitoring for entire ML platform.

---

## 📊 Add Custom ML Metrics

```bash
# Enhanced API with ML metrics
pip install prometheus-client

cat > src/api_with_ml_metrics.py << 'EOF'
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import mlflow.sklearn
import time
import numpy as np

app = FastAPI()

# Define metrics
predictions_total = Counter('predictions_total', 'Total predictions', ['model_version'])
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')
prediction_confidence = Histogram('prediction_confidence', 'Prediction confidence')
model_loaded = Gauge('model_loaded', 'Model loaded successfully')
api_errors = Counter('api_errors_total', 'API errors', ['error_type'])

# Load model
try:
    model = mlflow.sklearn.load_model("models:/ChurnPredictor/Production")
    model_loaded.set(1)
except Exception as e:
    model_loaded.set(0)
    raise

@app.post("/predict")
async def predict(features: list):
    start = time.time()
    
    try:
        X = np.array(features)
        predictions = model.predict(X)
        
        # Try to get prediction probabilities
        if hasattr(model, 'predict_proba'):
            probas = model.predict_proba(X)
            confidence = np.max(probas, axis=1).mean()
            prediction_confidence.observe(confidence)
        
        # Record metrics
        predictions_total.labels(model_version='1.0').inc(len(predictions))
        prediction_latency.observe(time.time() - start)
        
        return {"predictions": predictions.tolist()}
    
    except Exception as e:
        api_errors.labels(error_type=type(e).__name__).inc()
        raise

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": bool(model_loaded._value.get())}
EOF
```

**Why**: Custom metrics track ML-specific behavior: prediction rate, confidence, model load status.

---

## 📈 Grafana Dashboard

```bash
# Install Grafana
docker run -d -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana

# Add Prometheus datasource (in Grafana UI: Configuration → Data Sources)
# Name: Prometheus
# URL: http://prometheus:9090

# Create dashboard JSON
cat > grafana-dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "ML API Monitoring",
    "panels": [
      {
        "title": "Predictions Per Second",
        "targets": [{"expr": "rate(predictions_total[5m])"}],
        "type": "graph"
      },
      {
        "title": "P95 Latency",
        "targets": [{"expr": "histogram_quantile(0.95, prediction_latency_seconds)"}],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [{"expr": "rate(api_errors_total[5m])"}],
        "type": "graph"
      },
      {
        "title": "Average Confidence",
        "targets": [{"expr": "avg(prediction_confidence)"}],
        "type": "gauge"
      }
    ]
  }
}
EOF

# Import dashboard in Grafana UI: Dashboards → Import → Upload JSON
```

**Why**: Dashboards visualize key metrics: throughput, latency, errors, confidence. Quick diagnosis.

---

## 🚨 Alerting Rules

```bash
# Create alert rules
cat > alerts.yml << 'EOF'
groups:
  - name: mlops_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(api_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High API error rate"
          description: "Error rate is {{ $value }} errors/sec"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, prediction_latency_seconds) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High prediction latency"
          description: "P95 latency is {{ $value }}s"
      
      - alert: ModelNotLoaded
        expr: model_loaded == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Model failed to load"
          description: "Model is not loaded in API"
      
      - alert: LowConfidence
        expr: avg(prediction_confidence) < 0.6
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low prediction confidence"
          description: "Average confidence is {{ $value }}"
EOF

# Reload Prometheus
curl -X POST http://localhost:9090/-/reload
```

**Why**: Alerts notify on-call engineers of issues. Proactive response before users notice.

---

## 🔍 Distributed Tracing

```bash
# Install OpenTelemetry
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi

cat > src/api_with_tracing.py << 'EOF'
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

app = FastAPI()

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@app.post("/predict")
async def predict(features: list):
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("load_model"):
        # Model loading logic
        pass
    
    with tracer.start_as_current_span("preprocess"):
        # Preprocessing logic
        pass
    
    with tracer.start_as_current_span("inference"):
        # Prediction logic
        pass
    
    return {"predictions": [1, 0]}
EOF

# Run Jaeger for trace visualization
docker run -d -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
# Open http://localhost:16686
```

**Why**: Tracing shows request flow through services. Debug latency bottlenecks, identify slow components.

---

## 📊 SLO Monitoring

```bash
# Define SLOs
cat > slos.yaml << 'EOF'
slos:
  - name: api_availability
    description: "API should be available 99.9% of time"
    target: 0.999
    metric: up{job="mlops-api"}
  
  - name: api_latency
    description: "95% of requests complete in < 500ms"
    target: 0.95
    metric: histogram_quantile(0.95, prediction_latency_seconds) < 0.5
  
  - name: api_success_rate
    description: "99% of requests succeed"
    target: 0.99
    metric: rate(predictions_total[5m]) / (rate(predictions_total[5m]) + rate(api_errors_total[5m]))
EOF

# Monitor SLO compliance in Grafana
# Create SLO dashboard showing:
# - Current SLO compliance %
# - Error budget remaining
# - Burn rate
```

**Why**: SLOs quantify reliability. Track error budget to balance features vs stability.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Set up Prometheus and Grafana, monitor API metrics.

1. **Start Prometheus and Grafana**:
```bash
mkdir -p ~/mlops-lab-11 && cd ~/mlops-lab-11
docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
docker run -d -p 3000:3000 grafana/grafana
```

2. **Run API with metrics**:
```bash
# Copy api_with_ml_metrics.py
uvicorn api_with_ml_metrics:app --host 0.0.0.0 --port 8000 &
```

3. **Generate load**:
```bash
for i in {1..100}; do
  curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features": [[5.1, 3.5, 1.4, 0.2]]}'
done
```

4. **View metrics**:
```bash
# Prometheus: http://localhost:9090
# Query: rate(predictions_total[1m])
# Grafana: http://localhost:3000 (admin/admin)
# Add Prometheus datasource, create graph
```

**Expected output**: Metrics visible in Prometheus, graphs in Grafana.

---

## ❓ Quiz (5 Questions)

1. **What are the four golden signals?**
   - Answer: Latency, traffic, errors, saturation.

2. **What is the difference between metrics and logs?**
   - Answer: Metrics = aggregated time-series numbers. Logs = discrete event records.

3. **Why use distributed tracing?**
   - Answer: Debug request flow across services, identify latency bottlenecks.

4. **What is an SLO?**
   - Answer: Service Level Objective—internal target for reliability (e.g., 99.9% uptime).

5. **When should alerts fire?**
   - Answer: When SLOs are at risk or violated, not for every minor event (avoid alert fatigue).

---

## ⚠️ Common Mistakes

1. **Too many alerts** → Alert fatigue, ignored pages.  
   *Fix*: Alert only on SLO violations, actionable issues.

2. **No dashboards** → Blind to system health.  
   *Fix*: Build dashboards for golden signals + ML metrics.

3. **Not monitoring model metrics** → Miss drift, confidence drops.  
   *Fix*: Track prediction rate, confidence, feature distributions.

4. **Long scrape intervals** → Miss short-lived issues.  
   *Fix*: Use 15s scrape interval for real-time visibility.

5. **No log aggregation** → Debugging requires SSH to every pod.  
   *Fix*: Use ELK, Loki, or CloudWatch Logs for centralized logging.

---

## 🛠️ Troubleshooting

**Issue**: "Prometheus not scraping targets"  
→ **Root cause**: Wrong endpoint, firewall, or service discovery issue.  
→ **Fix**: Check Prometheus UI → Targets, verify /metrics accessible, check network policies.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Prometheus scrape failures"

**Issue**: "Grafana dashboard shows no data"  
→ **Root cause**: Wrong datasource, query error, or time range issue.  
→ **Fix**: Test query in Prometheus first, check Grafana datasource config, adjust time range.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Grafana no data"

---

## 📚 Key Takeaways

- **Observability** = metrics + logs + traces for understanding system behavior
- **Prometheus** scrapes metrics, **Grafana** visualizes, **Alertmanager** notifies
- **Track golden signals**: latency, traffic, errors, saturation
- **ML-specific metrics**: prediction rate, confidence, feature distributions
- **SLOs** quantify reliability targets, guide incident response
- **Distributed tracing** debugs complex request flows

---

## 🚀 Next Steps

- **Module 12**: Drift detection and automated retraining triggers
- **Module 13**: Security, compliance, and cost optimization
- **Hands-on**: Build comprehensive monitoring for Churn Predictor

---

**[← Module 10](10-ci-cd-and-environments.md)** | **[Next: Module 12 →](12-drift-detection-and-retraining.md)**

# Lecture 12.4 – Logging & Tracing for Model Services

## Human Transcript

Logs tell you what happened. Traces tell you the journey of a request.

**Structured Logging**: JSON logs with consistent fields. Searchable, parseable.
```python
logger.info("Prediction made", extra={
    "request_id": req_id,
    "model_version": "v1.2",
    "latency_ms": 45,
    "prediction": 1
})
```

**Distributed Tracing**: Track requests across services. Use OpenTelemetry, Jaeger, or Zipkin.

**What to log for ML**:
- Input features (sampled, for debugging)
- Model version used
- Prediction and confidence
- Latency breakdown
- Any errors or warnings

Balance detail vs volume. Log enough to debug, not so much that storage explodes.

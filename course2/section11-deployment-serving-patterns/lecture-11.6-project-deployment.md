# Lecture 11.6 – Designing a Simple Production-Like Deployment for Our Project

## Human Transcript

Let's design our churn model deployment. Here's the architecture:

```
Internet → Load Balancer → Kubernetes Cluster
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────▼─────┐       ┌─────▼─────┐
              │  Model    │       │  Model    │
              │ Pod (v1)  │       │ Pod (v2)  │
              │  90%      │       │  10%      │
              └───────────┘       └───────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Model Registry   │
                    │    (MLflow)       │
                    └───────────────────┘
```

Key components:
1. FastAPI service in Docker container
2. Kubernetes deployment with 3 replicas
3. Service for internal load balancing
4. Ingress for external access
5. HorizontalPodAutoscaler for dynamic scaling
6. ConfigMap for configuration
7. Secrets for credentials

This gives us: high availability, auto-scaling, canary capability, and easy rollbacks.

Start simple, add complexity as needed. A well-configured single service is better than a poorly managed complex system.

This concludes Section 11 on deployment architectures.

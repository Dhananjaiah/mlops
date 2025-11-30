# Lecture 11.4 – Basic Kubernetes Concepts for MLOps

## Human Transcript

You don't need to be a Kubernetes expert, but you need to understand the basics.

**Pod**: Smallest deployable unit. Contains one or more containers. Your model runs in a pod.

**Deployment**: Manages pods. Defines how many replicas, handles rolling updates, auto-restarts failed pods.

**Service**: Stable network endpoint for pods. Pods come and go, services stay.

**Ingress**: External access to services. Routes traffic from outside the cluster.

Basic deployment manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: churn-model
  template:
    spec:
      containers:
      - name: model
        image: registry/churn-model:v1
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

Key MLOps considerations: resource limits, health checks, horizontal pod autoscaling, GPU scheduling.

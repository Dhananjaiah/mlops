# Lecture 11.3 – Deploying on VM vs Docker Swarm vs Kubernetes

## Human Transcript

Where do you run your model service? Here are the main options:

**Virtual Machines (VMs)**: Simple to understand. SSH in, run your app. Good for: small scale, simple deployments. Bad for: scaling, resource efficiency, automation.

**Docker Swarm**: Docker's native orchestration. Easier than Kubernetes, good for smaller teams. Handles basic scaling and service discovery.

**Kubernetes**: The industry standard for container orchestration. Complex but powerful. Auto-scaling, self-healing, declarative configuration. Essential for large-scale ML deployments.

My recommendation:
- Learning/prototypes: VM or local Docker
- Small production: Docker Swarm or managed container service (ECS, Cloud Run)
- Production at scale: Kubernetes (preferably managed: EKS, GKE, AKS)

Most enterprises end up on Kubernetes because they need the scaling and operational capabilities it provides.

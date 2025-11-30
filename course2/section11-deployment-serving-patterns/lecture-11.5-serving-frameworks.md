# Lecture 11.5 – Model Serving Frameworks (KFServing, Seldon, BentoML)

## Human Transcript

You don't have to build everything from scratch. Model serving frameworks handle common patterns.

**KServe (formerly KFServing)**: Kubernetes-native, supports multiple frameworks, auto-scaling, canary deployments. Great for standardized serving on K8s.

**Seldon Core**: Feature-rich, supports complex inference graphs, A/B testing, explainability. Enterprise-focused.

**BentoML**: Developer-friendly, packages models with API in one artifact, supports multiple deployment targets.

**TensorFlow Serving / TorchServe**: Framework-specific, highly optimized for their respective models.

**Triton Inference Server (NVIDIA)**: Multi-framework, optimized for GPU, supports batching and model ensembles.

Choose based on:
- Your ML framework (TensorFlow, PyTorch, sklearn)
- Infrastructure (Kubernetes vs serverless)
- Team expertise
- Features needed (A/B testing, explainability, batching)

For most teams, start with BentoML or a simple FastAPI service, then graduate to KServe or Seldon when you need advanced features.

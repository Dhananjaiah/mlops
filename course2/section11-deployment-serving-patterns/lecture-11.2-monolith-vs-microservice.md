# Lecture 11.2 – Monolith vs Microservice Model APIs

## Human Transcript

Should your model be part of a larger application or its own service? Let's compare.

**Monolith**: Model embedded in main application. Simpler deployment, lower latency for internal calls. But: harder to scale model independently, updates require full app redeploy.

**Microservice**: Model as standalone API. Independent scaling, independent deployment, can use different tech stack. But: network latency, more infrastructure complexity.

For ML, microservices usually win because:
- Models need different scaling (GPU vs CPU)
- Models update more frequently than app code
- Different teams own different models
- Easier to A/B test model versions

Start simple with a monolith for prototypes, but plan for microservices in production.

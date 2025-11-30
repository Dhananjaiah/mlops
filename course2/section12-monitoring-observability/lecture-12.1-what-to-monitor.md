# Lecture 12.1 – What to Monitor in ML Systems (Infra, App, Model)

## Human Transcript

Welcome to Section 12 on monitoring. ML systems have three layers to monitor:

**Infrastructure**: CPU, memory, disk, network. Is your server healthy?

**Application**: Request count, error rate, latency. Is your API working?

**Model**: Prediction distribution, feature drift, accuracy. Is your model still correct?

Traditional software stops at layer 2. ML adds layer 3, which is unique and critical.

A model can be "working" (returning predictions) but "wrong" (predictions are garbage). You need model-specific monitoring to catch this.

# Lecture 12.2 – Metrics: Latency, Error Rate, Throughput, Resource Usage

## Human Transcript

Standard application metrics you must track:

**Latency**: How long requests take. Track p50, p95, p99 percentiles. P99 matters most - your worst 1% of users.

**Error Rate**: Percentage of failed requests. 5xx errors (server), 4xx errors (client). Alert on sudden increases.

**Throughput**: Requests per second. Know your baseline, alert on anomalies (too high or too low).

**Resource Usage**: CPU, memory, GPU utilization. High usage = capacity planning needed. Low usage = over-provisioned.

Set baselines, then alert on deviations. What's normal for your system? Then watch for changes.

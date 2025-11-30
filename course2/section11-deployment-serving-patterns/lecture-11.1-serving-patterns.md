# Lecture 11.1 – Online vs Offline vs Near-Real-Time Serving

## Human Transcript

Welcome to Section 11 on deployment architectures. Let's start by understanding the three main serving patterns.

**Online (Real-time) Serving**: Predictions happen on-demand, in milliseconds. User makes a request, model responds immediately. Examples: fraud detection at checkout, recommendation when user opens app.

**Offline (Batch) Serving**: Predictions are pre-computed for all entities on a schedule. Results stored in database. Examples: next-day delivery estimates computed overnight, weekly churn risk scores.

**Near-Real-Time Serving**: A middle ground. Predictions computed with slight delay (seconds to minutes) often using streaming. Examples: dynamic pricing updated every minute, real-time dashboards.

Choosing the right pattern depends on:
- Latency requirements (milliseconds vs hours)
- Data freshness needs
- Compute costs
- Infrastructure complexity

Most production systems use a combination. Batch for bulk predictions, online for high-value real-time decisions.

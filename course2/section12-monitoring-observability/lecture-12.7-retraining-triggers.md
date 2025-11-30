# Lecture 12.7 – Closing the Loop: Retraining Triggers & Feedback

## Human Transcript

Monitoring should drive action. When drift is detected, retrain.

**Retraining triggers**:
- Scheduled: Weekly/monthly regardless of drift
- Drift-based: Automatic when drift exceeds threshold
- Performance-based: When accuracy drops
- Manual: Data scientist decides

**Feedback loops**:
```
Production predictions → Collect outcomes → Compare to predictions → Measure accuracy → Trigger retraining
```

**Implementation**:
```python
def check_retraining_needed(drift_score, accuracy, thresholds):
    if drift_score > thresholds['drift']:
        return True, "drift_detected"
    if accuracy < thresholds['accuracy']:
        return True, "accuracy_degradation"
    return False, None
```

The goal: a self-healing system that maintains quality automatically.

This concludes Section 12 on monitoring.

# Lecture 12.6 – Alerts & Incident Response Playbooks for ML

## Human Transcript

Alerts notify you when something's wrong. Playbooks tell you what to do.

**Good alert design**:
- Actionable: Someone can do something about it
- Clear: Explains what's wrong
- Prioritized: Critical vs warning vs info

**ML-specific alerts**:
- Model latency > 500ms for 5 minutes
- Error rate > 1% for 10 minutes
- Prediction drift score > threshold
- Feature null rate > 10%

**Incident playbooks**:
```
ALERT: High Error Rate
1. Check error logs for patterns
2. Verify model is loaded correctly
3. Check input data quality
4. If model issue, rollback to previous version
5. If data issue, contact data team
6. Update incident channel with status
```

Document your playbooks. When 3am incidents happen, you don't want to think - you want to follow steps.

# Lecture 12.3 – Model-Specific Metrics: Drift, Data Skew, Concept Drift

## Human Transcript

ML-specific monitoring concepts:

**Data Drift**: Input features change distribution. Model trained on data from 2022, but 2024 data looks different.

**Concept Drift**: The relationship between features and target changes. What predicted churn last year doesn't predict it now.

**Prediction Drift**: Model outputs shift unexpectedly. Suddenly predicting more positives than usual.

Detection methods:
- Statistical tests (KS test, PSI)
- Distribution comparisons
- Reference windows

```python
def detect_drift(reference_data, current_data):
    from scipy.stats import ks_2samp
    
    for col in reference_data.columns:
        stat, p_value = ks_2samp(reference_data[col], current_data[col])
        if p_value < 0.05:
            print(f"Drift detected in {col}")
```

Monitor drift continuously. It's the leading indicator of model degradation.

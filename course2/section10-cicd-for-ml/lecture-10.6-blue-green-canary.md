# Lecture 10.6 – Blue/Green & Canary Deployments for ML Services

## Human Transcript

Let's talk about deployment strategies that minimize risk. Blue/green and canary deployments are essential for production ML systems.

Blue/Green deployment: You have two identical environments. Blue is live, green is standby. Deploy to green, test it, then switch traffic.

```yaml
# Blue/Green with Kubernetes
apiVersion: v1
kind: Service
metadata:
  name: churn-model
spec:
  selector:
    app: churn-model
    version: blue  # Switch to 'green' to cutover
  ports:
    - port: 80
      targetPort: 8000
```

Canary deployment: Gradually shift traffic to the new version. Start with 5%, monitor, increase to 25%, then 50%, then 100%.

```yaml
# Canary with Istio
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: churn-model
spec:
  hosts:
    - churn-model
  http:
    - route:
        - destination:
            host: churn-model
            subset: stable
          weight: 90
        - destination:
            host: churn-model
            subset: canary
          weight: 10
```

For ML specifically, canary deployments let you compare model performance in real-time:

```python
def compare_canary_metrics(stable_metrics, canary_metrics):
    comparisons = {
        'accuracy_diff': canary_metrics['accuracy'] - stable_metrics['accuracy'],
        'latency_diff': canary_metrics['p99_latency'] - stable_metrics['p99_latency'],
        'error_rate_diff': canary_metrics['error_rate'] - stable_metrics['error_rate']
    }
    
    # Canary should be at least as good
    should_promote = (
        comparisons['accuracy_diff'] >= -0.02 and
        comparisons['latency_diff'] <= 10 and
        comparisons['error_rate_diff'] <= 0.01
    )
    
    return should_promote, comparisons
```

Best practice: Start with 5% traffic, wait 1 hour, check metrics. If good, increase to 25%, wait 4 hours. Then 50% for 24 hours. Only then go to 100%.

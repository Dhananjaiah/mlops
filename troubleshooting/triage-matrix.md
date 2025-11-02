# MLOps Troubleshooting Triage Matrix

## How to Use This Matrix

1. Find your **Symptom** in the table
2. Run **Triage Commands** to gather information
3. Identify **Likely Root Cause**
4. Apply the **Fix**
5. Run **Verify** commands to confirm resolution
6. Implement **Prevention** measures

---

## Training & Experiments

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **Training OOM (Out of Memory)** | `kubectl top pods`<br>`docker stats`<br>`htop` | Batch size too large<br>Model too big<br>Memory leak | Reduce batch size<br>Use gradient checkpointing<br>Increase pod memory | Training completes | Set memory limits<br>Monitor memory usage<br>Use smaller models or mixed precision |
| **Training slow** | `nvidia-smi`<br>`top`<br>Check I/O wait | No GPU acceleration<br>Data loading bottleneck<br>Small batch size | Enable CUDA<br>Use DataLoader with workers<br>Increase batch size | Training time <50% of baseline | Profile code<br>Use GPU<br>Optimize data pipeline |
| **CUDA not found** | `nvidia-smi`<br>`nvcc --version`<br>`python -c "import torch; print(torch.cuda.is_available())"` | Drivers not installed<br>Wrong PyTorch version<br>Container without GPU | Install NVIDIA drivers<br>Install CUDA-enabled PyTorch<br>Use GPU-enabled base image | `torch.cuda.is_available() == True` | Use pre-built ML containers<br>Document GPU requirements |
| **Model overfits** | Plot train vs val loss<br>Check params | Model too complex<br>Insufficient data<br>Data leakage | Add regularization<br>Collect more data<br>Check for leakage | Val loss decreases | Use cross-validation<br>Monitor val metrics<br>Check data splits |
| **Non-reproducible results** | Check random seeds<br>Check DVC versions<br>Check library versions | Random seed not set<br>Data changed<br>Library versions differ | Set all random seeds<br>Version data with DVC<br>Pin dependencies | Same metrics on rerun | Lock all seeds<br>Version everything<br>Use lock files |

---

## MLflow & Artifacts

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **MLflow offline or empty** | `curl http://mlflow:5000`<br>`docker ps \| grep mlflow`<br>`kubectl get pods -n mlops` | Server not running<br>Wrong tracking URI<br>Database offline | Start MLflow server<br>Set `MLFLOW_TRACKING_URI`<br>Check DB connection | MLflow UI loads<br>Experiments visible | Health checks<br>Monitor MLflow<br>Use persistent DB |
| **Artifact upload fails** | `aws s3 ls s3://bucket/`<br>Check S3 permissions<br>Check network | No S3 permissions<br>Bucket doesn't exist<br>Network issue | Add IAM policy<br>Create bucket<br>Check network rules | `mlflow.log_artifact()` succeeds | Set up IAM roles<br>Pre-create buckets<br>Test connectivity |
| **Model registration fails** | `mlflow models list`<br>Check run exists<br>Check artifact path | Run doesn't exist<br>Artifact missing<br>Model format invalid | Verify run_id<br>Check artifact was logged<br>Use correct log function | Model appears in registry | Validate before registering<br>Use MLflow autolog |
| **Can't load model** | Check model URI<br>`mlflow models list`<br>Check model stage | Wrong stage<br>Model archived<br>Version deleted | Use correct stage/version<br>Restore from archive | `mlflow.sklearn.load_model()` works | Document model URIs<br>Don't delete prod models |

---

## DVC & Data

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **DVC remote access denied** | `dvc remote list`<br>`aws s3 ls s3://bucket/`<br>Check credentials | Missing credentials<br>Wrong bucket<br>IAM permissions | Set AWS credentials<br>Verify bucket name<br>Add IAM policy | `dvc push` succeeds | Use IAM roles<br>Document setup<br>Test in CI |
| **DVC pipeline not rerunning** | `dvc status`<br>`dvc dag` | Cached, no changes<br>Dependencies not tracked | `dvc repro --force`<br>Add `-d` for dependencies | Pipeline reruns | Track all dependencies<br>Use checksums |
| **Data schema mismatch** | Check column names<br>Check dtypes<br>Sample data | Schema changed<br>Wrong data version<br>Preprocessing bug | Update schema<br>Pull correct DVC version<br>Fix preprocessing | Data loads without errors | Validate schema<br>Version data<br>Document changes |

---

## API & Serving

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **API 500 errors** | Check logs<br>`curl /health`<br>`kubectl logs pod-name` | Model not loaded<br>Input validation failed<br>Dependency missing | Load model at startup<br>Add Pydantic validation<br>Install dependencies | `curl /predict` returns 200 | Health checks<br>Input validation<br>Test in CI |
| **API 503 Service Unavailable** | `curl /ready`<br>Check pod status<br>Check model loading | Model failed to load<br>MLflow unreachable<br>Resource exhaustion | Fix model URI<br>Check MLflow connectivity<br>Increase resources | `/ready` returns 200 | Readiness probes<br>Monitor resources |
| **High API latency** | Trace requests<br>Profile code<br>`kubectl top pods` | Large model<br>No batching<br>CPU throttling | Optimize model<br>Batch requests<br>Increase CPU | P95 latency <500ms | Load test<br>Monitor latency<br>Autoscale |
| **Request validation errors** | Check request schema<br>Check Pydantic model | Wrong input format<br>Missing fields<br>Type mismatch | Fix request format<br>Update Pydantic model<br>Add examples in docs | Valid requests succeed | OpenAPI docs<br>Request examples<br>Validate in tests |

---

## Airflow & Pipelines

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **Airflow webserver fails** | `lsof -i :8080`<br>`airflow db check`<br>Check logs | Port in use<br>DB not initialized<br>Config error | Kill process on port<br>`airflow db init`<br>Fix airflow.cfg | Webserver starts | Document setup<br>Use docker-compose |
| **Airflow DAG not loaded** | `airflow dags list`<br>Check DAG file syntax<br>Check dags_folder | Python syntax error<br>Not in dags_folder<br>Import error | Fix syntax<br>Move to dags_folder<br>Install dependencies | DAG appears in UI | Pre-commit hooks<br>Test DAGs locally |
| **Airflow task stuck** | `airflow tasks state`<br>`kubectl get pods`<br>Check logs | Resource exhaustion<br>Upstream failure<br>Deadlock | Increase resources<br>Fix upstream task<br>Clear and retry | Task completes | Set timeouts<br>Monitor resources<br>Add retries |

---

## Kubernetes & Deployment

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **CrashLoopBackOff** | `kubectl describe pod`<br>`kubectl logs pod-name`<br>Check events | App crashes on start<br>Wrong command<br>Missing dependencies | Fix startup code<br>Correct CMD/entrypoint<br>Install deps | Pod runs | Test image locally<br>Add health checks |
| **ImagePullBackOff** | `kubectl describe pod`<br>Check image name<br>Check registry auth | Wrong image name<br>Image doesn't exist<br>Registry auth failed | Fix image tag<br>Build and push image<br>Add imagePullSecrets | Pod pulls image | Verify image exists<br>Test pull<br>CI builds image |
| **K8s deployment stuck** | `kubectl get pods`<br>`kubectl describe deployment`<br>`kubectl get events` | Insufficient resources<br>Image pull failure<br>Readiness probe failing | Increase cluster resources<br>Fix image<br>Fix probe | Deployment rolls out | Resource requests<br>Quotas<br>Test deploys |
| **Autoscaler thrash** | Check HPA metrics<br>`kubectl get hpa`<br>Monitor CPU | Metrics wrong<br>Thresholds too sensitive<br>Traffic spike | Fix metrics server<br>Adjust thresholds<br>Scale manually | Stable replica count | Tune autoscaling<br>Load test<br>Monitor closely |

---

## Monitoring & Alerts

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **Prometheus scrape failures** | Check Prometheus UI → Targets<br>`curl /metrics`<br>Check network | Wrong endpoint<br>Firewall blocks<br>Service down | Fix metrics path<br>Open firewall<br>Start service | Targets up in Prometheus | Test metrics endpoint<br>Document ports |
| **Grafana no data** | Test query in Prometheus<br>Check datasource<br>Adjust time range | Wrong datasource<br>Query error<br>No data in range | Fix datasource URL<br>Fix PromQL<br>Adjust time | Data appears in Grafana | Test queries<br>Document dashboards |
| **Alert fatigue** | Check alert frequency<br>Review thresholds | Thresholds too sensitive<br>Flapping<br>Too many alerts | Adjust thresholds<br>Add `for: 5m`<br>Consolidate alerts | Only actionable alerts | Tune carefully<br>Review regularly |
| **False drift alerts** | Check baseline data<br>Check thresholds<br>Review distributions | Wrong baseline<br>Thresholds too tight<br>Seasonal patterns | Update baseline<br>Relax thresholds<br>Account for seasonality | Alerts match reality | Rolling baselines<br>Validate thresholds |

---

## Security & Compliance

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **CI security scan failures** | Check Trivy report<br>Check CVE details | HIGH/CRITICAL CVE<br>Outdated dependency<br>Vulnerable base image | Update package<br>Use newer base image<br>Suppress false positive | Scan passes | Regular updates<br>Minimal images<br>SBOM tracking |
| **Secrets in git** | `gitleaks detect`<br>Check git history | Accidental commit<br>No pre-commit hook | Remove from history<br>Rotate secret<br>Install gitleaks hook | No secrets detected | Pre-commit hooks<br>Secrets manager<br>`.gitignore` |
| **RBAC permission denied** | `kubectl auth can-i`<br>Check Role/RoleBinding<br>Check service account | Wrong service account<br>Missing permissions<br>Namespace mismatch | Fix service account<br>Add permissions<br>Use correct namespace | Action succeeds | Test RBAC<br>Document permissions<br>Least privilege |

---

## Cost & Performance

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **Cost spike** | Check cloud billing<br>Check resource usage<br>`kubectl top` | Runaway training<br>No autoscaling down<br>Resource leak | Stop runaway jobs<br>Enable scale-down<br>Clean up resources | Costs normal | Budgets<br>Alerts<br>Quotas<br>Right-sizing |
| **Batch job OOM** | Check memory usage<br>Check batch size<br>Profile code | Batch too large<br>Memory leak<br>Large model | Use chunked reading<br>Fix leak<br>Increase memory | Job completes | Test with production data<br>Monitor memory |
| **Kafka consumer lag** | `kafka-consumer-groups --describe`<br>Check throughput | Too slow inference<br>Single consumer<br>Network issue | Optimize inference<br>Add consumers<br>Check network | Lag decreases | Batch predictions<br>Scale consumers<br>Monitor lag |
| **Slow hyperparameter tuning** | Profile training<br>Check parallelization | Serial execution<br>Too many configs<br>Slow eval | Use parallel (n_jobs=-1)<br>Random search<br>Early stopping | Tuning faster | Use RandomSearch<br>Parallelize<br>Sample hyperparams |

---

## General Debugging

| Symptom | Triage Commands | Likely Root Causes | Fix | Verify | Prevent |
|---------|----------------|-------------------|-----|--------|---------|
| **"It works on my machine"** | Compare environments<br>Check versions<br>Check configs | Different dependencies<br>Different env vars<br>Different data | Pin dependencies<br>Use .env files<br>Version data | Works everywhere | Docker<br>Lock files<br>Document setup |
| **Intermittent failures** | Check logs over time<br>Check network<br>Check resource usage | Race condition<br>Network flakiness<br>Resource contention | Add retries<br>Fix race<br>Increase resources | Reliable execution | Idempotency<br>Retries<br>Monitoring |
| **Can't reproduce issue** | Check exact versions<br>Check data<br>Check random seeds | Different data version<br>Non-deterministic<br>Different config | Version data<br>Set random seeds<br>Document config | Issue reproduces | Version everything<br>Document thoroughly |

---

## Quick Reference: Debugging Commands

```bash
# Kubernetes
kubectl get pods -n mlops
kubectl describe pod <pod-name> -n mlops
kubectl logs <pod-name> -n mlops --tail=100
kubectl exec -it <pod-name> -n mlops -- /bin/bash

# Docker
docker ps
docker logs <container-id> --tail=100
docker stats
docker exec -it <container-id> /bin/bash

# MLflow
curl http://localhost:5000/health
mlflow runs list --experiment-name <name>
mlflow models list

# DVC
dvc status
dvc dag
dvc repro --force

# Airflow
airflow dags list
airflow tasks list <dag-id>
airflow tasks logs <dag-id> <task-id> <execution-date>

# Monitoring
curl http://localhost:9090/api/v1/targets  # Prometheus
curl http://localhost:8000/metrics  # App metrics
```

---

## Escalation Path

When all else fails:

1. **Gather information**:
   - Copy error messages, logs, stack traces
   - Note steps to reproduce
   - Check recent changes (git log, deployments)

2. **Search for similar issues**:
   - GitHub issues for the tool
   - Stack Overflow
   - MLOps Community Slack

3. **Ask for help**:
   - Post in team Slack with full context
   - Create GitHub issue with minimal repro
   - Tag on-call engineer if production impact

4. **Document solution**:
   - Update this matrix with new issue
   - Add to runbook
   - Share learning with team

---

**Last Updated**: 2024-01-01  
**Maintainers**: MLOps Team  
**Feedback**: Open PR to add new issues

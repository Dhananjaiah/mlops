# Makefile for MLOps Churn Predictor Project
.PHONY: help install test lint docker-build docker-push deploy-dev deploy-prod clean

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
DOCKER_REGISTRY := ghcr.io/mlops-course
IMAGE_NAME := churn-predictor
VERSION := $(shell git describe --tags --always --dirty)
NAMESPACE_DEV := mlops-dev
NAMESPACE_PROD := mlops-prod

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Setup and Installation
install: ## Install dependencies
	$(PIP) install uv
	uv venv
	. .venv/bin/activate && uv pip install -e ".[dev]"
	pre-commit install

install-ci: ## Install dependencies for CI
	$(PIP) install uv
	uv pip install -e ".[dev]"

# Development
run-api: ## Run API server locally
	uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

run-train: ## Run training locally
	$(PYTHON) src/train.py

run-batch: ## Run batch scoring
	$(PYTHON) src/batch_score.py data/raw/customers.csv data/scored/predictions.csv

run-drift: ## Run drift detection
	$(PYTHON) src/detect_drift.py data/baseline.csv data/current.csv

# Testing
test: ## Run all tests
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit: ## Run unit tests
	pytest tests/unit/ -v

test-integration: ## Run integration tests
	pytest tests/integration/ -v

test-model: ## Run model tests
	pytest tests/model/ -v

test-smoke: ## Run smoke tests
	./scripts/smoke_test.sh

# Code Quality
lint: ## Run linters
	black --check src/ tests/
	ruff check src/ tests/
	mypy src/

format: ## Format code
	black src/ tests/
	ruff check --fix src/ tests/

security-scan: ## Run security scans
	trivy fs . --severity HIGH,CRITICAL
	gitleaks detect --source . --no-git
	safety check

# Docker
docker-build: ## Build Docker images
	docker build -f serving/Dockerfile.api -t $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:$(VERSION) .
	docker build -f Dockerfile.train -t $(DOCKER_REGISTRY)/$(IMAGE_NAME)-train:$(VERSION) .
	docker tag $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:$(VERSION) $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:latest

docker-push: ## Push Docker images to registry
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:$(VERSION)
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:latest
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME)-train:$(VERSION)

docker-run: ## Run API in Docker
	docker run -d -p 8000:8000 \
		-e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 \
		--name churn-api \
		$(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:latest

# Docker Compose
compose-up: ## Start local stack
	docker compose up -d

compose-down: ## Stop local stack
	docker compose down

compose-logs: ## View logs
	docker compose logs -f

compose-ps: ## Show running services
	docker compose ps

# Data
dvc-init: ## Initialize DVC
	dvc init
	dvc remote add -d local /tmp/dvc-remote
	git add .dvc .dvcignore
	git commit -m "Initialize DVC"

dvc-push: ## Push data to DVC remote
	dvc push

dvc-pull: ## Pull data from DVC remote
	dvc pull

generate-data: ## Generate sample data
	$(PYTHON) scripts/generate_data.py

# Kubernetes
k8s-create-namespace-dev: ## Create dev namespace
	kubectl create namespace $(NAMESPACE_DEV) || true

k8s-create-namespace-prod: ## Create prod namespace
	kubectl create namespace $(NAMESPACE_PROD) || true

deploy-dev: k8s-create-namespace-dev ## Deploy to dev environment
	kubectl apply -k infra/k8s/overlays/dev/
	kubectl rollout status deployment/mlops-api -n $(NAMESPACE_DEV)

deploy-prod: k8s-create-namespace-prod ## Deploy to prod environment (requires approval)
	@echo "Deploying to production..."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		kubectl apply -k infra/k8s/overlays/prod/; \
		kubectl rollout status deployment/mlops-api -n $(NAMESPACE_PROD); \
	fi

k8s-logs-dev: ## View logs in dev
	kubectl logs -n $(NAMESPACE_DEV) -l app=mlops-api --tail=100 -f

k8s-logs-prod: ## View logs in prod
	kubectl logs -n $(NAMESPACE_PROD) -l app=mlops-api --tail=100 -f

k8s-port-forward-dev: ## Port forward dev API
	kubectl port-forward -n $(NAMESPACE_DEV) svc/mlops-api 8000:80

k8s-port-forward-prod: ## Port forward prod API
	kubectl port-forward -n $(NAMESPACE_PROD) svc/mlops-api 8000:80

# MLflow
mlflow-start: ## Start MLflow server
	mlflow server \
		--backend-store-uri sqlite:///mlflow.db \
		--default-artifact-root ./mlruns \
		--host 0.0.0.0 \
		--port 5000

mlflow-list-experiments: ## List MLflow experiments
	mlflow experiments list

mlflow-list-runs: ## List runs for experiment
	@read -p "Experiment name: " exp_name; \
	mlflow runs list --experiment-name $$exp_name

# Airflow
airflow-init: ## Initialize Airflow
	airflow db init
	airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@mlops.dev \
		--password admin

airflow-start: ## Start Airflow webserver and scheduler
	airflow webserver --port 8080 & \
	airflow scheduler &

airflow-trigger: ## Trigger training DAG
	airflow dags trigger train_churn_model

# Monitoring
prometheus-query: ## Query Prometheus
	@read -p "Query: " query; \
	curl -s "http://localhost:9090/api/v1/query?query=$$query" | jq .

grafana-import-dashboard: ## Import Grafana dashboard
	@read -p "Dashboard JSON file: " file; \
	curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
		-H "Content-Type: application/json" \
		-d @$$file

# Cleanup
clean: ## Clean generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/
	rm -rf dist/ build/

clean-docker: ## Remove Docker containers and images
	docker compose down -v
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:$(VERSION) || true
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE_NAME)-api:latest || true

clean-k8s: ## Clean Kubernetes resources
	kubectl delete namespace $(NAMESPACE_DEV) || true
	kubectl delete namespace $(NAMESPACE_PROD) || true

# CI/CD Simulation
ci: install-ci lint test security-scan ## Run CI checks locally
	@echo "✅ CI checks passed"

cd-dev: docker-build docker-push deploy-dev ## Simulate CD to dev
	@echo "✅ Deployed to dev"

# All-in-one
all: install lint test docker-build ## Install, lint, test, and build
	@echo "✅ All tasks completed"

# Quick start
quickstart: compose-up generate-data run-train run-api ## Quick start local environment
	@echo "✅ Local environment ready"
	@echo "API: http://localhost:8000/docs"
	@echo "MLflow: http://localhost:5000"
	@echo "Grafana: http://localhost:3000 (admin/admin)"

# Version
version: ## Show version
	@echo "Version: $(VERSION)"

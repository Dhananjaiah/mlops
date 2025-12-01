# GitHub Cheatsheet for MLOps/DevOps Engineers

## Git Fundamentals

### Setup & Configuration
```bash
# Configure user identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Configure editor
git config --global core.editor "vim"

# View configuration
git config --list
git config --global --list

# Configure line endings
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows

# Set default branch name
git config --global init.defaultBranch main

# Configure credential helper
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'
```

### Repository Initialization
```bash
# Initialize new repository
git init
git init my-project

# Clone repository
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git custom-name
git clone --depth 1 https://github.com/user/repo.git  # Shallow clone

# Clone specific branch
git clone -b develop https://github.com/user/repo.git

# Clone with submodules
git clone --recursive https://github.com/user/repo.git
```

---

## Basic Git Operations

### Staging & Committing
```bash
# Check status
git status
git status -s  # Short format

# Stage changes
git add file.txt
git add .                    # Stage all changes
git add -p                   # Interactive staging
git add *.py                 # Stage by pattern

# Unstage files
git reset HEAD file.txt
git restore --staged file.txt  # Modern way

# Commit changes
git commit -m "feat: add new feature"
git commit -am "fix: bug fix"  # Stage and commit tracked files
git commit --amend             # Amend last commit
git commit --amend --no-edit   # Amend without changing message

# Conventional commits (best practice)
git commit -m "feat: add user authentication"
git commit -m "fix: resolve memory leak in training loop"
git commit -m "docs: update API documentation"
git commit -m "chore: update dependencies"
git commit -m "refactor: restructure model serving code"
```

### Viewing History
```bash
# View commit history
git log
git log --oneline
git log --graph --oneline --all
git log --since="2 weeks ago"
git log --author="John"
git log --grep="bug"

# View specific file history
git log file.txt
git log -p file.txt  # Show patches

# View changes
git show HEAD
git show commit-hash
git show HEAD~3      # 3 commits ago

# Compare changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff HEAD~2 HEAD       # Between commits
git diff branch1..branch2  # Between branches
```

### Undoing Changes
```bash
# Discard working directory changes
git restore file.txt
git checkout -- file.txt  # Old way

# Unstage file
git restore --staged file.txt

# Revert commit (creates new commit)
git revert HEAD
git revert commit-hash

# Reset (CAUTION: destructive)
git reset --soft HEAD~1   # Keep changes staged
git reset --mixed HEAD~1  # Keep changes unstaged (default)
git reset --hard HEAD~1   # Discard all changes

# Clean untracked files
git clean -n       # Dry run
git clean -f       # Remove untracked files
git clean -fd      # Remove untracked files and directories
```

---

## Branching & Merging

### Branch Management
```bash
# List branches
git branch
git branch -a      # All branches (local + remote)
git branch -r      # Remote branches

# Create branch
git branch feature-x
git checkout -b feature-x         # Create and switch
git switch -c feature-x           # Modern way

# Switch branches
git checkout main
git switch main    # Modern way

# Rename branch
git branch -m old-name new-name
git branch -m new-name  # Rename current branch

# Delete branch
git branch -d feature-x   # Safe delete (merged only)
git branch -D feature-x   # Force delete

# Delete remote branch
git push origin --delete feature-x
```

### Merging
```bash
# Merge branch into current branch
git merge feature-x
git merge feature-x --no-ff  # Always create merge commit

# Merge with strategy
git merge -X theirs feature-x  # Prefer their changes
git merge -X ours feature-x    # Prefer our changes

# Abort merge
git merge --abort

# View merged branches
git branch --merged
git branch --no-merged
```

### Rebasing
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (clean up history)
git rebase -i HEAD~3

# Continue/abort rebase
git rebase --continue
git rebase --abort

# Rebase with autosquash
git rebase -i --autosquash main
```

### Cherry-picking
```bash
# Apply specific commit to current branch
git cherry-pick commit-hash
git cherry-pick commit1 commit2  # Multiple commits

# Cherry-pick without committing
git cherry-pick -n commit-hash
```

---

## Remote Repository Operations

### Remote Management
```bash
# List remotes
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# Change remote URL
git remote set-url origin https://github.com/user/new-repo.git

# Remove remote
git remote remove upstream

# Fetch from remote
git fetch origin
git fetch --all

# Pull changes
git pull origin main
git pull --rebase origin main  # Rebase instead of merge

# Push changes
git push origin main
git push -u origin feature-x   # Set upstream and push
git push --force-with-lease    # Safer force push
git push --tags                # Push tags
```

### Fork Workflow
```bash
# 1. Fork repository on GitHub, then clone
git clone https://github.com/your-username/repo.git
cd repo

# 2. Add upstream remote
git remote add upstream https://github.com/original-owner/repo.git

# 3. Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 4. Create feature branch
git checkout -b feature-x

# 5. Make changes and push
git add .
git commit -m "feat: add feature"
git push -u origin feature-x

# 6. Create pull request on GitHub UI
```

---

## GitHub Actions CI/CD

### Basic Workflow Structure
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Manual trigger

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### MLOps-Specific Workflows

#### Model Training Workflow
```yaml
# .github/workflows/train-model.yml
name: Train Model

on:
  workflow_dispatch:
    inputs:
      experiment_name:
        description: 'MLflow experiment name'
        required: true
        default: 'default'
      dataset_version:
        description: 'DVC dataset version (commit hash)'
        required: true

jobs:
  train:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Setup DVC
        uses: iterative/setup-dvc@v1
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Pull data from DVC
        run: |
          dvc remote add -d myremote s3://my-bucket/dvc-cache
          dvc pull
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Train model
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          MLFLOW_EXPERIMENT_NAME: ${{ github.event.inputs.experiment_name }}
        run: |
          python src/train.py \
            --experiment-name $MLFLOW_EXPERIMENT_NAME \
            --dataset-version ${{ github.event.inputs.dataset_version }}
      
      - name: Upload model artifacts
        uses: actions/upload-artifact@v3
        with:
          name: trained-model
          path: models/
```

#### Model Deployment Workflow
```yaml
# .github/workflows/deploy-model.yml
name: Deploy Model

on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Model version to deploy'
        required: true
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Setup AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name mlops-cluster --region us-east-1
      
      - name: Download model from MLflow
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
        run: |
          python scripts/download_model.py \
            --model-version ${{ github.event.inputs.model_version }} \
            --output-path ./model
      
      - name: Build and push Docker image
        run: |
          docker build -t ${{ secrets.ECR_REGISTRY }}/ml-model:${{ github.event.inputs.model_version }} .
          docker push ${{ secrets.ECR_REGISTRY }}/ml-model:${{ github.event.inputs.model_version }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/ml-api \
            ml-api=${{ secrets.ECR_REGISTRY }}/ml-model:${{ github.event.inputs.model_version }} \
            -n ${{ github.event.inputs.environment }}
      
      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/ml-api -n ${{ github.event.inputs.environment }}
      
      - name: Run smoke tests
        run: |
          python tests/smoke_test.py --endpoint https://api-${{ github.event.inputs.environment }}.example.com
```

#### Data Validation Workflow
```yaml
# .github/workflows/validate-data.yml
name: Validate Data Quality

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install great-expectations pandas boto3
      
      - name: Download data
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          python scripts/download_data.py --date today
      
      - name: Run data validation
        run: |
          python scripts/validate_data.py
      
      - name: Upload validation results
        uses: actions/upload-artifact@v3
        with:
          name: validation-results
          path: validation_results/
      
      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Data validation failed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Reusable Workflows
```yaml
# .github/workflows/reusable-docker-build.yml
name: Reusable Docker Build

on:
  workflow_call:
    inputs:
      image_name:
        required: true
        type: string
      dockerfile:
        required: false
        type: string
        default: 'Dockerfile'
    secrets:
      registry_username:
        required: true
      registry_password:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker registry
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.registry_username }}
          password: ${{ secrets.registry_password }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ${{ inputs.dockerfile }}
          push: true
          tags: ${{ inputs.image_name }}:latest
```

### Matrix Builds
```yaml
# .github/workflows/test-matrix.yml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11']
        exclude:
          - os: macos-latest
            python-version: '3.9'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
```

---

## GitHub CLI (gh)

### Installation
```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

### Repository Operations
```bash
# Create repository
gh repo create my-project --public
gh repo create my-project --private --clone

# Clone repository
gh repo clone user/repo

# View repository
gh repo view
gh repo view user/repo --web

# Fork repository
gh repo fork user/repo
gh repo fork user/repo --clone

# List repositories
gh repo list
gh repo list user --limit 20

# Delete repository
gh repo delete user/repo
```

### Pull Requests
```bash
# Create pull request
gh pr create
gh pr create --title "Add feature" --body "Description"
gh pr create --base develop --head feature-x

# List pull requests
gh pr list
gh pr list --state open
gh pr list --label bug

# View pull request
gh pr view 123
gh pr view 123 --web
gh pr view 123 --comments

# Checkout pull request
gh pr checkout 123

# Review pull request
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Needs fixes"
gh pr review 123 --comment --body "LGTM"

# Merge pull request
gh pr merge 123
gh pr merge 123 --squash
gh pr merge 123 --rebase
gh pr merge 123 --merge

# Close pull request
gh pr close 123
```

### Issues
```bash
# Create issue
gh issue create
gh issue create --title "Bug: memory leak" --body "Description" --label bug

# List issues
gh issue list
gh issue list --state open
gh issue list --assignee @me
gh issue list --label bug

# View issue
gh issue view 42
gh issue view 42 --web

# Close issue
gh issue close 42

# Reopen issue
gh issue reopen 42
```

### GitHub Actions
```bash
# List workflows
gh workflow list

# View workflow
gh workflow view ci.yml

# Run workflow
gh workflow run ci.yml
gh workflow run deploy.yml -f environment=production

# List workflow runs
gh run list
gh run list --workflow=ci.yml

# View run details
gh run view 123456
gh run view --log

# Watch run
gh run watch

# Cancel run
gh run cancel 123456

# Re-run workflow
gh run rerun 123456
gh run rerun 123456 --failed  # Re-run only failed jobs

# Download artifacts
gh run download 123456
```

### Secrets Management
```bash
# Set secret
gh secret set MY_SECRET < secret.txt
echo "secret-value" | gh secret set MY_SECRET

# List secrets
gh secret list

# Delete secret
gh secret delete MY_SECRET

# Set environment secret
gh secret set MY_SECRET --env production
```

---

## Repository Management

### GitHub Repository Settings Best Practices
```bash
# Branch protection rules (via web UI or API)
# - Require pull request reviews
# - Require status checks to pass
# - Require branches to be up to date
# - Include administrators

# Using GitHub API
curl -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["ci", "test"]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "required_approving_review_count": 2,
      "dismiss_stale_reviews": true
    },
    "restrictions": null
  }'
```

### Labels
```bash
# Create label
gh label create "ml-model" --color "FF6B6B" --description "ML model related"
gh label create "data-pipeline" --color "4ECDC4"

# List labels
gh label list

# Delete label
gh label delete "old-label"

# Clone labels from another repo
gh label clone user/source-repo
```

### Releases
```bash
# Create release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

# Create release with assets
gh release create v1.0.0 model.pkl config.yaml --notes "Model release"

# List releases
gh release list

# View release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0
gh release download v1.0.0 --pattern "*.pkl"

# Delete release
gh release delete v1.0.0
```

---

## Real-Time MLOps Scenarios

### Scenario 1: Automated Model Retraining on Data Drift
```yaml
# .github/workflows/drift-detection-retrain.yml
name: Drift Detection and Retraining

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    outputs:
      drift_detected: ${{ steps.check_drift.outputs.drift_detected }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install evidently pandas boto3 mlflow
      
      - name: Download production data
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: python scripts/download_production_data.py --days 7
      
      - name: Check for drift
        id: check_drift
        run: |
          python scripts/detect_drift.py
          echo "drift_detected=$(cat drift_result.txt)" >> $GITHUB_OUTPUT
      
      - name: Upload drift report
        uses: actions/upload-artifact@v3
        with:
          name: drift-report
          path: reports/drift_report.html

  retrain:
    needs: detect-drift
    if: needs.detect-drift.outputs.drift_detected == 'true'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Trigger retraining
        run: |
          gh workflow run train-model.yml \
            -f experiment_name="drift_retrain_$(date +%Y%m%d)" \
            -f dataset_version="latest"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: "🚨 Data drift detected! Retraining triggered.",
              attachments: [{
                color: 'warning',
                text: 'Check the drift report artifact for details.'
              }]
            }
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Scenario 2: Multi-Environment Model Deployment with Approval Gates
```yaml
# .github/workflows/multi-env-deploy.yml
name: Multi-Environment Deployment

on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Model version (run_id from MLflow)'
        required: true

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to staging
        run: |
          python scripts/deploy_model.py \
            --model-version ${{ github.event.inputs.model_version }} \
            --environment staging
      
      - name: Run integration tests
        run: |
          python tests/integration_test.py \
            --endpoint ${{ secrets.STAGING_ENDPOINT }}
      
      - name: Generate deployment report
        run: |
          python scripts/generate_deployment_report.py \
            --model-version ${{ github.event.inputs.model_version }} \
            --environment staging \
            --output deployment_report.md
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('deployment_report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: 
      name: production
      url: https://api.example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Create backup of current model
        run: |
          python scripts/backup_current_model.py \
            --environment production
      
      - name: Deploy to production (canary)
        run: |
          python scripts/deploy_model.py \
            --model-version ${{ github.event.inputs.model_version }} \
            --environment production \
            --strategy canary \
            --canary-percent 10
      
      - name: Monitor canary metrics
        run: |
          python scripts/monitor_deployment.py \
            --environment production \
            --duration 300  # 5 minutes
      
      - name: Complete rollout
        run: |
          python scripts/complete_canary_rollout.py \
            --model-version ${{ github.event.inputs.model_version }} \
            --environment production
      
      - name: Verify production deployment
        run: |
          python tests/smoke_test.py \
            --endpoint ${{ secrets.PRODUCTION_ENDPOINT }} \
            --threshold 0.95
```

### Scenario 3: Automated Model Versioning and Registry
```bash
# scripts/version_and_register_model.sh
#!/bin/bash

set -e

MODEL_NAME="churn_predictor"
RUN_ID=$1
STAGE=$2  # staging or production

# Download model from MLflow
mlflow artifacts download \
  --run-id $RUN_ID \
  --artifact-path model \
  --dst-path ./downloaded_model

# Get model metrics
METRICS=$(mlflow runs describe --run-id $RUN_ID | jq -r '.data.metrics')
ACCURACY=$(echo $METRICS | jq -r '.accuracy')
F1_SCORE=$(echo $METRICS | jq -r '.f1_score')

# Register model
VERSION=$(mlflow models register \
  --model-uri runs:/$RUN_ID/model \
  --name $MODEL_NAME | jq -r '.version')

echo "Model registered as version $VERSION"

# Add tags
mlflow models set-tag \
  --name $MODEL_NAME \
  --version $VERSION \
  --key "accuracy" \
  --value $ACCURACY

mlflow models set-tag \
  --name $MODEL_NAME \
  --version $VERSION \
  --key "f1_score" \
  --value $F1_SCORE

mlflow models set-tag \
  --name $MODEL_NAME \
  --version $VERSION \
  --key "github_sha" \
  --value $GITHUB_SHA

# Transition to stage if metrics meet threshold
if (( $(echo "$ACCURACY >= 0.85" | bc -l) )); then
  mlflow models transition \
    --name $MODEL_NAME \
    --version $VERSION \
    --stage $STAGE \
    --archive-existing-versions
  
  echo "Model transitioned to $STAGE stage"
else
  echo "Model accuracy $ACCURACY below threshold 0.85, not transitioning"
  exit 1
fi
```

### Scenario 4: DVC Data Versioning in CI/CD
```yaml
# .github/workflows/data-versioning.yml
name: Data Versioning

on:
  push:
    paths:
      - 'data/**'
      - 'data/*.dvc'

jobs:
  version-data:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup DVC
        uses: iterative/setup-dvc@v1
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Setup DVC remote
        run: |
          dvc remote add -d myremote s3://my-dvc-bucket/cache
          dvc remote modify myremote region us-east-1
      
      - name: Push data to DVC remote
        run: dvc push
      
      - name: Generate data report
        run: |
          python scripts/generate_data_report.py > data_report.md
      
      - name: Create release with data version
        run: |
          DATA_VERSION="data-$(date +%Y%m%d-%H%M%S)"
          gh release create $DATA_VERSION \
            --title "Data Release $DATA_VERSION" \
            --notes-file data_report.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Scenario 5: Automated Security Scanning for ML Models
```yaml
# .github/workflows/security-scan.yml
name: Security Scanning

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  scan-dependencies:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Safety check
        run: |
          pip install safety
          safety check --json > safety-report.json || true
      
      - name: Upload safety report
        uses: actions/upload-artifact@v3
        with:
          name: safety-report
          path: safety-report.json

  scan-secrets:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  scan-model:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install MLSec tools
        run: |
          pip install adversarial-robustness-toolbox tensorflow
      
      - name: Test model robustness
        run: |
          python scripts/test_adversarial_robustness.py \
            --model-path models/latest.pkl \
            --output adversarial-report.json
      
      - name: Upload robustness report
        uses: actions/upload-artifact@v3
        with:
          name: adversarial-report
          path: adversarial-report.json

  scan-container:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t ml-model:test .
      
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ml-model:test
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## GitHub API Integration

### Using GitHub REST API
```bash
# Set your token
export GITHUB_TOKEN="your_personal_access_token"

# Get user info
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# List repositories
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos?per_page=100

# Get repository info
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo

# Create repository
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{
    "name": "ml-project",
    "description": "Machine Learning Project",
    "private": false,
    "auto_init": true
  }'

# List pull requests
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/pulls

# Create pull request
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/owner/repo/pulls \
  -d '{
    "title": "New feature",
    "body": "Description of changes",
    "head": "feature-branch",
    "base": "main"
  }'

# List workflow runs
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/actions/runs

# Trigger workflow
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/owner/repo/actions/workflows/deploy.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "environment": "production",
      "model_version": "v1.2.3"
    }
  }'
```

### Python Script for GitHub Automation
```python
# github_automation.py
import os
import requests
from typing import Dict, Any

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }
    
    def get_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def list_pull_requests(self, owner: str, repo: str, state: str = "open") -> list:
        """List pull requests"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_pull_request(
        self, 
        owner: str, 
        repo: str, 
        title: str,
        head: str,
        base: str,
        body: str = ""
    ) -> Dict[str, Any]:
        """Create a pull request"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def trigger_workflow(
        self,
        owner: str,
        repo: str,
        workflow_id: str,
        ref: str,
        inputs: Dict[str, str] = None
    ) -> None:
        """Trigger a workflow"""
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
        data = {"ref": ref}
        if inputs:
            data["inputs"] = inputs
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
    
    def list_workflow_runs(
        self,
        owner: str,
        repo: str,
        workflow_id: str = None,
        status: str = None
    ) -> list:
        """List workflow runs"""
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs"
        params = {}
        if workflow_id:
            params["workflow_id"] = workflow_id
        if status:
            params["status"] = status
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()["workflow_runs"]
    
    def get_workflow_run_logs(self, owner: str, repo: str, run_id: int) -> bytes:
        """Download workflow run logs"""
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content

# Example usage
if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    client = GitHubClient(token)
    
    # Trigger model training workflow
    client.trigger_workflow(
        owner="your-org",
        repo="ml-project",
        workflow_id="train-model.yml",
        ref="main",
        inputs={
            "experiment_name": "production_model",
            "dataset_version": "latest"
        }
    )
    
    # Check recent workflow runs
    runs = client.list_workflow_runs(
        owner="your-org",
        repo="ml-project",
        status="completed"
    )
    
    for run in runs[:5]:
        print(f"Run {run['id']}: {run['name']} - {run['conclusion']}")
```

---

## Git Hooks for MLOps

### Pre-commit Hook for Data Validation
```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running pre-commit checks..."

# Check for large files (>100MB)
large_files=$(git diff --cached --name-only | xargs -I {} du -m {} 2>/dev/null | awk '$1 > 100 {print $2}')
if [ -n "$large_files" ]; then
    echo "Error: Large files detected (>100MB). Use DVC for data versioning:"
    echo "$large_files"
    exit 1
fi

# Check if model files are tracked by DVC
model_files=$(git diff --cached --name-only | grep -E '\.(pkl|h5|pth|onnx|pt)$')
if [ -n "$model_files" ]; then
    for file in $model_files; do
        if [ ! -f "${file}.dvc" ]; then
            echo "Error: Model file $file not tracked by DVC"
            echo "Run: dvc add $file"
            exit 1
        fi
    done
fi

# Validate Jupyter notebooks are cleared
notebooks=$(git diff --cached --name-only | grep '\.ipynb$')
if [ -n "$notebooks" ]; then
    for notebook in $notebooks; do
        if grep -q '"outputs": \[' "$notebook"; then
            echo "Error: Notebook $notebook has outputs. Clear before committing."
            echo "Run: jupyter nbconvert --clear-output --inplace $notebook"
            exit 1
        fi
    done
fi

# Run tests
if [ -d "tests" ]; then
    echo "Running tests..."
    pytest tests/ -v
    if [ $? -ne 0 ]; then
        echo "Error: Tests failed"
        exit 1
    fi
fi

echo "Pre-commit checks passed!"
exit 0
```

### Pre-push Hook for Model Quality Gate
```bash
# .git/hooks/pre-push
#!/bin/bash

echo "Running pre-push checks..."

# Check if there are uncommitted model files
uncommitted_models=$(git ls-files --modified | grep -E '\.(pkl|h5|pth|onnx)$')
if [ -n "$uncommitted_models" ]; then
    echo "Error: Uncommitted model files detected:"
    echo "$uncommitted_models"
    exit 1
fi

# Validate latest model meets quality threshold
if [ -f "scripts/validate_model_quality.py" ]; then
    echo "Validating model quality..."
    python scripts/validate_model_quality.py
    if [ $? -ne 0 ]; then
        echo "Error: Model does not meet quality thresholds"
        exit 1
    fi
fi

# Check for secrets in code
if command -v gitleaks &> /dev/null; then
    echo "Scanning for secrets..."
    gitleaks detect --source . --verbose
    if [ $? -ne 0 ]; then
        echo "Error: Secrets detected in code"
        exit 1
    fi
fi

echo "Pre-push checks passed!"
exit 0
```

---

## Best Practices & Tips

### Commit Message Conventions
```bash
# Types
feat:     # New feature
fix:      # Bug fix
docs:     # Documentation changes
style:    # Code style changes (formatting, etc.)
refactor: # Code refactoring
perf:     # Performance improvements
test:     # Adding or updating tests
chore:    # Build process or auxiliary tool changes
ci:       # CI/CD changes

# Examples
git commit -m "feat(model): add XGBoost classifier"
git commit -m "fix(api): resolve memory leak in prediction endpoint"
git commit -m "docs(readme): update deployment instructions"
git commit -m "perf(training): optimize data loading pipeline"
git commit -m "ci(github): add automated model deployment workflow"
```

### Branch Naming Conventions
```bash
# Feature branches
feature/user-authentication
feature/add-xgboost-model

# Bug fix branches
fix/memory-leak-training
fix/api-timeout-issue

# Hotfix branches (production)
hotfix/critical-security-patch

# Release branches
release/v1.2.0

# Experiment branches
experiment/transformer-model
experiment/new-feature-engineering
```

### .gitignore for ML Projects
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# Data (track with DVC instead)
data/
*.csv
*.parquet
*.feather

# Models (track with DVC/MLflow)
models/
*.pkl
*.h5
*.pth
*.onnx
*.pb
*.pt

# ML artifacts
mlruns/
outputs/
checkpoints/
wandb/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
secrets/

# Logs
logs/
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
```

### Security Best Practices
```bash
# 1. Never commit secrets
# Use GitHub Secrets for sensitive data
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set MLFLOW_TRACKING_URI

# 2. Use environment-specific secrets
gh secret set API_KEY --env production
gh secret set API_KEY --env staging

# 3. Scan for secrets regularly
gitleaks detect --source . --verbose

# 4. Use .gitignore for sensitive files
echo ".env" >> .gitignore
echo "secrets/" >> .gitignore

# 5. Rotate credentials regularly
# Update secrets every 90 days

# 6. Use least privilege principle
# Give workflows only necessary permissions
```

### Collaboration Tips
```bash
# 1. Keep commits small and focused
git add -p  # Stage hunks interactively

# 2. Write descriptive commit messages
# Bad:  "fix bug"
# Good: "fix(training): resolve OOM error in batch processing"

# 3. Rebase before merging
git checkout feature-branch
git fetch origin
git rebase origin/main

# 4. Use draft PRs for work in progress
gh pr create --draft

# 5. Request specific reviewers
gh pr create --reviewer alice,bob

# 6. Link issues to PRs
# In PR description: "Closes #42"

# 7. Keep PRs focused
# One feature/fix per PR

# 8. Update PR branch regularly
git fetch origin
git merge origin/main
# or
git rebase origin/main
```

---

## Troubleshooting

### Common Issues

#### Authentication Issues
```bash
# Re-authenticate with GitHub CLI
gh auth logout
gh auth login

# Check authentication status
gh auth status

# Use SSH instead of HTTPS
git remote set-url origin git@github.com:user/repo.git

# Configure SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add to GitHub: Settings > SSH and GPG keys
```

#### Large File Issues
```bash
# Remove large file from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file' \
  --prune-empty --tag-name-filter cat -- --all

# Use BFG Repo-Cleaner (faster)
bfg --delete-files large-file.dat
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push cleaned history
git push origin --force --all
```

#### Merge Conflicts
```bash
# View conflicts
git status

# Abort merge
git merge --abort

# Resolve conflicts manually, then:
git add conflicted-file.py
git commit

# Use merge tool
git mergetool

# Accept all changes from one side
git checkout --ours file.py    # Keep our changes
git checkout --theirs file.py  # Keep their changes
```

#### CI/CD Workflow Failures
```bash
# View workflow run logs
gh run view --log

# Re-run failed jobs
gh run rerun 123456 --failed

# Debug workflow locally with act
act -l  # List jobs
act push  # Run on push event
act -j test  # Run specific job
```

---

## Resources

### Official Documentation
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Manual](https://cli.github.com/manual/)

### Tutorials & Guides
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Skills](https://skills.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Tools
- [GitKraken](https://www.gitkraken.com/) - Git GUI client
- [Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph) - VS Code extension
- [act](https://github.com/nektos/act) - Run GitHub Actions locally
- [gitleaks](https://github.com/gitleaks/gitleaks) - Secrets detection

---

**[Back to Main Cheatsheets](../README.md)**

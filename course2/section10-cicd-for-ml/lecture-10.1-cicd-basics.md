# Lecture 10.1 – CI/CD Basics Refresher (Build, Test, Deploy)

## Human Transcript

Welcome to Section 10. We're going to talk about CI/CD for machine learning systems. This is where your ML code becomes professional, production-grade software.

Let me start with a quick refresher on CI/CD for those who might be newer to it or coming from a pure data science background.

CI stands for Continuous Integration. CD stands for Continuous Delivery (or sometimes Continuous Deployment). Together, they're a set of practices that automate the process of getting code from development to production.

Let me explain why this matters.

Imagine you're working on a team. Multiple people are changing code every day. How do you know their changes work together? How do you know they didn't break anything? How do you get those changes safely to production?

Without CI/CD, it's chaos. "Works on my machine" becomes the dreaded phrase. Integration problems surface at the worst time. Releases are painful, stressful events that everyone dreads.

With CI/CD, changes flow smoothly. Problems are caught early. Releases become boring (in a good way).

Let's break down the components.

Continuous Integration (CI). Every time someone pushes code, automated processes run:

1. Build - Compile the code, install dependencies
2. Test - Run unit tests, integration tests
3. Check - Run linters, security scanners, code quality tools

If any step fails, the team knows immediately. The code doesn't get merged until it passes.

```yaml
# Example: GitHub Actions CI workflow
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          black --check src/
          flake8 src/
      
      - name: Run tests
        run: pytest tests/ -v --cov=src/
      
      - name: Check code coverage
        run: |
          coverage report --fail-under=80
```

Continuous Delivery (CD). After CI passes, the code is ready to be deployed. With Continuous Delivery, you can deploy at any time with the push of a button. With Continuous Deployment, it happens automatically.

```yaml
# Example: Deployment workflow
name: Deploy

on:
  push:
    branches: [main]  # Only deploy from main

jobs:
  deploy:
    needs: [build-and-test]  # Only run if CI passes
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t my-app:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          docker tag my-app:${{ github.sha }} $REGISTRY/my-app:${{ github.sha }}
          docker push $REGISTRY/my-app:${{ github.sha }}
      
      - name: Deploy to staging
        run: |
          kubectl set image deployment/my-app my-app=$REGISTRY/my-app:${{ github.sha }}
```

The typical CI/CD pipeline looks like this:

```
Developer pushes code
        ↓
┌───────────────────────────────────────────────┐
│              CI Pipeline                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │
│  │  Build  │→ │  Test   │→ │ Code Quality│   │
│  └─────────┘  └─────────┘  └─────────────┘   │
└───────────────────────────────────────────────┘
        ↓ (if all pass)
┌───────────────────────────────────────────────┐
│              CD Pipeline                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │
│  │ Package │→ │ Deploy  │→ │  Validate   │   │
│  │         │  │ Staging │  │             │   │
│  └─────────┘  └─────────┘  └─────────────┘   │
│                   ↓ (if staging OK)           │
│              ┌─────────┐                      │
│              │ Deploy  │                      │
│              │  Prod   │                      │
│              └─────────┘                      │
└───────────────────────────────────────────────┘
```

Key concepts you should know:

Pull Request (PR) / Merge Request (MR). When you want to merge your changes into the main branch, you create a PR. The CI pipeline runs on this PR. Other developers review the code. Only when tests pass and reviewers approve does the code get merged.

Main/trunk branch. The primary branch that represents what's in production (or ready for production). Changes flow into main from feature branches.

Feature branches. Short-lived branches where developers work on features. Once done, they create a PR to merge into main.

```bash
# Typical workflow
git checkout -b feature/add-new-model
# ... make changes ...
git add .
git commit -m "Add new churn model"
git push origin feature/add-new-model
# Create PR on GitHub
# Wait for CI to pass
# Get code review
# Merge to main
```

Environments. Most teams have multiple environments:
- Development - where developers work
- Staging - a production-like environment for testing
- Production - the real thing

Code flows through these environments:

```
feature branch → main → staging → production
```

Tags and releases. When you're ready for a release, you tag the commit:

```bash
git tag v1.2.0
git push origin v1.2.0
```

Tags can trigger special deployment pipelines.

Popular CI/CD tools:

- GitHub Actions - built into GitHub, very popular
- GitLab CI - built into GitLab
- Jenkins - self-hosted, very flexible, older
- CircleCI - cloud-based
- Azure DevOps - Microsoft's solution
- AWS CodePipeline - AWS native

For most teams starting out, I recommend GitHub Actions or GitLab CI. They're easy to set up and free for public repositories.

Why is this important for ML?

ML code is still code. It needs the same rigor:
- Tests to catch bugs
- Linting for code quality
- Automated builds to catch dependency issues
- Consistent deployment process

But ML also has special needs:
- Data validation
- Model validation
- Longer running tests (training)
- More complex artifacts (models, not just binaries)

In the next lectures, we'll explore what makes ML CI/CD different and how to handle those differences.

Any questions on the basics? Let's move forward.

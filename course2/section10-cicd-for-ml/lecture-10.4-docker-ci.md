# Lecture 10.4 – Building Docker Images & Pushing to Registry in CI

## Human Transcript

Alright, tests are passing. Now we need to package our application into a Docker image and push it to a registry. This is a critical step in CI/CD because the image is what actually gets deployed.

Let me show you how to set this up properly.

Basic Docker build in CI:

```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build image
        run: |
          docker build -t churn-model:${{ github.sha }} .
      
      - name: Test image
        run: |
          docker run --rm churn-model:${{ github.sha }} python -c "import src; print('Import OK')"
```

Now let's add pushing to a registry. I'll show examples for different registries.

Docker Hub:

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: |
            myuser/churn-model:${{ github.sha }}
            myuser/churn-model:latest
```

AWS ECR (Elastic Container Registry):

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-role
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push
        env:
          REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          REPOSITORY: churn-model
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $REGISTRY/$REPOSITORY:$IMAGE_TAG .
          docker push $REGISTRY/$REPOSITORY:$IMAGE_TAG
          
          # Also tag as latest for main branch
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            docker tag $REGISTRY/$REPOSITORY:$IMAGE_TAG $REGISTRY/$REPOSITORY:latest
            docker push $REGISTRY/$REPOSITORY:latest
          fi
```

Google Container Registry / Artifact Registry:

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Configure Docker for GCR
        run: gcloud auth configure-docker gcr.io
      
      - name: Build and push
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT }}/churn-model:${{ github.sha }} .
          docker push gcr.io/${{ secrets.GCP_PROJECT }}/churn-model:${{ github.sha }}
```

GitHub Container Registry (GHCR):

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/churn-model:${{ github.sha }}
            ghcr.io/${{ github.repository }}/churn-model:latest
```

Now let's add some best practices.

Image tagging strategy:

```yaml
- name: Generate tags
  id: meta
  uses: docker/metadata-action@v4
  with:
    images: myregistry/churn-model
    tags: |
      type=sha,prefix=
      type=ref,event=branch
      type=ref,event=pr
      type=semver,pattern={{version}}
      type=semver,pattern={{major}}.{{minor}}
      type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

- name: Build and push
  uses: docker/build-push-action@v4
  with:
    tags: ${{ steps.meta.outputs.tags }}
```

This creates multiple tags:
- `abc123def` - commit SHA
- `main` or `feature-branch` - branch name
- `pr-42` - pull request number
- `1.2.3`, `1.2` - semantic version (if you push a tag)
- `latest` - only on main branch

Caching for faster builds:

```yaml
- name: Build and push
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: myregistry/churn-model:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

This caches Docker layers using GitHub Actions cache, dramatically speeding up builds.

Multi-platform builds:

```yaml
- name: Set up QEMU
  uses: docker/setup-qemu-action@v2

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v2

- name: Build and push
  uses: docker/build-push-action@v4
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: myregistry/churn-model:${{ github.sha }}
```

Scanning for vulnerabilities:

```yaml
- name: Build image
  run: docker build -t churn-model:${{ github.sha }} .

- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: churn-model:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload Trivy scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'

- name: Fail on critical vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: churn-model:${{ github.sha }}
    exit-code: '1'
    severity: 'CRITICAL'
```

Including model in the image. Sometimes you want to bake the model into the image:

```yaml
- name: Download model from MLflow
  run: |
    mlflow artifacts download \
      -r ${{ secrets.MLFLOW_RUN_ID }} \
      -d ./models

- name: Build image with model
  run: |
    docker build \
      --build-arg MODEL_PATH=./models/model \
      -t churn-model:${{ github.sha }} .
```

The Dockerfile would include:

```dockerfile
ARG MODEL_PATH
COPY ${MODEL_PATH} /app/models/
```

Testing the built image:

```yaml
- name: Build image
  run: docker build -t churn-model:test .

- name: Start container
  run: |
    docker run -d --name test-container -p 8000:8000 churn-model:test
    sleep 10  # Wait for startup

- name: Run smoke tests
  run: |
    curl -f http://localhost:8000/health
    curl -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"customers": [{"customer_id": "T1", "tenure": 12, "monthly_charges": 50}]}'

- name: Check logs for errors
  if: always()
  run: docker logs test-container

- name: Cleanup
  if: always()
  run: docker stop test-container && docker rm test-container
```

Complete workflow putting it all together:

```yaml
name: Build, Test, and Push

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/churn-model

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/ -v

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Generate metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
```

That's the complete setup for building and pushing Docker images in CI. The key points: tag intelligently, use caching, scan for vulnerabilities, and test before pushing.

Next, we'll look at continuous delivery of models and APIs.

Questions?

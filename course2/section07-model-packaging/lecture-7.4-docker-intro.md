# Lecture 7.4 – Introduction to Docker for MLOps (Images, Containers, Registries)

## Human Transcript

Alright, so we've got our model, we've got our API, and everything works perfectly on your laptop. Now comes the classic problem. You send it to your colleague and they say "it doesn't work on my machine." Different Python version. Different dependencies. Different operating system. This is where Docker comes in.

Docker is a containerization technology that lets you package your application along with everything it needs to run. Your code, your dependencies, your Python version, even parts of the operating system. Everything goes into a single package called an image. And then you can run that image on any computer that has Docker installed, and it works exactly the same way.

Let me explain the basic concepts.

An image is like a blueprint. It contains all the files and configuration your application needs. But it's not running. It's just a static package.

A container is a running instance of an image. When you run an image, Docker creates a container. You can have multiple containers running from the same image. Each one is isolated from the others.

A registry is where you store images. Docker Hub is the public registry where you can find images for common software. Companies usually have private registries for their own images.

Let me show you an example. Say you want to run a PostgreSQL database. Instead of installing PostgreSQL on your machine, configuring it, dealing with different versions, you just run:

```bash
docker run postgres:14
```

Docker downloads the PostgreSQL 14 image from Docker Hub and runs it in a container. Done. In seconds. And when you're finished, you can stop the container and your system is clean.

Now let's talk about how to build your own images. You do this with a Dockerfile. A Dockerfile is a text file that describes what should go into the image. It's a series of instructions, and Docker executes them one by one to build the image.

Here's a basic Dockerfile for our churn model API:

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Let me explain each line.

`FROM python:3.10-slim` says we're starting with a base image that already has Python 3.10 installed. The `slim` variant is smaller because it doesn't include things we don't need. There are other variants like `alpine` which is even smaller, but can have compatibility issues with some Python packages.

`WORKDIR /app` sets the working directory inside the container. All subsequent commands run from this directory.

`COPY requirements.txt .` copies just the requirements file first. Why not copy everything at once? Docker caching. Docker caches each layer of the build. If the requirements file hasn't changed, Docker can reuse the cached layer where dependencies were installed. This makes rebuilds much faster when you're just changing code, not dependencies.

`RUN pip install --no-cache-dir -r requirements.txt` installs the Python packages. The `--no-cache-dir` flag tells pip not to cache downloaded packages, which keeps the image smaller.

`COPY . .` copies the rest of your application code into the image.

`EXPOSE 8000` documents that the container listens on port 8000. This doesn't actually publish the port; it's more like documentation.

`CMD` specifies the command that runs when you start a container from this image.

To build this image, you run:

```bash
docker build -t churn-model:v1 .
```

The `-t` flag tags the image with a name. The `.` means use the current directory as the build context.

To run it:

```bash
docker run -p 8000:8000 churn-model:v1
```

The `-p 8000:8000` maps port 8000 on your machine to port 8000 in the container. Now you can access your API at `http://localhost:8000`.

Let me show you some more advanced Dockerfile techniques that are particularly useful for ML models.

Multi-stage builds. ML images can get huge because of all the dependencies. Multi-stage builds let you use one image for building and a smaller one for running:

```dockerfile
# Build stage
FROM python:3.10 AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The builder stage installs all the dependencies. The runtime stage only copies the installed packages. Build tools and cache don't end up in the final image.

Including the model in the image. For simpler deployments, you might want to bake the model into the image:

```dockerfile
# Copy model file
COPY models/churn_model_v1.joblib /app/models/

# Set environment variable for model path
ENV MODEL_PATH=/app/models/churn_model_v1.joblib
```

But there's a tradeoff here. If the model is in the image, you need to rebuild and redeploy the image every time you retrain. Some teams prefer to load the model from external storage like S3 at startup. We'll discuss this more later.

Non-root user. For security, it's best not to run as root in the container:

```dockerfile
# Create non-root user
RUN useradd -m appuser
USER appuser

WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .
```

Health checks in Docker:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

This tells Docker how to check if your container is healthy. If the health check fails, Docker can restart the container.

Now let's talk about registries. Once you've built an image, you need to store it somewhere so others can use it. Docker Hub is the public registry, but for production you'll usually use a private registry like:

- AWS ECR (Elastic Container Registry)
- Google Container Registry
- Azure Container Registry
- GitHub Container Registry
- Self-hosted registries like Harbor

To push to a registry, you first tag the image with the registry URL:

```bash
# Tag for AWS ECR
docker tag churn-model:v1 123456789.dkr.ecr.us-east-1.amazonaws.com/churn-model:v1

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/churn-model:v1
```

The image name format is: `registry-url/repository-name:tag`

Some useful Docker commands you'll use all the time:

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List images
docker images

# Stop a container
docker stop <container-id>

# Remove a container
docker rm <container-id>

# Remove an image
docker rmi <image-id>

# View container logs
docker logs <container-id>

# Execute a command in a running container
docker exec -it <container-id> bash

# View resource usage
docker stats
```

The `docker exec -it <container-id> bash` command is super useful for debugging. It opens a shell inside the running container so you can poke around, check files, run commands.

One more thing: environment variables. Don't hardcode configuration in your image. Use environment variables:

```dockerfile
ENV MODEL_PATH=/app/models/model.joblib
ENV LOG_LEVEL=INFO
```

And override them at runtime:

```bash
docker run -e MODEL_PATH=/data/new_model.joblib -e LOG_LEVEL=DEBUG churn-model:v1
```

This makes your image configurable without rebuilding.

Alright, that's the Docker basics. The key takeaway is that Docker gives you consistency. Build once, run anywhere. Your image works the same on your laptop, in CI/CD, in staging, and in production.

In the next lecture, we'll put all this together and build a production-ready Docker image for our model service, with all the best practices we've discussed.

See you there.

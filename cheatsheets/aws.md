# AWS Cheatsheet for MLOps/DevOps Engineers

## AWS CLI Setup & Configuration

### Installation
```bash
# Linux (x86_64) - with signature verification
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip.sig" -o "awscliv2.sig"
# Optional: Verify signature with AWS public key
# gpg --import aws-cli-public-key.asc
# gpg --verify awscliv2.sig awscliv2.zip
unzip awscliv2.zip
sudo ./aws/install

# macOS
brew install awscli

# Verify installation
aws --version

# Note: Installing via pip is deprecated for AWS CLI v2
# Use the methods above (curl installer or brew) instead
```

### Configuration
```bash
# Configure AWS CLI (interactive)
aws configure

# Configure with specific profile
aws configure --profile production

# List profiles
aws configure list-profiles

# View configuration
aws configure list
aws configure list --profile production

# Set specific configuration values
aws configure set region us-east-1
aws configure set output json
aws configure set aws_access_key_id YOUR_KEY
aws configure set aws_secret_access_key YOUR_SECRET

# Use specific profile for command
aws s3 ls --profile production

# Set default profile for session
export AWS_PROFILE=production
export AWS_DEFAULT_REGION=us-east-1
```

### Configuration Files
```bash
# ~/.aws/config
[default]
region = us-east-1
output = json

[profile production]
region = us-west-2
output = json

[profile staging]
region = us-east-1
output = yaml

# ~/.aws/credentials
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = secret...

[production]
aws_access_key_id = AKIA...
aws_secret_access_key = secret...
role_arn = arn:aws:iam::123456789:role/MLOpsRole
source_profile = default

# Using IAM roles (recommended for EC2/ECS)
# No credentials file needed - uses instance metadata
```

### MFA & SSO
```bash
# Get session token with MFA
aws sts get-session-token \
  --serial-number arn:aws:iam::123456789:mfa/user \
  --token-code 123456

# Configure SSO
aws configure sso
aws sso login --profile sso-profile

# Use SSO profile
aws s3 ls --profile sso-profile
```

---

## IAM (Identity & Access Management)

### Users & Groups
```bash
# List users
aws iam list-users

# Create user
aws iam create-user --user-name mlops-user

# Delete user
aws iam delete-user --user-name old-user

# List groups
aws iam list-groups

# Create group
aws iam create-group --group-name MLOpsEngineers

# Add user to group
aws iam add-user-to-group \
  --user-name mlops-user \
  --group-name MLOpsEngineers

# Remove user from group
aws iam remove-user-from-group \
  --user-name mlops-user \
  --group-name MLOpsEngineers
```

### Access Keys
```bash
# Create access key for user
aws iam create-access-key --user-name mlops-user

# List access keys
aws iam list-access-keys --user-name mlops-user

# Delete access key
aws iam delete-access-key \
  --user-name mlops-user \
  --access-key-id AKIA...

# Rotate access keys
aws iam update-access-key \
  --user-name mlops-user \
  --access-key-id AKIA... \
  --status Inactive
```

### Policies
```bash
# List policies
aws iam list-policies
aws iam list-policies --scope Local  # Customer managed

# Get policy
aws iam get-policy --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Create policy
aws iam create-policy \
  --policy-name MLOpsPolicy \
  --policy-document file://policy.json

# Attach policy to user
aws iam attach-user-policy \
  --user-name mlops-user \
  --policy-arn arn:aws:iam::123456789:policy/MLOpsPolicy

# Attach policy to group
aws iam attach-group-policy \
  --group-name MLOpsEngineers \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Detach policy
aws iam detach-user-policy \
  --user-name mlops-user \
  --policy-arn arn:aws:iam::123456789:policy/MLOpsPolicy

# List attached policies
aws iam list-attached-user-policies --user-name mlops-user
```

### Roles
```bash
# List roles
aws iam list-roles

# Create role
aws iam create-role \
  --role-name MLOpsEC2Role \
  --assume-role-policy-document file://trust-policy.json

# Attach policy to role
aws iam attach-role-policy \
  --role-name MLOpsEC2Role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Create instance profile
aws iam create-instance-profile \
  --instance-profile-name MLOpsInstanceProfile

# Add role to instance profile
aws iam add-role-to-instance-profile \
  --instance-profile-name MLOpsInstanceProfile \
  --role-name MLOpsEC2Role
```

### Example IAM Policies for MLOps
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "MLOpsS3Access",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::mlops-data-bucket/*",
        "arn:aws:s3:::mlops-models-bucket/*"
      ]
    },
    {
      "Sid": "ECRAccess",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Sid": "SageMakerAccess",
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateTrainingJob",
        "sagemaker:DescribeTrainingJob",
        "sagemaker:CreateModel",
        "sagemaker:CreateEndpoint",
        "sagemaker:CreateEndpointConfig",
        "sagemaker:InvokeEndpoint"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## S3 (Simple Storage Service)

### Bucket Operations
```bash
# List buckets
aws s3 ls
aws s3api list-buckets

# Create bucket
aws s3 mb s3://my-mlops-bucket
aws s3api create-bucket \
  --bucket my-mlops-bucket \
  --region us-east-1

# Create bucket in specific region (not us-east-1)
aws s3api create-bucket \
  --bucket my-mlops-bucket \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# Delete bucket
aws s3 rb s3://my-mlops-bucket
aws s3 rb s3://my-mlops-bucket --force  # Delete with contents

# List bucket contents
aws s3 ls s3://my-mlops-bucket/
aws s3 ls s3://my-mlops-bucket/data/ --recursive
aws s3 ls s3://my-mlops-bucket/ --human-readable --summarize
```

### File Operations
```bash
# Upload file
aws s3 cp model.pkl s3://my-mlops-bucket/models/
aws s3 cp data/ s3://my-mlops-bucket/data/ --recursive

# Download file
aws s3 cp s3://my-mlops-bucket/models/model.pkl .
aws s3 cp s3://my-mlops-bucket/data/ ./data/ --recursive

# Sync directories (efficient for large datasets)
aws s3 sync ./local-data/ s3://my-mlops-bucket/data/
aws s3 sync s3://my-mlops-bucket/data/ ./local-data/

# Move/rename objects
aws s3 mv s3://my-mlops-bucket/old.pkl s3://my-mlops-bucket/new.pkl
aws s3 mv data/ s3://my-mlops-bucket/data/ --recursive

# Delete objects
aws s3 rm s3://my-mlops-bucket/old-model.pkl
aws s3 rm s3://my-mlops-bucket/old-data/ --recursive

# Copy between buckets
aws s3 cp s3://source-bucket/file s3://dest-bucket/file
```

### Advanced S3 Operations
```bash
# Upload with storage class
aws s3 cp model.pkl s3://bucket/models/ --storage-class GLACIER

# Upload with server-side encryption
aws s3 cp data.csv s3://bucket/data/ --sse AES256

# Generate presigned URL
aws s3 presign s3://my-bucket/model.pkl --expires-in 3600

# List multipart uploads
aws s3api list-multipart-uploads --bucket my-bucket

# Abort multipart uploads
aws s3api abort-multipart-upload \
  --bucket my-bucket \
  --key large-file.tar.gz \
  --upload-id UPLOAD_ID

# Get object metadata
aws s3api head-object --bucket my-bucket --key model.pkl

# Copy with metadata
aws s3api copy-object \
  --bucket my-bucket \
  --copy-source my-bucket/old.pkl \
  --key new.pkl \
  --metadata "version=1.0,trained=2024-01-01"
```

### Bucket Configuration
```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Enable logging
aws s3api put-bucket-logging \
  --bucket my-bucket \
  --bucket-logging-status file://logging.json

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json

# Set bucket policy
aws s3api put-bucket-policy \
  --bucket my-bucket \
  --policy file://bucket-policy.json

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration file://encryption.json
```

### Example S3 Lifecycle Policy (for ML Data)
```json
{
  "Rules": [
    {
      "Id": "MoveOldModelsToGlacier",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "models/"
      },
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "Id": "DeleteOldTrainingData",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "training-data/"
      },
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

---

## EC2 (Elastic Compute Cloud)

### Instance Management
```bash
# List instances
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"

# List instances (formatted)
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress]' \
  --output table

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.large \
  --key-name my-key-pair \
  --security-group-ids sg-123456 \
  --subnet-id subnet-123456 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ml-training-server}]'

# Launch GPU instance for ML training
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type p3.2xlarge \
  --key-name my-key-pair \
  --iam-instance-profile Name=MLOpsInstanceProfile \
  --block-device-mappings file://block-device-mappings.json \
  --user-data file://user-data.sh

# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Reboot instance
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# Get instance status
aws ec2 describe-instance-status --instance-ids i-1234567890abcdef0
```

### AMIs
```bash
# List AMIs
aws ec2 describe-images --owners self

# Create AMI from instance
aws ec2 create-image \
  --instance-id i-1234567890abcdef0 \
  --name "ml-training-server-v1" \
  --description "ML training server with CUDA 11.8"

# Copy AMI to another region
aws ec2 copy-image \
  --source-region us-east-1 \
  --source-image-id ami-123456 \
  --region us-west-2 \
  --name "ml-training-server-v1-west"

# Deregister AMI
aws ec2 deregister-image --image-id ami-123456
```

### Security Groups
```bash
# List security groups
aws ec2 describe-security-groups

# Create security group
aws ec2 create-security-group \
  --group-name mlops-sg \
  --description "Security group for MLOps servers" \
  --vpc-id vpc-123456

# Add inbound rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-123456 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Add multiple rules
aws ec2 authorize-security-group-ingress \
  --group-id sg-123456 \
  --ip-permissions file://ip-permissions.json

# Remove rule
aws ec2 revoke-security-group-ingress \
  --group-id sg-123456 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

### Key Pairs
```bash
# List key pairs
aws ec2 describe-key-pairs

# Create key pair
aws ec2 create-key-pair \
  --key-name my-key-pair \
  --query 'KeyMaterial' \
  --output text > my-key-pair.pem

# Set permissions
chmod 400 my-key-pair.pem

# Delete key pair
aws ec2 delete-key-pair --key-name old-key-pair
```

### Volumes (EBS)
```bash
# List volumes
aws ec2 describe-volumes

# Create volume
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 100 \
  --volume-type gp3 \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=ml-data-volume}]'

# Attach volume
aws ec2 attach-volume \
  --volume-id vol-123456 \
  --instance-id i-1234567890abcdef0 \
  --device /dev/sdf

# Detach volume
aws ec2 detach-volume --volume-id vol-123456

# Create snapshot
aws ec2 create-snapshot \
  --volume-id vol-123456 \
  --description "ML data backup 2024-01-01"

# List snapshots
aws ec2 describe-snapshots --owner-ids self

# Delete snapshot
aws ec2 delete-snapshot --snapshot-id snap-123456
```

### User Data Script for ML Instance
```bash
#!/bin/bash
# user-data.sh - Bootstrap ML training instance

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Install NVIDIA drivers
apt-get install -y ubuntu-drivers-common
ubuntu-drivers autoinstall

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update
apt-get install -y nvidia-container-toolkit
systemctl restart docker

# Install Python and ML libraries
apt-get install -y python3-pip python3-venv
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install tensorflow mlflow dvc boto3 pandas scikit-learn

# Mount EBS volume
mkfs -t ext4 /dev/nvme1n1
mkdir /data
mount /dev/nvme1n1 /data
echo "/dev/nvme1n1 /data ext4 defaults,nofail 0 2" >> /etc/fstab

# Setup MLflow
pip3 install mlflow[extras]
mkdir -p /opt/mlflow
cd /opt/mlflow
nohup mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlops-artifacts \
  --host 0.0.0.0 &

echo "ML instance setup complete" > /var/log/user-data.log
```

---

## ECR (Elastic Container Registry)

### Repository Management
```bash
# Create repository
aws ecr create-repository \
  --repository-name ml-api \
  --image-scanning-configuration scanOnPush=true

# List repositories
aws ecr describe-repositories

# Delete repository
aws ecr delete-repository \
  --repository-name ml-api \
  --force  # Delete even if it contains images

# Get repository URI
aws ecr describe-repositories \
  --repository-names ml-api \
  --query 'repositories[0].repositoryUri' \
  --output text
```

### Image Operations
```bash
# Get login password
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag ml-api:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest

# Push image
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest

# Pull image
docker pull 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest

# List images
aws ecr list-images --repository-name ml-api

# Describe images
aws ecr describe-images --repository-name ml-api

# Delete image
aws ecr batch-delete-image \
  --repository-name ml-api \
  --image-ids imageTag=v1.0.0
```

### Lifecycle Policies
```bash
# Put lifecycle policy
aws ecr put-lifecycle-policy \
  --repository-name ml-api \
  --lifecycle-policy-text file://lifecycle-policy.json

# Example lifecycle policy
cat > lifecycle-policy.json << 'EOF'
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 10 images",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
```

---

## ECS (Elastic Container Service)

### Cluster Management
```bash
# Create cluster
aws ecs create-cluster --cluster-name mlops-cluster

# List clusters
aws ecs list-clusters

# Describe cluster
aws ecs describe-clusters --clusters mlops-cluster

# Delete cluster
aws ecs delete-cluster --cluster mlops-cluster
```

### Task Definitions
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# List task definitions
aws ecs list-task-definitions

# Describe task definition
aws ecs describe-task-definition --task-definition ml-api:1

# Deregister task definition
aws ecs deregister-task-definition --task-definition ml-api:1
```

### Example Task Definition for ML API
```json
{
  "family": "ml-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "ml-api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "MLFLOW_TRACKING_URI",
          "value": "http://mlflow.example.com"
        },
        {
          "name": "MODEL_VERSION",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "AWS_ACCESS_KEY_ID",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:mlops/aws-credentials:access_key_id::"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ml-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### Services
```bash
# Create service
aws ecs create-service \
  --cluster mlops-cluster \
  --service-name ml-api \
  --task-definition ml-api:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-123456],securityGroups=[sg-123456],assignPublicIp=ENABLED}"

# Update service
aws ecs update-service \
  --cluster mlops-cluster \
  --service ml-api \
  --desired-count 3

# Update service with new task definition
aws ecs update-service \
  --cluster mlops-cluster \
  --service ml-api \
  --task-definition ml-api:2 \
  --force-new-deployment

# List services
aws ecs list-services --cluster mlops-cluster

# Describe service
aws ecs describe-services \
  --cluster mlops-cluster \
  --services ml-api

# Delete service
aws ecs delete-service \
  --cluster mlops-cluster \
  --service ml-api \
  --force
```

### Tasks
```bash
# Run task
aws ecs run-task \
  --cluster mlops-cluster \
  --task-definition ml-training:1 \
  --count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-123456],securityGroups=[sg-123456]}"

# List tasks
aws ecs list-tasks --cluster mlops-cluster

# Describe tasks
aws ecs describe-tasks \
  --cluster mlops-cluster \
  --tasks task-id

# Stop task
aws ecs stop-task \
  --cluster mlops-cluster \
  --task task-id
```

---

## Lambda

### Function Management
```bash
# Create function
aws lambda create-function \
  --function-name ml-inference \
  --runtime python3.11 \
  --role arn:aws:iam::123456789:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip

# List functions
aws lambda list-functions

# Get function
aws lambda get-function --function-name ml-inference

# Update function code
aws lambda update-function-code \
  --function-name ml-inference \
  --zip-file fileb://function.zip

# Update function configuration
aws lambda update-function-configuration \
  --function-name ml-inference \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables={MODEL_VERSION=v1.0.0}

# Delete function
aws lambda delete-function --function-name ml-inference
```

### Invoke Function
```bash
# Invoke function (synchronous)
aws lambda invoke \
  --function-name ml-inference \
  --payload '{"features": [1, 2, 3]}' \
  response.json

# Invoke function (asynchronous)
aws lambda invoke \
  --function-name ml-inference \
  --invocation-type Event \
  --payload '{"features": [1, 2, 3]}' \
  response.json

# View logs
aws logs tail /aws/lambda/ml-inference --follow
```

### Example Lambda Function for ML Inference
```python
# lambda_function.py
import json
import boto3
import pickle

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Load model from S3
    bucket = 'ml-models'
    key = 'churn_model.pkl'
    
    response = s3.get_object(Bucket=bucket, Key=key)
    model = pickle.loads(response['Body'].read())
    
    # Get features from event
    features = event.get('features', [])
    
    # Make prediction
    prediction = model.predict([features])
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'prediction': int(prediction[0]),
            'probability': float(model.predict_proba([features])[0][1])
        })
    }
```

---

## SageMaker

### Training Jobs
```bash
# Create training job
aws sagemaker create-training-job \
  --training-job-name churn-model-training \
  --role-arn arn:aws:iam::123456789:role/SageMakerRole \
  --algorithm-specification \
    TrainingImage=382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest,TrainingInputMode=File \
  --input-data-config file://input-data-config.json \
  --output-data-config S3OutputPath=s3://mlops-models/output \
  --resource-config InstanceType=ml.m5.xlarge,InstanceCount=1,VolumeSizeInGB=30 \
  --stopping-condition MaxRuntimeInSeconds=3600

# Describe training job
aws sagemaker describe-training-job --training-job-name churn-model-training

# List training jobs
aws sagemaker list-training-jobs

# Stop training job
aws sagemaker stop-training-job --training-job-name churn-model-training
```

### Models
```bash
# Create model
aws sagemaker create-model \
  --model-name churn-model \
  --primary-container Image=382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest,ModelDataUrl=s3://mlops-models/model.tar.gz \
  --execution-role-arn arn:aws:iam::123456789:role/SageMakerRole

# List models
aws sagemaker list-models

# Delete model
aws sagemaker delete-model --model-name churn-model
```

### Endpoints
```bash
# Create endpoint configuration
aws sagemaker create-endpoint-config \
  --endpoint-config-name churn-model-config \
  --production-variants VariantName=AllTraffic,ModelName=churn-model,InstanceType=ml.t2.medium,InitialInstanceCount=1

# Create endpoint
aws sagemaker create-endpoint \
  --endpoint-name churn-model-endpoint \
  --endpoint-config-name churn-model-config

# Describe endpoint
aws sagemaker describe-endpoint --endpoint-name churn-model-endpoint

# Update endpoint
aws sagemaker update-endpoint \
  --endpoint-name churn-model-endpoint \
  --endpoint-config-name churn-model-config-v2

# Delete endpoint
aws sagemaker delete-endpoint --endpoint-name churn-model-endpoint

# Invoke endpoint
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name churn-model-endpoint \
  --body '{"features": [1, 2, 3]}' \
  --content-type application/json \
  output.json
```

### Batch Transform Jobs
```bash
# Create batch transform job
aws sagemaker create-transform-job \
  --transform-job-name churn-batch-inference \
  --model-name churn-model \
  --transform-input DataSource={S3DataSource={S3DataType=S3Prefix,S3Uri=s3://mlops-data/batch-input/}},ContentType=text/csv \
  --transform-output S3OutputPath=s3://mlops-data/batch-output/ \
  --transform-resources InstanceType=ml.m5.xlarge,InstanceCount=1

# Describe transform job
aws sagemaker describe-transform-job --transform-job-name churn-batch-inference
```

---

## CloudWatch

### Logs
```bash
# List log groups
aws logs describe-log-groups

# Create log group
aws logs create-log-group --log-group-name /aws/lambda/ml-inference

# List log streams
aws logs describe-log-streams --log-group-name /aws/lambda/ml-inference

# Get log events
aws logs get-log-events \
  --log-group-name /aws/lambda/ml-inference \
  --log-stream-name 2024/01/01/stream

# Tail logs
aws logs tail /aws/lambda/ml-inference --follow

# Filter logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/ml-inference \
  --filter-pattern "ERROR"

# Delete log group
aws logs delete-log-group --log-group-name /aws/lambda/ml-inference
```

### Metrics
```bash
# List metrics
aws cloudwatch list-metrics --namespace AWS/EC2

# Put custom metric
aws cloudwatch put-metric-data \
  --namespace MLOps \
  --metric-name PredictionLatency \
  --value 125.5 \
  --unit Milliseconds \
  --dimensions Model=churn-predictor,Version=v1.0.0

# Get metric statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum
```

### Alarms
```bash
# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu-usage \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --alarm-actions arn:aws:sns:us-east-1:123456789:mlops-alerts

# List alarms
aws cloudwatch describe-alarms

# Delete alarm
aws cloudwatch delete-alarms --alarm-names high-cpu-usage
```

---

## Secrets Manager

### Secret Management
```bash
# Create secret
aws secretsmanager create-secret \
  --name mlops/db-credentials \
  --secret-string '{"username":"admin","password":"secret123"}'

# Get secret value
aws secretsmanager get-secret-value --secret-id mlops/db-credentials

# Update secret
aws secretsmanager update-secret \
  --secret-id mlops/db-credentials \
  --secret-string '{"username":"admin","password":"newsecret456"}'

# List secrets
aws secretsmanager list-secrets

# Delete secret
aws secretsmanager delete-secret \
  --secret-id mlops/db-credentials \
  --recovery-window-in-days 7

# Restore secret
aws secretsmanager restore-secret --secret-id mlops/db-credentials
```

---

## Systems Manager (SSM)

### Parameter Store
```bash
# Put parameter
aws ssm put-parameter \
  --name /mlops/model-version \
  --value "v1.0.0" \
  --type String

# Put secure parameter
aws ssm put-parameter \
  --name /mlops/api-key \
  --value "secret-key-123" \
  --type SecureString

# Get parameter
aws ssm get-parameter --name /mlops/model-version

# Get parameter with decryption
aws ssm get-parameter \
  --name /mlops/api-key \
  --with-decryption

# Get parameters by path
aws ssm get-parameters-by-path --path /mlops/

# List parameters
aws ssm describe-parameters

# Delete parameter
aws ssm delete-parameter --name /mlops/old-config
```

### Session Manager
```bash
# Start session with EC2 instance
aws ssm start-session --target i-1234567890abcdef0

# Run command on instances
aws ssm send-command \
  --document-name "AWS-RunShellScript" \
  --targets "Key=tag:Environment,Values=production" \
  --parameters 'commands=["df -h","free -m"]'

# Get command invocation
aws ssm get-command-invocation \
  --command-id command-id \
  --instance-id i-1234567890abcdef0
```

---

## Real-Time MLOps Scenarios

### Scenario 1: Automated Model Training Pipeline
```bash
#!/bin/bash
# train-and-deploy.sh - Complete ML training and deployment pipeline

set -e

# Configuration
MODEL_NAME="churn-predictor"
S3_DATA_BUCKET="s3://mlops-data"
S3_MODEL_BUCKET="s3://mlops-models"
ECR_REPO="123456789.dkr.ecr.us-east-1.amazonaws.com/ml-api"
CLUSTER_NAME="mlops-cluster"
SERVICE_NAME="ml-api"

# Step 1: Pull latest data from S3
echo "Pulling training data from S3..."
aws s3 sync ${S3_DATA_BUCKET}/training/ ./data/

# Step 2: Launch SageMaker training job
echo "Starting SageMaker training job..."
TRAINING_JOB_NAME="${MODEL_NAME}-$(date +%Y%m%d-%H%M%S)"

aws sagemaker create-training-job \
  --training-job-name ${TRAINING_JOB_NAME} \
  --role-arn arn:aws:iam::123456789:role/SageMakerRole \
  --algorithm-specification \
    TrainingImage=382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest,TrainingInputMode=File \
  --input-data-config file://training-config.json \
  --output-data-config S3OutputPath=${S3_MODEL_BUCKET}/${TRAINING_JOB_NAME}/ \
  --resource-config InstanceType=ml.m5.xlarge,InstanceCount=1,VolumeSizeInGB=30 \
  --stopping-condition MaxRuntimeInSeconds=3600

# Step 3: Wait for training to complete
echo "Waiting for training job to complete..."
aws sagemaker wait training-job-completed-or-stopped \
  --training-job-name ${TRAINING_JOB_NAME}

# Check if training succeeded
STATUS=$(aws sagemaker describe-training-job \
  --training-job-name ${TRAINING_JOB_NAME} \
  --query 'TrainingJobStatus' \
  --output text)

if [ "$STATUS" != "Completed" ]; then
  echo "Training failed with status: $STATUS"
  exit 1
fi

# Step 4: Download and validate model
echo "Downloading trained model..."
aws s3 cp ${S3_MODEL_BUCKET}/${TRAINING_JOB_NAME}/output/model.tar.gz ./model.tar.gz
tar -xzf model.tar.gz

# Validate model (custom script)
python scripts/validate_model.py --model-path ./model

# Step 5: Build and push Docker image with new model
echo "Building Docker image..."
docker build -t ${MODEL_NAME}:${TRAINING_JOB_NAME} .

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ${ECR_REPO}

# Tag and push
docker tag ${MODEL_NAME}:${TRAINING_JOB_NAME} ${ECR_REPO}:${TRAINING_JOB_NAME}
docker tag ${MODEL_NAME}:${TRAINING_JOB_NAME} ${ECR_REPO}:latest
docker push ${ECR_REPO}:${TRAINING_JOB_NAME}
docker push ${ECR_REPO}:latest

# Step 6: Create SageMaker model
echo "Creating SageMaker model..."
aws sagemaker create-model \
  --model-name ${MODEL_NAME}-${TRAINING_JOB_NAME} \
  --primary-container \
    Image=382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest,ModelDataUrl=${S3_MODEL_BUCKET}/${TRAINING_JOB_NAME}/output/model.tar.gz \
  --execution-role-arn arn:aws:iam::123456789:role/SageMakerRole

# Step 7: Update ECS service with new image
echo "Updating ECS service..."
TASK_DEFINITION=$(aws ecs describe-services \
  --cluster ${CLUSTER_NAME} \
  --services ${SERVICE_NAME} \
  --query 'services[0].taskDefinition' \
  --output text)

# Register new task definition with updated image
NEW_TASK_DEF=$(aws ecs describe-task-definition \
  --task-definition ${TASK_DEFINITION} \
  --query 'taskDefinition' | \
  jq --arg IMAGE "${ECR_REPO}:${TRAINING_JOB_NAME}" \
    '.containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)')

aws ecs register-task-definition --cli-input-json "$NEW_TASK_DEF" > /dev/null

# Update service
aws ecs update-service \
  --cluster ${CLUSTER_NAME} \
  --service ${SERVICE_NAME} \
  --force-new-deployment

# Step 8: Wait for deployment to complete
echo "Waiting for deployment to complete..."
aws ecs wait services-stable \
  --cluster ${CLUSTER_NAME} \
  --services ${SERVICE_NAME}

# Step 9: Run smoke tests
echo "Running smoke tests..."
ENDPOINT_URL=$(aws ecs describe-services \
  --cluster ${CLUSTER_NAME} \
  --services ${SERVICE_NAME} \
  --query 'services[0].loadBalancers[0].targetGroupArn' \
  --output text)

python scripts/smoke_test.py --endpoint ${ENDPOINT_URL}

# Step 10: Update CloudWatch dashboard
echo "Updating CloudWatch metrics..."
aws cloudwatch put-metric-data \
  --namespace MLOps \
  --metric-name ModelVersion \
  --value 1 \
  --dimensions Model=${MODEL_NAME},Version=${TRAINING_JOB_NAME}

echo "Deployment complete! Model version: ${TRAINING_JOB_NAME}"
```

### Scenario 2: Batch Inference Pipeline
```bash
#!/bin/bash
# batch-inference.sh - Run batch predictions on S3 data

set -e

# Configuration
MODEL_NAME="churn-predictor"
INPUT_BUCKET="s3://mlops-data/batch-input"
OUTPUT_BUCKET="s3://mlops-data/batch-output"
DATE=$(date +%Y%m%d)

# Step 1: Create batch transform job
echo "Starting batch transform job..."
TRANSFORM_JOB_NAME="${MODEL_NAME}-batch-${DATE}"

aws sagemaker create-transform-job \
  --transform-job-name ${TRANSFORM_JOB_NAME} \
  --model-name ${MODEL_NAME} \
  --transform-input \
    DataSource={S3DataSource={S3DataType=S3Prefix,S3Uri=${INPUT_BUCKET}/}},ContentType=text/csv,SplitType=Line \
  --transform-output S3OutputPath=${OUTPUT_BUCKET}/${DATE}/ \
  --transform-resources InstanceType=ml.m5.xlarge,InstanceCount=2 \
  --batch-strategy MultiRecord \
  --max-payload-in-mb 6 \
  --max-concurrent-transforms 4

# Step 2: Wait for completion
echo "Waiting for batch inference to complete..."
aws sagemaker wait transform-job-completed-or-stopped \
  --transform-job-name ${TRANSFORM_JOB_NAME}

# Step 3: Download and process results
echo "Downloading results..."
aws s3 sync ${OUTPUT_BUCKET}/${DATE}/ ./results/

# Step 4: Generate report
python scripts/generate_batch_report.py \
  --input-dir ./results/ \
  --output batch_report_${DATE}.html

# Step 5: Upload report
aws s3 cp batch_report_${DATE}.html s3://mlops-reports/

# Step 6: Send notification
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123456789:mlops-notifications \
  --subject "Batch Inference Complete" \
  --message "Batch inference job ${TRANSFORM_JOB_NAME} completed. Report: s3://mlops-reports/batch_report_${DATE}.html"

echo "Batch inference complete!"
```

### Scenario 3: Model Monitoring and Drift Detection
```bash
#!/bin/bash
# monitor-model.sh - Monitor model performance and detect drift

set -e

# Configuration
MODEL_NAME="churn-predictor"
CLOUDWATCH_NAMESPACE="MLOps"
DRIFT_THRESHOLD=0.05

# Step 1: Collect production predictions from CloudWatch Logs
echo "Collecting production data..."
aws logs filter-log-events \
  --log-group-name /aws/ecs/ml-api \
  --filter-pattern "[time, request_id, prediction, *]" \
  --start-time $(date -d '1 day ago' +%s)000 \
  --output json > production_logs.json

# Step 2: Download reference data from S3
aws s3 cp s3://mlops-data/reference/reference_data.csv ./

# Step 3: Run drift detection
python scripts/detect_drift.py \
  --production-logs production_logs.json \
  --reference-data reference_data.csv \
  --output drift_report.json

# Step 4: Parse drift score
DRIFT_SCORE=$(jq -r '.drift_score' drift_report.json)

# Step 5: Publish metrics to CloudWatch
aws cloudwatch put-metric-data \
  --namespace ${CLOUDWATCH_NAMESPACE} \
  --metric-name DataDrift \
  --value ${DRIFT_SCORE} \
  --dimensions Model=${MODEL_NAME}

# Step 6: Check if drift threshold exceeded
if (( $(echo "$DRIFT_SCORE > $DRIFT_THRESHOLD" | bc -l) )); then
  echo "Drift detected! Score: ${DRIFT_SCORE}"
  
  # Trigger alarm
  aws cloudwatch set-alarm-state \
    --alarm-name model-drift-alarm \
    --state-value ALARM \
    --state-reason "Drift score ${DRIFT_SCORE} exceeds threshold ${DRIFT_THRESHOLD}"
  
  # Trigger retraining
  aws lambda invoke \
    --function-name trigger-model-retraining \
    --payload "{\"model_name\": \"${MODEL_NAME}\", \"drift_score\": ${DRIFT_SCORE}}" \
    response.json
  
  echo "Retraining triggered"
else
  echo "No significant drift detected. Score: ${DRIFT_SCORE}"
fi

# Step 7: Upload drift report
aws s3 cp drift_report.json s3://mlops-reports/drift/$(date +%Y%m%d)/

echo "Model monitoring complete!"
```

### Scenario 4: Multi-Region Deployment
```bash
#!/bin/bash
# multi-region-deploy.sh - Deploy model to multiple AWS regions

set -e

# Configuration
MODEL_NAME="churn-predictor"
IMAGE_TAG="latest"
REGIONS=("us-east-1" "us-west-2" "eu-west-1")

# Step 1: Build and push image to primary region
PRIMARY_REGION="us-east-1"
PRIMARY_ECR="123456789.dkr.ecr.${PRIMARY_REGION}.amazonaws.com"

echo "Building image in ${PRIMARY_REGION}..."
aws ecr get-login-password --region ${PRIMARY_REGION} | \
  docker login --username AWS --password-stdin ${PRIMARY_ECR}

docker build -t ${MODEL_NAME}:${IMAGE_TAG} .
docker tag ${MODEL_NAME}:${IMAGE_TAG} ${PRIMARY_ECR}/${MODEL_NAME}:${IMAGE_TAG}
docker push ${PRIMARY_ECR}/${MODEL_NAME}:${IMAGE_TAG}

# Step 2: Replicate to other regions
for REGION in "${REGIONS[@]}"; do
  if [ "$REGION" != "$PRIMARY_REGION" ]; then
    echo "Replicating to ${REGION}..."
    
    # Create ECR repository in target region
    aws ecr create-repository \
      --repository-name ${MODEL_NAME} \
      --region ${REGION} 2>/dev/null || true
    
    # Pull from primary
    docker pull ${PRIMARY_ECR}/${MODEL_NAME}:${IMAGE_TAG}
    
    # Push to target region
    TARGET_ECR="123456789.dkr.ecr.${REGION}.amazonaws.com"
    aws ecr get-login-password --region ${REGION} | \
      docker login --username AWS --password-stdin ${TARGET_ECR}
    
    docker tag ${MODEL_NAME}:${IMAGE_TAG} ${TARGET_ECR}/${MODEL_NAME}:${IMAGE_TAG}
    docker push ${TARGET_ECR}/${MODEL_NAME}:${IMAGE_TAG}
  fi
done

# Step 3: Deploy to each region
for REGION in "${REGIONS[@]}"; do
  echo "Deploying to ${REGION}..."
  
  # Update ECS service
  aws ecs update-service \
    --cluster mlops-cluster \
    --service ml-api \
    --force-new-deployment \
    --region ${REGION}
  
  # Wait for deployment
  aws ecs wait services-stable \
    --cluster mlops-cluster \
    --services ml-api \
    --region ${REGION}
  
  echo "Deployment to ${REGION} complete"
done

echo "Multi-region deployment complete!"
```

### Scenario 5: Cost Optimization
```bash
#!/bin/bash
# cost-optimization.sh - Analyze and optimize AWS costs for ML workloads

set -e

# Step 1: Analyze EC2 instances
echo "Analyzing EC2 instances..."
aws ec2 describe-instances \
  --filters "Name=tag:Project,Values=mlops" \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,LaunchTime]' \
  --output table

# Find stopped instances older than 7 days
STOPPED_INSTANCES=$(aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=stopped" \
  --query "Reservations[*].Instances[?LaunchTime<='$(date -d '7 days ago' --iso-8601)'].[InstanceId]" \
  --output text)

if [ -n "$STOPPED_INSTANCES" ]; then
  echo "Terminating old stopped instances..."
  aws ec2 terminate-instances --instance-ids $STOPPED_INSTANCES
fi

# Step 2: Analyze S3 storage
echo "Analyzing S3 storage..."
for BUCKET in $(aws s3 ls | awk '{print $3}'); do
  SIZE=$(aws s3 ls s3://${BUCKET} --recursive --summarize | grep "Total Size" | awk '{print $3}')
  echo "Bucket: ${BUCKET}, Size: ${SIZE} bytes"
done

# Step 3: Clean up old ML artifacts
echo "Cleaning up old ML artifacts..."
aws s3 rm s3://mlops-models/experiments/ --recursive \
  --exclude "*" --include "*/$(date -d '30 days ago' +%Y/%m/%d)/*"

# Step 4: Optimize EBS volumes
echo "Finding unused EBS volumes..."
UNUSED_VOLUMES=$(aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].[VolumeId,Size,CreateTime]' \
  --output text)

echo "$UNUSED_VOLUMES"

# Step 5: Review ECR images
echo "Cleaning up old ECR images..."
for REPO in $(aws ecr describe-repositories --query 'repositories[*].repositoryName' --output text); do
  # Keep only last 10 images
  IMAGE_DIGESTS=$(aws ecr list-images --repository-name ${REPO} \
    --query 'imageIds[10:].[imageDigest]' --output text)
  
  if [ -n "$IMAGE_DIGESTS" ]; then
    for DIGEST in $IMAGE_DIGESTS; do
      aws ecr batch-delete-image \
        --repository-name ${REPO} \
        --image-ids imageDigest=${DIGEST}
    done
  fi
done

# Step 6: Generate cost report
echo "Generating cost report..."
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=SERVICE \
  --output json > cost_report.json

# Step 7: Create cost anomaly alert
aws ce put-anomaly-subscription \
  --subscription-name mlops-cost-anomaly \
  --threshold-expression '{"Dimensions": {"Key": "SERVICE", "Values": ["Amazon SageMaker", "Amazon EC2"]}}' \
  --subscribers \
    '[{"Type": "SNS", "Address": "arn:aws:sns:us-east-1:123456789:mlops-alerts"}]'

echo "Cost optimization complete!"
```

---

## Best Practices

### Security Best Practices
```bash
# 1. Use IAM roles instead of access keys
# Attach IAM role to EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-1234567890abcdef0 \
  --iam-instance-profile Name=MLOpsInstanceProfile

# 2. Enable MFA for sensitive operations
aws iam enable-mfa-device \
  --user-name admin \
  --serial-number arn:aws:iam::123456789:mfa/admin \
  --authentication-code-1 123456 \
  --authentication-code-2 789012

# 3. Use Secrets Manager for credentials
aws secretsmanager get-secret-value \
  --secret-id mlops/db-credentials \
  --query 'SecretString' \
  --output text

# 4. Enable encryption at rest
aws s3api put-bucket-encryption \
  --bucket mlops-data \
  --server-side-encryption-configuration file://encryption.json

# 5. Use VPC endpoints for private communication
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-123456 \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-123456
```

### Cost Optimization
```bash
# 1. Use Spot Instances for training
aws ec2 request-spot-instances \
  --spot-price "0.05" \
  --instance-count 1 \
  --type "one-time" \
  --launch-specification file://spot-spec.json

# 2. Use S3 Intelligent-Tiering
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket mlops-data \
  --id intelligent-tiering \
  --intelligent-tiering-configuration file://tiering-config.json

# 3. Enable S3 lifecycle policies
aws s3api put-bucket-lifecycle-configuration \
  --bucket mlops-data \
  --lifecycle-configuration file://lifecycle.json

# 4. Use Auto Scaling
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name mlops-asg \
  --launch-configuration-name mlops-lc \
  --min-size 1 \
  --max-size 10 \
  --desired-capacity 2

# 5. Set up budget alerts
aws budgets create-budget \
  --account-id 123456789 \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

---

## Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Check credentials
aws sts get-caller-identity

# Verify IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:user/mlops-user \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::mlops-bucket/*

# Clear credentials cache
rm -rf ~/.aws/cli/cache
```

#### Region Issues
```bash
# Check current region
aws configure get region

# List available regions
aws ec2 describe-regions --output table

# Override region for single command
aws s3 ls --region us-west-2
```

#### Debugging
```bash
# Enable debug logging
aws s3 ls --debug

# Use --dry-run for testing (EC2 only)
aws ec2 run-instances --dry-run ...

# Check service health
aws health describe-event-aggregates \
  --aggregate-field eventTypeCategory

# View AWS Service Health Dashboard
# https://status.aws.amazon.com/
```

---

## Resources

### Official Documentation
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [AWS SDK Documentation](https://aws.amazon.com/tools/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### ML-Specific Resources
- [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/)
- [SageMaker Examples](https://github.com/aws/amazon-sagemaker-examples)

### Tools
- [aws-cli](https://github.com/aws/aws-cli) - Official AWS CLI
- [aws-vault](https://github.com/99designs/aws-vault) - Secure credential storage
- [awslogs](https://github.com/jorgebastida/awslogs) - Better CloudWatch Logs CLI
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python

---

**[Back to Main Cheatsheets](../README.md)**

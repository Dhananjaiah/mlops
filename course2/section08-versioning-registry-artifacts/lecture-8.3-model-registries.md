# Lecture 8.3 – Model Registries (MLflow Model Registry / SageMaker / Custom)

## Human Transcript

Alright, so we've talked about versioning code with Git and data with tools like DVC. Now let's talk about the third piece: model registries.

A model registry is basically a database of trained models. But it's more than just storage. It tracks metadata, manages lifecycle stages, and controls who can promote models to production.

Think of it like a package repository for your models. Just like npm for JavaScript packages or PyPI for Python packages, a model registry stores your models and lets you retrieve specific versions.

Let me walk you through what a model registry does:

Storage. Obviously, it stores your model files. The trained weights, preprocessing objects, anything needed for inference.

Versioning. Every time you register a model, it gets a version number. Version 1, 2, 3, and so on. You can always retrieve any version.

Metadata. For each model version, you store information like:
- When it was trained
- Who trained it
- What data was used
- What hyperparameters were used
- What metrics it achieved
- The code version

Lifecycle stages. Models typically go through stages: staging, production, archived. The registry tracks which stage each version is in.

Lineage. Where did this model come from? What experiment? What run? The registry tracks this lineage.

Let's look at MLflow Model Registry since it's open source and widely used:

```python
import mlflow

# First, log a model during training
with mlflow.start_run():
    # ... training code ...
    
    # Log the model
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="churn-prediction-model"
    )
```

That's it. The model is now registered. You can see it in the MLflow UI. Let's query it:

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# List all versions of a model
versions = client.search_model_versions("name='churn-prediction-model'")
for v in versions:
    print(f"Version {v.version}: {v.current_stage}, run_id={v.run_id}")

# Get the latest version
latest = client.get_latest_versions("churn-prediction-model", stages=["Production"])
```

Managing lifecycle stages:

```python
# Transition a model to staging
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=3,
    stage="Staging"
)

# After testing, promote to production
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=3,
    stage="Production"
)

# Archive an old version
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=1,
    stage="Archived"
)
```

Loading a model from the registry:

```python
# Load by version number
model = mlflow.sklearn.load_model("models:/churn-prediction-model/3")

# Load production version
model = mlflow.sklearn.load_model("models:/churn-prediction-model/Production")

# Load staging version
model = mlflow.sklearn.load_model("models:/churn-prediction-model/Staging")
```

See how powerful this is? In your production code, you can just load "models:/churn-prediction-model/Production" and you always get the current production model. When you promote a new version, the change is automatic.

Now let's look at AWS SageMaker Model Registry. It's similar conceptually but with AWS integration:

```python
import boto3

sm_client = boto3.client('sagemaker')

# Register a model
response = sm_client.create_model_package(
    ModelPackageGroupName='churn-model-group',
    ModelPackageDescription='Churn model v1',
    InferenceSpecification={
        'Containers': [{
            'Image': '123456789.dkr.ecr.us-east-1.amazonaws.com/churn-inference:latest',
            'ModelDataUrl': 's3://bucket/models/churn/model.tar.gz'
        }],
        'SupportedContentTypes': ['application/json'],
        'SupportedResponseMIMETypes': ['application/json']
    },
    ModelApprovalStatus='PendingManualApproval'  # Requires approval
)

# Approve a model for production
sm_client.update_model_package(
    ModelPackageArn=model_package_arn,
    ModelApprovalStatus='Approved'
)
```

SageMaker has built-in approval workflows. You can require manual approval before a model goes to production.

Google's Vertex AI has similar functionality:

```python
from google.cloud import aiplatform

# Upload a model
model = aiplatform.Model.upload(
    display_name="churn-model",
    artifact_uri="gs://bucket/models/churn/",
    serving_container_image_uri="gcr.io/project/serving-image"
)

# Create model version
model_version = model.create_version(
    version_description="Version trained on Q4 data",
)
```

Now, what if you want a custom registry? Some teams build their own because:
- They need specific features
- They want to integrate with existing systems
- They're not using MLflow or cloud platforms

A simple custom registry might look like this:

```python
# models_registry.py
import boto3
import json
from datetime import datetime

class ModelRegistry:
    def __init__(self, bucket, table_name):
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.bucket = bucket
    
    def register_model(self, name, version, model_path, metadata):
        """Register a new model version."""
        s3_key = f"models/{name}/{version}/model.joblib"
        
        # Upload model to S3
        self.s3.upload_file(model_path, self.bucket, s3_key)
        
        # Store metadata in DynamoDB
        self.table.put_item(Item={
            'model_name': name,
            'version': version,
            'stage': 'Staging',
            's3_path': f"s3://{self.bucket}/{s3_key}",
            'registered_at': datetime.now().isoformat(),
            'metadata': json.dumps(metadata)
        })
    
    def get_model(self, name, version=None, stage=None):
        """Get model by version or stage."""
        if version:
            response = self.table.get_item(
                Key={'model_name': name, 'version': version}
            )
        else:
            # Get by stage
            response = self.table.query(
                KeyConditionExpression='model_name = :name',
                FilterExpression='stage = :stage',
                ExpressionAttributeValues={
                    ':name': name,
                    ':stage': stage
                }
            )
        return response.get('Item')
    
    def promote_to_production(self, name, version):
        """Promote a model version to production."""
        # Demote current production
        current_prod = self.get_model(name, stage='Production')
        if current_prod:
            self.table.update_item(
                Key={'model_name': name, 'version': current_prod['version']},
                UpdateExpression='SET stage = :stage',
                ExpressionAttributeValues={':stage': 'Archived'}
            )
        
        # Promote new version
        self.table.update_item(
            Key={'model_name': name, 'version': version},
            UpdateExpression='SET stage = :stage',
            ExpressionAttributeValues={':stage': 'Production'}
        )
```

This is simplified, but shows the basic pattern. Storage (S3) plus metadata database (DynamoDB).

Some best practices for model registries:

Always include model signatures. Document exactly what inputs the model expects and what outputs it produces:

```python
from mlflow.models.signature import infer_signature

# During training
signature = infer_signature(X_train, model.predict(X_train))
mlflow.sklearn.log_model(model, "model", signature=signature)
```

Include example inputs:

```python
mlflow.sklearn.log_model(
    model, 
    "model",
    input_example=X_train[:5].to_dict(orient='records')
)
```

Add descriptions to model versions:

```python
client.update_model_version(
    name="churn-prediction-model",
    version=3,
    description="Trained on Q4 2023 data. Uses gradient boosting. F1 score: 0.85"
)
```

Use tags for filtering:

```python
client.set_model_version_tag(
    name="churn-prediction-model",
    version=3,
    key="experiment_type",
    value="hyperparameter_tuning"
)
```

Alright, that's model registries. The key points are: store models with metadata, manage lifecycle stages, enable easy retrieval by version or stage, and track lineage back to training runs.

In the next lecture, we'll dive deeper into model states and what staging, production, and archived actually mean in practice.

Questions? Let's continue.

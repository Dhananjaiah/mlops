# Lecture 7.3 – Building a REST API with FastAPI / Flask for the Model

## Human Transcript

Alright, so we've got our model packaged up nicely, and we've got a solid predict function. Now we need to make this model accessible over the network. And the way we do that is by building a REST API.

If you've never built an API before, don't worry. It's actually pretty straightforward. A REST API is just a way for programs to talk to each other over HTTP. Same protocol your web browser uses. The client sends a request, your server processes it, and sends back a response.

Now, there are two main frameworks people use in Python for building APIs: Flask and FastAPI. Flask has been around for a while and is very simple to learn. FastAPI is newer but has some really nice features like automatic documentation and built-in validation. For ML models, I recommend FastAPI. It's fast, it's modern, and it has features that are particularly useful for ML serving.

Let me show you a basic FastAPI setup for our churn model:

```python
# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
import logging

from churn_model.models.predict import ChurnPredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Churn Prediction API",
    description="API for predicting customer churn",
    version="1.0.0"
)

# Load the model at startup
predictor = None

@app.on_event("startup")
async def load_model():
    global predictor
    logger.info("Loading model...")
    predictor = ChurnPredictor("models/churn_model_v1.joblib")
    logger.info("Model loaded successfully")

# Define request schema
class CustomerData(BaseModel):
    customer_id: str
    age: int
    tenure: int
    monthly_charges: float
    total_charges: Optional[float] = None
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Age must be between 0 and 120')
        return v
    
    @validator('monthly_charges')
    def charges_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Monthly charges must be positive')
        return v

class PredictionRequest(BaseModel):
    customers: List[CustomerData]

class PredictionResponse(BaseModel):
    success: bool
    predictions: Optional[List[int]] = None
    probabilities: Optional[List[float]] = None
    model_version: Optional[str] = None
    error: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": predictor is not None}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert request to format expected by predictor
    data = [customer.dict() for customer in request.customers]
    
    # Make predictions
    result = predictor.predict(data)
    
    return PredictionResponse(**result)

# Single prediction endpoint (convenience)
@app.post("/predict/single")
async def predict_single(customer: CustomerData):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    result = predictor.predict(customer.dict())
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    
    return {
        "customer_id": customer.customer_id,
        "churn_prediction": result['predictions'][0],
        "churn_probability": result['probabilities'][0] if result.get('probabilities') else None
    }
```

Let me walk you through what's happening here.

First, we import FastAPI and some related tools. Pydantic is the library FastAPI uses for data validation. When you define a Pydantic model like `CustomerData`, FastAPI automatically validates incoming requests against that schema. If someone sends a request with invalid data, they get a helpful error message without you writing any validation code.

The `@app.on_event("startup")` decorator tells FastAPI to run this function when the server starts. This is where we load our model. We do it here instead of at import time because loading a model can be slow and might fail. If it fails at startup, we know immediately. If we tried to load it on the first request, the first user would get a slow, possibly failed response.

The `CustomerData` class defines what a valid customer record looks like. Notice the validators. They check that age is reasonable and that charges are positive. FastAPI will automatically reject any request that doesn't pass these checks.

The `/health` endpoint is crucial. This is how Kubernetes or your load balancer knows if your service is healthy. It's a simple GET request that returns "healthy" if everything is working. Always have a health endpoint.

The `/predict` endpoint is the main one. It accepts a POST request with a list of customers and returns predictions for all of them. The `response_model=PredictionResponse` tells FastAPI what the response will look like, which helps with documentation and validation.

The `/predict/single` endpoint is a convenience for when you just have one customer. It's a simpler interface for simple use cases.

Now let me show you how to run this. You'll need to install a few packages first:

```bash
pip install fastapi uvicorn
```

Uvicorn is an ASGI server that runs FastAPI applications. To start the server:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag tells it to restart when you change code, which is great for development. In production, you wouldn't use that flag.

Once it's running, you can test it. FastAPI automatically generates interactive documentation at `http://localhost:8000/docs`. This is incredibly useful. You can see all your endpoints, their expected inputs and outputs, and even test them right from the browser.

Let me show you how to call the API from Python:

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict/single",
    json={
        "customer_id": "CUST001",
        "age": 35,
        "tenure": 24,
        "monthly_charges": 65.50
    }
)
print(response.json())

# Batch prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "customers": [
            {"customer_id": "CUST001", "age": 35, "tenure": 24, "monthly_charges": 65.50},
            {"customer_id": "CUST002", "age": 42, "tenure": 6, "monthly_charges": 89.00},
            {"customer_id": "CUST003", "age": 28, "tenure": 48, "monthly_charges": 45.00}
        ]
    }
)
print(response.json())
```

Or using curl from the command line:

```bash
curl -X POST "http://localhost:8000/predict/single" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "CUST001", "age": 35, "tenure": 24, "monthly_charges": 65.50}'
```

Now, let's talk about some important considerations for production APIs.

Error handling. What we have is a good start, but in production you want more detailed error handling. Different HTTP status codes for different error types. 400 for bad input, 500 for server errors, 503 if the model isn't ready.

```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": str(type(exc).__name__)}
    )
```

Authentication. You probably don't want just anyone calling your API. FastAPI supports various authentication methods. Here's a simple API key approach:

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/predict")
async def predict(request: PredictionRequest, api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... rest of the code
```

Rate limiting. You might want to limit how many requests a client can make. This prevents abuse and helps manage costs.

Request ID tracking. For debugging, it's helpful to give each request a unique ID that appears in logs.

```python
import uuid

@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(f"Request {request_id}: {request.method} {request.url.path}")
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

Async considerations. FastAPI is asynchronous, which means it can handle many requests concurrently. But your model predictions are probably synchronous. For CPU-bound work like ML inference, you might want to run predictions in a thread pool:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.post("/predict")
async def predict(request: PredictionRequest):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, 
        predictor.predict, 
        [c.dict() for c in request.customers]
    )
    return result
```

CORS. If your API will be called from web browsers, you need to configure Cross-Origin Resource Sharing:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Alright, that's the basics of building an API for your model. The key points are: use Pydantic for input validation, always have a health endpoint, load your model at startup, and think about error handling from the beginning.

In the next lecture, we're going to containerize this API with Docker. That's when it becomes truly portable and ready for deployment anywhere.

Questions? Let's move on.

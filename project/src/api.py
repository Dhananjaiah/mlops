from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import mlflow.sklearn
import numpy as np
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ML Model API", version="1.0.0")

# Load model at startup
MODEL_URI = "models:/ChurnPredictor/Production"
model = None

@app.on_event("startup")
async def load_model():
    global model
    try:
        mlflow.set_tracking_uri("http://mlflow:5000")
        model = mlflow.sklearn.load_model(MODEL_URI)
        logger.info(f"Model loaded from {MODEL_URI}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # Don't raise - allow service to start even if model isn't available yet
        logger.warning("Service starting without model - will retry on requests")

# Request/Response models
class PredictionRequest(BaseModel):
    features: List[List[float]] = Field(..., example=[[5.1, 3.5, 1.4, 0.2]])
    
    class Config:
        schema_extra = {
            "example": {
                "features": [[5.1, 3.5, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]
            }
        }

class PredictionResponse(BaseModel):
    predictions: List[int]
    model_version: str = "1.0"

# Health endpoints
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    """Readiness check"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready", "model": MODEL_URI}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make predictions"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        X = np.array(request.features)
        predictions = model.predict(X).tolist()
        
        logger.info(f"Predicted {len(predictions)} samples")
        return PredictionResponse(predictions=predictions, model_version="1.0")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Metadata endpoint
@app.get("/model/info")
async def model_info():
    """Get model metadata"""
    return {
        "model_uri": MODEL_URI,
        "framework": "scikit-learn",
        "model_type": "RandomForestClassifier"
    }

# Lecture 7.2 – Writing a Clean Inference Function (predict())

## Human Transcript

Alright, so in the last lecture we talked about structuring your training code as a proper Python package. Now let's talk about the most important function in that entire package: the `predict()` function.

Here's the thing. Your training code might run once a week. Maybe once a day. But your inference code, your `predict()` function, that runs thousands or millions of times. Every time someone wants a prediction, that function gets called. So it needs to be rock solid.

Let me tell you about a mistake I made early in my career. I had a model that worked great in testing. Beautiful accuracy, all the metrics looked good. But when we deployed it, it crashed constantly. Why? Because my predict function assumed the input data would always be perfect. It assumed there would never be missing values. It assumed the data types would always be correct. And of course, in the real world, none of that was true.

So let me walk you through how to write a predict function that actually works in production.

First, let's look at what a bad predict function looks like:

```python
# Don't do this!
def predict(data):
    features = data[['age', 'income', 'tenure']]
    prediction = model.predict(features)
    return prediction
```

What's wrong with this? Everything. Let me count the ways.

One, it doesn't validate the input. What if `data` is None? What if it's missing columns? What if the values are wrong types?

Two, it modifies data in place. If you pass a DataFrame, pandas operations might change the original data.

Three, it doesn't handle errors. If anything goes wrong, it just crashes.

Four, it doesn't return useful information. Just a raw prediction with no context.

Now let me show you what a production-ready predict function looks like:

```python
# src/churn_model/models/predict.py
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Union
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)

class ChurnPredictor:
    """Production-ready predictor for customer churn."""
    
    def __init__(self, model_path: str):
        """Load the trained model and associated artifacts."""
        self.model_path = Path(model_path)
        self._load_model()
        
    def _load_model(self):
        """Load model and any preprocessing artifacts."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        
        artifacts = joblib.load(self.model_path)
        self.model = artifacts['model']
        self.feature_columns = artifacts['feature_columns']
        self.scaler = artifacts.get('scaler')  # Optional
        self.model_version = artifacts.get('version', 'unknown')
        
        logger.info(f"Loaded model version {self.model_version}")
    
    def _validate_input(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean input data."""
        # Make a copy to avoid modifying original
        df = data.copy()
        
        # Check for required columns
        missing_cols = set(self.feature_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for unexpected columns (warning only)
        extra_cols = set(df.columns) - set(self.feature_columns)
        if extra_cols:
            logger.warning(f"Ignoring extra columns: {extra_cols}")
        
        # Select only the features we need, in the right order
        df = df[self.feature_columns]
        
        # Check for missing values
        null_counts = df.isnull().sum()
        if null_counts.any():
            logger.warning(f"Missing values found: {null_counts[null_counts > 0].to_dict()}")
            # You might want to impute here, or raise an error
            df = self._handle_missing_values(df)
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in a production-safe way."""
        # Simple strategy: fill with median for numeric columns
        # In real life, you'd load the median values from training
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna('unknown')
        return df
    
    def _preprocess(self, df: pd.DataFrame) -> np.ndarray:
        """Apply any preprocessing steps."""
        features = df.values
        
        if self.scaler is not None:
            features = self.scaler.transform(features)
        
        return features
    
    def predict(self, data: Union[pd.DataFrame, Dict, List[Dict]]) -> Dict[str, Any]:
        """
        Make predictions on input data.
        
        Args:
            data: Input data as DataFrame, dict (single record), 
                  or list of dicts (multiple records)
        
        Returns:
            Dictionary containing predictions and metadata
        """
        try:
            # Convert input to DataFrame if needed
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                raise ValueError(f"Unsupported input type: {type(data)}")
            
            n_records = len(df)
            logger.info(f"Making predictions for {n_records} records")
            
            # Validate and preprocess
            df = self._validate_input(df)
            features = self._preprocess(df)
            
            # Make predictions
            predictions = self.model.predict(features)
            probabilities = None
            
            # Get probabilities if available
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features)[:, 1]
            
            # Build response
            response = {
                'success': True,
                'predictions': predictions.tolist(),
                'model_version': self.model_version,
                'n_records': n_records
            }
            
            if probabilities is not None:
                response['probabilities'] = probabilities.tolist()
            
            return response
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'validation_error'
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'error_type': 'prediction_error'
            }
```

Now that's a lot more code. Let me break down what's happening here and why each part matters.

First, we're using a class instead of a bare function. Why? Because loading a model is expensive. It might take seconds. We don't want to load the model every single time we make a prediction. By using a class, we load it once in `__init__` and then reuse it for all predictions.

Second, look at the `_load_model` method. Notice how we're loading not just the model, but also the feature columns and any preprocessing objects like scalers. This is crucial. Your inference code needs to know exactly what features the model expects and in what order. If you trained with columns in order A, B, C and then call predict with B, A, C, you're going to get garbage results. Maybe not errors, just wrong predictions, which is worse.

Third, the `_validate_input` method. This is your first line of defense. It checks that all required columns are present. It warns about extra columns. It handles missing values. It ensures the data is in the right format.

Fourth, we accept multiple input types. Sometimes you'll get a single dictionary from an API request. Sometimes you'll get a list of dictionaries. Sometimes you'll get a DataFrame from a batch job. The function handles all of these.

Fifth, the response is a dictionary, not just a raw prediction. It includes the prediction itself, but also the model version, the number of records processed, probabilities if available, and most importantly, a success flag and error information if something went wrong.

This last point is really important for debugging. In production, when something goes wrong, you need to know why. Was it a validation error? A model error? What was the input that caused it? Without this information, debugging is basically guessing.

Now, let me talk about some other best practices for predict functions.

Determinism. Your predict function should be deterministic. Given the same input and the same model, it should always produce the same output. This might seem obvious, but it's easy to mess up. If you're doing any random sampling in preprocessing, that's a bug.

Performance. Think about how your function will be called. If it's called for single records in real time, optimize for latency. If it's called for batches in a batch job, optimize for throughput. These are different optimizations.

Logging. Log inputs and outputs. Not necessarily every single prediction in production, that would be too much data. But at least log summaries. How many predictions per minute? What's the distribution of predictions? This helps you catch issues early.

Memory. Watch your memory usage. If someone passes a million records, don't load them all into memory at once. Process in chunks.

Let me show you how to add batch processing:

```python
def predict_batch(self, data: pd.DataFrame, batch_size: int = 1000) -> Dict[str, Any]:
    """Process large datasets in batches."""
    all_predictions = []
    all_probabilities = []
    
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i + batch_size]
        result = self.predict(batch)
        
        if not result['success']:
            return result  # Return error immediately
        
        all_predictions.extend(result['predictions'])
        if 'probabilities' in result:
            all_probabilities.extend(result['probabilities'])
    
    return {
        'success': True,
        'predictions': all_predictions,
        'probabilities': all_probabilities if all_probabilities else None,
        'model_version': self.model_version,
        'n_records': len(data)
    }
```

One more thing. Version compatibility. If you trained your model with scikit-learn 1.0 and you're trying to load it with scikit-learn 1.2, it might not work. Or worse, it might work but give slightly different results. So include the library versions in your model artifacts and check them at load time.

```python
def _check_compatibility(self, artifacts):
    """Check that model was trained with compatible library versions."""
    trained_sklearn = artifacts.get('sklearn_version')
    current_sklearn = sklearn.__version__
    
    if trained_sklearn and trained_sklearn != current_sklearn:
        logger.warning(
            f"Model trained with sklearn {trained_sklearn}, "
            f"but running with {current_sklearn}"
        )
```

Alright, that's a lot about the predict function. The key takeaway is this: your predict function is the interface between your model and the rest of the world. It needs to be robust, well-tested, and informative when things go wrong.

In the next lecture, we're going to wrap this predict function in a REST API so it can be called over the network. That's when things start to get really exciting, because suddenly your model can be used by any application, not just Python code.

Any questions? Great, see you in the next one.

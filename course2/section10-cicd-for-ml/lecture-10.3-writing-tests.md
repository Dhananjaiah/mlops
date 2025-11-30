# Lecture 10.3 – Writing Tests for ML Code (Unit, Integration, Smoke)

## Human Transcript

Let's get practical. How do you actually write tests for ML code? What do you test? How do you make tests fast enough to run in CI?

I'm going to show you three types of tests: unit tests, integration tests, and smoke tests. Each serves a different purpose.

Unit Tests. These test individual functions in isolation. They should be fast, running in milliseconds. You should have hundreds of them.

What to unit test in ML code:
- Data preprocessing functions
- Feature engineering logic
- Input validation
- Output formatting
- Utility functions

```python
# tests/unit/test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from src.preprocessing import (
    clean_missing_values,
    encode_categoricals,
    scale_features,
    validate_schema
)

class TestCleanMissingValues:
    def test_fills_numeric_with_median(self):
        df = pd.DataFrame({'a': [1.0, 2.0, np.nan, 4.0]})
        result = clean_missing_values(df)
        assert result['a'].iloc[2] == 2.0  # median of 1, 2, 4
    
    def test_fills_categorical_with_mode(self):
        df = pd.DataFrame({'b': ['x', 'x', None, 'y']})
        result = clean_missing_values(df)
        assert result['b'].iloc[2] == 'x'  # mode
    
    def test_does_not_modify_original(self):
        df = pd.DataFrame({'a': [1.0, np.nan]})
        result = clean_missing_values(df)
        assert pd.isna(df['a'].iloc[1])  # Original unchanged

class TestEncodeCategoricals:
    def test_one_hot_encoding(self):
        df = pd.DataFrame({'color': ['red', 'blue', 'red']})
        result = encode_categoricals(df, method='onehot')
        assert 'color_red' in result.columns
        assert 'color_blue' in result.columns
    
    def test_label_encoding(self):
        df = pd.DataFrame({'size': ['S', 'M', 'L', 'M']})
        result = encode_categoricals(df, method='label')
        assert result['size'].dtype == 'int64'
        assert set(result['size'].unique()) == {0, 1, 2}
    
    def test_handles_unseen_categories(self):
        df_train = pd.DataFrame({'color': ['red', 'blue']})
        encoder = fit_encoder(df_train)
        
        df_test = pd.DataFrame({'color': ['red', 'green']})  # 'green' is new
        result = transform_with_encoder(df_test, encoder)
        # Should handle gracefully, not crash

class TestValidateSchema:
    def test_passes_valid_data(self):
        df = pd.DataFrame({
            'customer_id': ['A1', 'A2'],
            'tenure': [12, 24],
            'churned': [0, 1]
        })
        assert validate_schema(df) == True
    
    def test_fails_missing_column(self):
        df = pd.DataFrame({
            'customer_id': ['A1', 'A2'],
            'tenure': [12, 24]
            # Missing 'churned'
        })
        with pytest.raises(ValueError, match="Missing column: churned"):
            validate_schema(df)
    
    def test_fails_wrong_type(self):
        df = pd.DataFrame({
            'customer_id': ['A1', 'A2'],
            'tenure': ['twelve', 'twenty-four'],  # Should be int
            'churned': [0, 1]
        })
        with pytest.raises(TypeError, match="tenure should be numeric"):
            validate_schema(df)
```

Testing model code with mocks:

```python
# tests/unit/test_predictor.py
from unittest.mock import Mock, patch
from src.predictor import ChurnPredictor

class TestChurnPredictor:
    def test_predict_returns_correct_format(self):
        # Mock the model
        mock_model = Mock()
        mock_model.predict.return_value = np.array([0, 1, 0])
        mock_model.predict_proba.return_value = np.array([
            [0.8, 0.2],
            [0.3, 0.7],
            [0.9, 0.1]
        ])
        
        predictor = ChurnPredictor.__new__(ChurnPredictor)
        predictor.model = mock_model
        predictor.feature_columns = ['a', 'b']
        predictor.scaler = None
        
        result = predictor.predict([
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 4},
            {'a': 5, 'b': 6}
        ])
        
        assert result['success'] == True
        assert len(result['predictions']) == 3
        assert len(result['probabilities']) == 3
    
    def test_handles_invalid_input(self):
        predictor = ChurnPredictor.__new__(ChurnPredictor)
        predictor.feature_columns = ['a', 'b']
        
        result = predictor.predict({'a': 1})  # Missing 'b'
        
        assert result['success'] == False
        assert 'error' in result
```

Integration Tests. These test how components work together. They're slower but catch issues that unit tests miss.

```python
# tests/integration/test_training_pipeline.py
import pytest
import pandas as pd
from src.pipeline import TrainingPipeline

@pytest.fixture
def sample_training_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'customer_id': [f'C{i}' for i in range(100)],
        'tenure': np.random.randint(1, 60, 100),
        'monthly_charges': np.random.uniform(20, 100, 100),
        'churned': np.random.choice([0, 1], 100)
    })

class TestTrainingPipeline:
    def test_end_to_end_training(self, sample_training_data, tmp_path):
        """Test full training pipeline."""
        # Save sample data
        data_path = tmp_path / "data.parquet"
        sample_training_data.to_parquet(data_path)
        
        # Run pipeline
        pipeline = TrainingPipeline()
        result = pipeline.run(
            data_path=str(data_path),
            output_path=str(tmp_path / "model")
        )
        
        # Check outputs
        assert result['success'] == True
        assert 'model_path' in result
        assert 'metrics' in result
        assert result['metrics']['accuracy'] > 0.5  # Better than random
    
    def test_pipeline_logs_to_mlflow(self, sample_training_data, tmp_path):
        """Test that pipeline correctly logs to MLflow."""
        import mlflow
        
        with mlflow.start_run():
            pipeline = TrainingPipeline()
            pipeline.run(str(tmp_path / "data.parquet"))
            
            run = mlflow.active_run()
            assert run.data.metrics.get('accuracy') is not None
            assert run.data.params.get('model_type') is not None

@pytest.mark.slow
class TestModelInference:
    def test_model_can_load_and_predict(self, trained_model_path):
        """Test that saved model loads and makes predictions."""
        predictor = ChurnPredictor(trained_model_path)
        
        test_input = {
            'tenure': 12,
            'monthly_charges': 50.0
        }
        
        result = predictor.predict(test_input)
        
        assert result['success'] == True
        assert result['predictions'][0] in [0, 1]
```

Smoke Tests. Quick sanity checks that things are working. Run these in production deployments.

```python
# tests/smoke/test_api.py
import requests

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """API should return healthy status."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_prediction_endpoint_accepts_valid_input():
    """API should accept valid prediction request."""
    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "customers": [{
                "customer_id": "TEST001",
                "tenure": 12,
                "monthly_charges": 50.0
            }]
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_prediction_endpoint_rejects_invalid_input():
    """API should reject invalid input gracefully."""
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"customers": [{"invalid": "data"}]}
    )
    assert response.status_code in [400, 422]

def test_api_response_time():
    """API should respond within acceptable time."""
    import time
    
    start = time.time()
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"customers": [{"customer_id": "T", "tenure": 12, "monthly_charges": 50.0}]}
    )
    elapsed = time.time() - start
    
    assert elapsed < 1.0  # Should respond within 1 second
```

Model-specific tests:

```python
# tests/model/test_model_quality.py
import pytest
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score

class TestModelQuality:
    @pytest.fixture
    def model_and_data(self):
        model = joblib.load("models/latest/model.joblib")
        test_data = joblib.load("data/test/test_data.joblib")
        return model, test_data
    
    def test_accuracy_above_threshold(self, model_and_data):
        model, data = model_and_data
        predictions = model.predict(data['X'])
        accuracy = accuracy_score(data['y'], predictions)
        assert accuracy >= 0.75, f"Accuracy {accuracy} below threshold"
    
    def test_no_extreme_predictions(self, model_and_data):
        """Model should not predict all same class."""
        model, data = model_and_data
        predictions = model.predict(data['X'])
        unique_preds = np.unique(predictions)
        assert len(unique_preds) > 1, "Model predicts single class"
    
    def test_predictions_are_calibrated(self, model_and_data):
        """Probabilities should roughly match observed frequencies."""
        model, data = model_and_data
        proba = model.predict_proba(data['X'])[:, 1]
        
        # Bin predictions and check calibration
        bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        for i in range(len(bins)-1):
            mask = (proba >= bins[i]) & (proba < bins[i+1])
            if mask.sum() > 10:  # Enough samples
                bin_proba = proba[mask].mean()
                actual_rate = data['y'][mask].mean()
                assert abs(bin_proba - actual_rate) < 0.2
```

Organizing tests in CI:

```yaml
# .github/workflows/test.yml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/unit -v --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/integration -v

  slow-model-tests:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # Only on main
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/model -v --slow
```

Key takeaways:
- Unit tests: fast, isolated, many of them
- Integration tests: slower, test components together
- Smoke tests: quick sanity checks for deployments
- Mark slow tests and run them selectively

In the next lecture, we'll look at building and pushing Docker images in CI.

Any questions?

# Lecture 7.6 – Local Testing of the Model API (curl, Postman, simple UI)

## Human Transcript

Alright, so we've built our API and we've containerized it. Now before we push this anywhere, we need to test it. And I mean really test it. Not just "it doesn't crash" but actually verify it does what we expect.

Let me show you how to test your model API thoroughly using different tools.

First, let's start our service locally:

```bash
# If using Docker
docker run -d -p 8000:8000 --name churn-api churn-model:v1

# Or if running directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Now let's test with curl. Curl is a command-line tool that comes with most operating systems. It's simple and scriptable.

Test the health endpoint first:

```bash
curl http://localhost:8000/health
```

You should see something like:
```json
{"status": "healthy", "model_loaded": true}
```

If you see this, great. The service is up and the model is loaded. If not, check the logs:

```bash
docker logs churn-api
```

Now let's test a single prediction:

```bash
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "age": 35,
    "tenure": 24,
    "monthly_charges": 65.50
  }'
```

The response should look like:
```json
{
  "customer_id": "TEST001",
  "churn_prediction": 0,
  "churn_probability": 0.23
}
```

Test batch predictions:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [
      {"customer_id": "TEST001", "age": 35, "tenure": 24, "monthly_charges": 65.50},
      {"customer_id": "TEST002", "age": 22, "tenure": 3, "monthly_charges": 95.00},
      {"customer_id": "TEST003", "age": 55, "tenure": 60, "monthly_charges": 45.00}
    ]
  }'
```

Now let's test error cases. This is important. Your API should handle bad input gracefully.

Test missing required field:

```bash
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "age": 35
  }'
```

You should get a 422 Validation Error with a message about missing fields.

Test invalid data types:

```bash
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "age": "not a number",
    "tenure": 24,
    "monthly_charges": 65.50
  }'
```

Again, should be a 422 error.

Test out-of-range values:

```bash
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "age": -5,
    "tenure": 24,
    "monthly_charges": 65.50
  }'
```

If you added validators for age, this should fail too.

Now let me show you Postman. Postman is a GUI tool for testing APIs. It's much easier to use than curl for complex requests.

Download Postman from their website and install it. Then:

1. Create a new request
2. Set the method to POST
3. Enter the URL: `http://localhost:8000/predict/single`
4. Go to the Headers tab and add: `Content-Type: application/json`
5. Go to the Body tab, select "raw" and "JSON"
6. Paste your JSON body
7. Click Send

Postman shows you the response nicely formatted. You can also:
- Save requests in collections for later
- Create test scripts that run automatically
- Set up environment variables for different environments
- Generate code snippets in various languages

Here's a Postman test script example:

```javascript
// Add this in the "Tests" tab
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has predictions", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('predictions');
});

pm.test("Response time is under 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

Now let's talk about FastAPI's built-in documentation. Navigate to `http://localhost:8000/docs` in your browser. This is the Swagger UI that FastAPI generates automatically.

You can:
- See all your endpoints
- See request and response schemas
- Try out requests directly in the browser
- See example values

There's also `http://localhost:8000/redoc` which shows the same information in a different format.

Now let me show you a simple Python test script you can run:

```python
# test_api.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] == True
    print("✓ Health check passed")

def test_single_prediction():
    payload = {
        "customer_id": "TEST001",
        "age": 35,
        "tenure": 24,
        "monthly_charges": 65.50
    }
    response = requests.post(f"{BASE_URL}/predict/single", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_prediction" in data
    assert data["churn_prediction"] in [0, 1]
    print("✓ Single prediction passed")

def test_batch_prediction():
    payload = {
        "customers": [
            {"customer_id": "TEST001", "age": 35, "tenure": 24, "monthly_charges": 65.50},
            {"customer_id": "TEST002", "age": 22, "tenure": 3, "monthly_charges": 95.00},
        ]
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["predictions"]) == 2
    print("✓ Batch prediction passed")

def test_validation_error():
    payload = {
        "customer_id": "TEST001",
        "age": -5,  # Invalid
        "tenure": 24,
        "monthly_charges": 65.50
    }
    response = requests.post(f"{BASE_URL}/predict/single", json=payload)
    assert response.status_code == 422
    print("✓ Validation error handled correctly")

def test_latency():
    payload = {
        "customer_id": "TEST001",
        "age": 35,
        "tenure": 24,
        "monthly_charges": 65.50
    }
    
    times = []
    for _ in range(10):
        start = time.time()
        response = requests.post(f"{BASE_URL}/predict/single", json=payload)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    p99_time = sorted(times)[8]  # 90th percentile with 10 samples
    
    print(f"✓ Latency test: avg={avg_time*1000:.2f}ms, p90={p99_time*1000:.2f}ms")
    assert avg_time < 0.5, "Average latency too high"

if __name__ == "__main__":
    test_health()
    test_single_prediction()
    test_batch_prediction()
    test_validation_error()
    test_latency()
    print("\n🎉 All tests passed!")
```

Run it with:
```bash
python test_api.py
```

For more serious testing, you might want to use pytest:

```python
# tests/test_api_integration.py
import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def api_client():
    """Check API is running before tests."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
    except Exception as e:
        pytest.skip(f"API not available: {e}")
    yield requests.Session()

class TestHealthEndpoint:
    def test_health_returns_200(self, api_client):
        response = api_client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
    
    def test_health_shows_model_loaded(self, api_client):
        response = api_client.get(f"{BASE_URL}/health")
        data = response.json()
        assert data["model_loaded"] == True

class TestPredictionEndpoint:
    @pytest.fixture
    def valid_customer(self):
        return {
            "customer_id": "TEST001",
            "age": 35,
            "tenure": 24,
            "monthly_charges": 65.50
        }
    
    def test_single_prediction_success(self, api_client, valid_customer):
        response = api_client.post(
            f"{BASE_URL}/predict/single",
            json=valid_customer
        )
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == "TEST001"
        assert data["churn_prediction"] in [0, 1]
    
    def test_missing_field_returns_422(self, api_client):
        response = api_client.post(
            f"{BASE_URL}/predict/single",
            json={"customer_id": "TEST001"}  # Missing required fields
        )
        assert response.status_code == 422
```

Run with:
```bash
pytest tests/test_api_integration.py -v
```

Finally, let me show you how to build a simple HTML UI for testing. Create a file called `test_ui.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Churn Prediction Test UI</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        input, button { margin: 10px 0; padding: 10px; width: 100%; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        #result { padding: 20px; margin-top: 20px; background: #f8f9fa; border-radius: 5px; }
        .error { background: #f8d7da; color: #721c24; }
        .success { background: #d4edda; color: #155724; }
    </style>
</head>
<body>
    <h1>Churn Prediction Test</h1>
    
    <label>Customer ID:</label>
    <input type="text" id="customer_id" value="CUST001">
    
    <label>Age:</label>
    <input type="number" id="age" value="35">
    
    <label>Tenure (months):</label>
    <input type="number" id="tenure" value="24">
    
    <label>Monthly Charges ($):</label>
    <input type="number" id="monthly_charges" value="65.50" step="0.01">
    
    <button onclick="predict()">Predict Churn</button>
    
    <div id="result"></div>
    
    <script>
        async function predict() {
            const data = {
                customer_id: document.getElementById('customer_id').value,
                age: parseInt(document.getElementById('age').value),
                tenure: parseInt(document.getElementById('tenure').value),
                monthly_charges: parseFloat(document.getElementById('monthly_charges').value)
            };
            
            try {
                const response = await fetch('http://localhost:8000/predict/single', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('result');
                
                if (response.ok) {
                    resultDiv.className = 'success';
                    resultDiv.innerHTML = `
                        <h3>Prediction Result</h3>
                        <p><strong>Customer:</strong> ${result.customer_id}</p>
                        <p><strong>Churn Prediction:</strong> ${result.churn_prediction === 1 ? 'Will Churn' : 'Will Stay'}</p>
                        <p><strong>Probability:</strong> ${(result.churn_probability * 100).toFixed(1)}%</p>
                    `;
                } else {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = `<h3>Error</h3><p>${JSON.stringify(result.detail)}</p>`;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `<p class="error">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
```

Open this file in your browser and you can test your API with a nice UI. Note: you'll need CORS enabled in your API for this to work from a local file.

Alright, that covers local testing. The key takeaway is: test thoroughly before deploying. Test happy paths, test error cases, test edge cases, test performance. Find the bugs on your laptop, not in production.

This wraps up Section 7 on model packaging. We've gone from raw training code to a properly packaged, API-wrapped, containerized, and tested model service.

In the next section, we'll talk about versioning all of this: your data, your code, and your models. Because when something goes wrong in production, you need to know exactly what version of everything is running.

See you there!

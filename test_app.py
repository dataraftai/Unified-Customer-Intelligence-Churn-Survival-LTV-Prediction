from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_prediction_endpoint():
    sample_payload = {
        "senior_citizen": "No",
        "partner": "Yes",
        "dependents": "No",
        "tenure": 1,
        "phone_service": "Yes",
        "multiple_lines": "No",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "No",
        "streaming_movies": "No",
        "contract": "Month-to-month",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
        "monthly_charges": 70.35,
        "total_charges": 70.35
    }
    
    response = client.post("/predict", json=sample_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "churn_analysis" in data
    assert "ltv_analysis" in data
    assert "business_segment" in data
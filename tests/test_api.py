import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_data_status():
    response = client.get("/api/data-status")
    assert response.status_code == 200
    data = response.json()
    assert "project_1" in data
    assert "project_2" in data

def test_stations():
    response = client.get("/api/stations")
    assert response.status_code == 200
    assert "stations" in response.json()

def test_forecast_live_valid_predictions():
    response = client.get('/api/forecast/live?station=Delhi_Avg&hours=72')
    assert response.status_code == 200
    data = response.json()
    assert 'forecasts' in data
    assert len(data['forecasts']) == 72
    # Ensure properties exist for Recharts dataKey
    assert 'prediction' in data['forecasts'][0]
    assert type(data['forecasts'][0]['prediction']) in [float, int]

def test_forecast_explanation_endpoint():
    response = client.get('/api/forecast/explanation?station=Delhi_Avg')
    assert response.status_code == 200
    data = response.json()
    assert 'top_positive_factors' in data
    assert 'top_negative_factors' in data
    assert 'data_status' in data

import pytest
import responses
import math
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, LiveObservation, LiveWeather
from app.services.ingestion import OpenAQAdapter, OpenMeteoAdapter
from app.config.settings import settings

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def adapter():
    settings.openaq_api_key = "test-key"
    settings.openaq_base_url = "https://api.openaq.org/v3"
    a = OpenAQAdapter()
    a.target_locations = [{"id": "235", "name": "Anand Vihar"}]
    return a

def mock_v3_location(sensor_id=1, parameter="pm25", lat=28.1, lon=77.1):
    return {
        "results": [{
            "id": 235,
            "coordinates": {"latitude": lat, "longitude": lon},
            "sensors": [{"id": sensor_id, "parameter": {"name": parameter, "units": "µg/m³"}}]
        }]
    }

def mock_v3_measurement(val=45.2, dt="2026-10-01T12:00:00Z"):
    return {
        "results": [{
            "value": val,
            "period": {"datetimeTo": {"utc": dt}}
        }]
    }

@responses.activate
def test_successful_openaq_response(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(), status=200)
    
    res = adapter.ingest(db)
    assert res["success"] is True
    assert res["observations_inserted"] == 1
    
    obs = db.query(LiveObservation).first()
    assert obs.status == "OBSERVED"
    assert obs.value == 45.2

@responses.activate
def test_empty_response(adapter, db):
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json={"results": []}, status=200)
    res = adapter.ingest(db)
    assert res["observations_received"] == 0

@responses.activate
def test_malformed_json(adapter, db):
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", body="{bad_json", status=200)
    res = adapter.ingest(db)
    # The try/except in ingest catches it and continues
    assert res["observations_inserted"] == 0

@responses.activate
def test_http_401(adapter, db):
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json={}, status=401)
    res = adapter.ingest(db)
    assert res["observations_inserted"] == 0

@responses.activate
def test_http_403(adapter, db):
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json={}, status=403)
    res = adapter.ingest(db)
    assert res["observations_inserted"] == 0

@responses.activate
def test_http_429(adapter, db):
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json={}, status=429)
    res = adapter.ingest(db)
    assert res["observations_inserted"] == 0

@responses.activate
def test_http_500(adapter, db):
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json={}, status=500)
    res = adapter.ingest(db)
    assert res["observations_inserted"] == 0

@responses.activate
def test_timeout(adapter, db):
    import requests
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", body=requests.exceptions.Timeout())
    res = adapter.ingest(db)
    assert res["success"] is False

@responses.activate
def test_missing_pollutant(adapter, db):
    # Pass a parameter that is NOT in pollutant_map
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(parameter="unknown"), status=200)
    res = adapter.ingest(db)
    assert res["observations_rejected"] == 0 # It just skips
    assert res["observations_inserted"] == 0

@responses.activate
def test_missing_value(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(val=None), status=200)
    res = adapter.ingest(db)
    assert res["observations_rejected"] == 1

@responses.activate
def test_invalid_timestamp(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(dt="not-a-date"), status=200)
    res = adapter.ingest(db)
    assert res["observations_rejected"] == 1

@responses.activate
def test_nan(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(val=math.nan), status=200)
    res = adapter.ingest(db)
    assert res["observations_rejected"] == 1

@responses.activate
def test_infinity(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(val=math.inf), status=200)
    res = adapter.ingest(db)
    assert res["observations_rejected"] == 1

@responses.activate
def test_invalid_coordinates(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(lat=None, lon=None), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(), status=200)
    res = adapter.ingest(db)
    assert res["observations_rejected"] == 1

@responses.activate
def test_duplicate_measurement(adapter, db):
    responses.add(responses.GET, re.compile(r"https://api.openaq.org/v3/locations\?.*"), json={"results": [{"id": 235, "name": "Delhi Test"}]}, match_querystring=False, status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/locations/235", json=mock_v3_location(), status=200)
    responses.add(responses.GET, "https://api.openaq.org/v3/sensors/1/measurements?limit=1", json=mock_v3_measurement(), status=200)
    
    adapter.ingest(db)
    res = adapter.ingest(db)
    assert res["observations_inserted"] == 0
    assert res["duplicates_skipped"] == 1

def test_api_key_missing(db):
    settings.openaq_api_key = ""
    a = OpenAQAdapter()
    res = a.ingest(db)
    assert res["success"] is False
    assert res["error"] == "No API key configured."

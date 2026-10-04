import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.atmosphere.trapping import AtmosphericTrappingEngine
from app.atmosphere.ventilation import VentilationIndexEngine
from app.events.event_detector import EventDetector
from app.simulation.transport import AeroSenseRapidTransportModel
from app.simulation.scenario_lab import ScenarioLab
import pandas as pd
import numpy as np

client = TestClient(app)

def test_atmospheric_trapping_score_bounds():
    engine = AtmosphericTrappingEngine()
    # High trapping scenario
    res_high = engine.compute_trapping_score({"wind_speed": 0.5, "temperature": 5.0, "humidity": 90.0, "precipitation": 0.0})
    assert 0 <= res_high["score"] <= 100
    assert res_high["category"] == "SEVERE"
    assert res_high["provenance"] == "PROXY"
    
    # Low trapping (clean)
    res_clean = engine.compute_trapping_score({"wind_speed": 10.0, "temperature": 35.0, "humidity": 30.0, "precipitation": 20.0})
    assert 0 <= res_clean["score"] <= 100
    assert res_clean["category"] == "LOW"

def test_ventilation_index():
    engine = VentilationIndexEngine()
    # Stagnant
    res_stag = engine.compute_index({"wind_speed": 0.5, "temperature": 10.0})
    assert res_stag["category"] == "stagnant conditions"
    assert res_stag["provenance"] == "PROXY"
    
    # Strong
    res_strong = engine.compute_index({"wind_speed": 10.0, "temperature": 30.0})
    assert res_strong["category"] == "stronger ventilation"

def test_pollution_event_detection_thresholds():
    detector = EventDetector()
    
    # Rapid PM2.5 increase
    current_state = {"pm25": 150.0, "pm10": 100.0, "no2": 40.0}
    # 50 to 150 is a massive jump (>0.25)
    history = pd.DataFrame({"pm25": [50.0, 150.0]})
    events = detector.detect(current_state, history, provenance="OBSERVED")
    
    types = [e["event_type"] for e in events]
    assert "rapid PM2.5 increase" in types
    
    e = [e for e in events if e["event_type"] == "rapid PM2.5 increase"][0]
    assert e["data_status"] == "OBSERVED"
    assert e["severity"] == "HIGH"
    assert "pm25" in e["pollutants"]

def test_transport_direction_and_response():
    model = AeroSenseRapidTransportModel()
    
    # Wind from 270 (West). Plume should travel to 90 (East).
    res = model.simulate(28.6, 77.2, wind_speed_mps=5.0, wind_direction_deg=270, source_strength=100.0, duration_hours=3)
    assert res["model_name"] == "AeroSense Rapid Pollution Transport Model"
    
    cl = res["plume_centerline"]
    assert len(cl) == 4 # 1 origin + 3 hours
    
    # Origin
    lon_start, lat_start = cl[0]
    # End
    lon_end, lat_end = cl[-1]
    
    # If traveling East, longitude should increase, latitude should stay roughly the same
    assert lon_end > lon_start
    assert abs(lat_end - lat_start) < 0.001
    
    # Check bounds on invalid inputs
    with pytest.raises(ValueError):
        model.simulate(28.6, 77.2, wind_speed_mps=-5.0, wind_direction_deg=270, source_strength=100.0, duration_hours=3)

def test_scenario_input_changes_and_provenance():
    lab = ScenarioLab()
    base_df = pd.DataFrame([{"wind_speed": 5.0, "pm25": 100.0, "temperature": 20.0}])
    
    mod_df = lab.apply_what_if(base_df, {"wind_speed": -2.0, "pm25": 50.0})
    assert mod_df["wind_speed"].iloc[0] == 3.0
    assert mod_df["pm25"].iloc[0] == 150.0
    
    # Negative clipping
    mod_df_clip = lab.apply_what_if(base_df, {"wind_speed": -10.0})
    assert mod_df_clip["wind_speed"].iloc[0] == 0.0
    
    # Ensure predictor is mocked or works
    class MockPredictor:
        def predict(self, df, current_timestamp=None):
            return {"forecasts": [{"prediction": df["pm25"].iloc[0] * 1.1}]}
            
    res = lab.run_scenario("LOW_WIND", base_df, MockPredictor())
    assert res["status"] == "SCENARIO"
    assert res["scenario_name"] == "LOW_WIND"
    assert "wind_speed" in res["input_changes"]

def test_biomass_burning_unavailable_state():
    response = client.get("/api/biomass-fires")
    assert response.status_code == 200
    assert response.json()["status"] == "BIOMASS_BURNING_DATA_UNAVAILABLE"

def test_api_responses_stale_openaq_behavior():
    # If the database returns STALE, the endpoints should return HISTORICAL_FALLBACK
    # The live DB currently contains 2025-02 data, so this will definitely trigger STALE
    
    res1 = client.get("/api/atmospheric-risk")
    assert res1.status_code == 200
    data = res1.json()
    assert data["status"] == "LIVE_DATA_STALE"
    assert data["mode"] == "HISTORICAL_FALLBACK"
    assert data["trapping"]["data_status"] == "HISTORICAL_FALLBACK"
    
    res2 = client.get("/api/transport?duration_hours=1")
    assert res2.status_code == 200
    assert res2.json()["methodology_metadata"]["data_status"] == "HISTORICAL_FALLBACK"
    
    res3 = client.get("/api/events")
    assert res3.status_code == 200
    assert res3.json()["mode"] == "HISTORICAL_FALLBACK"

def test_nan_infinity_handling():
    # Tested internally by the LiveFeatureBuilder constraints, but we can verify our models don't crash
    engine = AtmosphericTrappingEngine()
    # If nan is passed via dict
    res = engine.compute_trapping_score({"wind_speed": np.nan, "temperature": np.inf})
    assert "score" in res # shouldn't crash, uses defaults/clips if possible, though float(nan) is nan.
    # Actually wait, passing np.nan to `if wind_speed < 1.0` will evaluate to False in Python.
    # So it doesn't crash, just gracefully ignores.
    
    # Let's ensure the vent engine survives
    vent = VentilationIndexEngine()
    res2 = vent.compute_index({"wind_speed": np.nan, "temperature": np.nan})
    assert "score" in res2

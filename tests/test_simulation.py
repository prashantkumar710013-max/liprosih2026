import pytest
import pandas as pd
import math
from app.simulation.transport import AeroSenseRapidTransportModel
from app.simulation.biomass import BiomassBurningScenario
from app.simulation.scenario_lab import ScenarioLab

def test_transport_model_basic():
    model = AeroSenseRapidTransportModel()
    res = model.simulate(
        source_lat=28.6, source_lon=77.2,
        wind_speed_mps=5.0, wind_direction_deg=270, # Wind from West, plume goes East
        source_strength=100.0, duration_hours=2
    )
    
    assert res['arrival_time_hours'] == 2
    # 5 m/s = 18 km/h. 2 hours = 36 km
    assert math.isclose(res['total_travel_distance_km'], 36.0, rel_tol=0.01)
    
    geojson = res['geojson']
    assert geojson['type'] == 'FeatureCollection'
    
    # Check the centerline
    centerline = geojson['features'][0]['geometry']['coordinates']
    assert len(centerline) == 3 # source + 2 hours
    
    # Wind from 270 (West) means plume travels East (to ~90)
    # Longitude should increase, latitude should stay roughly same
    assert centerline[2][0] > centerline[0][0] 

def test_transport_invalid_inputs():
    model = AeroSenseRapidTransportModel()
    with pytest.raises(ValueError):
        model.simulate(28.6, 77.2, -5.0, 270, 100, 2)
    with pytest.raises(ValueError):
        model.simulate(28.6, 77.2, 5.0, 270, 100, 0)

def test_biomass_scenario():
    sim = BiomassBurningScenario()
    res = sim.run_scenario("punjab", 500, 10.0, 315, 12)
    assert res["scenario_type"] == "SIMULATED BIOMASS-BURNING SCENARIO"
    assert res["source_region"] == "Punjab"
    assert "simulated_plume" in res
    
    with pytest.raises(ValueError):
        sim.run_scenario("unknown_region", 500, 10, 315, 12)

def test_scenario_lab_what_if():
    lab = ScenarioLab()
    df = pd.DataFrame({
        "wind_speed": [5.0],
        "temperature": [20.0],
        "pm25": [100.0]
    })
    
    mod = lab.apply_what_if(df, {"wind_speed": -2.0, "pm25": -150.0}) # Should clip pm25 to 0
    assert mod['wind_speed'].iloc[0] == 3.0
    assert mod['pm25'].iloc[0] == 0.0

def test_scenario_lab_predefined():
    lab = ScenarioLab()
    df = pd.DataFrame({
        "wind_speed": [5.0],
        "temperature": [20.0],
        "pm25": [100.0]
    })
    
    class MockPredictor:
        def predict(self, x, current_timestamp=None):
            return {"forecasts": [{"prediction": 110.0}]}
            
    res = lab.run_scenario("LOW_WIND", df, MockPredictor())
    assert res["scenario_name"] == "LOW_WIND"
    
    with pytest.raises(ValueError):
        lab.run_scenario("NONEXISTENT", df, MockPredictor())

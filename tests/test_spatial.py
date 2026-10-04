import pytest
from app.spatial.stations import StationMap
from app.spatial.hotspots import HotspotDetector
from app.spatial.interpolation import SpatialInterpolator

def test_station_map():
    smap = StationMap()
    coords = smap.get_station_coords("Anand_Vihar")
    assert coords["lat"] > 28.0
    
    geojson = smap.get_all_stations_geojson()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) > 2

def test_hotspot_detector():
    detector = HotspotDetector()
    data = {
        "Anand_Vihar": {"current_pm25": 300, "forecast_max_24h": 320},
        "Punjabi_Bagh": {"current_pm25": 100, "pm25_growth": 0.05}
    }
    geojson = detector.detect_hotspots(data)
    assert geojson["type"] == "FeatureCollection"
    
    # Only Anand Vihar should trigger a hotspot based on thresholds > 250
    assert len(geojson["features"]) == 1
    assert geojson["features"][0]["properties"]["station_id"] == "Anand_Vihar"
    assert geojson["features"][0]["properties"]["severity"] == "SEVERE" # forecast > 300

def test_interpolation():
    interpolator = SpatialInterpolator()
    data = [
        {"lat": 28.0, "lon": 77.0, "value": 100.0},
        {"lat": 28.1, "lon": 77.0, "value": 150.0},
        {"lat": 28.0, "lon": 77.1, "value": 200.0},
        {"lat": 28.1, "lon": 77.1, "value": 250.0}
    ]
    geojson = interpolator.interpolate_field(data, resolution=5)
    assert geojson["type"] == "FeatureCollection"
    assert "ESTIMATED SPATIAL FIELD" in geojson["metadata"]["name"]
    # Points outside convex hull will be NaN, so we get < 25
    assert len(geojson["features"]) > 0

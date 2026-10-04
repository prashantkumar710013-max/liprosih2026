import pytest
import pandas as pd
import numpy as np
from app.features.temporal import TemporalFeatures
from app.features.lags import LagFeatures
from app.features.rolling import RollingFeatures
from app.features.pollution import PollutionFeatures
from app.features.weather import WeatherFeatures
from app.features.coupled import CoupledFeatures
from app.features.leakage import LeakageDetector

@pytest.fixture
def sample_data():
    dates = pd.date_range("2024-01-01", periods=10, freq="h")
    return pd.DataFrame({
        "timestamp": dates,
        "station": ["A"] * 10,
        "pm25": np.arange(10, 20, dtype=float),
        "pm10": np.arange(20, 30, dtype=float),
        "no2": np.arange(5, 15, dtype=float),
        "temperature": np.arange(15, 25, dtype=float),
        "humidity": np.arange(40, 50, dtype=float),
        "wind_speed": np.arange(1, 11, dtype=float),
        "wind_direction": np.arange(0, 100, 10, dtype=float)
    })

def test_temporal_features(sample_data):
    tf = TemporalFeatures()
    df = tf.transform(sample_data)
    assert 'hour' in df.columns
    assert 'sin_hour' in df.columns
    assert 'is_weekend' in df.columns

def test_lag_features(sample_data):
    lf = LagFeatures(target_cols=['pm25'], lags=[1, 2])
    df = lf.transform(sample_data)
    assert 'pm25_lag1' in df.columns
    assert pd.isna(df['pm25_lag1'].iloc[0])
    assert df['pm25_lag1'].iloc[1] == 10.0

def test_rolling_features(sample_data):
    rf = RollingFeatures(target_cols=['pm25'], windows=[3])
    df = rf.transform(sample_data)
    assert 'pm25_3h_mean' in df.columns
    # First valid rolling mean of size 3 for shifted(1) data should be at index 3
    assert pd.isna(df['pm25_3h_mean'].iloc[2])
    assert not pd.isna(df['pm25_3h_mean'].iloc[3])
    # Values at index 0, 1, 2 are 10, 11, 12
    # Shifted values for index 3 are those three values. Mean = 11.
    assert df['pm25_3h_mean'].iloc[3] == 11.0

def test_pollution_features(sample_data):
    pf = PollutionFeatures()
    df = pf.transform(sample_data)
    assert 'pm25_growth_rate' in df.columns
    assert 'pm25_pm10_ratio' in df.columns
    # PM25 growth at index 1: (11 - 10)/10 = 0.1
    assert abs(df['pm25_growth_rate'].iloc[1] - 0.1) < 1e-4

def test_weather_features(sample_data):
    wf = WeatherFeatures()
    df = wf.transform(sample_data)
    assert 'dew_point_approx' in df.columns
    assert 'wind_u' in df.columns

def test_coupled_features(sample_data):
    cf = CoupledFeatures()
    df = cf.transform(sample_data)
    assert 'wind_stagnation_index' in df.columns
    assert 'ventilation_proxy' in df.columns
    
def test_leakage_detector(sample_data):
    # Create an artificial leak
    sample_data['pm25_leak'] = sample_data['pm25']
    ld = LeakageDetector(target_cols=['pm25'])
    report = ld.check(sample_data)
    assert report['target_leakage_detected'] is True
    assert "pm25_leak is identical to pm25" in report['suspicious_features']

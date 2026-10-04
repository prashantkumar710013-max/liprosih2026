import pytest
import pandas as pd
from app.data.loaders import DataLoader
from app.data.normalizer import DataNormalizer
from app.data.validator import DataValidator
import os

def test_loader_missing_file():
    loader = DataLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_dataset("nonexistent.csv")

def test_normalizer():
    normalizer = DataNormalizer()
    df = pd.DataFrame({"PM2.5 (ug/m3)": [10, 20], "Temp": [25, 30], "WD": ["N", "S"]})
    norm_df = normalizer.normalize(df)
    assert "pm25" in norm_df.columns
    assert "temperature" in norm_df.columns
    assert "wind_direction" in norm_df.columns
    assert norm_df["pm25"].iloc[0] == 10

def test_validator():
    validator = DataValidator()
    df = pd.DataFrame({
        "timestamp": pd.date_range(start="2024-01-01", periods=3, freq="h"),
        "pm25": [10, -5, 2000],
        "temperature": [25, 30, 60]
    })
    
    report = validator.validate(df)
    assert report["missing_timestamps"] == 0
    assert report["negative_values"].get("pm25") == 1
    assert report["extreme_values"].get("pm25") == 2
    assert report["extreme_values"].get("temperature") == 1

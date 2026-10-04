import pytest
import pandas as pd
from app.events.event_detector import EventDetector

def test_rapid_increase():
    detector = EventDetector()
    current = {
        "pm25": 150
    }
    history = pd.DataFrame({"pm25": [50.0, 150.0]}) # growth = 2.0 (200% > 0.25)
    events = detector.detect(current, history=history)
    assert len(events) == 1
    assert events[0]['event_type'] == "rapid PM2.5 increase"

def test_multi_pollutant():
    detector = EventDetector()
    current = {
        "pm25": 110,
        "pm10": 160,
        "no2": 60
    }
    events = detector.detect(current)
    assert len(events) == 1
    assert events[0]['event_type'] == "multi-pollutant increase"

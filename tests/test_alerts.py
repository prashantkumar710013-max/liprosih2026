import pytest
from app.alerts.alert_engine import AlertEngine

def test_alerts():
    engine = AlertEngine()
    forecast = [
        {"horizon": 1, "prediction": 100},
        {"horizon": 2, "prediction": 160}, # Breaches 150 (Unhealthy)
        {"horizon": 3, "prediction": 260}, # Breaches 250 (Very Unhealthy)
        {"horizon": 4, "prediction": 270},
        {"horizon": 5, "prediction": 280},
        {"horizon": 6, "prediction": 290},
        {"horizon": 7, "prediction": 290},
        {"horizon": 8, "prediction": 290},
        {"horizon": 9, "prediction": 290},
        {"horizon": 10, "prediction": 290},
        {"horizon": 11, "prediction": 290},
        {"horizon": 12, "prediction": 290},
        {"horizon": 13, "prediction": 290},
        {"horizon": 14, "prediction": 290}, # 12 hours >= 250
    ]
    alerts = engine.generate_alerts(forecast)
    assert len(alerts) == 3
    # One for 150 breach, one for 250 breach, one for prolonged
    types = [a['alert_type'] for a in alerts]
    assert "PROLONGED_SEVERE_POLLUTION" in types
    
    breach_messages = [a['message'] for a in alerts if a['alert_type'] == 'THRESHOLD_BREACH_WARNING']
    assert len(breach_messages) == 2
    assert "exceed 150" in breach_messages[0]
    assert "exceed 250" in breach_messages[1]

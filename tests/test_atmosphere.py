import pytest
from app.atmosphere.trapping import AtmosphericTrappingEngine
from app.atmosphere.inversion import InversionProxy
from app.atmosphere.accumulation import PollutionAccumulationEngine

def test_trapping_score():
    engine = AtmosphericTrappingEngine()
    current_weather = {
        "wind_speed": 0.5, # +40
        "temperature": 8.0, # +30
        "humidity": 85.0, # +20
        "precipitation": 0.0 # 0
    }
    # Total score should be 90
    res = engine.compute_trapping_score(current_weather)
    assert res['score'] == 90.0
    assert res['category'] == "SEVERE"

def test_inversion_proxy():
    proxy = InversionProxy()
    # High chance inversion: night time, big temp drop, low wind, cold
    cw = {"temperature": 10.0, "wind_speed": 0.5, "hour": 2}
    pw = {"max_temperature_12h": 25.0} # Drop of 15
    res = proxy.compute_inversion_proxy(cw, pw)
    assert res['inversion_trapping_proxy']['score'] == 100.0 # 50 (drop) + 40 (wind) + 10 (cold)
    assert res['inversion_trapping_proxy']['category'] == "HIGH LIKELIHOOD"

def test_accumulation():
    acc = PollutionAccumulationEngine()
    res = acc.compute_accumulation(pm25_current=200, pm25_past_24h_mean=100, pm25_growth_rate=0.3, wind_stagnation=0.9)
    # persistence = 200/101 ~ 1.98 -> +30
    # growth = 0.3 -> +30
    # stagnation = 0.9 -> +40
    # total = 100
    assert res['accumulation_score'] == 100.0

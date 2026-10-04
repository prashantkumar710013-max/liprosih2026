from typing import Dict, Any

class VentilationIndexEngine:
    """
    Creates a normalized indicator representing relative atmospheric dispersion conditions.
    """
    def compute_index(self, current_weather: Dict[str, float]) -> Dict[str, Any]:
        wind_speed = current_weather.get('wind_speed', 5.0)
        temp = current_weather.get('temperature', 25.0)
        
        # A simple proxy for ventilation: Wind Speed * (Temperature factor)
        # Higher wind speed = more ventilation.
        # Higher temperature = deeper boundary layer (proxy).
        # We normalize to 0-100, where 100 is excellent ventilation.
        
        temp_factor = max(1.0, temp / 10.0)
        raw_vent = wind_speed * temp_factor * 10
        
        vent_index = min(100.0, max(0.0, raw_vent))
        
        if vent_index < 30:
            category = "stagnant conditions"
        elif vent_index < 60:
            category = "moderate ventilation"
        else:
            category = "stronger ventilation"
            
        return {
            "indicator": "VENTILATION_DISPERSION_INDEX",
            "score": round(vent_index, 1),
            "category": category,
            "provenance": "PROXY",
            "methodology": "Wind-speed and temperature driven relative dispersion estimate",
            "drivers": {
                "wind_speed": wind_speed,
                "temperature": temp
            }
        }

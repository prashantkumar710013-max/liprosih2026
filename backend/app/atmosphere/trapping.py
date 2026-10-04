from typing import Dict, Any
import numpy as np

class AtmosphericTrappingEngine:
    """
    Computes an ATMOSPHERIC_TRAPPING_SCORE (0-100).
    A high trapping score indicates that pollutants are likely to remain stagnant.
    Since actual PBL height is unavailable, this relies strictly on a PBL / VENTILATION PROXY.
    """
    
    @staticmethod
    def categorize_score(score: float) -> str:
        if score < 30:
            return "LOW"
        elif score < 60:
            return "MODERATE"
        elif score < 80:
            return "HIGH"
        else:
            return "SEVERE"

    def compute_trapping_score(self, current_weather: Dict[str, float]) -> Dict[str, Any]:
        """
        Uses available:
        - wind_speed
        - temperature
        - humidity
        - precipitation
        """
        score = 0.0
        
        wind_speed = current_weather.get('wind_speed', 5.0)
        temp = current_weather.get('temperature', 25.0)
        humidity = current_weather.get('humidity', 50.0)
        precip = current_weather.get('precipitation', 0.0)
        
        # 1. Wind (Max 40 points) - Stagnant air drives trapping
        if wind_speed < 1.0:
            score += 40
        elif wind_speed < 3.0:
            score += 25
        elif wind_speed < 6.0:
            score += 10
            
        # 2. Temperature (Max 30 points) - Cold air traps pollution via inversion proxy
        if temp < 10.0:
            score += 30
        elif temp < 15.0:
            score += 20
        elif temp < 20.0:
            score += 10
            
        # 3. Humidity (Max 20 points) - High humidity creates smog
        if humidity > 80.0:
            score += 20
        elif humidity > 60.0:
            score += 10
            
        # 4. Precipitation (Max -30 points) - Rain cleans the air (Scavenging)
        if precip > 5.0:
            score -= 30
        elif precip > 1.0:
            score -= 15
            
        final_score = float(np.clip(score, 0, 100))
        category = self.categorize_score(final_score)
        
        return {
            "indicator": "ATMOSPHERIC_TRAPPING_SCORE",
            "score": round(final_score, 1),
            "category": category,
            "provenance": "PROXY",
            "methodology": "Derived via PBL / VENTILATION PROXY using surface meteorology",
            "drivers": {
                "wind_speed": wind_speed,
                "temperature": temp,
                "humidity": humidity,
                "precipitation": precip
            }
        }

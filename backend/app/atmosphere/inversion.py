from typing import Dict, Any

class InversionProxy:
    """
    Since direct inversion detection requires vertical atmospheric profiles which are
    not available in standard surface datasets, this engine provides a mathematically
    derived proxy to estimate the likelihood of thermal inversion phenomena.
    """
    
    def compute_inversion_proxy(self, current_weather: Dict[str, float], past_weather: Dict[str, float]) -> Dict[str, Any]:
        """
        Uses temperature gradients (current vs past) and wind speed to estimate inversion.
        A strong nighttime cooling (past 12h max temp vs current night temp) with low wind
        highly correlates with surface inversions in winter.
        """
        current_temp = current_weather.get('temperature', 20.0)
        past_max_temp = past_weather.get('max_temperature_12h', 25.0)
        wind_speed = current_weather.get('wind_speed', 5.0)
        hour = current_weather.get('hour', 12)
        
        # Temp drop
        temp_drop = past_max_temp - current_temp
        
        score = 0.0
        drivers = []
        
        # 1. Night/Early Morning Cooling Effect
        if (hour >= 20 or hour <= 8):
            if temp_drop > 10.0:
                score += 50
                drivers.append("Severe diurnal temperature drop")
            elif temp_drop > 5.0:
                score += 25
                drivers.append("Moderate diurnal cooling")
                
        # 2. Wind Stagnation (Inversions require calm winds)
        if wind_speed < 1.0:
            score += 40
            drivers.append("Extreme wind stagnation")
        elif wind_speed < 2.5:
            score += 20
            drivers.append("Low wind speeds")
            
        # 3. Absolute Cold
        if current_temp < 12.0:
            score += 10
            drivers.append("Cold surface temperature")
            
        score = min(score, 100.0)
        
        if score > 75:
            category = "HIGH LIKELIHOOD"
            confidence = "MODERATE" # Proxy limit
        elif score > 40:
            category = "POSSIBLE"
            confidence = "LOW"
        else:
            category = "UNLIKELY"
            confidence = "MODERATE"
            
        if len(drivers) == 0:
            drivers.append("No significant inversion conditions detected")
            
        return {
            "inversion_trapping_proxy": {
                "score": score,
                "category": category,
                "confidence": confidence,
                "drivers": drivers
            }
        }

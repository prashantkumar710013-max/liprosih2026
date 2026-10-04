from typing import Dict, Any
import numpy as np

class PollutionAccumulationEngine:
    """
    Computes an accumulation_score estimating how quickly pollution is building up
    based on PM2.5 persistence, growth rate, wind stagnation, and weather.
    """
    
    def compute_accumulation(self, pm25_current: float, pm25_past_24h_mean: float, 
                             pm25_growth_rate: float, wind_stagnation: float) -> Dict[str, Any]:
        """
        - pm25_persistence: current / past 24h mean
        - pm25_growth_rate: current vs previous hour
        - wind_stagnation: typically 1 / (wind_speed + 0.1)
        """
        score = 0.0
        
        # 1. Persistence
        persistence = pm25_current / (pm25_past_24h_mean + 1.0)
        if persistence > 1.5:
            score += 30
        elif persistence > 1.2:
            score += 15
            
        # 2. Growth Rate (immediate accumulation)
        if pm25_growth_rate > 0.2: # 20% jump
            score += 30
        elif pm25_growth_rate > 0.05:
            score += 15
            
        # 3. Wind Stagnation (environmental enabler)
        if wind_stagnation > 0.8: # wind < ~1.1
            score += 40
        elif wind_stagnation > 0.3: # wind < ~3.2
            score += 20
            
        final_score = float(np.clip(score, 0, 100))
        
        return {
            "accumulation_score": round(final_score, 1),
            "metrics_used": {
                "persistence": round(persistence, 2),
                "growth_rate": round(pm25_growth_rate, 2),
                "stagnation": round(wind_stagnation, 2)
            }
        }

import pandas as pd
from typing import Dict, Any, List

class EventDetector:
    """
    Detects critical atmospheric and pollution events.
    Enforces strict provenance mapping and specific schema requirements.
    """
    
    def detect(self, current_state: Dict[str, Any], history: pd.DataFrame = None, provenance: str = "OBSERVED") -> List[Dict[str, Any]]:
        events = []
        
        timestamp = current_state.get("timestamp", "UNKNOWN")
        pm25 = current_state.get('pm25', 0.0)
        pm10 = current_state.get('pm10', 0.0)
        no2 = current_state.get('no2', 0.0)
        trapping = current_state.get('trapping_score', 0.0)
        precip = current_state.get('precipitation', 0.0)
        
        pm25_growth = 0.0
        if history is not None and not history.empty and 'pm25' in history.columns and len(history) > 1:
            recent_pm25 = history['pm25'].iloc[-1]
            prev_pm25 = history['pm25'].iloc[-2]
            if prev_pm25 > 0:
                pm25_growth = (recent_pm25 - prev_pm25) / prev_pm25
                
        # 1. Rapid PM2.5 Increase
        if pm25_growth > 0.25 and pm25 > 100:
            events.append({
                "event_type": "rapid PM2.5 increase",
                "start_time": timestamp,
                "end_time": "ONGOING",
                "severity": "HIGH",
                "pollutants": ["pm25"],
                "supporting_features": {"pm25_growth": round(pm25_growth, 2), "pm25": pm25},
                "data_status": provenance,
                "confidence": "HIGH"
            })
            
        # 2. Sustained PM2.5 Elevation
        if history is not None and not history.empty and 'pm25' in history.columns:
            recent_24 = history.tail(24)
            if len(recent_24) == 24 and (recent_24['pm25'] > 150).all():
                events.append({
                    "event_type": "sustained PM2.5 elevation",
                    "start_time": str(recent_24.iloc[0]['timestamp']) if 'timestamp' in recent_24.columns else timestamp,
                    "end_time": "ONGOING",
                    "severity": "SEVERE",
                    "pollutants": ["pm25"],
                    "supporting_features": {"24h_min_pm25": float(recent_24['pm25'].min())},
                    "data_status": provenance,
                    "confidence": "HIGH"
                })
                
        # 3. Multi-pollutant Increase
        if pm25 > 100 and pm10 > 150 and no2 > 50:
            events.append({
                "event_type": "multi-pollutant increase",
                "start_time": timestamp,
                "end_time": "ONGOING",
                "severity": "SEVERE",
                "pollutants": ["pm25", "pm10", "no2"],
                "supporting_features": {"pm25": pm25, "pm10": pm10, "no2": no2},
                "data_status": provenance,
                "confidence": "HIGH"
            })
            
        # 4. Stagnation-associated buildup
        if pm25 > 150 and trapping > 75:
            events.append({
                "event_type": "stagnation-associated buildup",
                "start_time": timestamp,
                "end_time": "ONGOING",
                "severity": "HIGH",
                "pollutants": ["pm25"],
                "supporting_features": {"trapping_score": trapping, "pm25": pm25},
                "data_status": "DERIVED" if provenance == "OBSERVED" else provenance,
                "confidence": "MODERATE"
            })
            
        # 5. Rainfall-associated reduction
        if precip > 2.0 and pm25_growth < -0.1:
            events.append({
                "event_type": "rainfall-associated reduction",
                "start_time": timestamp,
                "end_time": "ONGOING",
                "severity": "LOW",
                "pollutants": ["pm25"],
                "supporting_features": {"precipitation": precip, "pm25_growth": round(pm25_growth, 2)},
                "data_status": provenance,
                "confidence": "HIGH"
            })
            
        return events

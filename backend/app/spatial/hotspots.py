from typing import Dict, Any, List
from .stations import StationMap

class HotspotDetector:
    """
    Detects spatial hotspots across the station network based on observed and forecasted data.
    """
    
    def __init__(self):
        self.station_map = StationMap()
        
    def detect_hotspots(self, station_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        station_data format: 
        {
            "Anand_Vihar": {"current_pm25": 280, "forecast_max_24h": 320, "pm25_growth": 0.15},
            ...
        }
        """
        features = []
        
        for sid, data in station_data.items():
            coords = self.station_map.get_station_coords(sid)
            reasons = []
            severity = "NONE"
            
            # Persistent high pollution
            if data.get("current_pm25", 0) > 250:
                reasons.append("Current PM2.5 > 250")
                severity = "HIGH"
                
            # Rapid deterioration
            if data.get("pm25_growth", 0) > 0.2:
                reasons.append("Rapid deterioration (>20% growth)")
                severity = "HIGH" if severity == "NONE" else "SEVERE"
                
            # Forecast high-risk
            if data.get("forecast_max_24h", 0) > 300:
                reasons.append("Forecast indicates PM2.5 > 300 in next 24h")
                severity = "SEVERE"
                
            if len(reasons) > 0:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [coords["lon"], coords["lat"]]
                    },
                    "properties": {
                        "station_id": sid,
                        "severity": severity,
                        "hotspot_reasons": reasons
                    }
                })
                
        return {
            "type": "FeatureCollection",
            "features": features
        }

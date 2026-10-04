from typing import Dict, Any, List

class StationMap:
    """
    Manages spatial coordinates for Delhi-NCR stations.
    """
    
    # Reliable Delhi DPCC/CPCB station coordinates
    STATIONS = {
        "Anand_Vihar": {"lat": 28.6476, "lon": 77.3158, "name": "Anand Vihar"},
        "Punjabi_Bagh": {"lat": 28.6740, "lon": 77.1310, "name": "Punjabi Bagh"},
        "RK_Puram": {"lat": 28.5632, "lon": 77.1869, "name": "RK Puram"},
        "ITO": {"lat": 28.6286, "lon": 77.2411, "name": "ITO"},
        "Delhi_Avg": {"lat": 28.6139, "lon": 77.2090, "name": "Delhi City Average"}
    }
    
    def get_station_coords(self, station_id: str) -> Dict[str, float]:
        return self.STATIONS.get(station_id, self.STATIONS["Delhi_Avg"])
        
    def get_all_stations_geojson(self) -> Dict[str, Any]:
        features = []
        for sid, data in self.STATIONS.items():
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [data["lon"], data["lat"]]
                },
                "properties": {
                    "station_id": sid,
                    "station_name": data["name"]
                }
            })
            
        return {
            "type": "FeatureCollection",
            "features": features
        }

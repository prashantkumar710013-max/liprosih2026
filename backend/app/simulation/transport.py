import math
from typing import Dict, Any, List

class LiproRapidTransportModel:
    """
    Lipro Rapid Pollution Transport Model.
    A lightweight advection/dispersion approximation. NOT WRF-Chem.
    """
    
    def __init__(self):
        # Rough approximations for regional transport
        self.KM_PER_LAT = 111.0
        # Dispersion factor (tan of half-angle of the plume spread)
        self.DISPERSION_FACTOR = 0.15 

    def _get_km_per_lon(self, lat: float) -> float:
        return 111.0 * math.cos(math.radians(lat))

    def simulate(self, source_lat: float, source_lon: float, 
                 wind_speed_mps: float, wind_direction_deg: float, 
                 source_strength: float, duration_hours: int) -> Dict[str, Any]:
        """
        wind_direction_deg: Meteorological wind direction (where wind blows FROM).
        """
        # Validate inputs
        if wind_speed_mps < 0:
            raise ValueError("Wind speed cannot be negative")
        if duration_hours <= 0:
            raise ValueError("Duration must be positive")
            
        # The plume travels in the OPPOSITE direction of the wind source
        travel_dir = (wind_direction_deg + 180.0) % 360.0
        travel_dir_rad = math.radians(travel_dir)
        
        # Speed in km/h
        speed_kmh = wind_speed_mps * 3.6
        
        centerline = []
        features = []
        
        current_lat = source_lat
        current_lon = source_lon
        
        # Add source point
        centerline.append([source_lon, source_lat])
        
        total_distance = 0.0
        
        for h in range(1, duration_hours + 1):
            distance_step = speed_kmh # km traveled in 1 hour
            total_distance += distance_step
            
            # Offsets in km
            dy_km = distance_step * math.cos(travel_dir_rad)
            dx_km = distance_step * math.sin(travel_dir_rad)
            
            # New lat/lon
            new_lat = current_lat + (dy_km / self.KM_PER_LAT)
            km_per_lon = self._get_km_per_lon(new_lat)
            new_lon = current_lon + (dx_km / km_per_lon)
            
            current_lat = new_lat
            current_lon = new_lon
            
            centerline.append([current_lon, current_lat])
            
            # Width and impact
            plume_width_km = total_distance * self.DISPERSION_FACTOR * 2
            
            # Simple Gaussian-like decay: impact decays with distance and lateral spread
            # Prevent div by zero
            relative_impact = source_strength / (1.0 + total_distance * 0.05)
            
            # Create a GeoJSON polygon representing the plume segment (simplified as a circle/buffer for visualization)
            # In a real front-end, a buffer around the LineString is better. Here we return properties.
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [current_lon, current_lat]
                },
                "properties": {
                    "hour": h,
                    "distance_km": round(total_distance, 2),
                    "plume_width_km": round(plume_width_km, 2),
                    "relative_impact": round(relative_impact, 2)
                }
            })
            
        geojson = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": centerline
                },
                "properties": {
                    "description": "Plume Centerline",
                    "travel_distance_km": round(total_distance, 2),
                    "arrival_time_hours": duration_hours
                }
            }] + features
        }
            
        return {
            "model_name": "Lipro Rapid Pollution Transport Model",
            "plume_centerline": centerline,
            "total_travel_distance_km": round(total_distance, 2),
            "arrival_time_hours": duration_hours,
            "geojson": geojson
        }

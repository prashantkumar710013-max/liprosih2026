import numpy as np
from scipy.interpolate import griddata
from typing import Dict, Any, List

class SpatialInterpolator:
    """
    Interpolates point observations into an ESTIMATED SPATIAL FIELD.
    """
    
    def interpolate_field(self, station_data: List[Dict[str, float]], resolution: int = 50) -> Dict[str, Any]:
        """
        station_data: list of dicts with 'lat', 'lon', 'value'
        resolution: grid size (N x N)
        Returns a GeoJSON polygon/grid structure.
        """
        if len(station_data) < 3:
            raise ValueError("Need at least 3 stations for valid 2D interpolation.")
            
        points = np.array([[d['lon'], d['lat']] for d in station_data])
        values = np.array([d['value'] for d in station_data])
        
        min_lon, max_lon = points[:, 0].min() - 0.05, points[:, 0].max() + 0.05
        min_lat, max_lat = points[:, 1].min() - 0.05, points[:, 1].max() + 0.05
        
        grid_lon, grid_lat = np.mgrid[min_lon:max_lon:complex(0, resolution), 
                                      min_lat:max_lat:complex(0, resolution)]
                                      
        # Linear interpolation
        grid_z = griddata(points, values, (grid_lon, grid_lat), method='linear')
        
        # We can return this as a set of center points for rendering heatmaps
        # In production we'd generate contour polygons, but a point grid is sufficient here.
        features = []
        for i in range(resolution):
            for j in range(resolution):
                val = grid_z[i, j]
                if not np.isnan(val):
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(grid_lon[i, j]), float(grid_lat[i, j])]
                        },
                        "properties": {
                            "estimated_value": round(float(val), 1)
                        }
                    })
                    
        return {
            "type": "FeatureCollection",
            "metadata": {
                "name": "ESTIMATED SPATIAL FIELD",
                "resolution": "Interpolated Grid (Not true 400m resolution)"
            },
            "features": features
        }

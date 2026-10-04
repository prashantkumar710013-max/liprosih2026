from typing import Dict, Any
from .transport import LiproRapidTransportModel

class BiomassBurningScenario:
    """
    Simulates a regional biomass-burning event (e.g. crop residue burning in Punjab/Haryana).
    This is a scenario, NOT a detected fire.
    """
    
    # Pre-defined regions mapping to roughly central lat/lon
    REGIONS = {
        "punjab": {"lat": 30.9, "lon": 75.85},
        "haryana": {"lat": 29.05, "lon": 76.08},
        "up": {"lat": 27.5, "lon": 79.0}
    }
    
    def __init__(self):
        self.transport_model = LiproRapidTransportModel()
        
    def run_scenario(self, source_region: str, emission_intensity: float, 
                     wind_speed_mps: float, wind_dir_deg: float, duration_hours: int) -> Dict[str, Any]:
                     
        if source_region.lower() not in self.REGIONS:
            raise ValueError(f"Unknown region: {source_region}")
            
        coords = self.REGIONS[source_region.lower()]
        
        # Run transport model
        result = self.transport_model.simulate(
            source_lat=coords['lat'],
            source_lon=coords['lon'],
            wind_speed_mps=wind_speed_mps,
            wind_direction_deg=wind_dir_deg,
            source_strength=emission_intensity,
            duration_hours=duration_hours
        )
        
        return {
            "scenario_type": "SIMULATED BIOMASS-BURNING SCENARIO",
            "source_region": source_region.capitalize(),
            "emission_intensity": emission_intensity,
            "simulated_plume": result['geojson'],
            "estimated_impact_at_tail": result['geojson']['features'][-1]['properties'].get('relative_impact', 0),
            "arrival_window_hours": result['arrival_time_hours']
        }

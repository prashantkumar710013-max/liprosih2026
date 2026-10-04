import pandas as pd
from typing import Dict, Any

class ScenarioLab:
    """
    Provides predefined scenarios and handles what-if modifications.
    Enforces strict provenance (SCENARIO).
    """
    
    PREDEFINED = {
        "BASELINE": {
            "changes": {},
            "assumptions": "No changes to current observed or historically fallback inputs."
        },
        "LOW_WIND": {
            "changes": {"wind_speed": -2.0},
            "assumptions": "Stagnant atmospheric conditions with a 2.0 m/s reduction in wind speed."
        },
        "HIGH_ATMOSPHERIC_TRAPPING": {
            "changes": {"wind_speed": -2.0, "temperature": -5.0, "humidity": 15.0},
            "assumptions": "Strong thermal inversion proxy: cooler surface temp, high humidity, low wind."
        },
        "REGIONAL_POLLUTION_INFLOW": {
            "changes": {"pm25": 100.0, "pm10": 150.0},
            "assumptions": "External advection event adding +100 PM2.5 and +150 PM10 to current boundary."
        },
        "RAIN_SCAVENGING": {
            "changes": {"precipitation": 10.0, "pm25": -50.0},
            "assumptions": "Wet deposition event (10mm precipitation) actively washing out PM2.5."
        },
        "BIOMASS_BURNING_SCENARIO": {
            "changes": {"pm25": 200.0, "pm10": 250.0, "co": 10.0, "no2": 30.0},
            "assumptions": "Massive regional biomass burning transport (crop residue) arriving at station."
        }
    }
    
    def apply_what_if(self, base_features: pd.DataFrame, modifications: Dict[str, float]) -> pd.DataFrame:
        df = base_features.copy()
        for col, delta in modifications.items():
            if col in df.columns:
                df[col] = df[col] + delta
                if col in ['wind_speed', 'precipitation', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3']:
                    df[col] = df[col].clip(lower=0.0)
                elif col == 'humidity':
                    df[col] = df[col].clip(lower=0.0, upper=100.0)
        return df

    def run_scenario(self, scenario_name: str, base_features: pd.DataFrame, predictor) -> Dict[str, Any]:
        name = scenario_name.upper().strip()
        if name not in self.PREDEFINED:
            raise ValueError(f"Unknown scenario: {scenario_name}")
            
        scenario_def = self.PREDEFINED[name]
        
        current_time = pd.Timestamp.utcnow()
        features_for_pred = base_features.drop(columns=['timestamp', 'station'], errors='ignore')
        
        # 1. Baseline forecast
        base_pred = predictor.predict(features_for_pred, current_timestamp=current_time)
        base_pm25 = base_pred["forecasts"][0]["prediction"] if "forecasts" in base_pred else 0
        
        # 2. Scenario features
        scen_features = self.apply_what_if(base_features, scenario_def["changes"])
        scen_features_for_pred = scen_features.drop(columns=['timestamp', 'station'], errors='ignore')
        
        # 3. Scenario forecast
        scen_pred = predictor.predict(scen_features_for_pred, current_timestamp=current_time)
        scen_pm25 = scen_pred["forecasts"][0]["prediction"] if "forecasts" in scen_pred else 0
        
        return {
            "scenario_name": name,
            "assumptions": scenario_def["assumptions"],
            "input_changes": scenario_def["changes"],
            "forecast_effect": {
                "baseline_t1_pm25": round(base_pm25, 2),
                "scenario_t1_pm25": round(scen_pm25, 2),
                "delta_pm25": round(scen_pm25 - base_pm25, 2)
            },
            "status": "SCENARIO"
        }

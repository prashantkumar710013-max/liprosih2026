import pandas as pd
import numpy as np

class CoupledFeatures:
    """Extracts features modeling the interaction between weather and pollution."""
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # Wind Stagnation Index: high when wind is low.
        if 'wind_speed' in df.columns:
            # Prevent div by zero
            df['wind_stagnation_index'] = 1.0 / (df['wind_speed'] + 0.1)
            
        # Humidity-Pollution Interaction: high humidity + high PM2.5 often exacerbates smog
        if 'humidity' in df.columns and 'pm25' in df.columns:
            df['humidity_pm25_interaction'] = df['humidity'] * df['pm25']
            
        # Temperature-Pollution Interaction
        if 'temperature' in df.columns and 'pm25' in df.columns:
            df['temperature_pm25_interaction'] = df['temperature'] * df['pm25']
            
        # Ventilation Proxy: roughly wind_speed * boundary layer height.
        # Since we lack BLH, we use temperature as a proxy for daytime mixing (very rough).
        if 'wind_speed' in df.columns and 'temperature' in df.columns:
            # Only positive temp impact mixing
            temp_pos = np.maximum(df['temperature'], 0.1)
            df['ventilation_proxy'] = df['wind_speed'] * temp_pos

        # Rain Scavenging Indicator: PM2.5 decreases when it rains.
        # Interaction between current rain and previous PM2.5
        if 'precipitation' in df.columns and 'pm25' in df.columns:
            df['rain_scavenging_indicator'] = df['precipitation'] * df['pm25']

        # Stability Proxy: combination of low wind and low temp
        if 'wind_speed' in df.columns and 'temperature' in df.columns:
            df['pressure_stability_proxy'] = 1.0 / (df['wind_speed'] * np.maximum(df['temperature'], 0.1) + 0.1)

        return df

import pandas as pd
import numpy as np

class WeatherFeatures:
    """Extracts derived features from weather data."""
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # Dew point approximation if temp and humidity exist
        # Td = T - ((100 - RH)/5.)
        if 'temperature' in df.columns and 'humidity' in df.columns:
            df['dew_point_approx'] = df['temperature'] - ((100 - df['humidity']) / 5.0)
            
        # Thermal inversion proxy: temperature gradient is hard without height data,
        # but a rough proxy for night-time cooling in winter is extreme drops in temp.
        # We handle this better in coupled features.
        
        # Wind components (U, V vectors)
        if 'wind_speed' in df.columns and 'wind_direction' in df.columns:
            rad = np.deg2rad(df['wind_direction'])
            df['wind_u'] = df['wind_speed'] * np.sin(rad)
            df['wind_v'] = df['wind_speed'] * np.cos(rad)
            
        # Precipitation flags
        if 'precipitation' in df.columns:
            df['is_raining'] = (df['precipitation'] > 0).astype(np.int32)
            df['heavy_rain'] = (df['precipitation'] > 10).astype(np.int32)

        return df

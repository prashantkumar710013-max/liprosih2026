import pandas as pd

class DataNormalizer:
    def __init__(self):
        # Maps expected source columns to standardized columns
        self.column_mapping = {
            # Pollutants
            'PM2.5': 'pm25',
            'PM2.5 (ug/m3)': 'pm25',
            'PM 2.5': 'pm25',
            'pm2.5': 'pm25',
            'pm2_5': 'pm25',
            'PM10': 'pm10',
            'PM10 (ug/m3)': 'pm10',
            'PM 10': 'pm10',
            'pm10': 'pm10',
            'NO2': 'no2',
            'NO2 (ug/m3)': 'no2',
            'nitrogen_dioxide': 'no2',
            'SO2': 'so2',
            'SO2 (ug/m3)': 'so2',
            'sulphur_dioxide': 'so2',
            'CO': 'co',
            'CO (mg/m3)': 'co',
            'Ozone': 'o3',
            'ozone': 'o3',
            'O3': 'o3',
            'O3 (ug/m3)': 'o3',
            'AQI': 'aqi',
            'aqi': 'aqi',
            'us_aqi': 'aqi',
            
            # Weather
            'Temp': 'temperature',
            'Temperature': 'temperature',
            'temp': 'temperature',
            'T2M': 'temperature',
            'RH': 'humidity',
            'Humidity': 'humidity',
            'humidity': 'humidity',
            'RH2M': 'humidity',
            'WS': 'wind_speed',
            'Wind Speed': 'wind_speed',
            'wind_speed': 'wind_speed',
            'WS10M': 'wind_speed',
            'WD': 'wind_direction',
            'Wind Direction': 'wind_direction',
            'wind_direction': 'wind_direction',
            'BP': 'pressure',
            'Pressure': 'pressure',
            'pressure': 'pressure',
            'Precipitation': 'precipitation',
            'Rain': 'precipitation',
            'precipitation': 'precipitation',
            'PRECTOTCORR': 'precipitation',
            
            # Others
            'From Date': 'timestamp',
            'To Date': 'timestamp_end',
            'date': 'timestamp',
            'datetime': 'timestamp'
        }

    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Renames columns based on the predefined mapping.
        If a column doesn't exist in the mapping, it's left as-is (but lowercased).
        """
        new_cols = {}
        for col in df.columns:
            mapped_col = self.column_mapping.get(col, str(col).lower().replace(' ', '_'))
            new_cols[col] = mapped_col
        
        return df.rename(columns=new_cols)

    def standardize_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensures pollutants and weather metrics are numeric.
        """
        numeric_cols = [
            'pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'aqi',
            'temperature', 'humidity', 'wind_speed', 'wind_direction',
            'pressure', 'precipitation'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        return df

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.normalize_columns(df)
        df = self.standardize_types(df)
        return df

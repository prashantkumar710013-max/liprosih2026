import pandas as pd
import numpy as np

class TemporalFeatures:
    """Extracts temporal features and cyclic encodings from timestamp."""
    
    def transform(self, df: pd.DataFrame, time_col: str = 'timestamp') -> pd.DataFrame:
        df = df.copy()
        if time_col not in df.columns:
            return df
            
        dt = df[time_col].dt
        
        # Basic extractions
        df['hour'] = dt.hour
        df['day'] = dt.day
        df['day_of_week'] = dt.dayofweek
        df['month'] = dt.month
        df['day_of_year'] = dt.dayofyear
        
        # isocalendar week
        df['week_of_year'] = dt.isocalendar().week.astype(np.int32)
        
        # Boolean / Categorical (represented as 0/1)
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(np.int32)
        df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 5)).astype(np.int32)
        df['is_morning'] = ((df['hour'] >= 6) & (df['hour'] <= 11)).astype(np.int32)
        df['is_evening'] = ((df['hour'] >= 17) & (df['hour'] <= 21)).astype(np.int32)
        
        # Cyclical encoding
        df['sin_hour'] = np.sin(2 * np.pi * df['hour'] / 24.0)
        df['cos_hour'] = np.cos(2 * np.pi * df['hour'] / 24.0)
        
        # Days in month vary, we will approximate max as 31 for sin/cos or exact
        days_in_month = dt.days_in_month
        df['sin_day'] = np.sin(2 * np.pi * df['day'] / days_in_month)
        df['cos_day'] = np.cos(2 * np.pi * df['day'] / days_in_month)
        
        df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12.0)
        df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12.0)
        
        return df

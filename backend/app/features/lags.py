import pandas as pd
from typing import List

class LagFeatures:
    """Extracts lag features for historical data."""
    
    def __init__(self, target_cols: List[str] = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'aqi'],
                 lags: List[int] = [1, 2, 3, 6, 12, 24]):
        self.target_cols = target_cols
        self.lags = lags

    def transform(self, df: pd.DataFrame, time_col: str = 'timestamp') -> pd.DataFrame:
        """
        Assumes dataframe is sorted by time.
        We group by station if station is present to avoid lagging across different locations.
        """
        df = df.copy()
        
        # Make sure data is sorted
        df = df.sort_values(by=time_col)
        
        groupby_col = 'station' if 'station' in df.columns else None
        
        for col in self.target_cols:
            if col not in df.columns:
                continue
            for lag in self.lags:
                col_name = f"{col}_lag{lag}"
                if groupby_col:
                    df[col_name] = df.groupby(groupby_col)[col].shift(lag)
                else:
                    df[col_name] = df[col].shift(lag)
                    
        return df

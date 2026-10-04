import pandas as pd
from typing import List

class RollingFeatures:
    """Extracts rolling window features."""
    
    def __init__(self, target_cols: List[str] = ['pm25', 'pm10', 'temperature'],
                 windows: List[int] = [3, 6, 12, 24]):
        self.target_cols = target_cols
        self.windows = windows

    def transform(self, df: pd.DataFrame, time_col: str = 'timestamp') -> pd.DataFrame:
        """
        Calculates rolling mean, std, min, max.
        Shift by 1 is CRITICAL so rolling window doesn't include the current timestamp (which would be a target leak).
        """
        df = df.copy()
        df = df.sort_values(by=time_col)
        
        groupby_col = 'station' if 'station' in df.columns else None
        
        for col in self.target_cols:
            if col not in df.columns:
                continue
                
            for w in self.windows:
                if groupby_col:
                    # Shift(1) per group
                    shifted = df.groupby(groupby_col)[col].shift(1)
                    # We can group the shifted series by the same station col
                    # rolling() on group preserves index if we use reset_index(0, drop=True)
                    df[f"{col}_{w}h_mean"] = shifted.groupby(df[groupby_col]).rolling(w).mean().reset_index(0, drop=True)
                    df[f"{col}_{w}h_std"]  = shifted.groupby(df[groupby_col]).rolling(w).std().reset_index(0, drop=True)
                    df[f"{col}_{w}h_min"]  = shifted.groupby(df[groupby_col]).rolling(w).min().reset_index(0, drop=True)
                    df[f"{col}_{w}h_max"]  = shifted.groupby(df[groupby_col]).rolling(w).max().reset_index(0, drop=True)
                else:
                    shifted = df[col].shift(1)
                    df[f"{col}_{w}h_mean"] = shifted.rolling(w).mean()
                    df[f"{col}_{w}h_std"] = shifted.rolling(w).std()
                    df[f"{col}_{w}h_min"] = shifted.rolling(w).min()
                    df[f"{col}_{w}h_max"] = shifted.rolling(w).max()
                    
        return df

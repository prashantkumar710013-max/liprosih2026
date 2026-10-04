import pandas as pd
import numpy as np

class PollutionFeatures:
    """Generates derived features purely from pollutants."""
    
    def transform(self, df: pd.DataFrame, time_col: str = 'timestamp') -> pd.DataFrame:
        df = df.copy()
        
        # Sort and group if needed for temporal calculations
        df = df.sort_values(by=time_col)
        groupby_col = 'station' if 'station' in df.columns else None

        # 1. Growth Rates (change compared to previous hour)
        pollutants = ['pm25', 'pm10', 'no2']
        for p in pollutants:
            if p in df.columns:
                if groupby_col:
                    prev = df.groupby(groupby_col)[p].shift(1)
                else:
                    prev = df[p].shift(1)
                
                # growth_rate = (current - prev) / (prev + 1e-5)
                # To avoid target leakage in predictive models, growth rate should be between t-1 and t-2
                # Since we want features representing the state at time T to predict T+1 or T+H,
                # growth rate AT time T is (val_T - val_{T-1}) / val_{T-1}
                df[f'{p}_growth_rate'] = (df[p] - prev) / (prev + 1e-5)

        # 2. Ratios (intra-hour relationships)
        # These do not leak the future, they just describe the current state
        if 'pm25' in df.columns and 'pm10' in df.columns:
            df['pm25_pm10_ratio'] = df['pm25'] / (df['pm10'] + 1e-5)
            
        if 'no2' in df.columns and 'pm25' in df.columns:
            df['no2_pm25_ratio'] = df['no2'] / (df['pm25'] + 1e-5)
            
        if 'so2' in df.columns and 'pm25' in df.columns:
            df['so2_pm25_ratio'] = df['so2'] / (df['pm25'] + 1e-5)

        if 'co' in df.columns and 'no2' in df.columns:
            df['co_no2_ratio'] = df['co'] / (df['no2'] + 1e-5)

        return df

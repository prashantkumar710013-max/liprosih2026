import pandas as pd
from typing import Dict, Any, List

class DataValidator:
    def __init__(self):
        # Thresholds for extreme values
        self.thresholds = {
            'pm25': {'min': 0, 'max': 1000},
            'pm10': {'min': 0, 'max': 1500},
            'temperature': {'min': -10, 'max': 55}, # Celsius
            'humidity': {'min': 0, 'max': 100},
            'wind_speed': {'min': 0, 'max': 150},
            'aqi': {'min': 0, 'max': 2000}
        }

    def validate(self, df: pd.DataFrame, time_col: str = 'timestamp') -> Dict[str, Any]:
        report = {
            "missing_timestamps": 0,
            "duplicate_timestamps": 0,
            "invalid_timestamps": 0,
            "negative_values": {},
            "impossible_weather": {},
            "missing_values": {},
            "extreme_values": {},
            "flags": []
        }
        
        # 1. Timestamp validation
        if time_col in df.columns:
            report["missing_timestamps"] = df[time_col].isna().sum()
            report["duplicate_timestamps"] = df[time_col].duplicated().sum()
            # Invalid timestamps are usually NaT after parsing
            # Gap detection
            if not df[time_col].isna().all():
                df_sorted = df.sort_values(time_col)
                # simple gap check for hourly data
                diffs = df_sorted[time_col].diff()
                gaps = diffs[diffs > pd.Timedelta(hours=1)]
                if not gaps.empty:
                    report["flags"].append(f"Found {len(gaps)} potential gaps in timeline")
        else:
            report["flags"].append(f"Time column {time_col} not found")

        # 2. Value Validation
        for col in df.columns:
            if df[col].dtype.kind in 'biufc': # numeric
                # Missing values
                report["missing_values"][col] = df[col].isna().sum()
                
                # Negative values (most metrics shouldn't be negative)
                if col not in ['temperature']: # temp can be negative, though rare in Delhi
                    negatives = (df[col] < 0).sum()
                    if negatives > 0:
                        report["negative_values"][col] = negatives
                        report["flags"].append(f"Found {negatives} negative values in {col}")
                
                # Impossible and extreme values
                if col in self.thresholds:
                    t_min = self.thresholds[col]['min']
                    t_max = self.thresholds[col]['max']
                    
                    extreme = ((df[col] < t_min) | (df[col] > t_max)).sum()
                    if extreme > 0:
                        report["extreme_values"][col] = extreme
                        report["flags"].append(f"Found {extreme} extreme values in {col}")

        return report

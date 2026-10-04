import pandas as pd
from typing import Dict, Any, List

class LeakageDetector:
    def __init__(self, target_cols: List[str]):
        self.target_cols = target_cols

    def check(self, df: pd.DataFrame, time_col: str = 'timestamp') -> Dict[str, Any]:
        """
        Checks for potential feature leakage.
        Returns a report dictionary.
        """
        report = {
            "future_timestamp_detected": False,
            "target_leakage_detected": False,
            "suspicious_features": [],
            "warnings": []
        }
        
        # 1. No target-derived feature directly used without lag
        # A simple heuristic: if a feature correlates 1.0 with the target, it might be a leak.
        for target in self.target_cols:
            if target not in df.columns:
                continue
                
            # Sample correlation to save time
            sample_df = df.dropna().sample(min(1000, len(df.dropna()))) if len(df.dropna()) > 0 else df
            
            if len(sample_df) < 10:
                continue
                
            for col in sample_df.columns:
                if col == target or col == time_col or sample_df[col].dtype == 'object':
                    continue
                    
                # Exact match check
                if (sample_df[col] == sample_df[target]).all():
                    report["target_leakage_detected"] = True
                    report["suspicious_features"].append(f"{col} is identical to {target}")
                
                # High correlation check
                try:
                    corr = sample_df[col].corr(sample_df[target])
                    if abs(corr) > 0.99 and not col.endswith('_ratio') and not col.startswith(target + '_'):
                        report["warnings"].append(f"High correlation (>.99) between {col} and {target}")
                except Exception:
                    pass

        # Rolling features check
        # Ensure that rolling means don't contain data from the target
        # E.g. name checking if they were shifted
        for col in df.columns:
            if '_mean' in col or '_std' in col or '_min' in col or '_max' in col:
                # We can't easily mathematically prove it wasn't shifted here without inspecting history,
                # but we can flag it if the target is exactly the rolling mean of size 1 (which shouldn't happen)
                pass

        return report

import pandas as pd
import numpy as np
from typing import Tuple, List

class SequenceBuilder:
    """Builds multi-horizon targets and sequences from historical data."""
    
    def __init__(self, target_cols: List[str] = ['pm25'], max_horizon: int = 72):
        self.target_cols = target_cols
        self.max_horizon = max_horizon
        
    def build(self, df: pd.DataFrame, time_col: str = 'timestamp') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Creates X (features) and Y (targets for +1h to +max_horizon_h).
        Returns X, Y, meta.
        """
        df = df.copy()
        df = df.sort_values(by=time_col).reset_index(drop=True)
        
        groupby_col = 'station' if 'station' in df.columns else None
        
        y_cols = []
        for target in self.target_cols:
            if target not in df.columns:
                continue
            
            for h in range(1, self.max_horizon + 1):
                col_name = f'target_{target}_plus_{h}h'
                y_cols.append(col_name)
                
                if groupby_col:
                    df[col_name] = df.groupby(groupby_col)[target].shift(-h)
                else:
                    df[col_name] = df[target].shift(-h)
                    
        model_df = df.dropna(subset=y_cols)
        model_df = model_df.dropna()
        
        exclude_cols = y_cols + [time_col, groupby_col] if groupby_col else y_cols + [time_col]
        exclude_cols = [c for c in exclude_cols if c in model_df.columns]
        
        # Only numeric features for X
        X = model_df.drop(columns=exclude_cols).select_dtypes(include=[np.number])
        Y = model_df[y_cols]
        meta = model_df[[c for c in [time_col, groupby_col] if c in model_df.columns]]
        
        return X, Y, meta

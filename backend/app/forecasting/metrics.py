import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, Any

def evaluate_multi_horizon(y_true: np.ndarray, y_pred: np.ndarray, horizons: list = [6, 12, 24, 48, 72]) -> Dict[str, Any]:
    """
    Evaluates specific horizons. 
    y_true and y_pred should be arrays of shape (N, max_horizon).
    """
    results = {}
    
    # overall metrics
    results['overall'] = {
        'mae': mean_absolute_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2': r2_score(y_true, y_pred)
    }
    
    # metrics for specific horizons (1-indexed in name, 0-indexed in array)
    for h in horizons:
        idx = h - 1
        if idx < y_true.shape[1]:
            results[f'{h}h'] = {
                'mae': mean_absolute_error(y_true[:, idx], y_pred[:, idx]),
                'rmse': np.sqrt(mean_squared_error(y_true[:, idx], y_pred[:, idx])),
                'r2': r2_score(y_true[:, idx], y_pred[:, idx])
            }
            
    return results

import numpy as np

class EmpiricalUncertainty:
    """
    Computes empirical prediction intervals based on training residuals.
    A simple but defensible method: assume errors are normally distributed per horizon.
    """
    
    def __init__(self):
        self.std_per_horizon = None
        
    def fit(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        y_true and y_pred shape: (N, H)
        Computes standard deviation of residuals per horizon.
        """
        residuals = y_true - y_pred
        self.std_per_horizon = np.std(residuals, axis=0)
        
    def predict_intervals(self, y_pred: np.ndarray, z_score: float = 1.96) -> tuple:
        """
        Returns (lower, upper). z_score=1.96 is ~95% confidence interval.
        """
        if self.std_per_horizon is None:
            # Fallback if not fitted properly
            H = y_pred.shape[1]
            # Simple heuristic: error grows linearly with time
            self.std_per_horizon = np.array([20.0 + (i * 0.5) for i in range(H)])
            
        margin = z_score * self.std_per_horizon
        lower = np.maximum(y_pred - margin, 0) # PM2.5 can't be negative
        upper = y_pred + margin
        
        return lower, upper

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any
from .uncertainty import EmpiricalUncertainty

class LiproPredictor:
    """Loads a trained model and makes API-ready predictions with uncertainty."""
    
    def __init__(self, model_dir: str, model_name: str = 'lipro_xgb.joblib'):
        self.model_path = os.path.join(model_dir, model_name)
        self.model = None
        self.uncertainty = EmpiricalUncertainty()
        # Initialize fallback uncertainty
        self.uncertainty.predict_intervals(np.zeros((1, 72))) 
        
    def load(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        self.model = joblib.load(self.model_path)
        
    def predict(self, X: pd.DataFrame, current_timestamp: pd.Timestamp) -> Dict[str, Any]:
        if self.model is None:
            self.load()
            
        import joblib
        
        # Align features to what the model expects, filling missing with 0
        if hasattr(self.model, "feature_names_in_"):
            expected_cols = list(self.model.feature_names_in_)
        elif hasattr(self.model.estimators_[0], "feature_names_in_"):
            expected_cols = list(self.model.estimators_[0].feature_names_in_)
        else:
            expected_cols = X.columns
            
        for col in expected_cols:
            if col not in X.columns:
                X[col] = 0.0
        X = X[expected_cols]
        
        with joblib.parallel_backend("sequential"):
            y_pred = self.model.predict(X)
            
        lower, upper = self.uncertainty.predict_intervals(y_pred)
        
        y_pred = y_pred[0]
        lower = lower[0]
        upper = upper[0]
        
        forecasts = []
        for h in range(len(y_pred)):
            target_time = current_timestamp + pd.Timedelta(hours=h+1)
            pred_val = float(y_pred[h])
            
            # Very simple risk heuristic
            risk = "Low"
            if pred_val > 250:
                risk = "Severe"
            elif pred_val > 150:
                risk = "High"
            elif pred_val > 50:
                risk = "Moderate"
                
            forecasts.append({
                "timestamp": target_time.isoformat(),
                "horizon": h + 1,
                "prediction": round(pred_val, 2),
                "lower_bound": round(float(lower[h]), 2),
                "upper_bound": round(float(upper[h]), 2),
                "confidence": "95%",
                "risk": risk
            })
            
        return {"forecasts": forecasts}

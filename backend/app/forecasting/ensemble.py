import pandas as pd
import numpy as np
from typing import List

class EnsemblePredictor:
    """Combines multiple models for a robust ensemble forecast."""
    
    def __init__(self, models: List[Any]):
        self.models = models
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        preds = []
        for model in self.models:
            preds.append(model.predict(X))
            
        return np.mean(preds, axis=0)

import shap
import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Any

class ModelExplainer:
    """
    Explainable AI module using SHAP.
    Explains the predictions of the trained XGBoost model.
    """
    def __init__(self, model_dir: str):
        self.model_path = os.path.join(model_dir, 'lipro_xgb.joblib')
        self.model = None
        self.explainer = None
        
    def load(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        # MultiOutputRegressor contains multiple estimators
        self.model = joblib.load(self.model_path)
        
        # For simplicity, we explain the first estimator (e.g., +1h forecast)
        # In a real app we'd explain the specific horizon requested, but SHAP 
        # on TreeExplainer works per tree.
        base_xgb = self.model.estimators_[0] 
        self.explainer = shap.TreeExplainer(base_xgb)
        
    def explain_instance(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Returns top positive and negative contributing factors for a single prediction.
        """
        if self.model is None or self.explainer is None:
            self.load()
            
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
            
        # Ensure single row
        X = X.iloc[[0]]
        
        # Get SHAP values
        import joblib
        with joblib.parallel_backend("sequential"):
            shap_values = self.explainer.shap_values(X)
        expected_value = self.explainer.expected_value
        
        if isinstance(shap_values, list): # Multi-class or other format
            shap_values = shap_values[0]
            
        sv = shap_values[0] # Single row
        
        # Match SHAP values with feature names
        feature_names = X.columns.tolist()
        feature_values = X.iloc[0].to_dict()
        
        contributions = []
        for i, fname in enumerate(feature_names):
            contributions.append({
                "feature": fname,
                "value": round(float(feature_values[fname]), 2),
                "impact": round(float(sv[i]), 2),
                "direction": "INCREASES_POLLUTION" if sv[i] > 0 else "DECREASES_POLLUTION",
                "importance": abs(float(sv[i]))
            })
            
        # Sort by absolute importance
        contributions = sorted(contributions, key=lambda x: x["importance"], reverse=True)
        
        top_positive = [c for c in contributions if c["impact"] > 0][:5]
        top_negative = [c for c in contributions if c["impact"] < 0][:5]
        
        return {
            "model_information": "Lipro XGBoost (+1h Horizon Tree)",
            "base_value": round(float(expected_value), 2),
            "top_positive_factors": top_positive,
            "top_negative_factors": top_negative,
            "feature_values": {c["feature"]: c["value"] for c in contributions[:10]} # top 10 for context
        }

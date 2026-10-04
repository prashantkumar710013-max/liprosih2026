import pytest
import pandas as pd
import numpy as np
import os
import joblib
from xgboost import XGBRegressor

from app.explainability.explainer import ModelExplainer

@pytest.fixture
def mock_explainer(tmp_path):
    # Create a mock model
    model_dir = str(tmp_path)
    os.makedirs(os.path.join(model_dir), exist_ok=True)
    
    # Needs MultiOutputRegressor, but we can just mock a standard XGBRegressor wrapped
    from sklearn.multioutput import MultiOutputRegressor
    base_xgb = XGBRegressor(n_estimators=5, max_depth=3)
    X = pd.DataFrame({"pm25_lag1": [100, 150, 200], "wind_speed": [2.0, 1.0, 5.0]})
    Y = pd.DataFrame({"target_plus_1h": [110, 160, 190]})
    
    multi = MultiOutputRegressor(base_xgb)
    multi.fit(X, Y)
    
    joblib.dump(multi, os.path.join(model_dir, 'aerosense_xgb.joblib'))
    
    explainer = ModelExplainer(model_dir)
    return explainer, X

def test_explain_instance(mock_explainer):
    explainer, X = mock_explainer
    row = X.iloc[[0]]
    
    explanation = explainer.explain_instance(row)
    
    assert "model_information" in explanation
    assert "base_value" in explanation
    assert "top_positive_factors" in explanation
    assert "top_negative_factors" in explanation
    
    # We should have features returned
    all_features = [f['feature'] for f in explanation['top_positive_factors']] + \
                   [f['feature'] for f in explanation['top_negative_factors']]
    
    assert len(all_features) > 0

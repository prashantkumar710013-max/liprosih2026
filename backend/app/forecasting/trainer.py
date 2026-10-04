import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from .metrics import evaluate_multi_horizon

class BaselineTrainer:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
    def train_persistence(self, X_test: pd.DataFrame, Y_test: pd.DataFrame, target_col_in_X: str = 'pm25'):
        """Persistence model: predicted future is simply the current value."""
        # y_pred shape: (N, max_horizon)
        # We just duplicate the current PM2.5 value across all horizons
        N = len(X_test)
        H = Y_test.shape[1]
        
        current_vals = X_test[target_col_in_X].values
        y_pred = np.tile(current_vals, (H, 1)).T
        
        metrics = evaluate_multi_horizon(Y_test.values, y_pred)
        return metrics

    def train_xgboost(self, X_train: pd.DataFrame, Y_train: pd.DataFrame, 
                      X_test: pd.DataFrame, Y_test: pd.DataFrame):
        print("Training XGBoost MultiOutput (this might take a minute)...")
        # Lightweight XGB for speed in this stage
        base_xgb = XGBRegressor(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
        multi_xgb = MultiOutputRegressor(base_xgb, n_jobs=-1)
        
        multi_xgb.fit(X_train, Y_train)
        y_pred = multi_xgb.predict(X_test)
        
        metrics = evaluate_multi_horizon(Y_test.values, y_pred)
        
        # Save model
        joblib.dump(multi_xgb, os.path.join(self.model_dir, 'lipro_xgb.joblib'))
        return metrics

    def train_rf(self, X_train: pd.DataFrame, Y_train: pd.DataFrame, 
                 X_test: pd.DataFrame, Y_test: pd.DataFrame):
        print("Training Random Forest MultiOutput...")
        # Extremely lightweight RF for speed
        rf = RandomForestRegressor(n_estimators=20, max_depth=5, random_state=42, n_jobs=-1)
        # RF naturally supports multi-output without wrapper, but wrapper or direct is fine
        rf.fit(X_train, Y_train)
        y_pred = rf.predict(X_test)
        
        metrics = evaluate_multi_horizon(Y_test.values, y_pred)
        
        joblib.dump(rf, os.path.join(self.model_dir, 'lipro_rf.joblib'))
        return metrics

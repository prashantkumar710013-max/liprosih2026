import os
import sys
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.data.loaders import DataLoader
from app.data.normalizer import DataNormalizer
from app.features.temporal import TemporalFeatures
from app.features.lags import LagFeatures
from app.features.rolling import RollingFeatures
from app.features.pollution import PollutionFeatures
from app.features.weather import WeatherFeatures
from app.features.coupled import CoupledFeatures
from app.features.leakage import LeakageDetector

def main():
    print("Loading data...")
    loader = DataLoader()
    normalizer = DataNormalizer()
    
    # We will use the recent hourly dataset for this baseline
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'source', 'project_2', 'delhi_air_quality_hourly_2023_2025.csv')
    
    if not os.path.exists(file_path):
        print(f"Data not found: {file_path}")
        return
        
    df, _ = loader.load_dataset(file_path)
    df = normalizer.normalize(df)
    
    # Needs a mock 'station' column since it's just one dataset representing Delhi average or a specific point
    if 'station' not in df.columns:
        df['station'] = 'Delhi_Avg'
        
    # Handle missing weather by merging if needed, or if the CSV already has both
    if 'temperature' not in df.columns:
        w_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'source', 'project_2', 'delhi_weather_daily_2023_2025.csv')
        w_df, _ = loader.load_dataset(w_path)
        w_df = normalizer.normalize(w_df)
        
        # simple merge on date (weather is daily, AQ is hourly)
        df['date_only'] = df['timestamp'].dt.date
        w_df['date_only'] = w_df['timestamp'].dt.date
        w_df = w_df.drop(columns=['timestamp'], errors='ignore')
        df = pd.merge(df, w_df, on='date_only', how='left').drop(columns=['date_only'])
        
        # ffill daily weather to hourly
        df = df.ffill()

    print("Applying feature engineering...")
    df = TemporalFeatures().transform(df)
    df = LagFeatures(target_cols=['pm25', 'pm10', 'no2'], lags=[1, 2, 3, 6, 12, 24]).transform(df)
    df = RollingFeatures(target_cols=['pm25', 'temperature'], windows=[6, 12, 24]).transform(df)
    df = PollutionFeatures().transform(df)
    df = WeatherFeatures().transform(df)
    df = CoupledFeatures().transform(df)
    
    print("Checking for leakage...")
    ld = LeakageDetector(target_cols=['pm25'])
    report = ld.check(df)
    
    leakage_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'LEAKAGE_REPORT.md')
    with open(leakage_path, 'w') as f:
        f.write("# Feature Leakage Report\n\n")
        for k, v in report.items():
            f.write(f"- **{k}**: {v}\n")
    print(f"Leakage report saved to {leakage_path}")

    out_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'features', 'aerosense_features.parquet')
    df.to_parquet(out_path)
    print(f"Saved features to {out_path} ({df.shape[0]} rows, {df.shape[1]} columns)")

    # Baseline Model for Feature Importance
    # Target: Predict next hour PM2.5 (T+1)
    # We shift pm25 by -1 to get the target
    print("Training baseline XGBoost for feature importance...")
    
    df = df.sort_values('timestamp')
    df['target_pm25_next_hr'] = df.groupby('station')['pm25'].shift(-1)
    
    # Drop rows where target is missing or inputs are extremely missing
    model_df = df.dropna(subset=['target_pm25_next_hr', 'pm25', 'pm25_lag1'])
    
    # Select numeric features
    features = [c for c in model_df.columns if c not in ['timestamp', 'station', 'target_pm25_next_hr'] and model_df[c].dtype in ['float64', 'float32', 'int64', 'int32']]
    
    X = model_df[features]
    y = model_df['target_pm25_next_hr']
    
    # Train-test split (time-based)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    xgb = XGBRegressor(n_estimators=50, max_depth=5, random_state=42)
    xgb.fit(X_train, y_train)
    
    preds = xgb.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Baseline MAE: {mae:.2f}")
    
    # Feature Importance
    importances = pd.DataFrame({
        'Feature': features,
        'Importance': xgb.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    imp_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'BASELINE_FEATURE_IMPORTANCE.md')
    with open(imp_path, 'w') as f:
        f.write("# Baseline Feature Importance\n\n")
        f.write("This is a lightweight XGBoost model predicting PM2.5 at T+1, purely for validating feature signals.\n\n")
        f.write(importances.head(30).to_markdown(index=False))
        
    print(f"Feature importance saved to {imp_path}")

if __name__ == "__main__":
    main()

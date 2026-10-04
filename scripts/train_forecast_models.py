import os
import sys
import pandas as pd
import numpy as np
from tabulate import tabulate

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.forecasting.sequence_builder import SequenceBuilder
from app.forecasting.trainer import BaselineTrainer

def main():
    print("Loading feature dataset...")
    features_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'features', 'aerosense_features.parquet')
    if not os.path.exists(features_path):
        print(f"Features not found at {features_path}. Run feature generation first.")
        return
        
    df = pd.read_parquet(features_path)
    
    print("Building sequences for 72-hour multi-horizon forecast...")
    sb = SequenceBuilder(target_cols=['pm25'], max_horizon=72)
    X, Y, meta = sb.build(df, time_col='timestamp')
    
    print(f"Generated {len(X)} sequences.")
    
    # Chronological Split (80% train, 20% test)
    # We do NOT shuffle.
    split_idx = int(len(X) * 0.8)
    
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    Y_train, Y_test = Y.iloc[:split_idx], Y.iloc[split_idx:]
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.")
    
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'aerosense')
    trainer = BaselineTrainer(model_dir=model_dir)
    
    print("\n--- Evaluating Persistence Baseline ---")
    persistence_metrics = trainer.train_persistence(X_test, Y_test, target_col_in_X='pm25')
    
    print("\n--- Training Random Forest ---")
    rf_metrics = trainer.train_rf(X_train, Y_train, X_test, Y_test)
    
    print("\n--- Training XGBoost (AeroSense Model) ---")
    xgb_metrics = trainer.train_xgboost(X_train, Y_train, X_test, Y_test)
    
    # Generate Evaluation Report
    report_lines = [
        "# Forecast Evaluation Report",
        "",
        "This report compares the multi-horizon forecasting models over 72 hours for PM2.5.",
        "The models were evaluated using a chronological split to prevent data leakage.",
        "",
        "## Models Evaluated",
        "- **Persistence**: Assumes current pollution level remains constant for next 72 hours.",
        "- **Random Forest**: Baseline tree ensemble.",
        "- **XGBoost (AeroSense Model)**: Advanced gradient boosted multi-output regressor using weather-coupled features.",
        "",
        "## Overall 72-Hour Average Performance",
        ""
    ]
    
    headers = ["Model", "MAE", "RMSE", "R²"]
    overall_table = [
        ["Persistence", f"{persistence_metrics['overall']['mae']:.2f}", f"{persistence_metrics['overall']['rmse']:.2f}", f"{persistence_metrics['overall']['r2']:.2f}"],
        ["Random Forest", f"{rf_metrics['overall']['mae']:.2f}", f"{rf_metrics['overall']['rmse']:.2f}", f"{rf_metrics['overall']['r2']:.2f}"],
        ["XGBoost", f"{xgb_metrics['overall']['mae']:.2f}", f"{xgb_metrics['overall']['rmse']:.2f}", f"{xgb_metrics['overall']['r2']:.2f}"]
    ]
    report_lines.append(tabulate(overall_table, headers, tablefmt="github"))
    
    report_lines.extend([
        "",
        "## Horizon-Specific Performance (MAE)",
        ""
    ])
    
    h_headers = ["Model", "6h", "12h", "24h", "48h", "72h"]
    h_table = [
        ["Persistence", f"{persistence_metrics.get('6h',{}).get('mae', 0):.2f}", f"{persistence_metrics.get('12h',{}).get('mae', 0):.2f}", f"{persistence_metrics.get('24h',{}).get('mae', 0):.2f}", f"{persistence_metrics.get('48h',{}).get('mae', 0):.2f}", f"{persistence_metrics.get('72h',{}).get('mae', 0):.2f}"],
        ["Random Forest", f"{rf_metrics.get('6h',{}).get('mae', 0):.2f}", f"{rf_metrics.get('12h',{}).get('mae', 0):.2f}", f"{rf_metrics.get('24h',{}).get('mae', 0):.2f}", f"{rf_metrics.get('48h',{}).get('mae', 0):.2f}", f"{rf_metrics.get('72h',{}).get('mae', 0):.2f}"],
        ["XGBoost", f"{xgb_metrics.get('6h',{}).get('mae', 0):.2f}", f"{xgb_metrics.get('12h',{}).get('mae', 0):.2f}", f"{xgb_metrics.get('24h',{}).get('mae', 0):.2f}", f"{xgb_metrics.get('48h',{}).get('mae', 0):.2f}", f"{xgb_metrics.get('72h',{}).get('mae', 0):.2f}"]
    ]
    
    report_lines.append(tabulate(h_table, h_headers, tablefmt="github"))
    
    out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'FORECAST_EVALUATION.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
        
    print(f"\nSaved evaluation report to {out_path}")

if __name__ == "__main__":
    main()

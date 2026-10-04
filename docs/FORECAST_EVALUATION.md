# Forecast Evaluation Report

This report compares the multi-horizon forecasting models over 72 hours for PM2.5.
The models were evaluated using a chronological split to prevent data leakage.

## Models Evaluated
- **Persistence**: Assumes current pollution level remains constant for next 72 hours.
- **Random Forest**: Baseline tree ensemble.
- **XGBoost (AeroSense Model)**: Advanced gradient boosted multi-output regressor using weather-coupled features.

## Overall 72-Hour Average Performance

| Model         |   MAE |   RMSE |   R² |
|---------------|-------|--------|------|
| Persistence   | 30.87 |  45.25 | 0.08 |
| Random Forest | 24.7  |  36.17 | 0.41 |
| XGBoost       | 22.94 |  33.89 | 0.48 |

## Horizon-Specific Performance (MAE)

| Model         |    6h |   12h |   24h |   48h |   72h |
|---------------|-------|-------|-------|-------|-------|
| Persistence   | 25.11 | 31.76 | 21.22 | 27.68 | 30.63 |
| Random Forest | 21    | 23.89 | 22.46 | 25.37 | 26.24 |
| XGBoost       | 15.95 | 19.8  | 21.67 | 26.87 | 26.63 |
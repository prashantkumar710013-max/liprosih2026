# Model Inventory

## Source Project 1: Air-Pollutant-Prediction-Delhi-main

### Cross-Section Models
| Model | Source project | Target | Input features | Training period | Evaluation method | Metrics | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Linear Regression | Project 1 | PM2.5 / PM10 | Weather conditions (Temperature, Wind Speed, Humidity, Pressure, Weather states) | 2017-2021 | Train/Test Split | RMSE, R-squared | Baseline linear prediction from weather |
| Lasso Regression (L1) | Project 1 | PM2.5 | Weather conditions | 2017-2021 | Train/Test Split | RMSE, R-squared | Regularized linear prediction |
| Ridge Regression (L2) | Project 1 | PM2.5 | Weather conditions | 2017-2021 | Train/Test Split | RMSE, R-squared | Regularized linear prediction |
| Decision Tree Regression | Project 1 | PM2.5 | Weather conditions | 2017-2021 | Train/Test Split | RMSE, R-squared | Non-linear tree-based prediction |
| RandomForest Regression (RFR) | Project 1 | PM2.5 | Weather conditions | 2017-2021 | Train/Test Split (w/ HPT) | RMSE, R-squared | Ensemble tree prediction |
| XGBoost (XGB) | Project 1 | PM2.5 | Weather conditions | 2017-2021 | Train/Test Split (w/ HPT) | RMSE, R-squared | Gradient boosted tree prediction |
| Artificial Neural Network (ANN) | Project 1 | PM2.5 | Weather conditions | 2017-2021 | Train/Test Split | RMSE, R-squared | Deep learning based cross-sectional prediction |

### Time-Series Models
| Model | Source project | Target | Input features | Training period | Evaluation method | Metrics | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ARIMA | Project 1 | PM2.5 | Historical PM2.5 | 2017-2021 | Train/Test Split | Error % | Univariate time-series forecasting |
| VARIMA | Project 1 | PM2.5 | Historical PM2.5, NO2, SO2, CO, Weather | 2017-2021 | Train/Test Split | Error % | Multivariate time-series forecasting |
| RNN | Project 1 | PM2.5 | Historical PM2.5 and covariates (Monthly) | 2017-2021 | Train/Test Split | Error % | Deep learning sequence prediction |
| Transformer | Project 1 | PM2.5 | Historical PM2.5, NO2, SO2, CO, Temp, Wind, Humidity, Pressure (Daily/Monthly) | 2017-2021 | Train/Test Split / Backtest | Error % | State-of-the-art attention-based time-series forecasting (Chosen for API deployment) |

## Source Project 2: delhi-air-quality-analysis-main

*(Specific model names are embedded in Jupyter notebooks; general ensemble methods inferred)*

| Model | Source project | Target | Input features | Training period | Evaluation method | Metrics | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Best Multiyear Model (e.g., XGBoost/RandomForest) | Project 2 | `target_pm2_5_next_day` | `pm2_5`, lags, rolling stats, `T2M`, `RH2M`, `WS10M`, `PRECTOTCORR`, `month`, `day_of_year` | 2023-2025 | Train/Test Split | RMSE, MAE (in `final_metrics_summary_2025.csv`) | Next-day forecasting |
| Risk Categorization Model | Project 2 | `risk_category_next_day` | Same as above | 2025 | Train/Test Split | Accuracy, F1-score | Predict risk category for next day |

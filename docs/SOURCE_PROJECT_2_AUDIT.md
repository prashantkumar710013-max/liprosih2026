# Source Project 2 Audit

## Project Structure
- `data/raw/`: Original unedited CSV files containing weather and AQI data.
- `data/processed/`: Cleaned and engineered datasets ready for modeling.
- `notebooks/`: Jupyter notebooks for data processing, analysis, and forecasting (`delhi_air_quality_forecasting_2025.ipynb`, `delhi_air_quality_multiyear_expansion.ipynb`).
- `outputs/`: Output plots, correlation matrices, and metric summaries.
- Assorted text documentation files detailing methodology, conclusions, and limitations.

## Datasets
- **Raw**: 
  - `delhi_air_quality_hourly_2023_2025.csv`
  - `delhi_air_quality_hourly_2025.csv`
  - `delhi_weather_daily_2023_2025.csv`
  - `delhi_weather_daily_2025.csv`
- **Processed**: 
  - `delhi_pm25_model_data_2025.csv`
  - `delhi_pm25_model_data_with_risk_2025.csv`
  - `delhi_pm25_multiyear_model_data_2023_2025.csv`

## Columns
- **Pollutants**: `pm2_5`, `pm10`, `nitrogen_dioxide`, `sulphur_dioxide`, `ozone`, `us_aqi`
- **Weather Variables**: `T2M` (Temperature), `RH2M` (Relative Humidity), `WS10M` (Wind Speed), `PRECTOTCORR` (Precipitation)
- **Target Variables**: `target_pm2_5_next_day`, `risk_category_next_day`
- **Lag Features**: `pm2_5_lag1`, `pm2_5_lag2`, `pm2_5_lag3`
- **Rolling Features**: `pm2_5_roll3`
- **Time Features**: `datetime`, `date`, `month`, `day_of_year`

## Date Ranges
- Hourly and daily data spanning from 2023-01-01 to 2025-12-31.

## Models
- Machine learning models explored in the notebooks (Notebook names indicate forecasting of PM2.5). Exact models are likely ensemble methods or standard ML approaches given the output summaries (e.g., `model_comparison_2025.csv`).

## Metrics
- Final metrics are evaluated and compared in CSV format (`final_metrics_summary_2025.csv`, `multiyear_model_comparison_2023_2025.csv`).

## Preprocessing
- Adding lags and rolling features for time-series forecasting.
- Creating target variables for the next day.
- Categorizing risk levels (`risk_category_next_day`).

## Visualization
- Time-series plots (`delhi_daily_pm25_2025.png`, `monthly_average_pm25_by_year_2023_2025.png`).
- Actual vs Predicted (`actual_vs_predicted_pm25_best_multiyear_model.png`).
- Distributions (`monthly_pm25_boxplot_2023_2025.png`).

## Limitations
- Relies on synthetic or extrapolated "2025" future data.
- Focused solely on data analysis and notebook forecasting, lacking a production deployment pipeline, APIs, or interactive dashboards.

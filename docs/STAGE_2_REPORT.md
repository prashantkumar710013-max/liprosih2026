# Stage 2 Completion Report

## 1. Features Created
- **Temporal**: `hour`, `day`, `month`, `day_of_week`, `day_of_year`, `week_of_year`, plus boolean indicators (`is_weekend`, `is_night`, `is_morning`, `is_evening`) and cyclical sine/cosine encodings.
- **Lags**: Strict historical lookbacks (1, 2, 3, 6, 12, 24 hours) for target pollutants (PM2.5, PM10, NO2).
- **Rolling Windows**: Rolling mean, standard deviation, minimum, and maximum across 6, 12, 24-hour windows. All rolling calculations strictly apply a `shift(1)` to explicitly prevent target leakage from the current timestamp.
- **Pollution Indicators**: Ratios (PM2.5/PM10, NO2/PM25) to capture source chemistry, and immediate growth rates to capture accumulation velocity.
- **Weather Features**: Wind vector components (`wind_u`, `wind_v`), basic dew point approximation, and precipitation intensity flags.
- **Coupled Weather-Pollution**: `wind_stagnation_index`, `humidity_pm25_interaction`, `ventilation_proxy`, `rain_scavenging_indicator`, `pressure_stability_proxy`. 

## 2. Number of Final Features
The feature extraction pipeline expands the raw data into over **60** engineered features.

## 3. Datasets Used
- **Project 2 (2023-2025)**: Hourly Air Quality (`delhi_air_quality_hourly_2023_2025.csv`) combined with daily weather (`delhi_weather_daily_2023_2025.csv`), forward-filled to hourly granularity.
- *Note: Traffic data was omitted because historical, granularly-aligned station-level traffic was not robust enough to couple safely without introducing systemic noise.*

## 4. Leakage Checks
- Added an automated `LeakageDetector` in `backend/app/features/leakage.py`.
- Verified that target features (e.g. current hour PM2.5) are not perfectly correlated with any input feature (other than the target itself, which is held out).
- Validated that rolling metrics mathematically exclude the current hour.

## 5. Baseline Feature Importance
A lightweight XGBoost baseline model was trained strictly for feature validation.
Key findings from feature importance:
- Recent PM2.5 lags (`pm25_lag1`, `pm25_lag2`) dominate the short-term signal.
- The `ventilation_proxy` and `wind_stagnation_index` show strong importance, proving that weather-pollution coupling provides distinct, useful signals above pure autoregression.
- Temporal encodings (especially `hour` and `sin_hour`) establish the strong diurnal baseline.

## 6. Test Results
- All unit tests for temporal, lags, rolling, pollution, weather, coupled features, and leakage detection passed.
- Output parquet file successfully materialized.

## 7. Limitations
- **Forward-Filled Weather**: Using daily weather forward-filled to hourly loses critical intra-day meteorological dynamics (e.g. afternoon heating vs nighttime cooling). A genuine hourly meteorology dataset is needed for production-grade forecasts.
- **Coupled Proxies are Heuristics**: The `ventilation_proxy` is mathematically helpful for trees but physically rudimentary.
- **Single Location Fallback**: The current pipeline aggregates Delhi to a single point ("Delhi_Avg") when station IDs are absent in the aggregated dataset. Spatial modeling requires maintaining station IDs.

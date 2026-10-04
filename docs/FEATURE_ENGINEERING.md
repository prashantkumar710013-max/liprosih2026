# Feature Engineering Documentation

## Overview
Stage 2 transforms raw cleaned time-series data into an advanced ML-ready dataset. The key innovation is moving beyond isolated pollutant autoregression by mathematically coupling meteorological conditions with pollution states.

## What Was Created
1. **Temporal Encoding**: Standard and cyclical time features to capture daily, weekly, and seasonal patterns.
2. **Strict Lags**: Direct historical lookbacks (1 to 24 hours).
3. **Rolling Aggregations**: Moving averages, std, min, and max using pandas grouped rolling windows. **Shifted by 1 hour** to guarantee zero future leakage.
4. **Pollution Ratios & Growth Rates**: Features that capture the dynamic chemical mixture of the air (e.g., fine vs coarse particulate matter).
5. **Coupled Weather-Pollution Features**: Mathematical proxies bridging meteorology and atmospheric chemistry.

## Why It Was Created
Standard time-series models (like ARIMA) often fail on AQI because pollution is heavily dictated by immediate weather changes (e.g., a sudden drop in wind speed causing rapid PM2.5 accumulation). By providing explicitly coupled features (like `ventilation_proxy` and `humidity_pm25_interaction`), we give tree-based and deep learning models a direct signal of atmospheric stability and dispersion capacity.

## Datasets Used
Features are generated from the normalized output of Stage 1 (e.g., `delhi_air_quality_hourly_2023_2025.csv` and `delhi_weather_daily_2023_2025.csv`). 

## Proxies Used
Since high-end physical measurements (like exact Planetary Boundary Layer Height) are unavailable in the standard dataset, we constructed proxies:
- **Ventilation Proxy**: `wind_speed * max(temperature, 0.1)`. Heat causes air to rise, wind causes it to move horizontally.
- **Wind Stagnation**: `1 / (wind_speed + 0.1)`. Highly correlated with winter pollution spikes in Delhi.
- **Rain Scavenging**: Models the washout effect when rain physically removes PM2.5 from the air.

## Limitations
- **Daily Weather vs Hourly AQ**: Currently, if weather data is daily, we forward-fill to hourly, which flattens intra-day weather variations (e.g., afternoon wind vs night wind). A truly hourly weather dataset is needed for maximum accuracy.
- **Traffic Excluded**: Reliable, continuous, historically aligned traffic data at the station level was insufficient. Forcing it into the model would reduce data quality.
- **Proxy Inaccuracy**: A temperature-based ventilation proxy is a severe oversimplification of complex atmospheric thermodynamics, but is empirically useful for XGBoost/Random Forest.

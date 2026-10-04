# Feature Dictionary

This document describes the features engineered for AeroSense Delhi forecasting.

## Temporal Features
- `hour`: Hour of the day (0-23)
- `day`: Day of the month
- `day_of_week`: Day of the week (0=Monday, 6=Sunday)
- `month`: Month of the year
- `day_of_year`: Day of the year
- `week_of_year`: ISO calendar week
- `is_weekend`: 1 if Saturday/Sunday, else 0
- `is_night`: 1 if hour >= 22 or <= 5
- `is_morning`: 1 if hour between 6 and 11
- `is_evening`: 1 if hour between 17 and 21
- `sin_hour`, `cos_hour`: Cyclical encoding of hour
- `sin_day`, `cos_day`: Cyclical encoding of day
- `sin_month`, `cos_month`: Cyclical encoding of month

## Lag Features
- `[pollutant]_lag[H]`: Pollutant value `H` hours prior to the current timestamp. Generated for 1, 2, 3, 6, 12, 24 hours. Prevents target leakage by enforcing strict lookback.

## Rolling Features
- `[pollutant]_[W]h_mean`: Rolling average over the past `W` hours (3, 6, 12, 24). Shifted by 1 hour to prevent target leakage.
- `[pollutant]_[W]h_std`: Rolling standard deviation.
- `[pollutant]_[W]h_min`: Rolling minimum.
- `[pollutant]_[W]h_max`: Rolling maximum.

## Pollution Features
- `[pollutant]_growth_rate`: (current - previous) / previous. Measures rapid accumulation.
- `pm25_pm10_ratio`: Ratio of fine to coarse particles.
- `no2_pm25_ratio`: Ratio indicating vehicular vs other combustion sources.
- `so2_pm25_ratio`: Ratio indicating industrial vs other sources.
- `co_no2_ratio`: Combustion efficiency proxy.

## Weather Features
- `dew_point_approx`: Estimated dew point from Temperature and Humidity.
- `wind_u`, `wind_v`: Vector components of wind direction and speed.
- `is_raining`: Boolean proxy (1 if precip > 0).
- `heavy_rain`: Boolean proxy (1 if precip > 10mm).

## Coupled Weather-Pollution Features (Proxies)
*Note: These are derived mathematical proxies for ML, not physical measurements.*
- `wind_stagnation_index`: Inverse of wind speed; higher when wind is calm.
- `humidity_pm25_interaction`: Product of RH and PM2.5 (smog proxy).
- `temperature_pm25_interaction`: Product of Temp and PM2.5.
- `ventilation_proxy`: Product of wind speed and positive temperature (rough proxy for boundary layer mixing).
- `rain_scavenging_indicator`: Product of precipitation and PM2.5 (models rain washing out pollution).
- `pressure_stability_proxy`: Inverse of wind and temp interaction.

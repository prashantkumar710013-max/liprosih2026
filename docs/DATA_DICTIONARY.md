# Data Dictionary

## Source Project 1: Air-Pollutant-Prediction-Delhi-main

### AQI Time-Series Training Dataset (`aqi_ts_train.csv`)
| Dataset | Source | Time range | Frequency | Station | Columns | Units if known | Missing data | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `aqi_ts_train.csv` | Project 1 | 2017-11 to 2021-11 | Daily / Hourly | Punjabi Bagh & Anand Vihar | `timestamp`, `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, `Temperature_in_AC`, `Wind_Speed_in_Kmph`, `Rel_Humidity`, `Dew_Point_in_AC`, `Atmospheric_Pressure_in_mb` | Temp (C), Wind (Kmph), Pressure (mb) | Imputed | Train time-series models |

### Weather Cross-Section Training Dataset (`X_PM2.5_Train.csv`)
| Dataset | Source | Time range | Frequency | Station | Columns | Units if known | Missing data | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `X_PM2.5_Train.csv` | Project 1 | 2017-11 to 2021-11 | Cross-section | Delhi | `Temperature_in_AC`, `Wind_Speed_in_Kmph`, `Rel_Humidity`, `Dew_Point_in_AC`, `Atmospheric_Pressure_in_mb`, `Thunder`, `Few_clouds`, `Rain`, `Clear`, `Cloudy` | Temp (C), Wind (Kmph), Pressure (mb) | Imputed | Train cross-sectional PM2.5 model |

## Source Project 2: delhi-air-quality-analysis-main

### Processed Multiyear Model Data (`delhi_pm25_multiyear_model_data_2023_2025.csv`)
| Dataset | Source | Time range | Frequency | Station | Columns | Units if known | Missing data | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `delhi_pm25_multiyear_model_data_2023_2025.csv` | Project 2 | 2023-01 to 2025-12 | Daily | Delhi | `date`, `pm2_5`, `pm10`, `nitrogen_dioxide`, `sulphur_dioxide`, `ozone`, `us_aqi`, `T2M`, `RH2M`, `WS10M`, `PRECTOTCORR`, `target_pm2_5_next_day`, `pm2_5_lag1`, `pm2_5_lag2`, `pm2_5_lag3`, `pm2_5_roll3`, `month`, `day_of_year` | Unknown | Imputed | Train models to predict next day PM2.5 |

### Processed Risk Model Data (`delhi_pm25_model_data_with_risk_2025.csv`)
| Dataset | Source | Time range | Frequency | Station | Columns | Units if known | Missing data | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `delhi_pm25_model_data_with_risk_2025.csv` | Project 2 | 2025 | Daily | Delhi | `date`, `pm2_5`, `pm10`, `nitrogen_dioxide`, `sulphur_dioxide`, `ozone`, `us_aqi`, `T2M`, `RH2M`, `WS10M`, `PRECTOTCORR`, `target_pm2_5_next_day`, `risk_category_next_day` | Unknown | Imputed | Train classification models for next day PM2.5 risk |

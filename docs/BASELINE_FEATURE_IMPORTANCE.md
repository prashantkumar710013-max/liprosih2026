# Baseline Feature Importance

This is a lightweight XGBoost model predicting PM2.5 at T+1, purely for validating feature signals.

| Feature                      |   Importance |
|:-----------------------------|-------------:|
| pm25                         |   0.831039   |
| pm25_growth_rate             |   0.0114865  |
| pm25_24h_mean                |   0.0110533  |
| pm10_growth_rate             |   0.00970346 |
| pressure_stability_proxy     |   0.0074152  |
| no2_growth_rate              |   0.00681482 |
| sin_hour                     |   0.00639691 |
| ventilation_proxy            |   0.00630741 |
| temperature_24h_min          |   0.00546272 |
| is_morning                   |   0.00466647 |
| temperature_12h_max          |   0.00457306 |
| cos_month                    |   0.00449429 |
| cos_hour                     |   0.00448776 |
| temperature_6h_max           |   0.00422427 |
| dew_point_approx             |   0.00411714 |
| temperature                  |   0.00354948 |
| pm25_24h_min                 |   0.00322926 |
| pm25_lag6                    |   0.00319592 |
| pm25_12h_min                 |   0.00306109 |
| hour                         |   0.00271571 |
| pm10_lag24                   |   0.00260429 |
| pm25_6h_max                  |   0.00250363 |
| temperature_12h_mean         |   0.00216692 |
| pm25_24h_std                 |   0.00207817 |
| temperature_pm25_interaction |   0.00200697 |
| so2                          |   0.00186021 |
| pm25_pm10_ratio              |   0.00184924 |
| no2_lag2                     |   0.00183447 |
| pm25_12h_max                 |   0.00179274 |
| no2                          |   0.00159006 |
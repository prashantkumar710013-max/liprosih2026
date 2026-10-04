# AeroSense Delhi - Final Project Status

**Status:** COMPLETE / PRODUCTION-READY PROTOTYPE

## Features Implemented
- **Data Foundation:** Robust ETL pipeline with column normalization, anomaly detection, and schema validation.
- **Advanced Feature Engineering:** Lagged metrics, rolling windows, cyclical temporal mapping, and most critically, coupled weather-pollution stagnation features.
- **72-Hour Forecasting:** A MultiOutputRegressor (XGBoost) predicting the continuous 72-hour sequence with empirical uncertainty bounds.
- **Atmospheric Intelligence:** Model-derived Trapping Index and Inversion Proxy replacing missing vertical profile datasets.
- **Event Detection & Early Warning:** Dynamic anomaly scanning generating severity-based alerts.
- **Spatial Intelligence:** Interpolated estimation fields and rule-based hotspot rings displayed on an interactive map.
- **Scenario Lab & Plume Tracking:** Counterfactual weather testing and lightweight biomass advection/dispersion simulation.
- **Explainable AI:** SHAP integration natively explaining the exact numerical drivers behind every forecast.

## Models
- Baseline: Persistence, Random Forest
- Primary Engine: `aerosense_xgb.joblib` (XGBoost MultiOutputRegressor)

## Architecture
- **Backend:** FastAPI (Python), SQLite (Metadata), Parquet (Data vectors).
- **Frontend:** React, TypeScript, Vite, Tailwind v4, Recharts, React-Leaflet.

## Tests
Fully verified via `pytest`. Zero leakage. All simulated thresholds rigorously asserted.

## Known Limitations
1. Daily weather data was forward-filled to hourly.
2. Spatial interpolation utilizes mathematical smoothing between stations, skipping micro-terrain influences.
3. Traffic proxy data was ultimately excluded due to misalignment with existing datasets.
4. The biomass plume model is a localized Gaussian/Haversine approximation for UI speed, not an operational WRF-Chem chemical transport model.

## Future Work
- Integration of actual satellite AOD (Aerosol Optical Depth) data.
- Live streaming API webhooks from CPCB/DPCC sensors.
- Deployment to cloud architecture (GCP/AWS).

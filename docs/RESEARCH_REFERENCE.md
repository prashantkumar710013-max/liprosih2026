# Research Reference

## Summary of Scientific Reports Paper (Jena et al., 2021)
The paper details the implementation of a 400m high-resolution operational air quality forecasting system for Delhi/NCR, capable of issuing 72-hour predictions for PM2.5 and AQI. It highlights the use of dynamical downscaling and chemical data assimilation to accurately capture neighborhood-level pollution episodes, particularly during extreme winter conditions exacerbated by biomass burning and stable meteorology.

## WHAT THE PAPER ACTUALLY IMPLEMENTS
- **WRF-Chem**: Uses the Weather Research and Forecasting model coupled with Chemistry (WRF-Chem) for dynamical downscaling (10km -> 2km -> 400m).
- **Data Assimilation (3D-VAR)**: Assimilates near real-time MODIS Aerosol Optical Depth (AOD) and in-situ surface PM2.5 observations via GSI, improving initial PM2.5 conditions by ~50%.
- **High-Resolution Emissions**: Uses a custom 400m High-resolution Delhi Emission Inventory (HrDEI) integrated with EDGAR-HTAP (anthropogenic), MEGAN (biogenic), and FINN (fire/biomass burning).
- **Physical/Chemical Processes**: Explicitly models boundary layer physics, synoptic advection, aerosol hygroscopic growth, and chemical transport using MOZART-4 (gas-phase) and GOCART (aerosols).
- **Performance Evaluation**: Demonstrates high skill for 72-h PM2.5 and AQI forecasting, particularly for "unhealthy" and "very unhealthy" risk categories.

## WHAT AEROSENSE WILL IMPLEMENT
*(To be aligned with our student prototype constraints)*
- **Data-Driven Machine Learning**: AeroSense will use pure machine learning/deep learning (e.g., Transformers, XGBoost) rather than computationally expensive numerical weather/chemistry models (WRF-Chem).
- **Tabular Forecasting**: We will predict PM2.5 at specific station coordinates or aggregated levels using tabular historical data (AQI, weather variables) rather than full 3D spatial grids.
- **Feature Engineering over Physics**: Instead of modeling physical atmospheric processes and emission inventories, AeroSense will rely on temporal features (lags, rolling averages) and localized weather variables (Temperature, Humidity, Wind).
- **Next-Day / Multi-Day Forecasting**: We will implement 24-h to 72-h forecasts by predicting future target variables based on past sequential inputs, without assimilating real-time satellite AOD retrievals.
- **Conceptual Borrowing**: AeroSense will borrow the concept of integrating meteorological data with pollution data and predicting categorical health risks/AQI, but achieved entirely through ML.

**Note**: AeroSense is a student prototype and is **not** equivalent to the operational, supercomputer-driven WRF-Chem chemical transport system described in the paper.

# Atmospheric Intelligence

The Atmospheric Intelligence module translates raw forecasting metrics into explainable atmospheric mechanisms. It bridges the gap between purely statistical ML predictions and physical meteorology.

## Key Subsystems
1. **Atmospheric Trapping Score:** A normalized proxy (0-100) estimating the likelihood of pollutants remaining stagnant at the surface due to low boundary layers, thermal inversions, and low wind speeds.
2. **Ventilation / Dispersion Index:** An indicator showing whether current conditions favor dispersion (high wind, thermal mixing) or stagnation.
3. **Pollution Event Engine:** Automatically detects conditions such as "rapid PM2.5 increase" or "stagnation-associated buildup".
4. **Rapid Transport Approximation:** A lightweight advection vector model estimating regional plume transport.
5. **Scenario Engine:** "What-if" simulations showing how the forecast changes under hypothetical meteorology or emissions.
6. **Explainability Engine:** A SHAP-based explainer connecting the XGBoost outputs to specific physical drivers.

All outputs dynamically respect the `LIVE_DATA_MAX_AGE_MINUTES` gate. If upstream telemetry is stale, these systems gracefully downgrade to `HISTORICAL_FALLBACK` status.

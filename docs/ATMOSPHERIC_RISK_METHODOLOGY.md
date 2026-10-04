# Atmospheric Risk Methodology

## Overview
AeroSense computes atmospheric risk via two main indicators: the Atmospheric Trapping Score and the Ventilation/Dispersion Index. Since direct planetary boundary layer (PBL) height measurements are not continuously available in the current dataset, these metrics serve as **PROXIES** derived from surface-level meteorology.

## 1. Atmospheric Trapping Score (0-100)
- **Inputs:** Wind speed, temperature, relative humidity, precipitation.
- **Calculation:**
  - **Wind Speed (Max 40 pts):** Highly stagnant air (<1 m/s) drives the highest trapping penalty.
  - **Temperature (Max 30 pts):** Cold air (<10°C) serves as an inversion proxy.
  - **Humidity (Max 20 pts):** High humidity (>80%) accelerates secondary aerosol formation and smog.
  - **Precipitation (Max -30 pts):** Rain acts as a scavenging agent, reducing the trapping score.
- **Normalization:** Score is rigidly clipped to the [0, 100] interval.
- **Assumptions:** Cold, stagnant, humid air is strongly correlated with wintertime pollution trapping in Delhi.
- **Provenance:** `PROXY` (or `HISTORICAL_FALLBACK` if upstream data is stale).

## 2. Ventilation / Dispersion Index
- **Inputs:** Wind speed, temperature.
- **Calculation:** `Wind Speed * (Temperature Factor) * 10`
- **Interpretation:** Distinguishes between `stagnant conditions`, `moderate ventilation`, and `stronger ventilation`.
- **Limitations:** Does not account for vertical wind shear or precise thermal lapse rates.

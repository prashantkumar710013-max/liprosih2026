# Scenario Methodology

## Overview
The `ScenarioLab` engine allows operators to isolate specific environmental variables and observe their direct impact on the XGBoost ML forecast without overwriting actual baseline data.

## Predefined Scenarios
- **LOW_WIND:** Stagnant atmospheric conditions (wind_speed -2.0).
- **HIGH_ATMOSPHERIC_TRAPPING:** Cooler temp, higher humidity, low wind.
- **REGIONAL_POLLUTION_INFLOW:** External advection event (PM2.5 +100).
- **RAIN_SCAVENGING:** Wet deposition (Precip +10, PM2.5 -50).
- **BIOMASS_BURNING_SCENARIO:** Massive regional transport injection.

## Provenance
All scenario outputs are explicitly tagged with `status: SCENARIO`. They represent hypothetical branching futures, not observed predictions.

## Biomass Support Note
Actual satellite-derived fire detections (e.g. VIIRS/MODIS) are not currently integrated. Attempting to fetch live fires from `/api/biomass-fires` will safely return `BIOMASS_BURNING_DATA_UNAVAILABLE`. The scenario engine, however, provides a sandbox to simulate the *effects* of such an event if one were to occur.

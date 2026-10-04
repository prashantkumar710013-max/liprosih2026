# Stage 5 Completion Report

## 1. Rapid Pollution Transport Model
Implemented in `backend/app/simulation/transport.py`.
Provides a lightweight advection and dispersion approximation for tracking pollutant plumes.
**Mathematical Assumptions & Limitations:**
- Uses a simplified 2D flat-Earth Haversine approximation tuned for regional distances (1 degree lat = 111km, 1 degree lon scaled by cosine of latitude).
- Dispersion spreads linearly based on a constant dispersion factor (assuming a steady-state Gaussian-like cone).
- This is an empirical fast-approximation for UI visualization and API speed, **NOT** a full chemical transport model like WRF-Chem. It ignores terrain topology, chemical transformation during transit, and complex planetary boundary layer physics.

## 2. Biomass-Burning Scenario
Implemented in `backend/app/simulation/biomass.py`.
Allows simulating the transport of smoke from agricultural fires in specific regions (e.g., Punjab, Haryana). 
**Important Note:** The engine explicitly flags its output as a `SIMULATED BIOMASS-BURNING SCENARIO` to ensure these forward projections are never mistaken for real-time satellite fire detections.

## 3. Scenario Lab & What-If Engine
Implemented in `backend/app/simulation/scenario_lab.py`.
Allows dynamically mutating the baseline atmospheric state (e.g., cutting wind speed by 2 m/s, adding 50 µg/m³ of PM2.5, introducing rain) and recalculating the resulting forecast.
**Methodology:**
- **Predefined Scenarios:** (e.g., `LOW_WIND`, `HIGH_TRAPPING`, `RAIN_SCAVENGING`) automatically apply curated deltas to the environmental state.
- **What-If Engine:** Allows arbitrary JSON modification of variables (temp, humidity, wind, pollutants). It actively prevents impossible physical values (e.g., negative wind speeds, negative precipitation, >100% humidity via pandas `.clip()`). 
- Features heavily coupled to mutated variables (like `wind_stagnation_index` and `ventilation_proxy`) are automatically recalculated before the mutated state is passed into the Stage 3 forecasting model.

## 4. API Endpoints
Integrated three `POST` endpoints to power the Scenario Lab UI:
- `POST /api/plume-simulation`: Generates the GeoJSON centerline, bounds, and impact gradient.
- `POST /api/scenario`: Overwrites current state with predefined conditions and generates a new forecast.
- `POST /api/what-if`: Accepts arbitrary variable modifications and generates a new forecast.

## 5. Visualizations
The transport engine emits compliant `GeoJSON` FeatureCollections containing LineStrings (centerline) and point properties (radius/impacts) that can be seamlessly rendered by frontend mapping libraries like Mapbox or Leaflet.

## 6. Testing
`tests/test_simulation.py` confirms trajectory math (e.g., ensuring wind blowing *from* 270° West forces the plume to travel East), validates payload formats, checks boundary clipping, and verifies error handling for invalid physical inputs.

*(End of Stage 5)*

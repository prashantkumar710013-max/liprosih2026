# Live Feature Pipeline

AeroSense Delhi implements a robust integration pipeline to safely stitch live telemetry from OpenAQ into its historical baseline, generating dynamic 72-hour forecasts without overwriting or polluting historical training datasets.

## Pipeline Architecture

Historical data
       ↓
Validated live observations
       ↓
Temporal alignment
       ↓
Freshness gate
       ↓
Feature engineering
       ↓
Existing predictor
       ↓
72-hour forecast

## Freshness Gate & Stale-Data Behavior
The system strictly enforces a freshness threshold (`LIVE_DATA_MAX_AGE_MINUTES=120`).
- **LIVE_DATA_VALID:** Real-time observations are safely merged, and the model returns `mode=LIVE_DATA`.
- **LIVE_DATA_STALE:** If the external telemetry is outdated (as is the case with current stored OpenAQ observations from 2025), the system triggers a **Safe Fallback**.
- **HISTORICAL_FALLBACK:** The API gracefully downgrades to pure historical inference, returning `mode=HISTORICAL_FALLBACK` and `status=LIVE_DATA_STALE`, explicitly preventing stale data from masquerading as fresh observations.

## Future-Data Leakage Prevention
During the Temporal Alignment phase, the `LiveFeatureBuilder` strictly iterates over observed SQLite records and drops any record where `timestamp > current_utc_time`. This guarantees that future predictions cannot accidentally access simulated future measurements, maintaining an absolute `T=0` boundary.

## Unit Handling & Missing Data
- Units are verified and standardized during ingestion (`µg/m³`).
- Missing measurements are intelligently forward-filled (limit=6 hours) matching the established scientific criteria of the baseline feature engineering. Missing historical stations trigger `LIVE_DATA_UNAVAILABLE`.

## Provenance
All historical and live outputs emitted by `/api/forecast/live` enforce strict provenance metadata arrays mapping `status = MODEL_FORECAST` across the entire prediction horizon.

## Permanent Source Status (OpenAQ)
A comprehensive bounding-box audit of the OpenAQ API v3 endpoints was conducted (122 sensors checked across 84 Delhi NCR locations):
- The newest absolute measurement found across the entire network was April 2026 (at Ved Vihar-Loni, Ghaziabad).
- Our target core stations (Anand Vihar, Punjabi Bagh, and R K Puram) remain halted at February 2025 updates in the upstream API.
- Therefore, OpenAQ is currently classified as an external historical/stale source rather than a real-time Delhi observation source.
- AeroSense must never represent these observations as current.
- The 120-minute freshness gate must remain strictly enforced, ensuring that OpenAQ data defaults gracefully to the HISTORICAL_FALLBACK protocol.

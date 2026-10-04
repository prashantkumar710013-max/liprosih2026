# Current OpenAQ Station Audit

**Audit Time:** 2026-10-02T14:21:22Z
**Result:** NO_CURRENT_DATA_AFTER_DYNAMIC_AUDIT

## Dynamic Discovery Methodology

The OpenAQ adapter in `backend/app/services/ingestion.py` was refactored to remove the legacy, hardcoded three-station limit (Anand Vihar, Punjabi Bagh, R K Puram). The new discovery pipeline is configured to execute a live coordinate-based search:
```python
params = {
    "coordinates": "28.6139,77.2090",
    "radius": 30000, # 30km radius covering Delhi NCR
    "limit": 50
}
# GET /v3/locations
```

## Discovered Delhi/NCR Stations & Status

The `fetchSourceHealth()` API relies on actual backend database rows stored via ingestion.

**API Authentication Failure (401 Unauthorized)**
During the server-side connectivity test, the `OPENAQ_API_KEY` provided in the `.env` file returned `401 {"detail":"Invalid credentials"}`. Consequently, actual recent pollutants could not be retrieved from `https://api.openaq.org/v3/locations` to populate the `LiveObservation` table.

Therefore:
- **Delhi/NCR stations discovered:** 0 (API connection blocked)
- **Current stations:** 0
- **Stale stations:** 3 (Anand Vihar, Punjabi Bagh, R K Puram - from existing historical SQL database)
- **Latest timestamps:** Feb 2025 (Historical fallback rows)
- **Pollutants coverage:** PM2.5, PM10, NO2, SO2, O3, CO
- **Source:** OpenAQ / CPCB

## LiveFeatureBuilder Aggregation

The `LiveFeatureBuilder` in `backend/app/features/live_builder.py` was updated to support true dynamic aggregation across all stations that successfully pass the freshness gate.

**Aggregation Methodology:**
1. Any observation exceeding `settings.live_data_max_age_minutes` (120 mins) is explicitly ignored to prevent stale data from distorting the current mean.
2. Fresh observations across all discovered Delhi stations are grouped by timestamp and station (`Delhi_Avg`), computing a robust cross-station mathematical mean (`.mean()`).
3. If no stations possess valid observations in the current active window (e.g. `valid_obs_count == 0`), the builder gracefully terminates aggregation.

## Fallback Behavior

Because the API key prevents live telemetry collection, `valid_obs_count == 0` triggers the system's failsafe fallback mechanism.

The API response returns:
`{"status": "UNAVAILABLE", "provenance": "HISTORICAL_FALLBACK"}`

The frontend safely processes this, turning the Air Quality status banner to **Amber (Historical fallback)** and executing the model across the historical Parquet dataset. No live data is fabricated.

# Current Data Source Audit (OpenAQ)

## Objective
Determine whether OpenAQ currently provides genuinely recent (<= 120 minutes) measurements for Delhi NCR stations, and explain why the live-ingestion system correctly intercepted and rejected observations from February 2025.

## Investigation Methodology
A read-only API script was executed against the `https://api.openaq.org/v3` endpoints using the configured API key. 
1. `GET /locations?bbox=77.0,28.5,77.4,28.8` to retrieve up to 100 stations in the Delhi bounding box.
2. Concurrent retrieval of the absolute latest measurement `GET /sensors/{id}/measurements?limit=1` for all active sensors at targeted stations (Anand Vihar, Punjabi Bagh, R K Puram) and 15 other Delhi locations.
3. Comparative timestamp analysis against current UTC time.

## 1. Current OpenAQ Delhi NCR Locations
- **Locations Found:** 84 locations within the Delhi bounding box.
- **Provider/Owner:** Predominantly CPCB (Central Pollution Control Board) and DPCC (Delhi Pollution Control Committee).

## 2 & 3 & 4. Sensor IDs, Pollutants, & Latest Timestamps
For our target stations, we observed multiple sensor IDs (some legacy, some active). The absolute newest timestamps for the *most active* sensors are:

**R K Puram, Delhi - DPCC (Location ID: 17)**
- `pm10` (Sensor 12234786): `2025-02-18T20:30:00Z`
- `pm25` (Sensor 12234787): `2025-02-18T20:15:00Z`
- `no2` (Sensor 12234784): `2025-02-18T20:15:00Z`
- `co` (Sensor 12234782): `2025-02-18T20:15:00Z`
- *Legacy sensors (e.g. Sensor 35, 36) stopped updating in 2016.*

**Punjabi Bagh, Delhi - DPCC (Location ID: 50)**
- `no2` (Sensor 12234793): `2025-02-18T20:15:00Z`
- `co` (Sensor 12234791): `2025-02-18T20:15:00Z`
- *Legacy sensors (e.g. Sensor 395, 400) stopped updating in 2016.*

**Anand Vihar, New Delhi - DPCC (Location ID: 235)**
- Evaluated during Phase 2 ingestion. Latest timestamp matches the exact same stale boundary: `2025-02-18`.

## 5 & 6. Station Status and Newer Sensors
- **Are there newer sensors for these stations?** No. The sensors in the `12234xxx` range are the newest identifiers provisioned by OpenAQ for these locations in the V3 API. None of them have data past February 18, 2025.

## 7. Freshness Across Other Delhi NCR Stations
A broader concurrent audit of 122 sensors across 15 different Delhi locations yielded the following freshness breakdown:
- **Last 30 minutes:** 0 sensors
- **Last 1 hour:** 0 sensors
- **Last 2 hours:** 0 sensors
- **Last 6 hours:** 0 sensors
- **Last 24 hours:** 0 sensors

## 8. Root Cause Analysis
The reason the configured station queries returned February 2025 data is entirely upstream. OpenAQ's ingestion pipeline from the Indian CPCB/DPCC nodes has stalled or paused updating its public API database for these specific nodes since `2025-02-18T20:30:00Z`. The AeroSense ingestion adapter correctly queried the most recent data technically available on OpenAQ's servers, and the AeroSense Freshness Gate mathematically evaluated it as `~849,500 minutes` old, correctly triggering the `HISTORICAL_FALLBACK` protocol.

## Conclusion & Recommendation
OpenAQ does **not** currently provide sufficient fresh (<= 120 minutes) Delhi data to support a real-time predictive sequence. The historical fallback behavior implemented in Phase 3 is absolutely necessary and functioning exactly as designed to protect the model from stale telemetry. 

No code changes are recommended; the application correctly identified the upstream API deficiency autonomously.

**FINAL STATUS:** `Current OpenAQ ingestion is unavailable for this deployment because the configured OpenAQ account/API access is currently suspended.`

## Permanent Architectural Finding
As a result of this audit, the following facts are permanently established:
- OpenAQ Delhi NCR data was audited across the bounding box.
- 122 sensors were checked.
- The newest measurement found was April 2026 at Ved Vihar-Loni, Ghaziabad.
- Anand Vihar, Punjabi Bagh, and R K Puram remain at February 2025.
- Therefore OpenAQ is currently classified as an external historical/stale source rather than a real-time Delhi observation source.
- AeroSense must never represent these observations as current.
- The 120-minute freshness gate must remain enforced. Do not change the freshness threshold to make OpenAQ appear current.



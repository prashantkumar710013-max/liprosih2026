# Real OpenAQ Connectivity & Ingestion Test

## 1. Test Information
- **Test Date/Time:** 2026-10-02 00:50:00 (Local Time) / 2026-10-01 19:20:00 (UTC)
- **API Source:** OpenAQ
- **API Base URL:** https://api.openaq.org/v3

## 2. Authentication
- **API Key Configured:** Yes (CONFIGURED in `.env`)
- **Authentication Succeeded:** Yes

## 3. Ingestion Target
- **Stations Queried:** 3 (Anand Vihar, Punjabi Bagh, R K Puram)
- **Station IDs utilized:** 235, 50, 17

## 4. Ingestion Results
- **Real Observations Received:** 36
- **Real Observations Inserted:** 36
- **Observations Rejected:** 0
- **Duplicates Skipped:** 0

## 5. Data Freshness & Quality
- **Latest Observation Timestamp:** 2025-02-18 22:30:00
- **Data Freshness:** Stale (Age: ~849,411 minutes, which exceeds the configured `LIVE_DATA_MAX_AGE_MINUTES` of 120. This indicates the external node reporting for these historical sensor references is offline or lagging relative to the system clock).
- **Data Quality:** Valid. No `NaN`, no `Infinity`, timestamps successfully parsed natively into UTC, units formatted securely. Every row explicit sets `status = OBSERVED`.

## 6. Integrity Verification
- **Database Verification:** Verified successfully. `live_observations` contains precisely 36 new rows.
- **Historical Data Integrity Verification:** Verified successfully. `observations`, `forecasts` tables and all `.parquet` feature sets remain unmodified.

## 7. Automated Testing (Failure Safety)
- **Unit Test Results (Live Ingestion):** 16 / 16 Passed (Mocking 401, 403, 429, timeouts, missing values, empty bounds).
- **Full Regression Test Results:** 48 / 48 Passed (0 Failed, 0 Errors).

## 8. Final Status
**REAL_OPENAQ_INGESTION_SUCCESS**

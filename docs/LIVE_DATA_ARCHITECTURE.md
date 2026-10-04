# Live Data Architecture

AeroSense Delhi now supports live programmatic data ingestion to overlay real-time observations onto its historical baseline.

## 1. Database Layer
Two new dedicated tables were created:
- `LiveObservation`: Stores OpenAQ air quality measurements.
- `LiveWeather`: Stores Open-Meteo meteorological data.

These tables use strict provenance (setting `status="OBSERVED"`) and maintain independent indexes, avoiding any schema corruption or overwriting of the core historical `observations` table.

## 2. Ingestion Services
The `backend/app/services/ingestion.py` module defines resilient HTTP adapters (`OpenAQAdapter`, `OpenMeteoAdapter`).
Key features:
- **Resilience:** Gracefully handles JSONDecodeErrors, timeouts, and missing parameters.
- **Deduplication:** Uses unique constraints on `source_measurement_id` (or deterministic temporal hashes) to prevent duplicate rows.
- **Validation:** Skips entries with NaN/Infinity or missing geolocation coordinates rather than fabricating mock values.



## Current OpenAQ Status
OpenAQ integration is implemented, but the currently configured OpenAQ account is suspended and therefore current external air-quality observations cannot presently be retrieved through that account. The platform actively relies on validated historical fallback.

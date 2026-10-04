# Forecast Rendering Fix & Runtime Verification

## 1. Problem Diagnosis
The user reported that the `Forecast` page loaded correctly (including X-axis horizons, headers, and mode banners), but the actual 72-hour `Recharts` graph was entirely blank. Additionally, the user requested an investigation into an apparent timestamp mismatch between "Latest observation" and "Forecast Origin".

## 2. Trace and Root Cause Analysis
- **API Endpoint:** `GET /api/forecast/live?station=Delhi_Avg&hours=72`
- **Backend Response Structure:**
  The FastAPI endpoint successfully processes inference from the `AeroSensePredictor-XGB` model and returns a list of dictionaries in `forecasts`.
  Example point:
  ```json
  {
      "timestamp": "2026-01-03T23:00:00",
      "horizon": 72,
      "prediction": 165.57,
      "lower_bound": 56.79,
      "upper_bound": 274.35,
      ...
  }
  ```
- **Root Cause:**
  The frontend `Forecast.tsx` Recharts configuration was configured to map the Y-axis to `dataKey="pm25"`. However, the API schema actually outputs the forecast value under the key `"prediction"`. The chart successfully rendered the layout but silently failed to draw the line because `pm25` evaluated to `undefined` for all 72 data points. 

## 3. Timestamp Consistency Explanation
The UI previously rendered:
- `Last observation: 18/02/25`
- `Forecast Origin: 31/12/2025`

**Is this a bug?** No, this is mathematically correct for `HISTORICAL_FALLBACK` mode.
- The `18/02/25` timestamp is provided by OpenAQ via `/api/source-health` as the literal last available pulse from a physical Delhi NCR sensor.
- The `31/12/2025` timestamp is the actual temporal origin of the historical parquet block (`aerosense_features.parquet`) injected into the model for inference when live data is stale. 
- *Fix Implemented:* Instead of manipulating these accurate timestamps, I updated the microcopy to clarify the context. The UI now dynamically renders `Historical Forecast Origin: [Date]` and `Last external observation: [Date]` depending on whether the system is in fallback mode.

## 4. Fixes Implemented
- **Frontend Mapping:** Updated `Forecast.tsx` Recharts component: `<Area dataKey="prediction" ... />`. 
- **Empty State Fallback:** Updated the Promise resolution block to strictly test for `.length === 0` and explicitly trigger the API error state: `"No forecast points returned."` instead of rendering a blank canvas.
- **Horizon Filtering:** Verified that changing the selector (12h, 24h, 48h, 72h) natively triggers the endpoint to dynamically slice the inference array.
- **Microcopy Revisions:** Adjusted the global header in `App.tsx` and the local banner in `Forecast.tsx` to differentiate between the ML forecast origin and the physical telemetry origin.

## 5. Testing and Validation
- **Automated Regression (`tests/test_api.py`)**: Added `test_forecast_live_valid_predictions` to programmatically assert that the output schema guarantees exactly `len() == 72` with valid `prediction` properties.
- `pytest tests/` - **PASS** (4 passing api tests, 78 total passing).
- `npm run build` - **PASS** (0 chunking/TypeScript errors).
- **Browser Output**: The 72-hour `pm25` trajectory successfully renders with gradients, tooltips, and correct numeric values.

**FINAL STATUS:** `FORECAST_RENDERING_FIXED`

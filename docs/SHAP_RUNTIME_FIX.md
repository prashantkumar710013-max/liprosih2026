# SHAP Explainer Runtime Fix

## 1. Problem Diagnosis
The user reported that the `Technical Mode` page displayed a generic `"SHAP Explainer connection failed."` message. The requirement was to track the exact failure point, restore full functionality, verify the `Event Detection` empty state string generation, and handle provenance labeling.

## 2. Trace and Root Cause Analysis
- **API Endpoint Involved**: `GET /api/forecast/explanation?station=Delhi_Avg`
- **Error Status**: `500 Internal Server Error`
- **Exception Caught in Logs**: `Model not found at E:\...\models\aerosense_xgb.joblib`
- **Root Cause**: The `get_explanation` endpoint route in `backend/app/main.py` was directly instantiating a new `ModelExplainer(model_dir)` rather than using the singleton global loader `get_explainer()`. Worse, it provided the base `models` directory path instead of `models/aerosense`, causing the `explainer.py` to target a non-existent path. Thus, the model failed to load, triggering the 500 error which rippled down to the UI.

## 3. Fix Details
- **Backend Model Initialization**: Modified `/api/forecast/explanation` to utilize the existing lazy-loading `get_explainer()` method. This not only provided the correct sub-directory path (`models/aerosense`) but also ensured `shap.TreeExplainer` is only initialized once in memory, drastically improving latency.
- **Frontend Error State Modification**: Removed the hardcoded `"SHAP Explainer connection failed."` string. Updated `ExplainableAI.tsx` to conditionally capture `err.response?.data?.detail` and display a localized, informative error component that gracefully explains exactly why explainability is unavailable if something breaks in the future.
- **Feature Extraction & Fallback**: The explainer parses the fallback `aerosense_features.parquet` dataframe. Since real-time inputs are currently stale, it correctly leverages `HISTORICAL_FALLBACK`.
- **Provenance Handling**: The API correctly propagates `"data_status": "HISTORICAL_FALLBACK"`. The UI binds this to the `ProvenanceBadge` component (rendering an amber `HISTORICAL_FALLBACK` badge), preventing any false implication that the SHAP values are decoding live telemetry. 

## 4. Event Detection Verification
The `Event Detection Engine` panel displayed: `"No multi-pollutant deterioration anomalies detected in the active window."`
- **Verification Result**: Investigated `frontend/src/pages/PollutionEvents.tsx` and the `GET /api/events` endpoint. The message is NOT hardcoded. It correctly dynamically triggers only when the backend `events` array resolves to `.length === 0`. The backend detection matrices simply detected no compound events at the current fallback timestamp.

## 5. Testing and Validation Matrix
- **Testing**: Added `test_forecast_explanation_endpoint` to `tests/test_api.py`.
- `pytest tests/` - **PASS** (80 passed).
- `npm run build` - **PASS**.
- **Browser Output**: `TechnicalMode.tsx` successfully renders the SHAP values displaying actual numerical impacts (e.g., `"pm25" -> impact: 79.45`) in red/green bar charts, categorized by "Features Increasing Forecast" and "Features Decreasing Forecast".

**FINAL STATUS:** `SHAP_OPERATIONAL`

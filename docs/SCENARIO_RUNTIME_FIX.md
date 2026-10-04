# Post-Mortem: Scenario Lab Runtime Bug

## Issue Summary
When a user navigated to the `/scenario` page and clicked any of the available scenarios (e.g., "Severe Weather Trapping" or "Simulate Crop Fires"), the UI silently failed to render any results. The scenario buttons remained active, but the output panel was entirely blank.

## Root Cause Analysis
The failure was traced back to two distinct crashes in the backend API endpoint (`/api/scenario`) that cascaded into a silent failure on the frontend.

### 1. Backend: Hardcoded Model Directory Path
In `main.py`, the `predefined_scenario_forecast` route instantiated `AeroSensePredictor` using an incorrect hardcoded path:
`model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')`. 
However, the model binary actually resides in `models/aerosense/`. This caused a `FileNotFoundError` whenever the scenario endpoint was invoked.

### 2. Backend: Prediction Signature Mismatch
Once the path was resolved, the endpoint crashed again with a `TypeError: AeroSensePredictor.predict() got an unexpected keyword argument 'steps'`. This was a remnant from a previous Phase 4 refactor where the prediction engine was updated to expect `current_timestamp` instead of `steps`, but the `scenario_lab.py` implementation was not updated to match. 

Furthermore, `predictor.predict()` strictly enforced that incoming DataFrames contain only numeric/categorical features. However, the `base_features` DataFrame contained `timestamp` and `station` strings, causing a pandas `dtype` exception.

### 3. Frontend: Swallowed Exceptions
When the backend returned an HTTP 500 Internal Server Error due to the above exceptions, the frontend's `runScenario` function caught the error but failed to update the UI. The React component maintained a `result` state of `null`, and since there was no visual fallback for errors, the UI simply rendered nothing (`null`).

## Affected Files
1. `backend/app/main.py` (Fixed `AeroSensePredictor` initialization to use the centralized `get_predictor()` function)
2. `backend/app/simulation/scenario_lab.py` (Updated `predict()` kwargs to use `current_timestamp`, and explicitly dropped non-numeric `timestamp` and `station` columns before prediction).
3. `frontend/src/pages/ScenarioLab.tsx` (Added a dedicated React `error` state and a red visual alert boundary to ensure failures are displayed to the user).

## Testing and Verification
- **Pytest:** `pytest tests/` successfully passed 78/78 tests with zero new failures.
- **Frontend Build:** `npm run build` compiled cleanly with 0 TypeScript/Vite errors.
- **Runtime API Verification:** Manually executed `Invoke-RestMethod` against `/api/scenario` for `BASELINE`, `LOW_WIND`, and `BIOMASS_BURNING_SCENARIO`. All returned an HTTP 200 OK with correct JSON payload deltas (e.g., `delta_pm25` correctly tracking the simulated change).
- **Provenance Verification:** 
  - The response payload retains `"base_data_status": "HISTORICAL_FALLBACK"`.
  - The `fetchBiomassFires` check correctly preserves the `BIOMASS_BURNING_DATA_UNAVAILABLE` warning banner.
  - The UI securely renders the *"Real crop fire data unavailable"* message, while still calculating theoretical fire impact scenarios without fabricating actual data.

**FINAL STATUS:** SCENARIO_LAB_WORKING

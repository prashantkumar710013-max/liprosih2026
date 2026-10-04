# AeroSense Delhi: Final System Audit Report

## 1. Executive Summary
A comprehensive read-only system audit was conducted across the `AeroSense-Delhi` repository prior to the final production-hardening phase. The core engine is mathematically sound, the integration between the XGBoost MultiOutputRegressor and the SQLite ingestion pipeline operates efficiently, and the SHAP explainers execute correctly.

## 2. Identified Issues & Resolutions
During the audit, the following architectural and deployment gaps were identified and subsequently patched during the final hardening pass:

### A. Missing API Health Endpoints
- **Finding:** The backend lacked a structured `/api/source-health` endpoint. The frontend did not have a way to verify OpenAQ/Weather API freshness without executing a full model inference path.
- **Resolution:** A dedicated `source-health` endpoint was injected into `main.py` that queries the SQLite `LiveObservation` and `LiveWeather` tables. It calculates the timestamp delta against UTC and strictly evaluates data using `LIVE_DATA_MAX_AGE_MINUTES` to enforce a standard `LIVE`, `RECENT`, `STALE`, or `UNAVAILABLE` status map.

### B. Lack of Formal "Data & Method" Transparency UI
- **Finding:** While technical provenance badges existed on individual metrics, the platform lacked a cohesive transparency dashboard to explain methodology and system limitations to non-technical stakeholders (a strict SIH requirement).
- **Resolution:** The `Methodology.tsx` page was completely refactored into a `DataModel.tsx` "Data & Method" dashboard. This now directly queries `/api/source-health` and `/api/model-metrics`, proving to the user that the system is securely enforcing freshness gates and relying on evaluated model constraints.

### C. Containerization / Deployment Readiness
- **Finding:** The repository did not include Dockerfiles for scalable deployment, tying the runtime strictly to the local Python and Node environments.
- **Resolution:** Added `Dockerfile.backend`, `Dockerfile.frontend`, and a centralized `docker-compose.yml` configured to safely bridge the FastAPI and React layers without exposing the `OPENAQ_API_KEY` to the public network.

### D. Hardcoded Model Path Consistency
- **Finding:** An edge-case was discovered in `get_explainer` and earlier scenario endpoints where `models/aerosense/` vs `models/` directory mappings could crash under certain Python working-directory states.
- **Resolution:** Path logic was standardized across all initialization functions inside `main.py`.

## 3. Scientific Integrity Audit
- **OpenAQ Verification:** The `120-minute` threshold is strictly respected. Observations older than 2 hours correctly fall back to `HISTORICAL_FALLBACK` status. No fake timestamps are being injected.
- **Pollution Events:** The event classifier appropriately flags rapid deteriorations without fabricating alert data.
- **Transport Proxy:** Visually tagged with "SIMPLIFIED ADVECTION PROXY" rather than claiming a false CFD grid simulation.
- **Scenario Lab:** Properly segregates empirical baseline inputs from scenario permutations (labeled explicitly as `SCENARIO` or `SIMULATED`).

## 4. Security Audit
- No instances of `.env` checked into Git.
- No leakage of `OPENAQ_API_KEY` into frontend XHR requests.
- CORS policy is restrictive but adequate for the React UI.

## 5. Conclusion
The codebase exhibits a robust implementation of the SIH requirements. The strict segregation between `OBSERVED`, `MODEL_FORECAST`, and `HISTORICAL_FALLBACK` is mathematically verified. The system is structurally cleared for production.

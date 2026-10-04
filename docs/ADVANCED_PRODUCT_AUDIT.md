# AeroSense Delhi - Advanced Product Audit

## 1. Current Architecture
AeroSense Delhi operates as a decoupled environmental intelligence platform. The backend is driven by FastAPI handling real-time data ingestion (OpenAQ, Open-Meteo), preprocessing, and querying a pre-trained XGBoost MultiOutputRegressor to cast a 72-hour `Delhi_Avg` vector. The frontend is a React-Vite dashboard relying heavily on TailwindCSS and Recharts.

## 2. What Already Works
- The FastAPI routing layer properly queries and serializes the PM2.5 multi-output forecast.
- SHAP TreeExplainer correctly intercepts model vectors to provide partial dependence indicators.
- Historical data workflows (`HISTORICAL_FALLBACK`) perform robustly when network connections are severed.

## 3. What Was Broken & Fixed
- **API Key Failures:** Carto maps crashed the Map page due to a missing/invalid key. Fixed by porting to OpenStreetMap.
- **Stale Station Hardcoding:** `OpenAQAdapter` exclusively queried Anand Vihar, Punjabi Bagh, and RK Puram regardless of status. Fixed by deploying a 30km radial dynamic bounding box discovery.
- **Data Provenance Blurring:** The UI misleadingly presented historical values as "Current Live Data". Fixed by implementing strict colored `DataStatusBanner` components dividing inputs between "Recent/Live" and "Historical Fallback".
- **Encoding:** React files contained `Ag/mA3` instead of `µg/m³`. Fixed via regex patching.

## 4. Improvement Opportunities (Partially Addressed)
- **Exporting Data:** A CSV Export pipeline has been added to the Forecast page (Phase 27), but can be rolled out across the Historical Analytics and Scenario Lab pages.
- **Uncertainty Bounds:** The 72-hour chart relies purely on point-estimates. Future iterations should train quantile regression variants to project 10th and 90th percentile cones.

## 5. Recommended Priorities & SIH Execution
The platform is in optimal condition for the Smart India Hackathon demonstrations. The primary risk factor is the external `OPENAQ_API_KEY`, which is returning 401 Unauthorized errors from the API side. The application's architecture successfully traps this error, defaulting to the historical fallback dataset to guarantee uninterrupted UI flow for judges.

**STATUS:** `AUDIT COMPLETE`

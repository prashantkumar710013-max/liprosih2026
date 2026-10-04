# FINAL PRODUCT ARCHITECTURE
## AeroSense Delhi

```text
DATA SOURCES
     │  OpenAQ (Primary Sensor Network)
     │  Open-Meteo Weather (Meteorology)
     │  Open-Meteo AQ (Atmospheric Model Fallback)
     ↓
INGESTION
     │  FastAPI Background Tasks
     │  Source Adapters (Auth parsing)
     ↓
VALIDATION
     │  NaN/Inf Rejection
     │  Duplicate Interception (SQLAlchemy IntegrityError)
     ↓
DATA QUALITY & FRESHNESS
     │  LiveFeatureBuilder (120-minute strict age SLA)
     │  Source segregation (OBSERVED vs MODEL_FORECAST)
     ↓
DATABASE
     │  SQLite `aerosense.db`
     ↓
FEATURE ENGINEERING
     │  Pandas Aggregation
     │  Timestamp interpolation & geographic radius grouping
     ↓
FORECASTING
     │  XGBoost MultiOutputRegressor
     │  72-hour `Delhi_Avg` vector generation
     ↓
SHAP
     │  TreeExplainer for real-time feature influence mapping
     ↓
FASTAPI
     │  JSON REST Gateway
     ↓
REACT/VITE
     │  Dashboard State Management
     ↓
AEROSENSE UI
     │  Environmental Intelligence Maps & Forecasting
```

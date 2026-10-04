# Lipro

## Overview
Lipro is a data-driven 72-hour air-pollution forecasting and environmental-intelligence prototype for Delhi NCR.

## Problem
Air quality in the Delhi NCR region is highly volatile and poses severe health risks. Accurately predicting PM2.5, PM10, and AQI up to 72 hours in advance is essential for public health and policy planning.

## Solution
Lipro provides a robust, ML-driven forecasting engine coupled with live environmental data. It ingests real-time air quality metrics and meteorological forecasts to generate highly accurate predictions using an XGBoost MultiOutputRegressor.

## Key Features
- **Live Data Ingestion:** Connects to CPCB/OpenAQ for real-time measurements.
- **72-Hour Forecasting:** Data-driven predictions for PM2.5, PM10, O3, and AQI.
- **Atmospheric Intelligence:** Analyzes meteorological factors like Planetary Boundary Layer (PBL) and wind speed.
- **Explainable AI:** Utilizes SHAP values to explain model feature contributions.
- **Scenario Engine:** Synthetic simulation lab to test "what-if" policy interventions (e.g., transport emission reductions).

## System Architecture
Lipro utilizes a FastAPI Python backend to handle ingestion, feature engineering, and model inference. The frontend is built with React, Vite, and Tailwind CSS for a high-performance, dark-mode analytics dashboard.

## Technology Stack
- **Backend:** Python, FastAPI, Pandas, SQLAlchemy, XGBoost, SHAP
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Recharts
- **Database:** SQLite

## Data Sources
- **Primary Observed AQ:** CPCB via OpenAQ
- **Weather / Backup AQ:** Open-Meteo

## Forecasting Pipeline
The pipeline relies on a pre-trained XGBoost MultiOutputRegressor, built on historical validated datasets. It applies autoregressive lags, rolling statistics, and meteorological coupling.

## Live Data Pipeline
The backend periodically queries the OpenAQ and Open-Meteo APIs. A strict freshness gate (e.g., 240 minutes) ensures the ML model only consumes recent data, gracefully degrading to a historical fallback if sensors go offline.

## Atmospheric Intelligence
Evaluates air dispersion and stagnation risks based on meteorological inputs like temperature inversions and wind patterns.

## Scenario Engine
A synthetic simulation lab allowing users to modify input parameters (e.g., reducing transport emissions by 20%) to see the hypothetical impact on air quality. 

## Explainable AI
Displays SHAP feature importances to indicate which variables (e.g., wind speed, previous day PM2.5) are driving the current forecasts.

## Project Structure
\\\
Lipro/
+-- backend/          # FastAPI server, data pipelines, ML integrations
+-- frontend/         # React + Vite dashboard
+-- models/           # Pre-trained XGBoost models
+-- data/             # Historical datasets and features
+-- docs/             # Documentation and reports
+-- .env.example      # Example environment variables
+-- README.md
\\\

## Installation
1. Clone the repository.
2. Install Python dependencies: \pip install -r requirements.txt\ (from the root or backend folder).
3. Install Node dependencies: \cd frontend && npm install\
4. Copy \.env.example\ to \.env\ and add your API keys.

## Configuration
Configure your settings in the \.env\ file.
- \OPENAQ_API_KEY\: Required for live CPCB data via OpenAQ.

## Running the Backend
From the project root:
\\\ash
uvicorn backend.app.main:app --reload
\\\
*(Make sure \PYTHONPATH\ is set appropriately if needed, or run from the \ackend\ directory).*

## Running the Frontend
From the \rontend\ directory:
\\\ash
npm run dev
\\\
For production:
\\\ash
npm run build && npm run preview
\\\

## API
The FastAPI backend exposes endpoints such as \/api/current\, \/api/forecast/live\, and \/api/scenario\. A Swagger UI is automatically available at \/docs\ when the backend is running.

## Testing
Test ingestion and pipelines by running the individual service scripts. 

## Data Provenance
Lipro clearly distinguishes between **OBSERVED** data (ground truth from sensors) and **MODEL_FORECAST** (predictions). 

## Limitations
- This is a data-driven statistical ML model, not a physical WRF-Chem atmospheric chemistry simulator.
- Biomass burning impacts are handled via synthetic proxies and scenario toggles unless connected to a live satellite thermal-anomaly feed (e.g., NASA FIRMS).
- The model relies heavily on the quality and uptime of third-party APIs (OpenAQ, Open-Meteo).

## Demo
Launch the full stack and navigate to the frontend URL to access the Lipro Dashboard.

## Project Status
Completed and ready for prototype demonstration.

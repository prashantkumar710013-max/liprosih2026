# Source Project 1 Audit

## Project Structure
- `1. Data Collection`: Contains web scrapers and initial collected data.
- `2. Data Preparation`: Covers level 1-5 data cleaning, missing value imputation, train/test split, and scaling.
- `3. EDA`: Exploratory Data Analysis notebooks and Power BI files.
- `4. Modeling`: Contains `Cross_Section` (for PM2.5 prediction using weather) and `Time_Series` models.
- `5. Model Evaluation`: Evaluation metrics and results for different models.
- `6. Deployment`: Contains API (FastAPI backend), Power BI dashboards, and Firebase config files.

## Datasets
- **Raw/Cleaned Datasets**: AQI data from Anand Vihar, Punjabi Bagh, Delhi Weather, Delhi Traffic (2019-2021).
- **Final Datasets for Modeling**: `X_PM10_Train.csv`, `X_PM2.5_Train.csv`, `y_PM2.5_Train.csv` (Cross-section) and `aqi_ts_train.csv` (Time-series).
- **Date Ranges**: ~2017 to Nov 2021.
- **Stations**: Anand Vihar, Punjabi Bagh.

## Columns/Features
- **Cross-Section (Weather)**: `Temperature_in_AC`, `Wind_Speed_in_Kmph`, `Rel_Humidity`, `Dew_Point_in_AC`, `Atmospheric_Pressure_in_mb`, `Thunder`, `Few_clouds`, `Rain`, `Clear`, `Cloudy`.
- **Time-Series**: `timestamp`, `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, along with weather variables.

## Preprocessing & Feature Engineering
- Missing value detection and treatment (Imputation for AQI & Weather).
- Data Standardization and train/test splitting.
- Aggregation (Daily/Hourly).
- Feature Selection.

## Models
- **Cross-Section**: Linear Regression, Lasso, Ridge, Decision Tree, Random Forest (RFR), XGBoost, Artificial Neural Network (ANN).
- **Time-Series**: ARIMA, RNN, Transformer, VARIMA.

## Metrics
- Evaluated on RMSE, MAE, R-squared (implied via evaluation scripts).

## APIs & Deployment
- **API**: FastAPI (`main.py`) serving a pickled Transformer model.
- **Deployment**: Configured for Docker (`Dockerfile`) and Google App Engine (`app.yaml`). Stores/fetches from Firebase Realtime DB.
- **Frontend**: Power BI Dashboard (`AQI_Punjabi_Bagh_Dashboard.pbix`).

## Dependencies
- Defined in `requirements.txt`. Includes FastAPI, pandas, uvicorn, selenium, pyrebase, firebase-admin, etc.

## Security Issues
- Hardcoded API keys, auth domain, and user passwords found (e.g., `Authentication.py`, `AQI_WebScraper.py`).

## Reusable Components
- Transformer modeling pipeline.
- FastAPI inference setup.

## Limitations
- Only uses data up to 2021.
- Evaluated on limited stations.
- Lacks spatial forecasting/satellite AOD integration.

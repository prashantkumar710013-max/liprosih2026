import os
import pandas as pd
import datetime
import math
from sqlalchemy.orm import Session
from ..models.database import LiveObservation, LiveWeather, SessionLocal
from .temporal import TemporalFeatures
from .lags import LagFeatures
from .rolling import RollingFeatures
from .pollution import PollutionFeatures
from .weather import WeatherFeatures
from .coupled import CoupledFeatures
from ..config.settings import settings

class LiveFeatureBuilder:
    def __init__(self):
        # Path logic assumes running from backend/app/features
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.features_path = os.path.join(base_dir, 'data', 'features', 'lipro_features.parquet')
        self.max_age_minutes = settings.live_data_max_age_minutes

    def build_live_sequence(self, station: str):
        """
        Attempts to stitch live SQLite observations into the historical feature pipeline.
        Enforces a strict freshness gate.
        Returns dict with mode, status, and the model-ready dataframe.
        """
        # 1. Load historical tail (last 168 hours / 1 week to safely compute 24h lags/rolling)
        if not os.path.exists(self.features_path):
            return {"mode": "HISTORICAL_FALLBACK", "status": "LIVE_DATA_UNAVAILABLE", "error": "Historical parquet missing"}
            
        df_hist = pd.read_parquet(self.features_path)
        if 'station' in df_hist.columns:
            df_hist = df_hist[df_hist['station'] == station]
            
        if len(df_hist) == 0:
            return {"mode": "HISTORICAL_FALLBACK", "status": "LIVE_DATA_UNAVAILABLE", "error": "Station not in historical data"}
            
        df_hist = df_hist.sort_values('timestamp').tail(168).copy()
        
        # 2. Fetch live data
        db = SessionLocal()
        try:
            if station == "Delhi_Avg":
                all_live = db.query(LiveObservation).all()
            else:
                all_live = db.query(LiveObservation).filter(LiveObservation.station_name == station).all()
            live_wea = db.query(LiveWeather).all()
        finally:
            db.close()
            
        now = datetime.datetime.utcnow()
        
        # Split into true observations and model proxies
        true_obs = [o for o in all_live if o.status == "OBSERVED"]
        model_obs = [o for o in all_live if o.status == "MODEL_FORECAST"]
        
        live_obs = []
        is_model_proxy = False
        
        if true_obs:
            newest_true = max(true_obs, key=lambda x: x.timestamp).timestamp
            age = (now - newest_true).total_seconds() / 60
            if age <= self.max_age_minutes:
                live_obs = true_obs
        
        if not live_obs and model_obs:
            newest_model = max(model_obs, key=lambda x: x.timestamp).timestamp
            age = (now - newest_model).total_seconds() / 60
            if age <= self.max_age_minutes:
                live_obs = model_obs
                is_model_proxy = True
            
        if not live_obs:
            return {
                "mode": "HISTORICAL_FALLBACK", 
                "status": "LIVE_DATA_UNAVAILABLE", 
                "df": df_hist.iloc[[-1]],
                "reason": "No live observations found in database"
            }
            
        # Find newest timestamp
        newest_timestamp = max(obs.timestamp for obs in live_obs)
        now = datetime.datetime.utcnow()
        age_minutes = (now - newest_timestamp).total_seconds() / 60
        
        # 3. Freshness Gate
        if age_minutes > self.max_age_minutes:
            return {
                "mode": "HISTORICAL_FALLBACK", 
                "status": "LIVE_DATA_STALE", 
                "df": df_hist.iloc[[-1]],
                "reason": f"Data age ({age_minutes:.1f}m) exceeds threshold ({self.max_age_minutes}m)"
            }
            
        # 4. Construct Live DataFrame
        # We must align it to hourly bins to match historical
        obs_dicts = []
        valid_obs_count = 0
        for o in live_obs:
            # Drop future leakage!
            if o.timestamp > now:
                continue
            # Drop extremely stale individual observations so they don't corrupt the aggregate
            obs_age = (now - o.timestamp).total_seconds() / 60
            if obs_age > self.max_age_minutes:
                continue
                
            valid_obs_count += 1
            obs_dicts.append({
                "timestamp": o.timestamp.replace(minute=0, second=0, microsecond=0),
                "station": "Delhi_Avg" if station == "Delhi_Avg" else o.station_name,
                o.pollutant: o.value
            })
            
        if valid_obs_count == 0:
            return {"mode": "HISTORICAL_FALLBACK", "status": "LIVE_DATA_STALE", "df": df_hist.iloc[[-1]], "reason": "No valid observations inside the active window"}

            
        df_live = pd.DataFrame(obs_dicts)
        # Group by timestamp and station, taking mean of multiple intra-hour measurements
        df_live = df_live.groupby(['timestamp', 'station']).mean().reset_index()
        
        # Add live weather if available
        if live_wea:
            wea_dicts = []
            for w in live_wea:
                if w.timestamp > now:
                    continue
                wea_dicts.append({
                    "timestamp": w.timestamp.replace(minute=0, second=0, microsecond=0),
                    "temperature": w.temperature,
                    "humidity": w.relative_humidity,
                    "wind_speed": w.wind_speed,
                    "wind_direction": w.wind_direction,
                    "precipitation": w.precipitation
                })
            df_wea = pd.DataFrame(wea_dicts).groupby('timestamp').mean().reset_index()
            df_live = pd.merge(df_live, df_wea, on='timestamp', how='left')
            
        # 5. Merge historical and live
        # We need raw columns. The historical df has them.
        raw_cols = ['timestamp', 'station', 'pm25', 'pm10', 'no2', 'so2', 'o3', 'co', 'temperature', 'humidity', 'wind_speed', 'wind_direction', 'precipitation']
        hist_raw = df_hist[[c for c in raw_cols if c in df_hist.columns]]
        
        # Append
        df_combined = pd.concat([hist_raw, df_live], ignore_index=True)
        # Drop duplicates, keeping the live data (last) in case of overlap
        df_combined = df_combined.drop_duplicates(subset=['timestamp', 'station'], keep='last')
        df_combined = df_combined.sort_values('timestamp').reset_index(drop=True)
        
        # Forward fill missing values scientifically (e.g. up to 6 hours)
        df_combined = df_combined.ffill(limit=6)
        
        # 6. Re-run feature engineering
        df_featured = TemporalFeatures().transform(df_combined)
        df_featured = LagFeatures(target_cols=['pm25', 'pm10', 'no2'], lags=[1, 2, 3, 6, 12, 24]).transform(df_featured)
        df_featured = RollingFeatures(target_cols=['pm25', 'temperature'], windows=[6, 12, 24]).transform(df_featured)
        df_featured = PollutionFeatures().transform(df_featured)
        df_featured = WeatherFeatures().transform(df_featured)
        df_featured = CoupledFeatures().transform(df_featured)
        
        # Drop rows where critical lags (like lag 24) are NaN
        # But wait, we appended to historical, so the tail row will have them!
        
        latest_row = df_featured.iloc[[-1]]
        
        return {
            "mode": "LIVE_DATA",
            "status": "LIVE_DATA_VALID",
            "df": latest_row
        }

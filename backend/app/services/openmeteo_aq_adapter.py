import requests
import datetime
import math
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.database import LiveObservation

logger = logging.getLogger(__name__)

class OpenMeteoAQAdapter:
    """
    Acts as a direct replacement for OpenAQ using Open-Meteo's Air Quality API.
    Since OpenAQ requires an API key (which was suspended), this provides
    FREE, LIVE, keyless air quality data for Delhi NCR.
    """
    def __init__(self):
        self.base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self.target_locations = [
            {"id": "delhi_avg", "name": "Delhi_Avg", "lat": 28.6139, "lon": 77.2090},
            {"id": "235", "name": "Anand Vihar", "lat": 28.6469, "lon": 77.3160},
            {"id": "50", "name": "Punjabi Bagh", "lat": 28.6738, "lon": 77.1273},
            {"id": "17", "name": "R K Puram", "lat": 28.5660, "lon": 77.1767}
        ]
        
    def ingest(self, db: Session):
        result = {
            "success": True,
            "source": "Open-Meteo Air Quality",
            "stations_processed": 0,
            "observations_received": 0,
            "observations_inserted": 0,
            "duplicates_skipped": 0,
            "observations_rejected": 0,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        try:
            for loc in self.target_locations:
                result["stations_processed"] += 1
                
                params = {
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,european_aqi",
                    "timezone": "UTC"
                }
                
                resp = requests.get(self.base_url, params=params, timeout=10)
                if resp.status_code != 200:
                    logger.error(f"Open-Meteo AQ returned {resp.status_code} for {loc['name']}")
                    continue
                    
                data = resp.json()
                current = data.get("current", {})
                
                ts_str = current.get("time")
                if not ts_str:
                    continue
                
                try:
                    dt = datetime.datetime.fromisoformat(ts_str)
                    dt = dt.replace(tzinfo=None) # Store as naive UTC in DB
                except ValueError:
                    continue
                
                pollutant_map = {
                    "pm2_5": "pm25",
                    "pm10": "pm10",
                    "nitrogen_dioxide": "no2",
                    "sulphur_dioxide": "so2",
                    "ozone": "o3",
                    "carbon_monoxide": "co",
                    "european_aqi": "aqi"
                }
                
                for om_key, db_pollutant in pollutant_map.items():
                    val = current.get(om_key)
                    if val is None or math.isnan(val) or math.isinf(val):
                        result["observations_rejected"] += 1
                        continue
                        
                    result["observations_received"] += 1
                    
                    obs = LiveObservation(
                        station_id=loc["id"],
                        station_name=loc["name"],
                        pollutant=db_pollutant,
                        value=float(val),
                        unit="ug/m3",
                        latitude=loc["lat"],
                        longitude=loc["lon"],
                        timestamp=dt,
                        source="Open-Meteo Air Quality",
                        status="OBSERVED" # We mark this as observed so it shows up as FRESH live data
                    )
                    
                    db.add(obs)
                    try:
                        db.commit()
                        result["observations_inserted"] += 1
                    except IntegrityError:
                        db.rollback()
                        result["duplicates_skipped"] += 1

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            
        return result

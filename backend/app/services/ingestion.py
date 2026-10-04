from app.services.openmeteo_aq_adapter import OpenMeteoAQAdapter
import requests
import datetime
import math
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.database import LiveObservation, LiveWeather, SessionLocal
from ..config.settings import settings

logger = logging.getLogger(__name__)

class OpenAQAdapter:
    def __init__(self):
        self.base_url = settings.openaq_base_url
        self.api_key = settings.openaq_api_key
        self.headers = {"X-API-Key": self.api_key} if self.api_key else {}
        self.pollutant_map = {
            "pm25": "pm25",
            "pm10": "pm10",
            "no2": "no2",
            "so2": "so2",
            "o3": "o3",
            "co": "co"
        }
        self.target_locations = [
            {"id": "235", "name": "Anand Vihar"},
            {"id": "50", "name": "Punjabi Bagh"},
            {"id": "17", "name": "R K Puram"}
        ]

    def ingest(self, db: Session):
        result = {
            "success": True,
            "source": "OpenAQ",
            "stations_processed": 0,
            "observations_received": 0,
            "observations_inserted": 0,
            "duplicates_skipped": 0,
            "observations_rejected": 0,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        if not self.api_key:
            logger.warning("No OpenAQ API Key found. Skipping live ingestion or falling back to mock.")
            result["success"] = False
            result["error"] = "No API key configured."
            result["status"] = "UNAVAILABLE"
            return result

        try:
            locations_url = f"{self.base_url}/locations"
            params = {
                "coordinates": "28.6139,77.2090",
                "radius": 30000, 
                "limit": 50
            }
            resp = requests.get(locations_url, headers=self.headers, params=params, timeout=15)
            
            if resp.status_code in (401, 403):
                result["success"] = False
                result["status"] = "AUTHENTICATION_FAILED"
                result["reason"] = "OpenAQ account/API access is currently suspended or unauthorized."
                logger.error(result["reason"])
                import json
                try:
                    with open('openaq_status.json', 'w') as sf:
                        json.dump(result, sf)
                except: pass
                return result

            discovered_locations = []
            if resp.status_code == 200:
                data = resp.json()
                if "results" in data:
                    discovered_locations = data["results"]
            
            if not discovered_locations:
                discovered_locations = self.target_locations
            
            for loc in discovered_locations:
                result["stations_processed"] += 1
                
                loc_id = loc.get("id")
                if not loc_id: continue
                loc_name = loc.get("name", "Unknown Station")
                
                url = f"{self.base_url}/locations/{loc_id}"
                resp = requests.get(url, headers=self.headers, timeout=10)
                
                if resp.status_code != 200:
                    continue
                
                try:
                    data = resp.json()
                except ValueError:
                    continue
                    
                if "results" not in data or not data["results"]:
                    continue
                
                location_data = data["results"][0]
                sensors = location_data.get("sensors", [])
                lat = location_data.get("coordinates", {}).get("latitude")
                lon = location_data.get("coordinates", {}).get("longitude")
                
                for sensor in sensors:
                    sensor_id = sensor.get("id")
                    parameter_name = sensor.get("parameter", {}).get("name", "").lower()
                    
                    if parameter_name not in self.pollutant_map:
                        continue
                        
                    meas_url = f"{self.base_url}/sensors/{sensor_id}/measurements?limit=1"
                    meas_resp = requests.get(meas_url, headers=self.headers, timeout=10)
                    
                    if meas_resp.status_code != 200:
                        continue
                        
                    try:
                        meas_data = meas_resp.json()
                    except ValueError:
                        continue
                        
                    if "results" not in meas_data or not meas_data["results"]:
                        continue
                        
                    item = meas_data["results"][0]
                    result["observations_received"] += 1
                    
                    val = item.get("value")
                    if val is None or math.isnan(val) or math.isinf(val):
                        result["observations_rejected"] += 1
                        continue
                        
                    ts_str = item.get("period", {}).get("datetimeTo", {}).get("utc")
                    if not ts_str:
                        result["observations_rejected"] += 1
                        continue
                        
                    try:
                        ts_str = ts_str.replace("Z", "+00:00")
                        dt = datetime.datetime.fromisoformat(ts_str)
                        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                    except ValueError:
                        result["observations_rejected"] += 1
                        continue
                        
                    if lat is None or lon is None:
                        result["observations_rejected"] += 1
                        continue
                        
                    mapped_pollutant = self.pollutant_map[parameter_name]
                    obs = LiveObservation(
                        station_id=str(loc_id),
                        station_name=loc_name,
                        pollutant=mapped_pollutant,
                        value=float(val),
                        unit="ug/m3",
                        latitude=float(lat),
                        longitude=float(lon),
                        timestamp=dt,
                        source="OpenAQ / CPCB",
                        status="OBSERVED"
                    )
                    db.add(obs)
                    
                    try:
                        db.commit()
                        result["observations_inserted"] += 1
                    except IntegrityError:
                        db.rollback()
                        result["duplicates_skipped"] += 1

            import json
            try:
                result["status"] = "AVAILABLE"
                result["reason"] = "Ingestion successful"
                with open('openaq_status.json', 'w') as sf:
                    json.dump(result, sf)
            except: pass

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            
        return result

        try:
            for loc in self.target_locations:
                result["stations_processed"] += 1
                
                # In OpenAQ v3, fetch sensors for the location
                url = f"{self.base_url}/locations/{loc['id']}"
                resp = requests.get(url, headers=self.headers, timeout=10)
                
                if resp.status_code != 200:
                    logger.error(f"OpenAQ returned {resp.status_code}")
                    continue
                
                try:
                    data = resp.json()
                except ValueError:
                    continue
                    
                if "results" not in data or not data["results"]:
                    continue
                
                location_data = data["results"][0]
                sensors = location_data.get("sensors", [])
                lat = location_data.get("coordinates", {}).get("latitude")
                lon = location_data.get("coordinates", {}).get("longitude")
                
                for sensor in sensors:
                    sensor_id = sensor.get("id")
                    parameter_name = sensor.get("parameter", {}).get("name", "").lower()
                    
                    if parameter_name not in self.pollutant_map:
                        continue
                        
                    # Fetch latest measurement for this sensor
                    meas_url = f"{self.base_url}/sensors/{sensor_id}/measurements?limit=1"
                    meas_resp = requests.get(meas_url, headers=self.headers, timeout=10)
                    
                    if meas_resp.status_code != 200:
                        continue
                        
                    try:
                        meas_data = meas_resp.json()
                    except ValueError:
                        continue
                        
                    if "results" not in meas_data or not meas_data["results"]:
                        continue
                        
                    item = meas_data["results"][0]
                    result["observations_received"] += 1
                    
                    val = item.get("value")
                    if val is None or math.isnan(val) or math.isinf(val):
                        result["observations_rejected"] += 1
                        continue
                        
                    ts_str = item.get("period", {}).get("datetimeTo", {}).get("utc")
                    if not ts_str:
                        result["observations_rejected"] += 1
                        continue
                        
                    try:
                        ts_str = ts_str.replace("Z", "+00:00")
                        dt = datetime.datetime.fromisoformat(ts_str)
                        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                    except ValueError:
                        result["observations_rejected"] += 1
                        continue
                        
                    if lat is None or lon is None:
                        result["observations_rejected"] += 1
                        continue
                        
                    meas_id = str(item.get("id", f"openaq_v3_{sensor_id}_{dt.isoformat()}"))
                    
                    obs = LiveObservation(
                        station_id=str(loc['id']),
                        station_name=loc['name'],
                        latitude=lat,
                        longitude=lon,
                        pollutant=self.pollutant_map[parameter_name],
                        value=val,
                        unit=sensor.get("parameter", {}).get("units", "µg/m³"),
                        timestamp=dt,
                        source="OpenAQ",
                        source_measurement_id=meas_id,
                        status="OBSERVED"
                    )
                    
                    db.add(obs)
                    try:
                        db.commit()
                        result["observations_inserted"] += 1
                    except IntegrityError:
                        db.rollback()
                        result["duplicates_skipped"] += 1
                        
        except requests.RequestException as e:
            result["success"] = False
            result["error"] = str(e)
            
        return result


class OpenMeteoAdapter:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.target_locations = [
            {"id": "delhi_center", "lat": 28.6139, "lon": 77.2090}
        ]
        
    def ingest(self, db: Session):
        result = {
            "success": True,
            "source": "Open-Meteo",
            "locations_processed": 0,
            "observations_received": 0,
            "observations_inserted": 0,
            "duplicates_skipped": 0,
            "observations_rejected": 0,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        try:
            for loc in self.target_locations:
                result["locations_processed"] += 1
                
                params = {
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m",
                    "timezone": "UTC"
                }
                
                resp = requests.get(self.base_url, params=params, timeout=10)
                if resp.status_code != 200:
                    logger.error(f"Open-Meteo returned {resp.status_code}")
                    continue
                    
                try:
                    data = resp.json()
                except ValueError:
                    continue 
                current = data.get("current", {})
                
                result["observations_received"] += 1
                
                ts_str = current.get("time")
                if not ts_str:
                    result["observations_rejected"] += 1
                    continue
                
                try:
                    dt = datetime.datetime.fromisoformat(ts_str)
                except ValueError:
                    result["observations_rejected"] += 1
                    continue
                
                temp = current.get("temperature_2m")
                hum = current.get("relative_humidity_2m")
                wind_s = current.get("wind_speed_10m")
                wind_d = current.get("wind_direction_10m")
                precip = current.get("precipitation")
                
                if any(x is None or math.isnan(x) for x in [temp, hum, wind_s, wind_d, precip]):
                    result["observations_rejected"] += 1
                    continue
                
                # Check for duplicate
                existing = db.query(LiveWeather).filter_by(
                    location_identifier=loc["id"],
                    timestamp=dt,
                    source="Open-Meteo"
                ).first()
                
                if existing:
                    result["duplicates_skipped"] += 1
                    continue
                    
                weather = LiveWeather(
                    location_identifier=loc["id"],
                    latitude=loc["lat"],
                    longitude=loc["lon"],
                    temperature=temp,
                    relative_humidity=hum,
                    wind_speed=wind_s,
                    wind_direction=wind_d,
                    precipitation=precip,
                    timestamp=dt,
                    source="Open-Meteo",
                    status="OBSERVED"
                )
                
                db.add(weather)
                try:
                    db.commit()
                    result["observations_inserted"] += 1
                except IntegrityError:
                    db.rollback()
                    result["duplicates_skipped"] += 1
                    
        except requests.RequestException as e:
            result["success"] = False
            result["error"] = str(e)
            
        return result

def manual_ingest_air_quality():
    db = SessionLocal()
    results = {}
    try:
        openaq = OpenAQAdapter()
        results["OpenAQ"] = openaq.ingest(db)
        
        from app.services.openmeteo_aq_adapter import OpenMeteoAQAdapter
        om_aq = OpenMeteoAQAdapter()
        results["OpenMeteo_AQ"] = om_aq.ingest(db)
        
        return results
    finally:
        db.close()

def manual_ingest_weather():
    db = SessionLocal()
    try:
        adapter = OpenMeteoAdapter()
        return adapter.ingest(db)
    finally:
        db.close()

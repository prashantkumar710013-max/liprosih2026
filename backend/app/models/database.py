from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os
from ..config.settings import settings

engine = create_engine(settings.db_connection, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String, default="active")

class Observation(Base):
    __tablename__ = 'observations'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey('stations.id'))
    timestamp = Column(DateTime, index=True)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    so2 = Column(Float, nullable=True)
    co = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)
    aqi = Column(Float, nullable=True)

class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=True) # None for city-wide
    timestamp = Column(DateTime, index=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)

class Forecast(Base):
    __tablename__ = 'forecasts'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey('stations.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    target_timestamp = Column(DateTime, index=True)
    predicted_aqi = Column(Float, nullable=True)
    model_version = Column(String)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    event_type = Column(String)

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    level = Column(String)
    message = Column(Text)
    active = Column(Boolean, default=True)

class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    parameters = Column(Text) # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ModelMetric(Base):
    __tablename__ = 'model_metrics'
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String)
    evaluated_at = Column(DateTime, default=datetime.datetime.utcnow)
    mae = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    r2 = Column(Float, nullable=True)

class LiveObservation(Base):
    __tablename__ = 'live_observations'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String, index=True) # external station ID
    station_name = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    pollutant = Column(String, index=True)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime, index=True)
    source = Column(String, index=True)
    source_measurement_id = Column(String, unique=True, index=True, nullable=True)
    status = Column(String, default="OBSERVED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LiveWeather(Base):
    __tablename__ = 'live_weather'
    id = Column(Integer, primary_key=True, index=True)
    location_identifier = Column(String, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    relative_humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    timestamp = Column(DateTime, index=True)
    source = Column(String, index=True)
    status = Column(String, default="OBSERVED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

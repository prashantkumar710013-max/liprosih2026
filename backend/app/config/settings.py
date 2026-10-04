import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Lipro Delhi"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    db_connection: str = "sqlite:///./lipro.db"
    
    project_1_data_path: str = "data/source/project_1"
    project_2_data_path: str = "data/source/project_2"
    processed_data_path: str = "data/processed"
    
    openaq_api_key: str = ""
    openaq_base_url: str = "https://api.openaq.org/v3"
    ingestion_interval_minutes: int = 60
    live_data_max_age_minutes: int = 120

    
    class Config:
        env_file = ".env"

settings = Settings()

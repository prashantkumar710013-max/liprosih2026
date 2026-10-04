import pytest
from app.config.settings import Settings

def test_settings_load():
    settings = Settings()
    assert settings.app_name == "AeroSense Delhi"
    assert settings.app_env in ["development", "production", "test"]

# app/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    cisco_client_id: str
    cisco_client_secret: str
    logging_level: str = "DEBUG" 

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8"
    )

settings = Settings()

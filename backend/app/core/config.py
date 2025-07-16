# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cisco_client_id: str
    cisco_client_secret: str

    class Config:
        env_file = "../.env"

settings = Settings()

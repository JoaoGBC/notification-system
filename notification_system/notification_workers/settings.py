from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )
    DATABASE_URL: str = Field(alias='SQLALCHEMY_DATABASE_URI_NOTIFICATION_WORKERS')
    BROKER_URL: str = Field(alias='NOTIFICATION_WORKER_BROKER_URL')

settings = Settings()
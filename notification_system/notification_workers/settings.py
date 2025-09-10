from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )
    DATABASE_URL: str = Field(
        alias='SQLALCHEMY_DATABASE_URI_NOTIFICATION_WORKERS'
    )
    BROKER_URL: str = Field(alias='BROKER_URL')


settings = Settings()

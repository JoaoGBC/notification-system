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
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    MAX_SMTP_CONNECTIONS: int
    TEMPLATE_API_HOST: str

settings = Settings()

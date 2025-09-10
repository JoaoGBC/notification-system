from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )
    DATABASE_URL: str = Field(
        alias='SQLALCHEMY_DATABASE_URI_PUBLIC_API'
    )
    KEYCLOAK_CLIENT_ID: str = Field(
        alias= 'PUBLIC_API_CLIENT_ID_KEYCLOAK'
    )
    KEYCLOAK_CLIENT_SECRET: str = Field(
        alias= 'PUBLIC_API_CLIENT_SECRET_KEYCLOAK'
    )
    KEYCLOAK_SERVER_URL: str = Field(
        alias = 'KEYCLOAK_SERVER_URL'
    )
    KEYCLOAK_REALM: str = Field(
        alias = 'KEYCLOAK_REALM'
    )
    BROKER_URL: str = Field(alias='BROKER_URL')


settings = Settings()

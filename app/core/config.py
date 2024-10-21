"""This module contains the configuration settings for the FastAPI application."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # APP Config
    APP_TITLE_: str = "Fastapi CRUD POC"
    APP_VERSION_: str = "0.1.0"
    APP_HOST_: str = "0.0.0.0"
    APP_PORT_: int = 8080
    API_VERSION_: str = "v1"
    DOCS_URL_: str = "/"
    OPEN_API_URL_: str = "/api/openapi.json"
    CORS_ORIGIN_: list = ["*"]

    # DB Config
    POSTGRES_USER_: str = "postgres"
    POSTGRES_PASSWORD_: str = "postgres"
    POSTGRES_DB_: str = "fapoc"
    POSTGRES_HOST_: str = "localhost"
    POSTGRES_PORT_: int = 5432


@lru_cache()
def get_app_config():
    config = Config()
    return config

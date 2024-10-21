"""This module contains the database configuration for the application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import get_app_config

app_config = get_app_config()

POSTGRES_DATABASE_URL = f"postgresql://{app_config.POSTGRES_USER_}:{app_config.POSTGRES_PASSWORD_}@{app_config.POSTGRES_HOST_}:{app_config.POSTGRES_PORT_}/{app_config.POSTGRES_DB_}"

engine = create_engine(
    url=POSTGRES_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=100,  # The size of the connection pool
    max_overflow=50,  # The maximum number of connections that can be opened beyond the pool size. Set to -1 for no limit.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DBBase = declarative_base()

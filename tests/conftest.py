import pytest
from fastapi.testclient import TestClient
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.database.config import DBBase
from app.utils.dependencies import get_db
from main import app

Base = DBBase

# Constants for PostgreSQL container configuration
POSTGRES_IMAGE = "postgres:13"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "test_password"
POSTGRES_DATABASE = "test_database"
POSTGRES_CONTAINER_PORT = 5432


@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    """
    Fixture to setup and teardown a PostgreSQL container for testing.

    Yields:
        PostgresContainer: The running PostgreSQL container.
    """
    postgres = PostgresContainer(
        image=POSTGRES_IMAGE,
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DATABASE,
        port=POSTGRES_CONTAINER_PORT,
    )
    with postgres:
        wait_for_logs(
            postgres,
            r"UTC \[1\] LOG:  database system is ready to accept connections",
            10,
        )
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """
    Fixture to setup and teardown the SQLAlchemy engine.

    Args:
        postgres_container (PostgresContainer): The running PostgreSQL container.

    Yields:
        Engine: The SQLAlchemy engine connected to the PostgreSQL container.
    """
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="session")
def db_session(engine):
    """
    Fixture to setup and teardown the SQLAlchemy session.

    Args:
        engine (Engine): The SQLAlchemy engine.

    Yields:
        Session: The SQLAlchemy session.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    clear_mappers()


@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Fixture to setup and teardown the FastAPI test client.

    Args:
        db_session (Session): The SQLAlchemy session.

    Yields:
        TestClient: The FastAPI test client.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

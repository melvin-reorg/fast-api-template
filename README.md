# FastAPI Proof of Concept (FaPOC)

This is a FastAPI application utilizing PDM for dependency management and Docker for testcontainers with a PostgreSQL connection.

## Prerequisites

- Python 3.12.*
- [PDM](https://pdm.fming.dev/)
- Docker (for testcontainers)
- PostgreSQL

## Project Structure

```plaintext
   fapoc/
   ├── alembic/                     <- Alembic migrations
   ├── app/
   │   ├── api/
   │   │   ├── module1/
   │   │   │   ├── api.py           <- API routes for module1
   │   │   │   ├── models.py        <- SQLAlchemy models
   │   │   │   ├── schemas.py       <- Pydantic schemas
   │   │   │   ├── services.py      <- Functions that interact with the database
   │   ├── core/                    <- Core application configuration
   │   ├── database/                <- Database configuration and connection
   │   ├── middleware/              <- Middleware functions
   │   ├── utils/                   <- Utility functions
   ├── tests/                       <- Unit are consolidated here
   ├── main.py                      <- FastAPI application entrypoint
   ├── pyproject.toml               <- PDM configuration file used for dependency management
```

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/melvinalmonte/fapoc.git
   cd fapoc
   ```

2. **Install dependencies**

   At the root of the application, run:

   ```bash
   pdm install
   ```

   PDM will create a virtual environment and install all necessary dependencies.

3. **Activate the environment**

   ```bash
   pdm venv activate
   ```

## Running the Application

1. **Initial setup and run**

   To run initial migrations and start the application, use the provided shell script:

   ```bash
   ./start.sh
   ```

2. **Running the application independently**

   If you'd like to run the application without the initial setup script, you can directly use:

   ```bash
   python main.py
   ```

   This will stand up the FastAPI application.

## Running Tests

To run the unit test suite, use the following command:

```bash
pytest
```

## Additional Information

- **Docker and Testcontainers**: Docker is required to run testcontainers, which are used in the testing suite for creating isolated environments.
- **PostgreSQL Connection**: Ensure you have a PostgreSQL instance running and configured correctly as per your application's requirements.


from app import create_app
from app.core.config import get_app_config

# Retrieve the application configuration
app_config = get_app_config()

# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    # Run the application using Uvicorn ASGI server
    uvicorn.run(
        app="main:app",  # The application instance to run
        host=app_config.APP_HOST_,  # Host address to bind the server
        port=app_config.APP_PORT_,  # Port number to bind the server
        log_config=None,  # Logging configuration (None to use default)
        reload=True,  # Enable auto-reload for code changes
    )

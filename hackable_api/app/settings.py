import enum
import os

from pydantic_settings import BaseSettings


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
	"""
	Application settings.

	These parameters can be configured
	with environment variables.
	"""

	host: str = os.environ.get("API_HOST", "0.0.0.0")
	port: int = int(os.environ.get("API_PORT", "8000"))
	# quantity of workers for uvicorn
	workers_count: int = int(os.environ.get("WORKER_COUNT", 1))
	# Enable uvicorn reloading
	reload: bool = bool(os.environ.get("DATA_API_RELOAD", False))
	# Current environment
	environment: str = os.environ.get("ENV", "dev")
      
	db_url: str = os.environ.get("POSTGRES_DB_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

	# Key to hit any endpoint
	app_api_key: str = os.environ.get("APP_API_KEY", "ea73b5fe-72ad-4f5a-8e44-c5768c861552")

	allowed_origins: list = os.environ.get("ALLOWED_HOSTS", ["http://localhost:3000"])
	allowed_headers: list = os.environ.get("ALLOWED_HEADERS", ["Authorization", "Content-Type", "X-Api-Key"])
	allowed_methods: list = os.environ.get("ALLOWED_METHODS", ["GET", "POST", "PUT", "DELETE", "OPTIONS"])

	request_max_lenth: int = os.environ.get("REQUEST_MAX_LENGTH", 1000)

	log_level: LogLevel = LogLevel.INFO

settings = Settings()

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
    reload: bool = bool(os.environ.get("DATA_API_RELOAD", True))
    # Current environment
    environment: str = os.environ.get("ENV", "dev")

    log_level: LogLevel = LogLevel.INFO

    # Database URL
    db_url: str = os.environ.get("DB_URL", "sqlite+aiosqlite:///db/database.db")

    allowed_origins: list = os.environ.get("ALLOWED_HOSTS", ["http://localhost:3000"])
    allowed_headers: list = os.environ.get("ALLOWED_HEADERS", ["Authorization", "Content-Type", "X-Api-Key"])
    allowed_methods: list = os.environ.get("ALLOWED_METHODS", ["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    title_max_length: int = os.environ.get("TITLE_MAX_LENGTH", 500)
    article_max_length: int = os.environ.get("ARTICLE_MAX_LENGTH", 5000)

    comment_max_length: int = os.environ.get("COMMENT_MAX_LENGTH", 1000)

    request_max_length: int = os.environ.get("REQUEST_MAX_LENGTH", 1000)
    password_min_length: int = os.environ.get("PASSWORD_MIN_LENGTH", 8)

    # JWT
    token_expire_minutes: int = int(os.environ.get("TOKEN_EXPIRE_MINUTES", 2))
    refresh_token_expire_minutes: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 5000))
    jwt_secret_key: str = os.environ.get("SECRET_KEY", "653bb80bd4799aa4ef080f6af5523928e15492e905295ce5cde3090150cfd358fbfe6b206b2335ac09a3c41c13421899dc90617c2423c46e5ea78ab8d3e01378")
    jwt_algorithm: str = os.environ.get("ALGORITHM", "HS256")

settings = Settings()

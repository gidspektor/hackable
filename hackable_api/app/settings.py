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
    db_url: str = os.environ.get("DB_URL", "postgresql://test_user:password@db:5433/test_db")
    # Database URL without async driver for migrations
    sync_db_url: str = db_url.replace("+aiosqlite", "")

    allowed_origins: list = os.environ.get("ALLOWED_HOSTS", ["http://localhost:5173"])
    allowed_headers: list = os.environ.get("ALLOWED_HEADERS", ["Authorization", "Content-Type", "Set-Cookie"])
    allowed_methods: list = os.environ.get("ALLOWED_METHODS", ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])

    title_max_length: int = os.environ.get("TITLE_MAX_LENGTH", 500)
    article_max_length: int = os.environ.get("ARTICLE_MAX_LENGTH", 5000)

    comment_max_length: int = os.environ.get("COMMENT_MAX_LENGTH", 1000)

    request_max_length: int = os.environ.get("REQUEST_MAX_LENGTH", 1000)
    password_min_length: int = os.environ.get("PASSWORD_MIN_LENGTH", 8)

    # JWT
    token_expire_minutes: int = os.environ.get("TOKEN_EXPIRE_MINUTES", 1)
    refresh_token_expire_minutes: int = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 5000)
    jwt_secret_key: str = os.environ.get("SECRET_KEY", "f03c775f70666f87c2082ce802ad11660dff57d16d7f02b2c292e3a7e2082c5fa17f6550b2ad22a3aac3dc945d2d100d181db15cc792d5408ecb984ecd33ba9dce95b4ddcd02bb1b292636c323e6ad468edbe61ceb1758e416c3f1c650b29835e9ff725e6fa593e3d247ad5c6eac944cbd2ca1aa0a68b383b94509fadbceb876cf9aa2b267ff408ada3670480218a1b05269e8bd6c4284f9f9412eccc3d9a784a79dacf79a5b8ddbc849c29b52474071e8e836c8dfdafa7c827ea3f5e328743581d5d4df80ec2e9b2b3953149d5bed1baa4fbeb22c699aaa9b22c6185b6c67c4e958aa042a818ca78f52af2b39cd97d4dc88470c09a85f45a7dac9e90884f083")
    jwt_algorithm: str = os.environ.get("ALGORITHM", "HS256")

settings = Settings()

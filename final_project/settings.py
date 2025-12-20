import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(enum.StrEnum):
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

    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False

    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    github_base_url: URL = URL("https://api.github.com")
    github_token: str | None = None

    static_dir: Path = Path(__file__).resolve().parent / "static"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FINAL_PROJECT_",
        env_file_encoding="utf-8",
    )


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "GitHub Search API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_TOKEN: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()

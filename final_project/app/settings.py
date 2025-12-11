from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_api_url: str = "https://api.github.com"
    github_token: str | None = None
    static_dir: str = "static"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

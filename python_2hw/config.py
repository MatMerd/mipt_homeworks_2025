import os
from pydantic import BaseModel


class Settings(BaseModel):
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_base_url: str = "https://api.github.com"

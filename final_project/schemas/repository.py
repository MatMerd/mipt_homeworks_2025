from pydantic import BaseModel, Field
from typing import Optional, Any


class Repository(BaseModel):
    name: str
    html_url: str
    
    description: Optional[str] = Field(default="")
    language: Optional[str] = Field(default="")

    stars: int = Field(alias="stargazers_count", default=0)
    forks: int = Field(alias="forks_count", default=0)

    created_at: str = ""
    updated_at: str = ""

    @staticmethod
    def get_headers() -> list[str]:
        return [
            "name", "html_url", "description",
            "language", "stars", "forks",
            "created_at", "updated_at"
        ]
    
    @staticmethod
    def get_headers_csv() -> str:
        return ",".join([
            "name", "html_url", "description",
            "language", "stars", "forks",
            "created_at", "updated_at"
        ])

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "html_url": self.html_url,
            "description": self.description,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def to_csv(self) -> str:
        values = [
            self.name,
            self.html_url,
            self.description or "",
            self.language or "",
            str(self.stars),
            str(self.forks),
            self.created_at,
            self.updated_at,
        ]
    
        escaped = []
        for v in values:
            s = v
            s = s.replace('"', '""')
        
            if any(c in s for c in ',;"\n\r'):
                s = f'"{s}"'

            escaped.append(s)

        return ",".join(escaped)

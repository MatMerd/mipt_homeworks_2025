from config import Settings
from services.repository_service import RepositoryService


def get_settings() -> Settings:
    # In a real app, this could be a singleton or from context
    return Settings()


def get_repository_service(settings: Settings = get_settings()) -> RepositoryService:
    return RepositoryService(settings)
